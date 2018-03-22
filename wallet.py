#!/usr/bin/env python3

class Wallet:
    
    def __init__(self, currency):
        self.currency = currency
        self.amount = self.loadAmount()
        
 #function to load amount of last trade
    def loadAmount(self):
        with open("WalletValue.txt", 'r') as f:
            amountLoaded = f.read()
            return float(amountLoaded)
        
 #function to save value of the wallet to a file after every trade            
    def saveAmount(self):
        with open("WalletValue.txt", "w") as file:
            file.write(self.amount)
            
    def setAmount(self, amount):   
        self.amount = amount
        self.saveAmount()
        
    def getAmount(self):
<<<<<<< HEAD
<<<<<<< HEAD
        return self.amount
=======
        return self.amount
>>>>>>> awe
=======
        return self.amount
>>>>>>> 347106cda715f1b8704de7a02cdbe674b1d05dac
