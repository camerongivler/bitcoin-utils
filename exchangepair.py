#!/usr/bin/env python3
import time

class ExchangePair:

    def __init__(self, exchange0, exchange1):
        self.exchange0 = exchange0
        self.exchange1 = exchange1

    def __getitem__(self, index):
        if index == 0:
            return self.exchange0
        elif index == 1:
            return self.exchange1
        else:
            raise IndexError( "Exchange Pair contains indices 0 and 1" )

    def getDiff(self, key, exchange):
        symbol = key + "-" + self[exchange].arbitrar.currency
        price1 = self[0].getLastTradePrice(symbol)
        price2 = self[1].getLastTradePrice(symbol)
        diff = price2 - price1
        diffp = diff / (price1  if price1 < price2 else price1) * 100
        # Print higher first
        print(symbol,":", (self[0].getName() if diff < 0 else self[1].getName()).ljust(6),
                str("%.3f" % diffp).rjust(6) + "%")
        price = price1 if exchange == 0 else price2
        return diffp, price

    # exchange is 0 or 1
    def buy(self, exchange, runningAverage):
        buyExch = self[exchange]
        bestKey = None
        bestDiff = float('Inf') if exchange == 0 else -float('Inf')
        bestPrice = 0
        i = 0
        for key in self[0].wallets.keys():
            if key == buyExch.arbitrar.currency: continue
            if not key in self[1].wallets.keys(): continue
            diffp, price = self.getDiff(key, exchange)
            runningAverage = runningAverage * 3599 / 3600 + diffp/3600
            i += 1

            if diffp < bestDiff and exchange == 0 or diffp > bestDiff and exchange == 1:
                bestKey = key
                bestDiff = diffp
                bestPrice = price

        buyExch.buy(bestKey)
        time.sleep(2*i if i > 0 else 2)

        buySymbol = buyExch.valueWallet.currency + "-" + buyExch.arbitrar.currency
        return buySymbol, bestPrice, bestKey, runningAverage
