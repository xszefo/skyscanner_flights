#!/usr/bin/python3

import os
import json
import requests

'''
Skrypt pobiera liste wszystkich krajow dostepnych na platformie SkyScanner
i tworzy slownik gdzie kluczem jest kod kraju, a wartoscia jego nazwa

Wynik jest zapisywany do pliku w formacie JSON

INPUT:
    brak
OUTPUT:
    dictionary[COUNTRY_CODE] = COUNTRY_NAME
'''

def get_country_codes(): 
    rapid_api_key = os.environ['RAPIDAPIKEY']

    url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/reference/v1.0/countries/en-US'
    
    headers = {
        'x-rapidapi-host': 'skyscanner-skyscanner-flight-search-v1.p.rapidapi.com',
        'x-rapidapi-key': rapid_api_key
        }

    response = requests.request('GET', url, headers=headers)
    response_json = response.json()
    countries_dict = {}

    for country in response_json['Countries']:
        code = country['Code']
        name = country['Name']

        countries_dict[code] = name

    with open('skyscanner_country_codes.txt', 'w') as f:
        json.dump(countries_dict, f)

if __name__ == '__main__':
    get_country_codes()
