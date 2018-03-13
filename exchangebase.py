class ExchangeBase:

    # The symbols will be taken in GDAX form (BTC-USD) and converted appropriately
    def getLastTradePrice(self, symbol):
        pass

    # The name of the exchange
    def getName(self):
        pass

    def exchange(sellWallet, buyWallet, amount, rate, fee):
        if sellWallet.amount < amount: return False
        sellWallet.amount -= amount
        buyWallet.amount += amount * (1-fee) * rate
        return True