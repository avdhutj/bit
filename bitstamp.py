import urllib, urllib2
import json
import hmac, hashlib
import time

class BitStamp:
	'Class Handling all Bitstamp Data'
	API_SECRET_KEY = 'MgpGk28vHL5Lz5OswK3reCfnw9TLOPo8'
	API_KEY = 'E5sTYF4nPKQ6yBnD9XrZYwVXHHAqqAAy'
	CLIENT_ID = '647636'
	def __init__(self):
		self.ticker = []
		self.timestamp = 0
		self.orderbook = []
		self.balance = []
		self.bids = []
		self.asks = []
	def getTicker(self):
		print "Getting Current Ticker"
		url = 'https://www.bitstamp.net/api/ticker/'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.ticker = json.load(res)
		self.timestamp = int(self.ticker['timestamp'])

		print self.timestamp + 1
		print self.ticker
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

	def getOrderBook(self):
		print "Getting Current Order Book"
		url = 'https://www.bitstamp.net/api/order_book/'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.orderbook = json.loads(res.read())
		self.bids = self.orderbook['bids']
		self.asks = self.orderbook['asks']

		print 'Got order book at ' + self.orderbook['timestamp']

	def printOrderBook(self):
		#print self.orderbook
		print 'Number of Bids: ' + str(len(self.bids))
		print 'Number of Asks: ' + str(len(self.asks))

		print 'Top Bid '
		print self.bids[0]
		print 'Top Ask '
		print self.asks[0]



bitstamp = BitStamp()

bitstamp.getOrderBook()
bitstamp.printOrderBook()

