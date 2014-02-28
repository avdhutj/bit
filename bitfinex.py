import urllib, urllib2
import json
import hmac, hashlib
import time

import keys

class Bitfinex:
	'Class Handling all Bitfinex Data'
	base_url = 'https://api.bitfinex.com/v1'
	def __init__(self):
		self.ticker = []
		self.timestamp = 0
		self.orderbook = []
		self.balance = []
		self.bids = []
		self.asks = []
		self.current = 0
	def getTicker(self):
		'Getting Current Ticker'
		url = Bitfinex.base_url + '/ticker/btcusd'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.ticker = json.load(res)
		self.timestamp = int(float(self.ticker['timestamp']))
		'print self.ticker'
		self.current = float(self.ticker['last_price'])
		


	def getOrderBook(self):
		print "Getting Current Order Book from Bitfinex"
		url = Bitfinex.base_url + '/book/btcusd'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.orderbook = json.loads(res.read())
		bids_unformatted = self.orderbook['bids']
		asks_unformatted = self.orderbook['asks']

		for bid in bids_unformatted:
			price = float(bid['price'])
			amount = float(bid['amount'])
			timestamp = float(bid['timestamp'])
			self.bids.append([price, amount, timestamp])

		for ask in asks_unformatted:
			price = float(ask['price'])
			amount = float(ask['amount'])
			timestamp = float(ask['timestamp'])
			self.asks.append([price, amount, timestamp])

		#self.bids = self.orderbook['bids']
		#self.asks = self.orderbook['asks']


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
		url = 'https://www.bitstamp.net/api/balance/'
		nonce = int(time.time())
		message = str(nonce) + BitStamp.CLIENT_ID + BitStamp.API_KEY
		signature = hmac.new(BitStamp.API_SECRET_KEY, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
		params = {
				'key' : BitStamp.API_KEY,
				'signature' : signature,
				'nonce' : str(nonce)
		}
		data = urllib.urlencode(params)
		req = urllib2.Request(url, data)
		print req.get_method()
		print req.get_full_url()
		print req.get_data()
		res = urllib2.urlopen(req)

		self.balance = json.load(res)

#bitfinex = Bitfinex()
#bitfinex.getTicker()
#print bitfinex.current
#bitfinex.getOrderBook()
#bitfinex.printOrderBook()
