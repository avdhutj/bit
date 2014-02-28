import urllib, urllib2
import json
import hmac, hashlib
import time
import keys

class BitStamp:
	'Class Handling all Bitstamp Data'
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
		url = 'https://www.bitstamp.net/api/ticker/'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.ticker = json.load(res)
		self.timestamp = int(self.ticker['timestamp'])
		self.current = float(self.ticker['last'])


	def getOrderBook(self):
		print "Getting Current Order Book from Bitstamp"
		url = 'https://www.bitstamp.net/api/order_book/'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.orderbook = json.loads(res.read())
		bids_unformatted = self.orderbook['bids']
		asks_unformatted = self.orderbook['asks']

		for bid in bids_unformatted:
			price = float(bid[0])
			amount = float(bid[1])
			self.bids.append([price, amount])

		for ask in asks_unformatted:
			price = float(ask[0])
			amount = float(ask[1])
			self.asks.append([price, amount])
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
		message = str(nonce) + keys.BITSTAMP_CLIENT_ID + keys.BITSTAMP_API_KEY
		signature = hmac.new(keys.BITSTAMP_API_SECRET_KEY, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
		params = {
				'key' : keys.BITSTAMP_API_KEY,
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

#bitstamp = BitStamp()
#bitstamp.getTicker()
#print bitstamp.current

