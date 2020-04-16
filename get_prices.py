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

def get_places(places_dict):
    places = {}

    for place in places_dict:
        place_id = place['PlaceId']
        place_name = place['CityName']
        places[place_id] = place_name
    return places

def get_carriers(carriers_dict):

    carriers = {}

    for carrier in carriers_dict:
        carrier_id = carrier['CarrierId']
        carrier_name = carrier['Name']
        carriers[carrier_id] = carrier_name
    return carriers

def get_quotes(quotes_dict):
    quotes = []
    
    for quote in quotes_dict:
        temp_quote = {}
        temp_quote['price'] = quote['MinPrice']
        temp_quote['is_direct'] = quote['Direct']
        temp_quote['departure_id'] = quote['OutboundLeg']['OriginId']
        temp_quote['destination_id'] = quote['OutboundLeg']['DestinationId']
        temp_quote['departure_date']= quote['OutboundLeg']['DepartureDate']
        temp_quote['carrier_ids'] = quote['OutboundLeg']['CarrierIds']
        quotes.append(temp_quote)
    
    return quotes

def get_prices(departure, destination, month, currency='PLN'): 
    rapid_api_key = os.environ['RAPIDAPIKEY']

    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/PL/PLN/en-US/WAW-sky/HAN-sky/2020-06"

    querystring = {"inboundpartialdate":"2019-12-01"}

    headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = response.json()

    places = get_places(response_json['Places'])
    carriers = get_carriers(response_json['Carriers'])
    
    quotes = get_quotes(response_json['Quotes'])
    
    print(50*'@')
    print('Najtansze loty Warszawa-Hanoi w 2020-06:')
    print(50*'@')
    for quote in quotes:
        carriers_temp = quote['carrier_ids']
        carriers_temp = [carriers[carrier] for carrier in carriers_temp]

        carriers_temp = ' '.join(carriers_temp)
        
        dst = places[quote['destination_id']]
        dep = places[quote['departure_id']]

        print('Departure: {}'.format(dep))
        print('Destination: {}'.format(dst))
        print('Date: {}'.format(quote['departure_date'].split('T')[0]))
        print('Price: {}'.format(quote['price']))
        print('Is direct: {}'.format(quote['is_direct']))
        print('Carrier: {}'.format(carriers_temp))
        print(50*"*")   
        
    return True

if __name__ == '__main__':
    dep = 'WAW-sky'
    dest = 'HAN-sky'
    curr = 'PLN'
    
    year = '2020'
    month = '06'
    best_price = get_prices(dep, dest, month, curr)
