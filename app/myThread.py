import os
import threading
import time
import playsound
import requests
from gtts import gTTS
from pygame import mixer
from app.TTScripts import get_stringid_from_symbol


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
         coinPrice = round(float(price), 2)
         language = 'en'
         myobj = gTTS(text=str(name + 'is' + str(coinPrice) + "$"), lang=language, slow=False)
         myobj.save(str(self.userid) + "price" + str(id) + ".mp3")
         mixer.init()
         mixer.music.load(str(self.userid) + "price" + str(id) + ".mp3")
         mixer.music.play()
         while mixer.music.get_busy():
            time.sleep(3)
         mixer.music.unload()
         os.remove(str(self.userid) + "price" + str(id) + ".mp3")
         #playsound.playsound(str(self.userid) + "price" + str(id) + ".mp3", True)
         #os.system("start " + str(self.userid) + "price" + str(id) + ".mp3")
         #os.remove(str(self.userid) + "price" + str(id) + ".mp3")
         # print("%s, %s - %s.".format(threadName, id, userid)
      return





