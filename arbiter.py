#!/usr/bin/env python3
import os, time
from wallet import Wallet
from krakenapi import Kraken
from geminiapi import Gemini
from gdaxapi import Gdax
from itertools import combinations

gemini.wallets["exchange"] = Gemini()
gdax.wallets["exchange"] = Gdax()
kraken.wallets["exchange"] = Kraken()

#Set up 'exchanges' dictionary to hold all of exchange wallets
exchanges = {}
exchanges["kraken"] = kraken.wallets
exchanges["gdax"] = gdax.wallets
exchanges["gemini"] = gemini.wallets

arbitrar = "USD"
cutoff = 1.22 # %  - this will guarentee 0.1% per trade
fee = 0.255 # %

trades=[]
#First trade loses money, but gets the ball rolling
#last = -cutoff/2
last = 0.408
totalGain = 1

def doArbitrage(exchange1, exchange2, arbitrar, key, price, bestDiff):

#Access the global variables already defined before the function
    global last, totalGain, trades

#sellWallet - Accesses the wallet of a certain exchange that has money in it. 
#"exchanges" is the dictionary containing all of the exchange wallets (i.e. krakenWallets). 
#[exchange1] is an inputted parameter and will access that inputted exchange wallet. 
#["value"] is which wallet had money in it.
    sellWallet = exchanges[exchange1]["value"]

#buyWallet - Access the USD wallet of an exchange wallet. 
#"exchanges" is the dictionary containing all of the exchange wallets (i.e. krakenWallets). 
#[exchange1] is an inputted parameter and will access that inputted exchange wallet. 
#[arbitrar] == "USD" -> accesses the USD wallet of an exchange wallet. 
#If the sellWallet is the USD wallet, then sellWallet == buyWallet(is that okay?).   
    buyWallet = exchanges[exchange1][arbitrar]

#sellSymbol - Creates a symbol by accessing the "currency" attribute of the Wallet class
#Adds on "-USD" to it. sellSymbol therefore can be == "USD-USD"(is that okay?).
    sellSymbol = sellWallet.currency + "-" + arbitrar

#sellRate - Accesses the "exchange" class. 
#Calls the "getLastTradePrice" method with the "sellSymbol" parameter on the inputted exchange class (i.e. Gemini()). 
#This returns the last trade price of the ["value"] coin in the exchange.
    sellRate = exchanges[exchange1]["exchange"].getLastTradePrice(sellSymbol)
    
#Moves the number of coins * value (includes fee) and puts it into the buy wallet
    Exchange.transact(sellWallet, buyWallet, sellWallet.amount, sellRate)

#Value of number of coins * value stored here
    exchanges[exchange1]["value"] = buyWallet

#sellWallet variable now changes to become equal to USD wallet of a different exchange.    
    sellWallet = exchanges[exchange2][arbitrar]

#buyWallet variable now becomes equal to the wallet specified by the inputted parameter 
#[key] of the second exchange. 
    buyWallet = exchanges[exchange2][key]

#buySymbol variable equals "[key]-USD"
    buySymbol = key + "-" + arbitrar

#The exchange method is now called again. Subtract everything from the sell wallet 
#and add it to the buy wallet. How come now it is 1/price and fee/100?
    Exchange.transact(sellWallet, buyWallet, sellWallet.amount, 1/price, fee/100)

#Set the value of the [exchange2] wallet == buyWallet 
    exchanges[exchange2]["value"] = buyWallet

#last = difference between exchanges on last trade
    realDiff = bestDiff - last
    last = bestDiff
    realGain = abs(realDiff) / 2 - 2*fee
    totalGain *= 1 + realGain/100
    localtime = time.asctime( time.localtime(time.time()) )
    trades.append("Sold "+sellSymbol+" at "+str(sellRate)+" on "+exchange1
            +"; Bought "+buySymbol+" at "+str(price)+" on "+exchange2
            +"; diff: " + str("%.3f" % bestDiff) + "%; gain: " + str("%.3f" % realDiff)+"%"
            +"\n\tReal Gain: " + str("%.3f" % realGain) + "%; Total (multiplier): "
            +str("%.6f" % totalGain) + "; time: "+localtime)
      
    time.sleep(2)

#Infinite loop
while True:

    #makes sure the exchange wallets are not the same  
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
            
            #loop through exchange wallets
            #i.e. exchName == 'kraken', exchange == krakenWallets
            for exchName, exchange in exchanges.items():
                print(exchName)
                
                #loop through coin wallets in each exchange wallet
                #i.e. walletName == 'LTC', wallet == Wallet object with 'LTC' currency parameter
                for walletName, wallet in exchange.items():
                    
                    #make sure wallet has value and is for one of the coins
                    if walletName == "exchange" or walletName == "value" or wallet.amount == 0: continue
                    
                    #Display the amount in that wallet
                    print(walletName,":",wallet.amount)
                print()

            #define some variables
            bestDiff = 0
            bestKey = ""
            bestPrice1 = 0
            bestPrice2 = 0
            
            #for each coin wallet in a certain exchange wallet
            #make sure it is a coin wallet and increase i by 1
            for key in exchanges[exchange1].keys():
                if key == arbitrar or key == "exchange" or key == "value": continue
                if not key in exchanges[exchange2].keys(): continue
                i += 1
                
                #first and second are equal to two different exchanges
                first = exchanges[exchange1]["exchange"]
                second = exchanges[exchange2]["exchange"]
                
                #get last trade prices for two different exchanges and see the difference 
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
                goal = last + cutoff if last + cutoff > cutoff/4 else cutoff/4
                print("goal : >" + str("%.3f" % goal) + "%")

            if arbitrarExchange == 2:
                goal = last - cutoff if last - cutoff < -cutoff/4 else -cutoff/4
                print("goal : <" + str("%.3f" % goal) + "%")
            print()

            if bestDiff >= goal and arbitrarExchange == 1: # price2 is higher
                doArbitrage(exchange2, exchange1, arbitrar, bestKey, bestPrice1, bestDiff)
                        
            if bestDiff <= goal and arbitrarExchange == 2: # price1 is higher
                doArbitrage(exchange1, exchange2, arbitrar, bestKey, bestPrice2, bestDiff)

            for trade in trades:
                print(trade)
            
        except Exception as e:
            localtime = time.asctime( time.localtime(time.time()) )
            trades.append("Unexpected error(" + localtime + "): " + str(e))
            time.sleep(2*i)

        # So we don't get rate limited by exchanges
        time.sleep(2*i)

