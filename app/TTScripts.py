import requests
from gtts import gTTS
import playsound
import os
import time

def check_price():
    while True:
        #https://api.coinbase.com/v2/prices/REP-USD/spot
        responseBTC = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
        data = responseBTC.json()
        price = data['data']['amount']
        print(price)
        language = 'en'
        myobj = gTTS(text=price, lang=language, slow=False)
        myobj.save("price.mp3")
        playsound.playsound('price.mp3', True)
        os.remove("price.mp3")
        time.sleep(4)

def prov():
    crypto = []
    fiat = []
    others = []
    r = requests.get("https://api.pro.coinbase.com/currencies")
    response = r.json()

    for i in range(len(response)):
        if response[i]['details']['type'] == 'crypto':
            crypto.append(response[i]['name'])
        elif response[i]['details']['type'] == 'fiat':
            fiat.append(response[i]['name'])
        else:
            others.append(response[i]['name'])
    print("Crypto: \n")
    print(len(crypto))

    print("Fiat: ]n")
    print(fiat)

    print("Others: \n")
    print(len(others))


def get_all():
    # This function returns all available cryptocurrencies on Coinbase.
    crypto = []
    r = requests.get("https://api.pro.coinbase.com/currencies")
    response = r.json()
    for i in range(len(response)):
        if response[i]['details']['type'] == 'crypto':
            crypto.append(response[i]['id'] + '-' + response[i]['name'])
    return crypto