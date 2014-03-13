
from btce_withdrawal import BTCEWithdrawal
import sys, os

print sys.argv[1]

bw = BTCEWithdrawal()
bw.setup()
bw.login()
bw.go(sys.argv[1])
