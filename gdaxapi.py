from exchangebase import ExchangeBase
from wallet import Wallet
import gdax

# We throttle public endpoints by IP: 3 requests per second, up to 6 requests per second in bursts.
class Gdax(ExchangeBase):
    g = gdax.PublicClient()

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC", 0)
        self.wallets["ETH"] = Wallet("ETH", 0)
        self.wallets["BCH"] = Wallet("BCH", 0)
        self.wallets["BTC"] = Wallet("BTC", 0.068213)
        self.wallets["USD"] = Wallet("USD", 0)
        self.valueWallet = self.wallets["BTC"]

        self.fee = 0.0025

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
