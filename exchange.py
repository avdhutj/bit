from common import AccountBalance
from common import OrderBook
class Exchange:
  public_url = ''
  private_url = ''
  def __init__(self):
    self.name = ''
    self.ticker = []
    self.orderBook = []
    self.balance = AccountBalance()
    self.orderBook = OrderBook()
    self.timestamp = 0
    self.ticker_price = 0
    self.trading_fee = 0
    self.transfer_fee = 0
  def getTicker(self):
    print 'Base Class, Should be called from child class'
    pass
  def getOrderBook(self, limit=50):
    pass
  #Private Functions
  def getBalance(self):
    pass
  def trade(self, typ, rate, amount):
    pass
