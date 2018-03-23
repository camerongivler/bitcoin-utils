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
lastKey = ""
for exchange in exchanges.values():
    exchange.setArbitrar(arbitrar)
    if exchange.valueWallet.currency != arbitrar:
        lastKey = exchange.valueWallet.currency

cutoff = 1.42 # %  - this will guarentee 0.2% per trade
#cutoff = 0 # for testing
runningAverage = 0.15 #keep track of the running average over the past ~2 hours

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
            if wallet.amount > 0: print(wallet.currency,":",round(wallet.amount,5))
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
        i = 1
        try:
            diffp, price = exchange.getDiff(lastKey, 0)

            # About 3600 price checks every 2 hours
            runningAverage = runningAverage * 3599/ 3600 + diffp/3600
            print()
            print("runningAverage: " + str("%.3f" % runningAverage) + "%")

            goal = 0
            if arbitrarExchange == 1:
                minimum = runningAverage + cutoff/3
                goal = last + cutoff if last + cutoff > minimum else minimum
                print("goal : >" + str("%.3f" % goal) + "%")

            if arbitrarExchange == 2:
                maximum = runningAverage - cutoff/3
                goal = last - cutoff if last - cutoff < maximum else maximum
                print("goal : <" + str("%.3f" % goal) + "%")
            print()

            if diffp >= goal and arbitrarExchange == 1 \
                    or diffp <= goal and arbitrarExchange == 2:

                sellExchange = 1 if arbitrarExchange == 1 else 0
                buyExchange = 0 if arbitrarExchange == 1 else 1

                sellSymbol, sellRate = exchange[sellExchange].sell()
                buySymbol, buyRate, lastKey, runningAverage = exchange.buy(0, runningAverage)

                totalValue = exchange[buyExchange].getValue() + exchange[sellExchange].getValue()
                #last = difference between exchanges on last trade
                realDiff = diffp - last
                exchange1fee = 2 * exchange[buyExchange].getFee() * exchange[buyExchange].getValue() / totalValue
                exchange2fee = 2 * exchange[sellExchange].getFee() * exchange[sellExchange].getValue() / totalValue
                realGain = abs(realDiff) / 2 - exchange1fee - exchange2fee
                totalGain *= 1 + realGain/100
                last = diffp
                localtime = time.asctime( time.localtime(time.time()) )

                trades.append("Sold "+sellSymbol+" at "+str(sellRate)+" on "+exchange[sellExchange].getName()
                        +"; Bought "+buySymbol+" at "+str(buyRate)+" on "+exchange[buyExchange].getName()
                        +"; diff: " + str("%.3f" % diffp) + "%; gain: " + str("%.3f" % realDiff)+"%"
                        +"\n\tReal Gain: " + str("%.3f" % realGain) + "%; Total (multiplier): "
                        +str("%.6f" % totalGain) + "; time: "+localtime
                        +"\n\t\tTotal Value of portfolio: "+str(totalValue))

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
        time.sleep(2*i if i > 0 else 2)

