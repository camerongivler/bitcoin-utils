import gdax

from exchangebase import ExchangeBase
from wallet import Wallet


# We throttle public endpoints by IP: 3 requests per second, up to 6 requests per second in bursts.
class Gdax(ExchangeBase):
    g = gdax.PublicClient()

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC", 0)
        self.wallets["ETH"] = Wallet("ETH", 0)
        self.wallets["BCH"] = Wallet("BCH", 0.2985074627)
        self.wallets["BTC"] = Wallet("BTC", 0)
        self.wallets["USD"] = Wallet("USD", 0)
        self.valueWallet = self.wallets["BCH"]

        self.fee = 0.0025
        # self.fee = 0

    def get_last_trade_price(self, symbol):
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def get_buy_price_for(self, key):
        return self.get_market_buy_price_for(key, self.arbitrar.amount * (1 - self.fee)) * (1 + self.fee)
        # return self.getHighestBidPriceFor(key) * (1 - self.fee)) * (1 + self.fee)

    def get_sell_price(self):
        key = self.valueWallet.currency
        return self.get_market_sell_price_for(key, self.wallets[key].amount * (1 - self.fee)) * (1 - self.fee)
        # return self.getLowestAskPriceFor(key) * (1 - self.fee)) * (1 - self.fee)

    def get_highest_bid_price_for(self, key):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        return float(book['bids'][0][0])

    def get_lowest_ask_price_for(self, key):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        return float(book['asks'][0][0])

    def get_market_buy_price_for(self, key, amount):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        full_amount = amount
        price = i = 0
        while amount > 0:
            this_price = float(book['asks'][i][0])
            volume = float(book['asks'][i][1])
            this_amount = amount if amount < volume * this_price else volume * this_price
            price += this_price * this_amount / full_amount
            amount -= this_amount
            i += 1
        return price

    def get_market_sell_price_for(self, key, amount):
        symbol = key + "-" + self.arbitrar.currency
        book = self.g.get_product_order_book(symbol, level=2)
        full_amount = amount
        price = i = 0
        while amount > 0:
            this_price = float(book['bids'][i][0])
            volume = float(book['bids'][i][1])
            this_amount = amount if amount < volume else volume
            price += this_price * this_amount / full_amount
            amount -= this_amount
            i += 1
        return price

    def get_name(self):
        return "gdax"
