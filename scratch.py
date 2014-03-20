#!/usr/bin/python
from bitfinex import Bitfinex
from btce import BTCE
from bot import Bot

bfinex = Bitfinex()
btce = BTCE()

bot = Bot()
bot.addExchange(btce)
bot.addExchange(bfinex)


print 'Running Bot'
bot.run()

#btcelogin.btce_to_bitfinex(0, 'haha')
