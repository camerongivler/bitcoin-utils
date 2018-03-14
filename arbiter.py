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
gdaxWallets["BTC"] = Wallet("gdax", "BTC", 0.0541765)
gdaxWallets["USD"] = Wallet("gdax", "USD", 0)
gdaxWallets["value"] = gdaxWallets["BTC"]

geminiWallets = {}
geminiWallets["exchange"] = Gemini()
geminiWallets["ETH"] = Wallet("gemini", "ETH", 0)
geminiWallets["BTC"] = Wallet("gemini", "BTC", 0)
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
cutoff = 1.22 # %  - this will guarentee 0.1% per trade
fee = 0.255 # %

trades=[]
#First trade loses money, but gets the ball rolling
last = -cutoff/2
totalGain = 1

def doArbitrage(exchange1, exchange2, arbitrar, key, price, bestDiff):
    global last, totalGain, trades
    sellWallet = exchanges[exchange1]["value"]
    buyWallet = exchanges[exchange1][arbitrar]
    sellSymbol = sellWallet.currency + "-" + arbitrar
    sellRate = exchanges[exchange1]["exchange"].getLastTradePrice(sellSymbol)
    Exchange.exchange(sellWallet, buyWallet, sellWallet.amount, sellRate)
    exchanges[exchange1]["value"] = buyWallet

    sellWallet = exchanges[exchange2][arbitrar]
    buyWallet = exchanges[exchange2][key]
    buySymbol = key + "-" + arbitrar
    Exchange.exchange(sellWallet, buyWallet, sellWallet.amount, 1/price, fee/100)
    exchanges[exchange2]["value"] = buyWallet

    realDiff = bestDiff - last
    last = bestDiff
    realGain = abs(realDiff) / 2 - 2*fee
    totalGain *= 1 + realGain/100
    trades.append("Sold "+sellSymbol+" at "+str(sellRate)+" on "+exchange1
            +"; Bought "+buySymbol+" at "+str(price)+" on "+exchange2
            +"; diff: " + str("%.3f" % bestDiff) + "%; gain: " + str("%.3f" % realDiff)+"%"
            +"\n\t\tReal Gain: " + str("%.3f" % realGain) + "%; Total (multiplier): "
            +str("%.6f" % totalGain))
            

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

        i = 0
        try:
            os.system('clear')
            for exchName, exchange in exchanges.items():
                print(exchName)
                for walletName, wallet in exchange.items():
                    if walletName == "exchange" or walletName == "value" or wallet.amount == 0: continue
                    print(walletName,":",wallet.amount)
                print()

            bestDiff = 0
            bestKey = ""
            bestPrice1 = 0
            bestPrice2 = 0
            
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
                print(symbol,":", (exchange1 if diff < 0 else exchange2).ljust(6),
                        str("%.3f" % diffp).rjust(6) + "%")

            print()
            goal = 0
            if arbitrarExchange == 1:
                goal = last + cutoff if last + cutoff > 0 else 0
                print("goal : >" + str("%.3f" % goal) + "%")

            if arbitrarExchange == 2:
                goal = last - cutoff if last - cutoff < 0 else 0
                print("goal : <" + str("%.3f" % goal) + "%")
            print()

            if bestDiff >= goal and arbitrarExchange == 1: # price2 is higher
                doArbitrage(exchange2, exchange1, arbitrar, bestKey, bestPrice1, bestDiff)
                        
            if bestDiff <= goal and arbitrarExchange == 2: # price1 is higher
                doArbitrage(exchange1, exchange2, arbitrar, bestKey, bestPrice2, bestDiff)

            for trade in trades:
                print(trade)
            
        except Exception as e:
            trades.append("Unexpected error: " + str(e))
            time.sleep(2*i)

        # So we don't get rate limited by exchanges
        time.sleep(2*i)

