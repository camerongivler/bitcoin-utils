from exchangebase import ExchangeBase
from wallet import Wallet
import gdax

class Gdax(ExchangeBase):
    
    def __init__(self):
        #set up wallets
        self.wallets = {}
        self.wallets["LTC"] = Wallet("gdax", "LTC", 0)
        self.wallets["ETH"] = Wallet("gdax", "ETH", 0)
        self.wallets["BCH"] = Wallet("gdax", "BCH", 0)
        self.wallets["BTC"] = Wallet("gdax", "BTC", 0)
        self.wallets["USD"] = Wallet("gdax", "USD", 500)
        self.fee = 0.0025
        self.value = self.wallets["USD"]
 
    g = gdax.PublicClient()

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
