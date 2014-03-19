import urllib, urllib2
import json
import hmac, hashlib
import time
from exchange import Exchange
from common import AccountBalance
import keys
import logging

class BTCE(Exchange):
	# 'Class Handling all BTCE Data'
	public_url = 'https://btc-e.com/api/2/'
	private_url = 'https://btc-e.com/tapi'
	def __init__(self):
		Exchange.__init__(self)
		self.name = 'Btce'
		self.trading_fee = 0.002
		self.transfer_fee = 0.001
		self.nonce = 1

		self.logger = logging.getLogger('BitBot.BTCE')

		#Find the correct nonce parameter
		print 'Computing correct nonce parameter'
		params = {
				'method' : 'getInfo',
				'nonce' : self.nonce
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

		error = res['error']
		error = error.split(' ')
		for word in error:
			if 'key' in word:
				n = word.replace('key', '')
				n = n.replace(':', '')
				n = n.replace(',', '')
				self.nonce = int(n)

	def getTicker(self):
		# 'Getting Current Ticker'
		self.logger.debug('Getting Ticker')
		url = BTCE.public_url + 'btc_usd/ticker'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		data = json.load(res)
		self.ticker = data['ticker']
		self.timestamp = self.ticker['updated']
		self.ticker_price = self.ticker['last']

	def getOrderBook(self, limit=50):
		self.logger.debug('Getting Ordebook')
		url = BTCE.public_url + 'btc_usd/depth/' + str(limit)
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		data = json.load(res)

		orderbook = data

		self.orderBook.bids = data['bids']
		self.orderBook.asks = data['asks']

	# Private Functions requiring authentication TODO
	def getBalance(self):

		# self.logger.debug('Getting Balance')
		#nonce = long(time.time() * 100000)
		# nonce = int(time.time())

		self.nonce = self.nonce + 1
		params = {
				'method' : 'getInfo',
				'nonce' : self.nonce
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

		try:
			res = urllib2.urlopen(req)

			res = json.load(res)

			if (res['success'] == 0):
				# print '*** Error Getting Accout balance *** '
				self.logger.warn('Error getting account balance')
				#self.logger.info(res['error'])
				return

			self.balance.usd = res['return']['funds']['usd']
			self.balance.btc = res['return']['funds']['btc']
			self.balance.open_orders = res['return']['open_orders']
			self.balance.timestamp = res['return']['server_time']

			# self.logger.info('Got BTCE Balance: USD: %f, BTC: %f', self.balance.usd, self.balance.btc)
		except:
			self.logger.warn('Error getting account balance')
			raise

	def trade(self, typ, rate, amount):

		self.logger.debug('Trading')

		#nonce = long(time.time() * 100000)
		# nonce = int(time.time())
		self.nonce = self.nonce + 1
		params = {
				'method' : 'Trade',
				'pair' : 'btc_usd',
				'type' : typ,
				'rate' : rate,
				'amount' : amount,
				'nonce' : self.nonce
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
		try:
			res = urllib2.urlopen(req)

			res = json.load(res)

			if(res['success'] == 0):
				self.logger.warn('Trade Failed - %s, %f, %f', typ, rate, amount)
				# self.logger.info(res['error'])
				# print 'Could not complete the transaction in BTCE'
				# print res
			else:
				self.logger.info('Trade Success - %s, %f, %f', typ, rate, amount)
				# print 'Suceess'
				# print res
		except Exception:
			self.logger.warn('Trade Failed - %s, %f, %f', typ, rate, amount)
			raise


if __name__ == "__main__":
	btce = BTCE()

	# btce.getOrderBook()
	# btce.getTicker()
	#btce.orderBook.printOrderBook()

	# btce.getBalance()
	# btce.balance.printBalance()

	# print btce.orderBook.asks[0][0]
	# btce.trade('buy', btce.orderBook.asks[0][0], 0.01)
	# time.sleep(1)
	# btce.trade('sell', btce.orderBook.bids[0][0], 0.01)
	#
	# btce.getBalance()
	# btce.balance.printBalance()
