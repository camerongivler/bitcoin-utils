#!/usr/bin/env python3
import time
from exchangebase import ExchangeBase

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


    # seller is either 1 or 0, indicating which wallet should sell crypto
    # The other wallet will buy crypto
    def doArbitrage(self, seller, key, bestDiff, last, totalGain, trades):

        exchange1 = self[seller]
        exchange2 = self[not seller]

        sellWallet = exchange1.valueWallet
        buyWallet = exchange1.arbitrar
        sellSymbol = sellWallet.currency + "-" + buyWallet.currency
        sellRate = exchange1.getLastTradePrice(sellSymbol)
        
        exchange1.transact(sellWallet, buyWallet, sellRate)

        sellWallet = exchange2.arbitrar
        buyWallet = exchange2.wallets[key]
        buySymbol = key + "-" + sellWallet.currency
        buyRate = exchange2.getLastTradePrice(buySymbol)

        # 1/buyrate because many exchanges don't accept USD-BTC
        exchange2.transact(sellWallet, buyWallet, 1/buyRate)

        totalValue = exchange1.getValue() + exchange2.getValue()
        #last = difference between exchanges on last trade
        realDiff = bestDiff - last

        # calculate more accurate fees based on how much money is in each exchange
        exchange1fee = 2 * exchange1.getFee() * exchange1.getValue() / totalValue
        exchange2fee = 2 * exchange2.getFee() * exchange2.getValue() / totalValue
        realGain = abs(realDiff) / 2 - exchange1fee - exchange2fee
        totalGain *= 1 + realGain/100
        localtime = time.asctime( time.localtime(time.time()) )
        trades.append("Sold "+sellSymbol+" at "+str(sellRate)+" on "+exchange1.getName()
                +"; Bought "+buySymbol+" at "+str(buyRate)+" on "+exchange2.getName()
                +"; diff: " + str("%.3f" % bestDiff) + "%; gain: " + str("%.3f" % realDiff)+"%"
                +"\n\tReal Gain: " + str("%.3f" % realGain) + "%; Total (multiplier): "
                +str("%.6f" % totalGain) + "; time: "+localtime
                +"\n\t\tTotal Value of portfolio: "+str(totalValue))

        time.sleep(4)
        return bestDiff, totalGain
