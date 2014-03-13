import urllib, urllib2, requests
import json
import hmac, hashlib, base64
import time

import keys
from exchange import Exchange

class Bitfinex(Exchange):
	'Class Handling all Bitfinex Data'
	private_url = 'https://api.bitfinex.com/v1/'
	public_url = 'https://api.bitfinex.com/v1/'
	def __init__(self):
		Exchange.__init__(self)
		self.name = 'Bitfinex'
		self.trading_fee = 0.0015
		self.transfer_fee = 0

	def getTicker(self):
		'Getting Current Ticker'
		url = Bitfinex.public_url + 'ticker/btcusd'
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		self.ticker = json.load(res)
		self.timestamp = int(float(self.ticker['timestamp']))
		self.ticker_price = float(self.ticker['last_price'])


	def getOrderBook(self, limit=50):
		url = Bitfinex.public_url + '/book/btcusd?limit_bids=' + str(limit) + '&limit_asks=' + str(limit)
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)

		orderbook = json.loads(res.read())
		bids_unformatted = orderbook['bids']
		asks_unformatted = orderbook['asks']

		for bid in bids_unformatted:
			price = float(bid['price'])
			amount = float(bid['amount'])
			timestamp = float(bid['timestamp'])
			self.orderBook.bids.append([price, amount, timestamp])

		for ask in asks_unformatted:
			price = float(ask['price'])
			amount = float(ask['amount'])
			timestamp = float(ask['timestamp'])
			self.orderBook.asks.append([price, amount, timestamp])

	# Private Functions requiring authentication TODO
	def getBalance(self):
		nonce = str(long(time.time() * 100000))
		payload = {
			'request' : '/v1/balances',
			'nonce' : nonce,
			'options' : {}
		}
		payload_json = json.dumps(payload)
		payload_str = str(base64.b64encode(payload_json))

		H = hmac.new(keys.BITFINEX_API_SECRET_KEY, payload_str, hashlib.sha384)
		sign = H.hexdigest()

		headers = {
				'X-BFX-APIKEY' : keys.BITFINEX_API_KEY,
				'X-BFX-PAYLOAD' : base64.b64encode(payload_json),
				'X-BFX-SIGNATURE' : sign
		}

		res = requests.get(Bitfinex.private_url + 'balances', data={}, headers=headers)

		if(res.status_code != 200):
			print 'Error getting Account Balance'
			pass

		result = res.json()

		#Format Result in Account Balance
		for wallet in result:
			if wallet['type'] == 'exchange' and wallet['currency'] == 'usd':
				self.balance.usd = float(wallet['amount'])
				continue
			if wallet['type'] == 'exchange' and wallet['currency'] == 'btc':
				self.balance.btc = float(wallet['amount'])

			self.balance.timestamp = time.time()

	def trade(self, typ, rate, amount):
		nonce = str(long(time.time() * 100000))
		payload = {
			'request' : '/v1/order/new',
			'nonce' : nonce,
			'symbol' : 'btcusd',
			'amount' : str(amount),
			'price' : str(rate),
			'exchange' : 'bitfinex',
			'side' : typ,
			'type' : 'exchange market'
		}
		payload_json = json.dumps(payload)
		payload_str = str(base64.b64encode(payload_json))

		H = hmac.new(keys.BITFINEX_API_SECRET_KEY, payload_str, hashlib.sha384)
		sign = H.hexdigest()

		headers = {
				'X-BFX-APIKEY' : keys.BITFINEX_API_KEY,
				'X-BFX-PAYLOAD' : base64.b64encode(payload_json),
				'X-BFX-SIGNATURE' : sign
		}

		res = requests.post(Bitfinex.private_url + 'order/new', data={}, headers=headers)

		if(res.status_code != 200 ):
			print 'Error placing the trade in Bitfinex'
			print res.content
			return

		result = res.json()


	def myTrades(self):

		nonce = str(long(time.time() * 100000))
		payload = {
			'request' : '/v1/mytrades',
			'nonce' : nonce,
			'symbol' : 'btcusd',
			'timestamp' : 0
		}
		payload_json = json.dumps(payload)
		payload_str = str(base64.b64encode(payload_json))

		H = hmac.new(keys.BITFINEX_API_SECRET_KEY, payload_str, hashlib.sha384)
		sign = H.hexdigest()

		headers = {
		'X-BFX-APIKEY' : keys.BITFINEX_API_KEY,
		'X-BFX-PAYLOAD' : base64.b64encode(payload_json),
		'X-BFX-SIGNATURE' : sign
		}

		res = requests.post(Bitfinex.private_url + 'mytrades', data={}, headers=headers)

		print 'Resopone Code: ' + str(res.status_code)
		print 'Response Content ' + str(res.content)


if __name__ == '__main__':
	bitfinex = Bitfinex()
	#bitfinex.getTicker()
	#print bitfinex.ticker_price

	# bitfinex.getOrderBook()
	#bitfinex.orderBook.printOrderBook()

	# bitfinex.trade('buy', bitfinex.orderBook.asks[0][0], 0.01)
	# bitfinex.trade('sell', bitfinex.orderBook.bids[0][0], 0.01)

	bitfinex.getBalance()
	bitfinex.balance.printBalance()

	#bitfinex.myTrades()
