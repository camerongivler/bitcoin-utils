from exchangebase import ExchangeBase
from wallet import Wallet
import gdax

class Gdax(ExchangeBase):
    g = gdax.PublicClient()

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("gdax", "LTC", 0)
        self.wallets["ETH"] = Wallet("gdax", "ETH", 0)
        self.wallets["BCH"] = Wallet("gdax", "BCH", 0)
        self.wallets["BTC"] = Wallet("gdax", "BTC", 0.063267)
        self.wallets["USD"] = Wallet("gdax", "USD", 0)

        self.fee = 0.0025

        self.value = self.wallets["BTC"]

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
