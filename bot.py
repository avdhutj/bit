import time
from exchange import Exchange
import withdrawal
import keys

class Bot:
  def __init__(self):
    self.exchanges = []

  def addExchange(self, exchange):
    self.exchanges.append(exchange)

  def executeArb(self, bExc, sExc, acceptable_arb_pct):

    #Go through the orderbook to find trades till we have sold all the btc's in the
    # selling exchange or we have exhausted money in our buying exchange
    btc_transacted = 0
    while sExc.balance.btc > 0.05 and bExc.balance.usd > 10.0:

      # if bid_idx >= len(bExc.orderBook.bids) or ask_idx >= len(sExc.orderBook.asks):
      #   break

      bExc.getOrderBook(1)
      sExc.getOrderBook(1)

      # Compute arbitrage
      pct_arb =  sExc.orderBook.bids[0][0]*(1-sExc.trading_fee) - bExc.orderBook.asks[0][0]*(1-bExc.trading_fee)
      pct_arb = (pct_arb / bExc.orderBook.asks[0][0]) * 100.0

      #print 'Current Arb ' + str(pct_arb) + '%'

      if pct_arb > acceptable_arb_pct:

        if bExc.orderBook.asks[0][1] < sExc.orderBook.bids[0][1]:

          amount_to_trade_btc = min(bExc.orderBook.asks[0][1], sExc.balance.btc)
          amount_to_trade_usd = min(bExc.orderBook.asks[0][1], bExc.balance.usd / bExc.orderBook.asks[0][0])

          amount_to_trade = min(amount_to_trade_btc, amount_to_trade_usd)

          print 'Buying: ' + str(amount_to_trade) + ' at ' + str(bExc.orderBook.asks[0][0])
          print 'Selling: ' + str(amount_to_trade) + ' at ' + str(sExc.orderBook.bids[0][0])

          bExc.trade('buy', bExc.orderBook.asks[0][0], amount_to_trade)
          sExc.trade('sell', sExc.orderBook.bids[0][0], amount_to_trade)

          #Check for transaction success and think what to do if it fails

          # Simulate the transaction
          bExc.balance.btc = bExc.balance.btc + amount_to_trade
          bExc.balance.usd = bExc.balance.usd - (bExc.orderBook.asks[0][0] * amount_to_trade)

          sExc.balance.btc = sExc.balance.btc - amount_to_trade
          sExc.balance.usd = sExc.balance.usd + (sExc.orderBook.bids[0][0] * amount_to_trade)

          btc_transacted = btc_transacted + amount_to_trade

        else:
          amount_to_trade_btc = min(sExc.orderBook.bids[0][1], sExc.balance.btc)
          amount_to_trade_usd = min(sExc.orderBook.bids[0][1], bExc.balance.usd / bExc.orderBook.asks[0][0])

          amount_to_trade = min(amount_to_trade_btc, amount_to_trade_usd)

          bExc.trade('buy', bExc.orderBook.asks[0][0], amount_to_trade)
          sExc.trade('sell', sExc.orderBook.bids[0][0], amount_to_trade)

          print 'Buying: ' + str(amount_to_trade) + ' at ' + str(bExc.orderBook.asks[0][0])
          print 'Selling: ' + str(amount_to_trade) + ' at ' + str(sExc.orderBook.bids[0][0])

          #Check for transaction success and think what to do if it fails

          #Simulate the transaction
          bExc.balance.btc = bExc.balance.btc + amount_to_trade
          bExc.balance.usd = bExc.balance.usd - (bExc.orderBook.asks[0][0] * amount_to_trade)

          sExc.balance.btc = sExc.balance.btc - amount_to_trade
          sExc.balance.usd = sExc.balance.usd + (sExc.orderBook.bids[0][0] * amount_to_trade)

          btc_transacted = btc_transacted + amount_to_trade

        time.sleep(0.5)

        bExc.getBalance()
        sExc.getBalance()

      else:
        # Arbitrage not acceptable
        break


    if btc_transacted > 0.05 :
      #Call selnium script
      print 'call selenium scripts with btc_transacted: ' + str(btc_transacted)

      if(bExc.name == 'Bitfinex'):
        withdrawal.bitfinex_withdrawal(keys.BTCE_DEPOSIT_ADDRESS, btc_transacted)
      elif bExc.name == 'Btce':
        withdrawal.btce_withdrawal(keys.BITFINEX_DEPOSIT_ADDRESS, btc_transacted + bExc.tranfer_fee)


  def run(self):
    if(len(self.exchanges) < 2):
      print 'Atleast add 2 exchanges to the bot'

    for exchange in self.exchanges:
      exchange.getBalance()

    # self.exchanges[0].balance.usd = 600.0
    # self.exchanges[1].balance.usd = 10.0

    live = False

    while True:

      print '***** Starting Iteration at ' + str(time.time()) + ' *********************'

      try:

        for exchange in self.exchanges:
          exchange.getTicker()
          print 'Ticker Price for ' + exchange.name + ' ' + str(exchange.ticker_price)

        for exchange in self.exchanges:
          exchange.getBalance()
          print 'Exchange: ' + exchange.name
          print 'USD balance: ' + str(exchange.balance.usd)
          print 'BTC balance: ' + str(exchange.balance.btc)

        # Forward Transfer
        usd_balance_ratio = self.exchanges[0].balance.usd / self.exchanges[1].balance.usd
        acceptable_arb_pct = 100.0

        # if usd_balance_ratio < 0.2:
        #   acceptable_arb_pct = 5.0
        # elif usd_balance_ratio > 0.2 and usd_balance_ratio < 0.5:
        #   acceptable_arb_pct = 4.0
        # elif usd_balance_ratio > 0.5 and usd_balance_ratio < 2:
        #   acceptable_arb_pct = 2.5
        # elif usd_balance_ratio > 2 and usd_balance_ratio < 5:
        #   acceptable_arb_pct = 2.0
        # elif usd_balance_ratio > 5:
        #   acceptable_arb_pct = 1.5

        if usd_balance_ratio < 0.5:
          acceptable_arb_pct = 4.0
        elif usd_balance_ratio > 0.5 and usd_balance_ratio < 2:
          acceptable_arb_pct = 3.0
        elif usd_balance_ratio > 2:
          acceptable_arb_pct = 2.0


        # self.get_acceptable_arb_pct(balance_ratio, acceptable_arb_pct, acceptable_arb_pct)

        print 'Btce Buy ---> Bitfinex Sell ARB PCT: ' + str(acceptable_arb_pct)

        # Execute trades
        # Buying in 0 and selling in 1
        self.executeArb(self.exchanges[0], self.exchanges[1], acceptable_arb_pct)


        # Reverse Transfer
        usd_balance_ratio = self.exchanges[1].balance.usd / self.exchanges[0].balance.usd


        # if balance_ratio < 0.2:
        #   acceptable_arb_pct = 2
        # elif balance_ratio > 0.2 and balance_ratio < 0.5:
        #   acceptable_arb_pct = 1.0
        # elif balance_ratio > 0.5 and balance_ratio < 2:
        #   acceptable_arb_pct = 0
        # elif balance_ratio > 2 and balance_ratio < 5:
        #   acceptable_arb_pct = -0.5
        # elif balance_ratio > 5:
        #   acceptable_arb_pct = -1.0

        if usd_balance_ratio < 0.5:
          acceptable_arb_pct = 1.0
        elif usd_balance_ratio > 0.5 and usd_balance_ratio < 2:
          acceptable_arb_pct = 0.0
        elif usd_balance_ratio > 2:
          acceptable_arb_pct = -1.0

        print 'Bitfinex Buy ---> Btce Sell ARB PCT: ' + str(acceptable_arb_pct)
        # Execute trades
        # Buying in 1 and selling in 0
        self.executeArb(self.exchanges[1], self.exchanges[0], acceptable_arb_pct)
      except:
        pass


      print 'Sleeping...'
      time.sleep(2)
