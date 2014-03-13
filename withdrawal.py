from bitfinex_withdrawal import BitfinexWithdrawal
from btce_withdrawal import BTCEWithdrawal
import keys

def bitfinex_withdrawal(withdrawal_address, amount):
  bw = BitfinexWithdrawal()
  bw.loginAndWithdraw(withdrawal_address, amount)

def btce_withdrawal(withdrawal_address, amount):
  bw = BTCEWithdrawal()
  bw.loginAndWithdraw(withdrawal_address, amount)

if __name__ == '__main__':
  # bitfinex_withdrawal(keys.BTCE_DEPOSIT_ADDRESS, 0.0)
  btce_withdrawal(keys.BITFINEX_DEPOSIT_ADDRESS, 0.0)
