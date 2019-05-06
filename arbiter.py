#!/usr/bin/env python3
import os
import sys
import time
import traceback
from itertools import combinations
from multiprocessing.pool import ThreadPool

from exchangebase import ExchangeBase
from exchangepair import ExchangePair
from gdaxapi import Gdax
from krakenapi import Kraken


class Arbiter:

    def __init__(self):
        # Set up 'exchanges' dictionary to hold all of the exchanges
        self.exchanges = {"kraken": Kraken(), "gdax": Gdax()}
        # exchanges["gemini"] = Gemini()

        self.cutoff = 0.1  # %gain on the trade

        self.exchangePairs = []
        for exchange in combinations(self.exchanges.values(), 2):  # 2 for pairs, 3 for triplets, etc
            self.exchangePairs.append(ExchangePair(self.cutoff, exchange[0], exchange[1]))

        self.arbitrar = "USD"
        self.lastKey = ""
        for exchange in self.exchanges.values():
            exchange.set_arbitrar(self.arbitrar)
            if exchange.valueWallet.currency != self.arbitrar:
                self.lastKey = exchange.valueWallet.currency

        self.trades = []
        # First trade loses money, but gets the ball rolling
        self.totalGain = 1

        self.pool = ThreadPool(processes=2)

    def run(self):
        os.system('clear')

        # always print out how much money there is each wallet that has money
        for exchName, exchange in self.exchanges.items():
            print(exchName)
            for walletName, wallet in exchange.wallets.items():
                if wallet.amount > 0:
                    print(wallet.currency, ":", round(wallet.amount, 5))
        print()

        for exchange in self.exchangePairs:  # 2 for pairs, 3 for triplets, etc
            # Check to make sure exactly one has USD
            arbitrar_exchange = 0
            if exchange[0].valueWallet.currency == self.arbitrar:
                arbitrar_exchange = 1
            if exchange[1].valueWallet.currency == self.arbitrar:
                arbitrar_exchange += 2
            if arbitrar_exchange == 0 or arbitrar_exchange == 3:
                continue
            i = 1
            try:
                diffp = exchange.get_diff(self.lastKey)

                last = exchange.last

                goal = 0
                if arbitrar_exchange == 1:
                    # goal = exchange.runningAverages[lastKey] + cutoff/2
                    goal = self.cutoff / 2
                    # goal = last + cutoff if last + cutoff > minimum else minimum
                    print("goal : >" + str("%.3f" % goal) + "%")

                if arbitrar_exchange == 2:
                    # goal = exchange.runningAverages[lastKey] - cutoff/2
                    goal = -self.cutoff / 2
                    # goal = last - cutoff if last - cutoff < maximum else maximum
                    print("goal : <" + str("%.3f" % goal) + "%")
                print()

                if diffp >= goal and arbitrar_exchange == 1 \
                        or diffp <= goal and arbitrar_exchange == 2:
                    sell_exchange = 1 if arbitrar_exchange == 1 else 0
                    buy_exchange = 0 if arbitrar_exchange == 1 else 1

                    # buy_symbol, buy_rate, lastKey = exchange.buy(buy_exchange)

                    # Do the buys and sells asynchronously
                    async_sell = self.pool.apply_async(ExchangeBase.sell, (exchange[sell_exchange],))
                    async_buy = self.pool.apply_async(ExchangeBase.buy, (exchange[buy_exchange], self.lastKey))
                    buy_symbol, buy_rate = async_buy.get()
                    sell_symbol, sell_rate = async_sell.get()

                    exchange.last = diffp

                    total_value = exchange[buy_exchange].get_value() + exchange[sell_exchange].get_value()
                    # last = difference between exchanges on last trade
                    real_diff = exchange.last - last

                    # divide by 2 bc we only make money on money in crypto,
                    # then again because we only make money in 1 direction (pos or neg)
                    real_gain = (sell_rate / buy_rate - 1) / 2 * 100
                    self.totalGain *= 1 + real_gain / 100
                    localtime = time.asctime(time.localtime(time.time()))

                    self.trades.append(
                        "Sold " + sell_symbol + " at " + str(sell_rate) + " on " + exchange[sell_exchange].get_name()
                        + "; Bought " + buy_symbol + " at " + str(buy_rate) + " on " + exchange[
                            buy_exchange].get_name()
                        + "; diff: " + str("%.3f" % exchange.last) + "%; gain: " + str("%.3f" % real_diff) + "%"
                        + "\n\tReal Gain: " + str("%.3f" % real_gain) + "%; Total (multiplier): "
                        + str("%.6f" % self.totalGain) + "; time: " + localtime
                        + "\n\t\tTotal Value of portfolio: " + str(total_value))

                for trade in self.trades:
                    print(trade)

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                localtime = time.asctime(time.localtime(time.time()))
                self.trades.append("Unexpected " + exc_type.__name__ +
                                   " at " + fname + ":" + str(exc_tb.tb_lineno) +
                                   " on " + localtime + ": \"" + str(e) + "\"")
                print(self.trades[-1])
                print(traceback.format_exc())
                time.sleep(max(2 * i, 2))

            # So we don't get rate limited by exchanges
            time.sleep(max(2 * i, 2))


if __name__ == "__main__":
    arbiter = Arbiter()

    # Infinite loop
    while True:
        try:
            arbiter.run()
        except KeyboardInterrupt:
            print("Goodbye.")
            break
