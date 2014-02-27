import urllib, urllib2
import json
import hmac, hashlib
import time

class BTCE:
	'Class Handling all BTCE Data'
	API_SECRET_KEY = '868cb4f680ded0354873927f1683a4b0f01cf6ab6a0b429ecf3893aceb6e1888'
	API_KEY = '31BO9572-ZLGY6JHA-X928DFLN-P242VR0H-QRFVBW6H'
	def __init__(self):
		self.ticker = []
		self.timestamp = 0
		self.orderbook = []
		self.balance = []
		self.bids = []
		self.asks = []

	def getTicker(self):
		print "Getting Current Ticker"
		url = 'https://btc-e.com/api/2/btc_usd/ticker'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		data = json.load(res)
		self.ticker = data['ticker']
		print self.ticker
		self.timestamp = self.ticker['updated']

	def getOrderBook(self):
		print "Getting Current Order Book from BTCE"
		url = 'https://btc-e.com/api/2/btc_usd/depth'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		data = json.load(res)
		self.orderbook = data
		self.bids = self.orderbook['bids']
		self.asks = self.orderbook['asks']

	def getInfo(self):
		print "Getting Current Ticker"
		url = 'https://btc-e.com/tapi'
		nonce = int(time.time())
		params = {
				'method' : 'getInfo',
				'nonce' : nonce
		}
		params = urllib.urlencode(params)
		H = hmac.new(BTCE.API_SECRET_KEY, digestmod=hashlib.sha512)
		H.update(params)
		sign = H.hexdigest()
		headers = {
				'Content-type' : 'application/x-www-form-urlencoded',
				'Key' : BTCE.API_KEY,
				'Sign' : sign
		}
		req = urllib2.Request(url, params, headers)
		res = urllib2.urlopen(req)

		print res.read()

	def printOrderBook(self):
		#print self.orderbook
		print 'Number of Bids: ' + str(len(self.bids))
		print 'Number of Asks: ' + str(len(self.asks))

		print 'Top Bid '
		print self.bids[0]
		print 'Top Ask '
		print self.asks[0]


