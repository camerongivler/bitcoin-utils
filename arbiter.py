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
gdaxWallets["BTC"] = Wallet("gdax", "BTC", 0.052212)
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

def doArbitrage(exchange1, exchange2, arbitrar, key, price):
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

        trades.append("Sold "+sellSymbol+" at "+str(sellRate)+
                "; Bought "+buySymbol+" at "+str(price))

        time.sleep(3)


while True:
    for combo in combinations(exchanges, 2):  # 2 for pairs, 3 for triplets, etc
        exchange1 = combo[0]
        exchange2 = combo[1]
        if exchange1 == exchange2: continue
        for key in exchanges[exchange1].keys():
            if key == arbitrar or key == "exchange" or key == "value": continue
            if not key in exchanges[exchange2].keys(): continue

            first = exchanges[exchange1]["exchange"]
            second = exchanges[exchange2]["exchange"]

            symbol = key + "-" + arbitrar
            price1 = first.getLastTradePrice(symbol)
            price2 = second.getLastTradePrice(symbol)

            diff = price2 - price1
            diffp = diff / (price1  if price1 < price2 else price1) * 100

            os.system('clear')

            for exchName, exchange in exchanges.items():
                print(exchName)
                for walletName, wallet in exchange.items():
                    if walletName == "exchange" or walletName == "value": continue
                    print(walletName,":",wallet.amount)
                print()

            # Print higher first
            print("Symbol     :", symbol)
            if(price1 >= price2):
                print(exchange1.ljust(10),":", "%.2e" % price1)
            print(exchange2.ljust(10),":", "%.2e" % price2)
            if(price1 < price2) :
                print(exchange1.ljust(10),":", "%.2e" % price1)

            #print("Diff       :", "%.2e" % diff)
            print("Diff %     :", str("%.3f" % diffp) + "%\n")

            if diffp > cutoff and exchanges[exchange1]["value"].currency == arbitrar: # price2 is higher
                doArbitrage(exchange2, exchange1, arbitrar, key, price1)
                trades[-1]+="; diff: " + str("%.3f" % diffp) + "%"
                        
            if diffp < -cutoff and exchanges[exchange2]["value"].currency == arbitrar: # price1 is higher
                doArbitrage(exchange1, exchange2, arbitrar, key, price2)
                trades[-1]+="; diff: " + str("%.3f" % diffp) + "%"

            for trade in trades:
                print(trade)
            print()

            time.sleep(2)
