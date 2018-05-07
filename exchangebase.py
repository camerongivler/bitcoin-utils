from wallet import Wallet
import time, os

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

    def getBuyPriceFor(self, key):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    def getSellPrice(self):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    def getHighestBidPriceFor(self, key):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    def getLowestAskPriceFor(self, key):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    def getMarketBuyPriceFor(self, key, amount):
        raise NotImplementedError( "Need to implement this in exchange subclass" )

    def getMarketSellPriceFor(self, key, amount):
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

    def buy(self, key):
        buySymbol = key + "-" + self.arbitrar.currency
        rate = self.getBuyPriceFor(key)
        #rate = self.buy_wait(buySymbol, rate);
        self.transact(self.arbitrar, self.wallets[key], 1/rate)
        return buySymbol, rate

    def sell(self):
        key = self.valueWallet.currency
        sellSymbol = key + "-" + self.arbitrar.currency
        rate = self.getSellPrice()
        #rate = self.sell_wait(sellSymbol, rate);
        self.transact(self.valueWallet, self.arbitrar, rate)
        return sellSymbol, rate

    def buy_wait(self, buySymbol, rate):
        last = -1
        while True:
            time.sleep(2)
            try:
                current = self.getLastTradePrice(buySymbol)
                os.system('clear')
                print("Waiting for",buySymbol,"ticker on",self.getName(),"to be less than","%.4f" % rate)
                print("Ticker:",current)
                if current < rate:
                    break
                if last != -1 and current > last and current / rate > 1.002:
                    rate = current / 1.002
                last = current
            except Exception as e:
                pass
        self.transact(self.arbitrar, self.wallets[key], 1/rate)
        return rate

    def sell_wait(self, sellSymbol, rate):
        last = -1
        while True:
            time.sleep(2)
            try:
                os.system('clear')
                current = self.getLastTradePrice(sellSymbol)
                print("Waiting for",sellSymbol,"ticker on",self.getName(),"to be greater than","%.4f" % rate)
                print("Ticker:",current)
                if current > rate:
                    break
                if last != -1 and current < last and rate / current > 1.002:
                    rate = current * 1.002
                last = current
            except Exception as e:
                pass
        return rate

    #exchange method that takes money from the sellWallet and adds
    #it to the buy wallet taking out the fee and multiplied by the rate
    def transact(self, sellWallet, buyWallet, rate):
        if(sellWallet == self.arbitrar):
            self.value = sellWallet.amount * (1 - self.fee)

        buyWallet.amount += sellWallet.amount * rate
        sellWallet.amount = 0
        self.valueWallet = buyWallet

        if(buyWallet == self.arbitrar):
            self.value = buyWallet.amount
