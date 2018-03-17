#!/usr/bin/env python3
import os, time, sys
from wallet import Wallet
from krakenapi import Kraken
from geminiapi import Gemini
from gdaxapi import Gdax
from itertools import combinations

#Set up 'exchanges' dictionary to hold all of the exchanges
exchanges = {}
exchanges["kraken"] = Kraken()
exchanges["gdax"] = Gdax()
#exchanges["gemini"] = Gemini()

arbitrar = "USD"
for exchange in exchanges.values():
    exchange.setArbitrar(arbitrar)

cutoff = 1.22 # %  - this will guarentee 0.1% per trade

trades=[]
#First trade loses money, but gets the ball rolling
last = -cutoff/2
totalGain = 1

def doArbitrage(exchange1, exchange2, arbitrar, key, price, bestDiff):

    #Access the global variables already defined before the function
    global last, totalGain, trades

    sellWallet = exchange1.value
    buyWallet = exchange1.arbitrar
    sellSymbol = sellWallet.currency + "-" + arbitrar
    sellRate = exchange1.getLastTradePrice(sellSymbol)
    
    exchange1.transact(sellWallet, buyWallet, sellWallet.amount, sellRate)

    sellWallet = exchange2.arbitrar
    buyWallet = exchange2.wallets[key]
    buySymbol = key + "-" + arbitrar

    exchange2.transact(sellWallet, buyWallet, sellWallet.amount, 1/price)

    #last = difference between exchanges on last trade
    realDiff = bestDiff - last
    last = bestDiff
    realGain = abs(realDiff) / 2 - exchange1.getFee() - exchange2.getFee()
    totalGain *= 1 + realGain/100
    localtime = time.asctime( time.localtime(time.time()) )
    trades.append("Sold "+sellSymbol+" at "+str(sellRate)+" on "+exchange1.getName()
            +"; Bought "+buySymbol+" at "+str(price)+" on "+exchange2.getName()
            +"; diff: " + str("%.3f" % bestDiff) + "%; gain: " + str("%.3f" % realDiff)+"%"
            +"\n\tReal Gain: " + str("%.3f" % realGain) + "%; Total (multiplier): "
            +str("%.6f" % totalGain) + "; time: "+localtime)
      
    time.sleep(2)

#Infinite loop
while True:
    os.system('clear')

    #always print out how much money there is each wallet that has money
    for exchName,exchange in exchanges.items():
        print(exchName)
        for walletName,wallet in exchange.wallets.items():
            if wallet.amount > 0: print(wallet.currency,":",wallet.amount)
    print()

    for exchange in combinations(exchanges.values(), 2): # 2 for pairs, 3 for triplets, etc
        # Check to make sure exactly one has USD
        arbitrarExchange = 0
        if exchange[0].value.currency == arbitrar:
            arbitrarExchange = 1
        if exchange[1].value.currency == arbitrar:
            arbitrarExchange += 2
        if arbitrarExchange == 0 or arbitrarExchange == 3:
            continue
        i = 0
        try:
            bestDiff = 0
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
                if diffp > bestDiff and arbitrarExchange == 1 or diffp < bestDiff and arbitrarExchange == 2:
                    bestDiff = diffp
                    bestKey = key
                    bestPrice1 = price1
                    bestPrice2 = price2

                # Print higher first
                print(symbol,":", (exchange[0].getName() if diff < 0 else exchange[1].getName()).ljust(6),
                        str("%.3f" % diffp).rjust(6) + "%")

            print()
            goal = 0
            if arbitrarExchange == 1:
                goal = last + cutoff if last + cutoff > cutoff/4 else cutoff/4
                print("goal : >" + str("%.3f" % goal) + "%")

            if arbitrarExchange == 2:
                goal = last - cutoff if last - cutoff < -cutoff/4 else -cutoff/4
                print("goal : <" + str("%.3f" % goal) + "%")
            print()

            if bestDiff >= goal and arbitrarExchange == 1: # price2 is higher
                doArbitrage(exchange[1], exchange[0], arbitrar, bestKey, bestPrice1, bestDiff)
                        
            if bestDiff <= goal and arbitrarExchange == 2: # price1 is higher
                doArbitrage(exchange[0], exchange[1], arbitrar, bestKey, bestPrice2, bestDiff)

            for trade in trades:
                print(trade)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            localtime = time.asctime(time.localtime(time.time()))
            trades.append("Unexpected "+exc_type.__name__+
                    " at "+fname +":"+str(exc_tb.tb_lineno)+
                    " on "+localtime+": \"" + str(e) + "\"")
            time.sleep(2*i)

        # So we don't get rate limited by exchanges
        time.sleep(2*i)

