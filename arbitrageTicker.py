#!/usr/bin/env python3
import os
import time
from itertools import combinations

from gdaxapi import Gdax
from geminiapi import Gemini
from krakenapi import Kraken
from wallet import Wallet

maxDiff = 0
maxDiffp = 0
minDiff = 0
minDiffp = 0
maxSymbol = ""
minSymbol = ""
maxExchange = ""
minExchange = ""

gdaxWallets = {"exchange": Gdax(),
               "LTC": Wallet("gdax", "LTC", 2.835),
               "ETH": Wallet("gdax", "ETH", 0.734),
               "BCH": Wallet("gdax", "BCH", 0.503),
               "BTC": Wallet("gdax", "BTC", 0.503),
               "USD": Wallet("gdax", "USD", 500)}

geminiWallets = {"exchange": Gemini(),
                 "ETH": Wallet("gemini", "ETH", 0.734),
                 "BTC": Wallet("gemini", "BTC", 0.503),
                 "USD": Wallet("gemini", "USD", 500)}

krakenWallets = {"exchange": Kraken(),
                 "LTC": Wallet("kraken", "LTC", 2.835),
                 "ETH": Wallet("kraken", "ETH", 0.734),
                 "BCH": Wallet("kraken", "BCH", 0.503),
                 "BTC": Wallet("kraken", "BTC", 0.503),
                 "USD": Wallet("kraken", "USD", 500)}

exchanges = {"kraken": krakenWallets, "gdax": gdaxWallets}

# exchanges["gemini"] = geminiWallets

arbitrar = "USD"

while True:
    for combo in combinations(exchanges, 2):  # 2 for pairs, 3 for triplets, etc
        exchange1 = combo[0]
        exchange2 = combo[1]
        if exchange1 == exchange2: continue
        for key in exchanges[exchange1].keys():
            if key == arbitrar or key == "exchange": continue
            if key not in exchanges[exchange2].keys(): continue

            first = exchanges[exchange1]["exchange"]
            second = exchanges[exchange2]["exchange"]

            symbol = key + "-" + arbitrar
            price1 = first.get_last_trade_price(symbol)
            price2 = second.get_last_trade_price(symbol)

            diff = price2 - price1
            diffp = diff / (price1 if price1 < price2 else price1) * 100

            if diffp > maxDiffp:
                maxDiff = diff
                maxDiffp = diffp
                maxSymbol = symbol
                maxExchange = exchange1 + "-" + exchange2

            if diffp < minDiffp:
                minDiff = diff
                minDiffp = diffp
                minSymbol = symbol
                minExchange = exchange1 + "-" + exchange2

            os.system('clear')

            # Print higher first
            print("Symbol     :", symbol)
            if price1 >= price2:
                print(exchange1.ljust(10), ":", "%.2e" % price1)
            print(exchange2.ljust(10), ":", "%.2e" % price2)
            if price1 < price2:
                print(exchange1.ljust(10), ":", "%.2e" % price1)

            print("Diff       :", "%.2e" % diff)
            print("Diff %     :", str("%.3f" % diffp) + "%\n")

            print("MaxSymbol  :", maxSymbol)
            print("MaxExchange:", maxExchange)
            print("MaxDiff    :", "%.2e" % maxDiff)
            print("MaxDiff %  :", str("%.3f" % maxDiffp) + "%\n")

            print("MinSymbol  :", minSymbol)
            print("MinExchange:", minExchange)
            print("MinDiff    :", "%.2e" % minDiff)
            print("MinDiff %  :", str("%.3f" % minDiffp) + "%")

            time.sleep(2)
