from exchangebase import ExchangeBase
from wallet import Wallet
import gdax

class Gdax(ExchangeBase):
    g = gdax.PublicClient()

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC")
        self.wallets["ETH"] = Wallet("ETH")
        self.wallets["BCH"] = Wallet("BCH")
        self.wallets["BTC"] = Wallet("BTC")
        self.wallets["USD"] = Wallet("USD")
        self.valueWallet = self.wallets["BTC"]

        self.fee = 0.0025

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
