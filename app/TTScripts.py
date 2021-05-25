import requests

def get_all():
    # This function returns all available cryptocurrencies on Coincap.
    crypto = []
    r = requests.get("https://api.coincap.io/v2/assets")
    response = r.json()
    for i in range(len(response['data'])):
        crypto.append(response['data'][i]['symbol'] + '-' + response['data'][i]['name'])
    return crypto

def get_stringid_from_symbol(symbol):
    r = requests.get("https://api.coincap.io/v2/assets")
    response = r.json()
    for i in range(len(response['data'])):
        if response['data'][i]['symbol'] == symbol:
            return response['data'][i]['id']

def get_price_from_symbol(symbol):
    r = requests.get("https://api.coincap.io/v2/assets")
    response = r.json()
    for i in range(len(response['data'])):
        if response['data'][i]['symbol'] == symbol:
            return response['data'][i]['priceUsd']