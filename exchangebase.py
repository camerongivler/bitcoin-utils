from wallet import Wallet

class ExchangeBase:
    
    def __init__(self):
        self.wallets = {}
        self.fee = 0
        self.value = Wallet("null",0)
        self.arbitrar = Wallet("null",0)
    
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
    def transact(self, sellWallet, buyWallet, rate):
        if(sellWallet == self.arbitrar):
            self.value = sellWallet.getAmount() * (1-self.fee)

        buyWallet.setAmount(buyWallet.getAmount() + sellWallet.getAmount() * (1-self.fee) * rate)
        sellWallet.setAmount(0)
        self.valueWallet = buyWallet

        if(buyWallet == self.arbitrar):
            self.value = buyWallet.getAmount()
