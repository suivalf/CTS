import threading
from app.TTScripts import check_price


class myThread (threading.Thread):

   def __init__(self, name, userid, symbol):
      threading.Thread.__init__(self)
      self.name = name
      self.userid = userid
      self.symbol = symbol


   def run(self):
      check_price(self.name, self.symbol, self.userid)
