import os
import threading
import time, io, urllib
import requests
from gtts import gTTS
from pygame import mixer
from app.TTScripts import get_stringid_from_symbol
import cloudinary
import cloudinary.uploader

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
         myobj.save(str(self.userid) + "price" + str(self.symbol) + ".mp3")
         pi = str(self.userid) + "price" + str(self.symbol)
         x=cloudinary.uploader.upload(str(self.userid) + "price" + str(self.symbol)+ ".mp3", public_id=pi,use_filename=True, unique_filename=False, resource_type="video")
         print(x['version'])
         #cloudinary.utils.cloudinary_url(pi)
         time.sleep(4)
         #---old
         #mixer.init()
         #mixer.music.load(str(self.userid) + "price" + str(id) + ".mp3")
         #mixer.music.play()
         #while mixer.music.get_busy():
            #time.sleep(3)
         #mixer.music.unload()
         #os.remove(str(self.userid) + "price" + str(id) + ".mp3")
      return


class myfile(object):
   def __init__(self, url):
      self.url = url
      self.file = ''
      self.pos = 0
      self.chunk_gen = self.stream()

   def stream(self):
      r = requests.get(self.url, stream=True)
      for chunk in r.iter_content(chunk_size=40972):
         if chunk:
            self.file += chunk
            yield

   def read(self, *args):
      size = args[0]
      while self.pos + size > len(self.file):
         try:
            self.chunk_gen.next()
         except StopIteration:
            break

      if len(args) > 0:
         ret = self.file[self.pos:self.pos + size]
         self.pos += size
         return ret

