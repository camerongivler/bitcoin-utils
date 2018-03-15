from exchangebase import ExchangeBase
from wallet import Wallet
import gdax

class Gdax(ExchangeBase):
    g = gdax.PublicClient()
    fee = 0.0025
    
    gdaxWallets = {}
    gdaxWallets["LTC"] = Wallet("gdax", "LTC", 0)
    gdaxWallets["ETH"] = Wallet("gdax", "ETH", 0)
    gdaxWallets["BCH"] = Wallet("gdax", "BCH", 0)
    gdaxWallets["BTC"] = Wallet("gdax", "BTC", 0)
    gdaxWallets["USD"] = Wallet("gdax", "USD", 487.36)
    gdaxWallets["value"] = gdaxWallets["USD"]
    
    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
