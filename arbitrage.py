import bitstamp, btce

def ComputeArb(Book1, Book2):
	if(Book1['bids'][0] < Book2['bids'][0]):
		BuyBook = Book1
		SellBook = Book2
	else:
		BuyBook = Book2
		SellBook = Book1
	
	done = 0
	ask_idx = 0
	bid_idx = 0

	arb = 0
	fees = 1

	SellPrice = SellBook['bids'][bid_idx][0]
	SellAmount = SellBook['bids'][bid_idx][1]
	BuyPrice = BuyBook['asks'][ask_idx][0]
	BuyAmount = BuyBook['asks'][ask_idx][1]

	diff = SellPrice - BuyPrice
	pct_arb = diff / SellPrice * 100
	print pct_arb
	while(done == 0):

		diff = SellPrice - BuyPrice
		pct_arb = diff / SellPrice * 100

		if(SellAmount < BuyAmount):
			arb += SellPrice * SellAmount * fees
			bid_idx = bid_idx + 1
			if(bid_idx >= len(SellBook['bids'])):
					break
		else:
			arb += BuyPrice * BuyAmount * fees
			ask_idx = ask_idx + 1

			if(ask_idx >= len(BuyBook['asks'])):
				break

		#print [ask_idx, bid_idx, arb, pct_arb]

		SellPrice = SellBook['bids'][bid_idx][0]
		SellAmount = SellBook['bids'][bid_idx][1]

		BuyPrice = BuyBook['asks'][ask_idx][0]
		BuyAmount = BuyBook['asks'][ask_idx][1]

		if(diff / SellPrice < 0.02):
			done = 1
	
	print 'Total Arbitrage: '
	print arb

bitstamp = bitstamp.BitStamp();
btce = btce.BTCE();

#Get Books
bitstamp.getOrderBook();
btce.getOrderBook();

#Compute Arbitrage depth
BitStampBook = {
		'asks' : bitstamp.asks,
		'bids' : bitstamp.bids
		}
BTCEBook = {
		'asks' : btce.asks,
		'bids' : btce.bids
		}

ComputeArb(BitStampBook, BTCEBook)
