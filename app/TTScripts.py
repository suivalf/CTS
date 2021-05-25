import requests
import multiprocessing
from gtts import gTTS
import playsound
import os
import time
exitFlag = 0
def check_price(threadName, symbol, userid, flag):
    id = get_stringid_from_symbol(symbol)
    while flag:
        if exitFlag:
            threadName.exit()
        responseBTC = requests.get('https://api.coincap.io/v2/assets/' + id)
        data = responseBTC.json()
        name = data['data']['name']
        price = data['data']['priceUsd']
        coinPrice = round(float(price), 4)
        language = 'en'
        myobj = gTTS(text=str(name + 'is' + str(coinPrice) + "$"), lang=language, slow=False)
        myobj.save(str(userid) + "price" + str(id) + ".mp3")
        #print(str(user.id) + "price" + str(id) + ".mp3")
        playsound.playsound(str(userid) + "price" + str(id) + ".mp3", True)
        os.remove(str(userid) + "price" + str(id) + ".mp3")
        #print("%s, %s - %s.".format(threadName, id, userid))
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