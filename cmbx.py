from campbx_extern import CampBX #External library
from exchange import Exchange
import time
import keys

class CMBX(Exchange):
  def __init__(self):
    Exchange.__init__(self)
    self.cbx_extern = CampBX(keys.CAMPBX_LOGIN, keys.CAMPBX_PASS)
    self.cbx_extern.debug_mode(True)
    self.name = 'CampBX'
  def getTicker(self):
    self.ticker = self.cbx_extern.xticker()
    self.timestamp = time.time()
    self.ticker_price = self.ticker['Last Trade']
  def getOrderBook(self):
    orderBook = self.cbx_extern.xdepth()
    self.orderBook.asks = orderBook['Asks']
    self.orderBook.bids = orderBook['Bids']

  #Authenticated Calls
  def getBalance(self):
    my_funds = self.cbx_extern.my_funds()
    print my_funds
    self.balance.usd = my_funds['Liquid USD']
    self.balance.btc = my_funds['Liquid BTC']
    #TODO Not implemented open orders

  def trade(self, typ, rate, amount):
    mode = ''
    if typ == 'sell':
      mode = 'QuickSell'
    elif typ == 'buy':
      mode = 'QuickBuy'
    self.cbx_extern.trade_enter({
      'TradeMode' : mode,
      'Quantity' : str(amount),
      'Price' : str(rate)
    })


if __name__ == '__main__':
  cmbx = CMBX()
  # cmbx.getOrderBook()
  cmbx.getBalance()
  # cmbx.balance.printBalance()
