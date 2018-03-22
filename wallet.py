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
        return self.amount
