import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

#STEP 1: GETTING CEDULAS AND ADD IT TO LIST AND GLOBAL VARIABLES
df_ids = pd.read_excel('./Lista de cedulas.xlsx')
cedulas = df_ids.Cedula.to_list()
national_rows = []
international_rows = []
counter = 0


#STEP 2: CONFIGURING NECESSARY INFORMATION
URL_CEDULA = 'https://elecciones2024.jce.gob.do/API/HoneyModules/FrontEnd/EventHandler?hfEventId=2&TabId=36&language=en-US&'

#Must copy curl from website and convert to headers.
headers_manual = {
}

NATIONAL_HD = [
    'Cedula', 'Posición Padrón', 'Colegio Origen', 
    'Código Colegio', 'Provincia', 'Municipio', 
    'Distrito Municipal', 'Codigo Circ.', 'Ciudad', 
    'Sector', 'Codigo Recinto', 'Recinto', 'Dirección Recinto'
]

INTERNATIONAL_HD = [
    'Cedula', 'OCLEE', 'Código del Recinto',
    'Descripción del Recinto', 'Dirección del Recinto',
    'País del Recinto', 'Demarcación', 'Código del Colegio',
    'Posición Página', 'Observación'
]


#STEP 3: MAKE POST REQUEST FOR EACH CEDULA AND SAVE IT TO DATAFRAME:
for cedula in cedulas:


    #Step 3.1: limiting requests and saving backup:
    if counter % 10 == 0 and counter != 0:
        df_national = pd.DataFrame(national_rows, columns=NATIONAL_HD)
        df_international = pd.DataFrame(international_rows, columns=INTERNATIONAL_HD)

        with pd.ExcelWriter('output.xlsx') as writer:
            df_national.to_excel(writer, sheet_name='National', index=False)
            df_international.to_excel(writer, sheet_name='International', index=False)

        print(counter)
        sleep(60)


    #Step 3.2: making post request:
    PAYLOAD = {'Cedula': cedula, 'Terms': False}
    response = requests.post(URL_CEDULA,headers=headers_manual, json=PAYLOAD)


    #Step 3.3: getting html table from response if post request was successful. 
    #If the request was not successful, print the status code and continue next iteration
    if response.status_code == 200:
        response_data = response.json()
        html_content = response_data[2]['messageTemplate']
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')
        div = soup.find('div', class_='HoneyModulesRoot')
        form_id = int(div.get('formid'))

    else:
        print("Failed to retrieve data, status code:", response.status_code)
        continue

    
    #Step 3.4: getting table rows
    for table in tables:
        rows = [str(cedula)]

        for tr in table.find_all('tr'):
            row = [td.text.strip() for td in tr.find_all('td')]
            if row:
                rows.append(''.join(row))

    #Step 3.5: Append rows to the list and setting counter
    if form_id == 3:
        national_rows.append(rows)
    else:
        international_rows.append(rows)

    counter += 1


#STEP 4: SAVING LAST ITERATION:
df_national = pd.DataFrame(national_rows, columns=NATIONAL_HD)
df_international = pd.DataFrame(international_rows, columns=INTERNATIONAL_HD)

with pd.ExcelWriter('Results.xlsx') as writer:
    df_national.to_excel(writer, sheet_name='National', index=False)
    df_international.to_excel(writer, sheet_name='International', index=False)