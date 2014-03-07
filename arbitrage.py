import bitstamp, btce, bitfinex

arb_thresh = 0.001
def ComputeArb(Book1, Book2):
	if((Book1.bids[0] + Book1.asks[0]) < (Book2.bids[0] + Book2.asks[0]) ):
		BuyBook = Book1
		SellBook = Book2
	else:
		BuyBook = Book2
		SellBook = Book1

	ask_idx = 0
	bid_idx = 0

	arb = 0
	fees = 1

	SellPrice = SellBook.bids[bid_idx][0]
	SellAmount = SellBook.bids[bid_idx][1]
	BuyPrice = BuyBook.asks[ask_idx][0]
	BuyAmount = BuyBook.asks[ask_idx][1]

	diff = SellPrice - BuyPrice
	pct_arb = diff / SellPrice * 100
	print pct_arb
	while(pct_arb > arb_thresh):

		diff = SellPrice - BuyPrice
		pct_arb = diff / SellPrice * 100

		if(SellAmount < BuyAmount):
			arb += SellPrice * SellAmount * fees
			bid_idx = bid_idx + 1
			if(bid_idx >= len(SellBook.bids)):
					break
		else:
			arb += BuyPrice * BuyAmount * fees
			ask_idx = ask_idx + 1

			if(ask_idx >= len(BuyBook.asks)):
				break

		#print [ask_idx, bid_idx, arb, pct_arb]

		SellPrice = SellBook.bids[bid_idx][0]
		SellAmount = SellBook.bids[bid_idx][1]

		BuyPrice = BuyBook.asks[ask_idx][0]
		BuyAmount = BuyBook.asks[ask_idx][1]

	print 'Total Arbitrage: '
	print arb


if __name__ == '__main__':
	bitfinex = bitfinex.Bitfinex()
	btce = btce.BTCE()

	bitfinex.getOrderBook()
	btce.getOrderBook()

	ComputeArb(btce.orderBook, bitfinex.orderBook)

# bitstamp = bitstamp.BitStamp()
# btce = btce.BTCE()
# bitfinex = bitfinex.Bitfinex()
#
# #Get Books
# bitstamp.getOrderBook()
# btce.getOrderBook()
# bitfinex.getOrderBook()
#
# print 'Bitstamp orderbook'
# bitstamp.printOrderBook()
# print 'BTCE orderbook'
# btce.printOrderBook()
# print 'Bitfinex orderbook'
# bitfinex.printOrderBook()
#
#
# #Compute Arbitrage depth
# BitStampBook = {
# 		'asks' : bitstamp.asks,
# 		'bids' : bitstamp.bids
# 		}
# BTCEBook = {
# 		'asks' : btce.asks,
# 		'bids' : btce.bids
# 		}
# BitfinexBook = {
# 		'asks' : bitfinex.asks,
# 		'bids' : bitfinex.bids
# 		}
#
# print 'Arbitrage between Bitstamp and BTCE'
# ComputeArb(BitStampBook, BTCEBook)
# print 'Arbitrage between Bitstamp and Bitfinex'
# ComputeArb(BitStampBook, BitfinexBook)
# print 'Arbitrage between Bitfinex and BTCE'
# ComputeArb(BTCEBook, BitfinexBook)
