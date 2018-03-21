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
