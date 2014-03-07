from bitfinex import Bitfinex
from btce import BTCE
from bot import Bot

bfinex = Bitfinex()
btce = BTCE()

bot = Bot()
bot.addExchange(bfinex)
bot.addExchange(btce)

bot.run()
