from wallet import Wallet

class ExchangeBase:
    
    def __init__(self):
        self.wallets = {}
        self.fee = 0
        self.value = Wallet("null","null",0)
        self.arbitrar = Wallet("null","null",0)
    
    # The symbols will be taken in GDAX form (BTC-USD) and converted appropriately
    def getLastTradePrice(self, symbol):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    # The name of the exchange
    def getName(self):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    # The name of the exchange, in percent
    def getFee(self):
        return self.fee*100
    
    # The arbitrar
    def setArbitrar(self, arbitrarName):
        self.arbitrar = self.wallets[arbitrarName]

    #exchange method that takes money from the sellWallet and adds
    #it to the buy wallet taking out the fee and multiplied by the rate
    def transact(self, sellWallet, buyWallet, amount, rate):
        if sellWallet.amount < amount: return False
        sellWallet.amount -= amount
        buyWallet.amount += amount * (1-self.fee) * rate
        self.value = buyWallet
        return True
