import urllib, urllib2
import json
import hmac, hashlib
import time
from common import AccountBalance
import keys

class BTCE:
	'Class Handling all BTCE Data'
	private_url = 'https://btc-e.com/tapi'
	def __init__(self):
		self.ticker = []
		self.timestamp = 0
		self.orderbook = []
		self.balance = AccountBalance();
		self.bids = []
		self.asks = []
		self.current = 0

	def getTicker(self):
		'Getting Current Ticker'
		url = 'https://btc-e.com/api/2/btc_usd/ticker'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		data = json.load(res)
		self.ticker = data['ticker']
		#print self.ticker
		self.timestamp = self.ticker['updated']
		self.current = self.ticker['last']

	def getOrderBook(self):
		print "Getting Current Order Book from BTCE"
		url = 'https://btc-e.com/api/2/btc_usd/depth'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		data = json.load(res)
		self.orderbook = data
		self.bids = self.orderbook['bids']
		self.asks = self.orderbook['asks']


	def printOrderBook(self):
		#print self.orderbook
		print 'Number of Bids: ' + str(len(self.bids))
		print 'Number of Asks: ' + str(len(self.asks))

		print 'Top Bid '
		print self.bids[0]
		print 'Top Ask '
		print self.asks[0]

	# Private Functions requiring authentication TODO
	def getBalance(self):

		nonce = int(time.time())
		params = {
				'method' : 'getInfo',
				'nonce' : nonce
		}
		params = urllib.urlencode(params)

		H = hmac.new(keys.BTCE_API_SECRET_KEY, digestmod=hashlib.sha512)
		H.update(params)
		sign = H.hexdigest()

		headers = {
				'Content-type' : 'application/x-www-form-urlencoded',
				'Key' : keys.BTCE_API_KEY,
				'Sign' : sign
		}
		req = urllib2.Request(BTCE.private_url, params, headers)
		res = urllib2.urlopen(req)

		res = json.load(res)

		self.balance.usd_balance = res['return']['funds']['usd']
		self.balance.btc_balance = res['return']['funds']['btc']
		self.balance.open_orders = res['return']['open_orders']
		self.balance.open_orders = res['return']['server_time']
	
	def trade(self, typ, rate, amount):

		nonce = int(time.time())
		params = {
				'method' : 'Trade',
				'pair' : 'btc_usd',
				'type' : typ,
				'rate' : rate,
				'amount' : amount,
				'nonce' : nonce
		}
		params = urllib.urlencode(params)

		H = hmac.new(keys.BTCE_API_SECRET_KEY, digestmod=hashlib.sha512)
		H.update(params)
		sign = H.hexdigest()

		headers = {
				'Content-type' : 'application/x-www-form-urlencoded',
				'Key' : keys.BTCE_API_KEY,
				'Sign' : sign
		}
		req = urllib2.Request(BTCE.private_url, params, headers)
		res = urllib2.urlopen(req)

		res = json.load(res)

		if(res['success'] == 0):
			print 'Could not complete the transaction'
			print res

if __name__ == "__main__":
	btce = BTCE()
	#btce.getBalance()
	#btce.balance.printBalance()
	btce.trade('buy', 600, 0.1)
