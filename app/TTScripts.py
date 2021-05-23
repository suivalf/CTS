import requests
from gtts import gTTS
import playsound
import os
import time

def check_price(symbol):
    id = get_stringid_from_symbol(symbol)
    while True:
        responseBTC = requests.get('https://api.coincap.io/v2/assets/' + id)
        data = responseBTC.json()
        name = data['data']['name']
        price = data['data']['priceUsd']
        coinPrice = round(float(price), 4)
        language = 'en'
        myobj = gTTS(text=str(name + 'currently at' + str(coinPrice)), lang=language, slow=False)
        myobj.save("price.mp3")
        playsound.playsound('price.mp3', True)
        os.remove("price.mp3")
        time.sleep(5)


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