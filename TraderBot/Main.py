import json
import subprocess as sp
from datetime import datetime

import time
import gdax

from CsvTrader import CsvTrader
from TraderBot.HistoricTrader import HistoricTrader
from TradingAlgorithm import TradingAlgorithm
from wallet import Wallet

public_client = gdax.PublicClient()

keys = json.load(open('../gdaxKey.json'))

# Sandbox API
auth_client = gdax.AuthenticatedClient(**keys)

#trader = HistoricTrader(public_client, auth_client)
trader = CsvTrader()

current_time = datetime(2016, 1, 1, 12, 30)

trader.set_current_time(current_time)

algo = TradingAlgorithm()
btc_wallet = Wallet('btc', 1)
usd_wallet = Wallet('usd', 500)
orig_value = None
first = None

last = None
try:
    while True:
        curr = trader.get_current_price()
        print(str(trader.get_current_time()) + ' - $' + str(curr))

        if curr is None:
            continue
        if first is None:
            first = curr

        buy = algo.how_much_btc_to_buy(curr, last, btc_wallet.amount, usd_wallet.amount)
        sell = algo.how_much_btc_to_sell(curr, last, btc_wallet.amount, usd_wallet.amount)

        if buy > 0:
            btc_wallet.amount += buy
            usd_wallet.amount -= buy * curr

        if sell > 0:
            btc_wallet.amount -= sell
            usd_wallet.amount += sell * curr

        total = usd_wallet.amount + btc_wallet.amount * curr

        if orig_value is None:
            orig_value = total

        mult = total/orig_value
        hold = curr/first

        print('btc      : ' + str(btc_wallet.amount))
        print('btc value: ' + str(btc_wallet.amount * curr))
        print('usd      : ' + str(usd_wallet.amount))
        print('total    : ' + str(total))
        print('orig     : ' + str(orig_value))
        print('mult     : ' + str(mult))
        print('HODL     : ' + str(hold))
        print('win pct  : ' + str(round((mult/hold - 1), 5) * 100) + '%')

        sp.call('clear', shell=True)

        last = curr
        trader.increment_time()
        if trader.is_finished():
            break
except KeyboardInterrupt:
    pass
