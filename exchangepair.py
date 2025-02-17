#!/usr/bin/env python3


class ExchangePair:

    def __init__(self, cutoff, exchange0, exchange1):
        self.exchange0 = exchange0
        self.exchange1 = exchange1
        self.runningAverages = {}  # keep track of the running average over the past ~2 hours
        for key in exchange0.wallets.keys():
            self.runningAverages[key] = -0.25
        self.last = 0.2 - cutoff / 2

    def __getitem__(self, index):
        if index == 0:
            return self.exchange0
        elif index == 1:
            return self.exchange1
        else:
            raise IndexError("Exchange Pair contains indices 0 and 1")

    def get_diff(self, key):
        buy_exchange = (0 if self[0].arbitrar == self[0].valueWallet else 1)
        # symbol = key + "-" + self[0].arbitrar.currency
        if buy_exchange == 0:
            price1 = self[0].get_buy_price_for(key)
            price2 = self[1].get_sell_price()
        else:
            price1 = self[0].get_sell_price()
            price2 = self[1].get_buy_price_for(key)

        return self.calculate_diff(key, price1, price2)

    def calculate_diff(self, key, price1, price2):
        symbol = key + "-" + self[0].arbitrar.currency

        diff = price2 - price1
        diffp = diff / (price1 if price1 < price2 else price1) * 100
        # Print higher first
        print(symbol, ":", (self[0].get_name() if diff < 0 else self[1].get_name()).ljust(6),
              str("%.3f" % diffp).rjust(6) + "%\n")

        # About 43200 price checks every 24 hours
        # self.runningAverages[key] = (self.runningAverages[key] * 43199 + diffp)/43200
        # About 3600 price checks every 2 hours
        # self.runningAverages[key] = (self.runningAverages[key] * 3599 + diffp)/3600
        # print("runningAverage: " + str("%.3f" % self.runningAverages[key]) + "%")

        return diffp

    # exchange is 0 or 1 - this is for multiple crypto arbitrage
    # def buy(self, exchange):
    #    buyExch = self[exchange]
    #    bestKey = None
    #    bestDiff = float('Inf') if exchange == 1 else -float('Inf')
    #    i = 0
    #    for key in self[0].wallets.keys():
    #        if key == buyExch.arbitrar.currency: continue
    #        if not key in self[1].wallets.keys(): continue
    #        symbol = key+"-"+buyExch.arbitrar.currency
    #        price1 = self[exchange].getLastTradePrice(symbol)
    #        price2 = self[not exchange].getLastTradePrice(symbol)
    #        diffp = self.calculateDiff(key, price1, price2)
    #        normalizedDiff = diffp - self.runningAverages[key]
    #        i += 1

    #        if normalizedDiff > bestDiff and exchange == 0 or normalizedDiff < bestDiff and exchange == 1:
    #            bestKey = key
    #            bestDiff = normalizedDiff

    #    buySymbol, buyRate = buyExch.buy(bestKey)
    #    self.last = bestDiff
    #    time.sleep(max(2*i, 2))

    #    return buySymbol, buyRate, bestKey
