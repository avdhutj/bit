class AccountBalance:
	'Class containing account balances for all exchanges'
	def __init__(self):
		self.usd = 0
		self.btc = 0
		self.open_orders = 0
		self.timestamp = 0
	def printBalance(self):
		print 'USD Balance: ' + str(self.usd)
		print 'BTC Balance: ' + str(self.btc)
		print 'Open Orders: ' + str(self.open_orders)
		print 'Timestamp: ' + str(self.timestamp)

class OrderBook:
	def __init__(self):
		self.bids = []
		self.asks = []

	def printOrderBook(self):
		print 'Number of Bids: ' + str(len(self.bids))
		print 'Number of Asks: ' + str(len(self.asks))
		print 'Top Bid '
		print self.bids[0]
		print 'Top Ask '
		print self.asks[0]

	class Trade:
		def __init__(self):
			self.exhange = ''
			self.typ = ''
			self.timestamp = ''
			self.order_id = ''
			self.amount = 0 #Btc amount
			self.rate = 0
		
