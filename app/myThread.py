import threading
import sys
import pyaudio
import wave
import requests
from app.TTScripts import check_price
from gtts import gTTS
import playsound
import os
import time
from app.TTScripts import get_price_from_symbol, get_stringid_from_symbol
class myThread (threading.Thread):

   def __init__(self, name, userid, symbol, flag):
      threading.Thread.__init__(self)
      self.name = name
      self.userid = userid
      self.symbol = symbol
      self._is_running = flag

   # function using _stop function
   def stop(self):
      self._is_running = 0


   def run(self):
      id = get_stringid_from_symbol(self.symbol)
      while(self._is_running == 1):
         responseBTC = requests.get('https://api.coincap.io/v2/assets/' + id)
         data = responseBTC.json()
         name = data['data']['name']
         price = data['data']['priceUsd']
         coinPrice = round(float(price), 4)
         language = 'en'
         myobj = gTTS(text=str(name + 'is' + str(coinPrice) + "$"), lang=language, slow=False)
         myobj.save(str(self.userid) + "price" + str(id) + ".mp3")
         playsound.playsound(str(self.userid) + "price" + str(id) + ".mp3", True)
         #os.system("start " + str(self.userid) + "price" + str(id) + ".mp3")
         os.remove(str(self.userid) + "price" + str(id) + ".mp3")
         # print("%s, %s - %s.".format(threadName, id, userid))
         time.sleep(5)
      return





