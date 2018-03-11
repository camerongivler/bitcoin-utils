#!/usr/bin/env python3
import krakenex, gdax, os, time
from pykrakenapi import KrakenAPI

#GDAX
g = gdax.PublicClient()

#Kraken
api = krakenex.API()
k = KrakenAPI(api)

maxDiff = 0
maxDiffp = 0

tickers = ["BTC-USD", "BCH-USD", "ETH-USD", "LTC-USD"]
               #"BCH-BTC", "ETH-BTC", "LTC-BTC"]
i = 0
while True:
    gdaxSymbol = tickers[i]
    i = (i + 1) % len(tickers)
    krakenSymbol = gdaxSymbol.replace("BTC", "XBT").replace("-","")

    krakenTicker = k.get_ticker_information(krakenSymbol)
    # c = last trade
    kraken = 1/float(krakenTicker['c'][0][0])

    gdax= 1/float(g.get_product_ticker(gdaxSymbol)['price'])

    diff = abs(gdax - kraken)
    diffp = diff / (gdax  if gdax < kraken else kraken) * 100

    if diffp > maxDiffp:
        maxDiff = diff
        maxDiffp = diffp
        maxSymbol = gdaxSymbol

    os.system('clear')

    # Print higher first
    print("Symbol    :", gdaxSymbol)
    if(gdax >= kraken):
        print("GDAX      :", "%.2e" % gdax)
    print("Kraken    :", "%.2e" % kraken)
    if(gdax < kraken):
        print("GDAX      :", "%.2e" % gdax)

    print("Diff      :", "%.2e" % diff)
    print("Diff %    :", str("%.3f" % diffp) + "%\n")

    print("MaxSymbol :", maxSymbol)
    print("MaxDiff   :", "%.2e" % maxDiff)
    print("MaxDiff % :", str("%.3f" % maxDiffp) + "%")

    time.sleep(2)
