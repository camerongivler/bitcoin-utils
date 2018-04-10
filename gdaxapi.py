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
        self.wallets["BCH"] = Wallet("BCH", 0.785447)
        self.wallets["BTC"] = Wallet("BTC", 0)
        self.wallets["USD"] = Wallet("USD", 0)
        self.valueWallet = self.wallets["BCH"]

        self.fee = 0.0025

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getBuyPriceFor(self, key):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        fullAmount = amount = self.arbitrar.amount
        price = i = 0
        while amount > 0:
            thisPrice = float(book['asks'][i][0])
            volume = float(book['asks'][i][1])
            thisAmount = amount if amount < volume * thisPrice else volume * thisPrice
            price += thisPrice * thisAmount / fullAmount
            amount -= thisAmount
            i += 1
        return price

    def getSellPrice(self):
        key = self.valueWallet.currency
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        fullAmount = amount = self.wallets[key].amount
        price = i = 0
        while amount > 0:
            thisPrice = float(book['bids'][i][0])
            volume = float(book['bids'][i][1])
            thisAmount = amount if amount < volume else volume
            price += thisPrice * thisAmount / fullAmount
            amount -= thisAmount
            i += 1
        return price

    def getHighestBidPriceFor(self, key):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        return float(book['bids'][0][0])

    def getLowestAskPriceFor(self, key):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        return float(book['asks'][0][0])

    def getName(self):
        return "gdax"
