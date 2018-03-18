from wallet import Wallet

class ExchangeBase:
    
    def __init__(self):
        self.wallets = {}
        self.fee = 0
        # Value of all wallets, in arbiter currency (USD)
        self.value = 0
        # Wallet that contains the value
        self.valueWallet = Wallet("null",0)
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
    
    # The value of the exchange, in arbitrar currency
    # NOTE: This value will be 0 until first transaction
    def getValue(self):
        return self.value
    
    # The arbitrar
    def setArbitrar(self, arbitrarName):
        self.arbitrar = self.wallets[arbitrarName]

    #exchange method that takes money from the sellWallet and adds
    #it to the buy wallet taking out the fee and multiplied by the rate
    def transact(self, sellWallet, buyWallet, rate):
        if(sellWallet == self.arbitrar):
            self.value = sellWallet.amount * (1-self.fee)

        buyWallet.amount += sellWallet.amount * (1-self.fee) * rate
        sellWallet.amount = 0
        self.valueWallet = buyWallet

        if(buyWallet == self.arbitrar):
            self.value = buyWallet.amount
