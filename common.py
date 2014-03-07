class AccountBalance:
	'Class containing account balances for all exchanges'
	def __init__(self):
		self.usd_balance = 0
		self.btc_balance = 0
		self.open_orders = 0
		self.timestamp = 0
	def printBalance(self):
		print 'USD Balance: ' + str(self.usd_balance)
		print 'BTC Balance: ' + str(self.btc_balance)
		print 'Open Orders: ' + str(self.open_orders)
		print 'Timestamp: ' + str(self.timestamp)
