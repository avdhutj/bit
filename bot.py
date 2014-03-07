import time
from exchange import Exchange

class Bot:
  def __init__(self):
    self.exchanges = []

  def addExchange(self, exchange):
    self.exchanges.append(exchange)

  def run(self):
    if(len(self.exchanges) < 2):
      print 'Atleast add 2 exchanges to the bot'

    while True:

      print 'Starting Iteration at ' + str(time.time())

      for exchange in self.exchanges:
        exchange.getTicker()
        print 'Ticker Price for ' + exchange.name + ' ' + str(exchange.ticker_price)

      print 'Sleeping...'
      time.sleep(2)
