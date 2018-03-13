#!/usr/bin/env python3
import os, time
from wallet import Wallet, Exchange
from krakenapi import Kraken
from geminiapi import Gemini
from gdaxapi import Gdax
from itertools import combinations

gdaxWallets = {}
gdaxWallets["exchange"] = Gdax()
gdaxWallets["LTC"] = Wallet("gdax", "LTC", 0)
gdaxWallets["ETH"] = Wallet("gdax", "ETH", 0)
gdaxWallets["BCH"] = Wallet("gdax", "BCH", 0)
gdaxWallets["BTC"] = Wallet("gdax", "BTC", 0.0548)
gdaxWallets["USD"] = Wallet("gdax", "USD", 0)
gdaxWallets["value"] = gdaxWallets["BTC"]

geminiWallets = {}
geminiWallets["exchange"] = Gemini()
geminiWallets["ETH"] = Wallet("gemini", "ETH", 0)
geminiWallets["BTC"] = Wallet("gemini", "BTC", 0.052212)
geminiWallets["USD"] = Wallet("gemini", "USD", 0)
geminiWallets["value"] = geminiWallets["BTC"]

krakenWallets = {}
krakenWallets["exchange"] = Kraken()
krakenWallets["LTC"] = Wallet("kraken", "LTC", 0)
krakenWallets["ETH"] = Wallet("kraken", "ETH", 0)
krakenWallets["BCH"] = Wallet("kraken", "BCH", 0)
krakenWallets["BTC"] = Wallet("kraken", "BTC", 0)
krakenWallets["USD"] = Wallet("kraken", "USD", 500)
krakenWallets["value"] = krakenWallets["USD"]

exchanges = {}
exchanges["kraken"] = krakenWallets
exchanges["gdax"] = gdaxWallets
#exchanges["gemini"] = geminiWallets

arbitrar = "USD"
cutoff = 0.75

trades=[]
#First trade loses money, but gets the ball rolling
last = -0.375

def doArbitrage(exchange1, exchange2, arbitrar, key, price, bestDiff):
        sellWallet = exchanges[exchange1]["value"]
        buyWallet = exchanges[exchange1][arbitrar]
        sellSymbol = sellWallet.currency + "-" + arbitrar
        sellRate = exchanges[exchange1]["exchange"].getLastTradePrice(sellSymbol)
        Exchange.exchange(sellWallet, buyWallet, sellWallet.amount, sellRate)
        exchanges[exchange1]["value"] = buyWallet

        sellWallet = exchanges[exchange2][arbitrar]
        buyWallet = exchanges[exchange2][key]
        buySymbol = key + "-" + arbitrar
        Exchange.exchange(sellWallet, buyWallet, sellWallet.amount, 1/price)
        exchanges[exchange2]["value"] = buyWallet

        realDiff = bestDiff - last
        trades.append("Sold "+sellSymbol+" at "+str(sellRate)+" on "+exchange1
                +"; Bought "+buySymbol+" at "+str(price)+" on "+exchange2
                +"; diff: " + str("%.3f" % realDiff) + "%")

        last = bestDiff

        time.sleep(2)

while True:
    for combo in combinations(exchanges, 2):  # 2 for pairs, 3 for triplets, etc
        exchange1 = combo[0]
        exchange2 = combo[1]
        if exchange1 == exchange2: continue

        # Check to make sure exactly one has USD
        arbitrarExchange = 0
        if exchanges[exchange1]["value"].currency == arbitrar:
            arbitrarExchange = 1
        if exchanges[exchange2]["value"].currency == arbitrar:
            arbitrarExchange += 2
        if arbitrarExchange == 0 or arbitrarExchange == 3:
            continue

        os.system('clear')
        for exchName, exchange in exchanges.items():
            print(exchName)
            for walletName, wallet in exchange.items():
                if walletName == "exchange" or walletName == "value": continue
                print(walletName,":",wallet.amount)
            print()

        bestDiff = 0
        bestKey = ""
        bestPrice1 = 0
        bestPrice2 = 0
        i = 0
        
        for key in exchanges[exchange1].keys():
            if key == arbitrar or key == "exchange" or key == "value": continue
            if not key in exchanges[exchange2].keys(): continue
            i += 1

            first = exchanges[exchange1]["exchange"]
            second = exchanges[exchange2]["exchange"]

            symbol = key + "-" + arbitrar
            price1 = first.getLastTradePrice(symbol)
            price2 = second.getLastTradePrice(symbol)

            diff = price2 - price1
            diffp = diff / (price1  if price1 < price2 else price1) * 100
            if diffp > bestDiff and arbitrarExchange == 1 or diffp < bestDiff and arbitrarExchange == 2:
                bestDiff = diffp
                bestKey = key
                bestPrice1 = price1
                bestPrice2 = price2

            # Print higher first
            print("Symbol :", symbol)
            print("Diff % :", exchange1 if diff < 0 else exchange2, str("%.3f" % diffp) + "%\n")

        if bestDiff >= cutoff + last and arbitrarExchange == 1: # price2 is higher
            doArbitrage(exchange2, exchange1, arbitrar, bestKey, bestPrice1, bestDiff)
                    
        if bestDiff <= last - cutoff and arbitrarExchange == 2: # price1 is higher
            doArbitrage(exchange1, exchange2, arbitrar, bestKey, bestPrice2, bestDiff)

        for trade in trades:
            print(trade)
        print()

        time.sleep(2*i)

