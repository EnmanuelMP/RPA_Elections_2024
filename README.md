# Cedula Scraper README

## Overview
This Python program is designed to scrape voter information from the Dominican Republic's 2024 electoral website (https://elecciones2024.jce.gob.do). It retrieves voter data based on the provided list of national identification numbers (cedulas).

## Dependencies
- **requests**: For making HTTP requests to the electoral website.
- **pandas**: For data manipulation and handling.
- **BeautifulSoup**: For parsing HTML content.
- **time**: For adding delays between requests.

## Usage
1. Prepare a list of cedulas in an Excel file named "Lista de cedulas.xlsx". The cedulas should be in a column named "Cedula".
2. Run the program.
3. The program will make POST requests for each cedula in the list and retrieve voter information.
4. The scraped data will be saved in an Excel file named "Results.xlsx", with separate sheets for national and international voters.

## Configuration
- **URL_CEDULA**: The URL of the electoral website's API endpoint.
- **headers_manual**: HTTP headers required for making requests to the API.
- **NATIONAL_HD**: Header names for the columns in the national voter data.
- **INTERNATIONAL_HD**: Header names for the columns in the international voter data.

## Limitations
- The program limits requests to the API by adding a delay of 60 seconds after every 10 requests to avoid being blocked.
- If a request fails, the program will print the status code and continue to the next cedula.

## Output
The scraped data is saved in an Excel file named "Results.xlsx", with separate sheets for national and international voters.