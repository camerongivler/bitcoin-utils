#!/usr/bin/env python3
import os, time, sys
from wallet import Wallet
from krakenapi import Kraken
from geminiapi import Gemini
from gdaxapi import Gdax
from itertools import combinations
from exchangepair import ExchangePair

#Set up 'exchanges' dictionary to hold all of the exchanges
exchanges = {}
exchanges["kraken"] = Kraken()
exchanges["gdax"] = Gdax()
#exchanges["gemini"] = Gemini()

exchangePairs = []
for exchange in combinations(exchanges.values(), 2): # 2 for pairs, 3 for triplets, etc
    exchangePairs.append(ExchangePair(exchange[0], exchange[1]))

arbitrar = "USD"
for exchange in exchanges.values():
    exchange.setArbitrar(arbitrar)

cutoff = 1.22 # %  - this will guarentee 0.1% per trade
#cutoff = 0.1 # for testing
runningAverage = 0.2 #keep track of the running average over the past ~2 hours

trades=[]
#First trade loses money, but gets the ball rolling
last = runningAverage-cutoff/2
totalGain = 1

#Infinite loop
while True:
    os.system('clear')

    #always print out how much money there is each wallet that has money
    for exchName,exchange in exchanges.items():
        print(exchName)
        for walletName,wallet in exchange.wallets.items():
            if wallet.amount > 0: print(wallet.currency,":",wallet.amount)
    print()

    for exchange in exchangePairs: # 2 for pairs, 3 for triplets, etc
        # Check to make sure exactly one has USD
        arbitrarExchange = 0
        if exchange[0].valueWallet.currency == arbitrar:
            arbitrarExchange = 1
        if exchange[1].valueWallet.currency == arbitrar:
            arbitrarExchange += 2
        if arbitrarExchange == 0 or arbitrarExchange == 3:
            continue
        i = 0
        try:
            bestDiff = runningAverage
            bestKey = ""
            bestPrice1 = 0
            bestPrice2 = 0
            
            #for each coin wallet in a certain exchange wallet
            #make sure it is a coin wallet and increase i by 1
            for key in exchange[0].wallets.keys():
                if key == arbitrar: continue
                if not key in exchange[1].wallets.keys(): continue
                i += 1
                
                #get last trade prices for two different exchanges and see the difference 
                symbol = key + "-" + arbitrar
                price1 = exchange[0].getLastTradePrice(symbol)
                price2 = exchange[1].getLastTradePrice(symbol)
                diff = price2 - price1
                diffp = diff / (price1  if price1 < price2 else price1) * 100
                # About 3600 price checks every 2 hours
                runningAverage = runningAverage * 3599/ 3600 + diffp/3600
                if diffp > bestDiff and arbitrarExchange == 1 or diffp < bestDiff and arbitrarExchange == 2:
                    bestDiff = diffp
                    bestKey = key
                    bestPrice1 = price1
                    bestPrice2 = price2

                # Print higher first
                print(symbol,":", (exchange[0].getName() if diff < 0 else exchange[1].getName()).ljust(6),
                        str("%.3f" % diffp).rjust(6) + "%")

            print()
            print("runningAverage: " + str("%.3f" % runningAverage) + "%")
            goal = 0
            if arbitrarExchange == 1:
                minimum = runningAverage + cutoff/4
                goal = last + cutoff if last + cutoff > minimum else minimum
                print("goal : >" + str("%.3f" % goal) + "%")

            if arbitrarExchange == 2:
                maximum = runningAverage - cutoff/4
                goal = last - cutoff if last - cutoff < maximum else maximum
                print("goal : <" + str("%.3f" % goal) + "%")
            print()

            if bestDiff >= goal and arbitrarExchange == 1: # price2 is higher
                last, totalGain = exchange.doArbitrage(1, bestKey, bestDiff, last, totalGain, trades)

            if bestDiff <= goal and arbitrarExchange == 2: # price1 is higher
                last, totalGain = exchange.doArbitrage(0, bestKey, bestDiff, last, totalGain, trades)

            for trade in trades:
                print(trade)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            localtime = time.asctime(time.localtime(time.time()))
            trades.append("Unexpected "+exc_type.__name__+
                    " at "+fname +":"+str(exc_tb.tb_lineno)+
                    " on "+localtime+": \"" + str(e) + "\"")
            print(trades[-1])
            time.sleep(2*i if i > 0 else 2)

        # So we don't get rate limited by exchanges
        time.sleep(2*i)

