import krakenex
from pykrakenapi import KrakenAPI

from exchangebase import ExchangeBase
from wallet import Wallet

# Every user of our API has a "call counter" which starts at 0.
# Ledger/trade history calls increase the counter by 2.
# Place/cancel order calls do not affect the counter.
# All other API calls increase the counter by 1.
# The user's counter is reduced every couple of seconds, and if the counter exceeds the user's maximum API access
# is suspended for 15 minutes. Tier 2 users have a maximum of 15 and their count gets reduced by 1 every 3 seconds.
# Tier 3 and 4 users have a maximum of 20; the count is reduced by 1 every 2 seconds for tier 3 users, and is reduced
# by 1 every 1 second for tier 4 users.

# I am tier 2 - 1 call every 3 seconds

symbols = {
    'BTC-USD': "XXBTZUSD",
    'ETH-USD': "XETHZUSD",
    'LTC-USD': "XLTCZUSD",
    'BCH-USD': "BCHUSD"
}


class Kraken(ExchangeBase):
    api = krakenex.API()
    k = KrakenAPI(api)

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC", 0)
        self.wallets["ETH"] = Wallet("ETH", 0)
        self.wallets["BCH"] = Wallet("BCH", 0)
        self.wallets["BTC"] = Wallet("BTC", 0)
        self.wallets["USD"] = Wallet("USD", 500)
        self.valueWallet = self.wallets["USD"]

        # Maker fee
        # self.fee = 0.0016
        # Taker fee
        self.fee = 0.0026

    def get_last_trade_price(self, symbol):
        my_symbol = symbol.replace("BTC", "XBT").replace("-", "")
        kraken_ticker = self.k.get_ticker_information(my_symbol)
        # c = last trade
        return float(kraken_ticker['c'][0][0])

    def get_buy_price_for(self, key):
        # Maker order
        # return self.getHighestBidPriceFor(key) * (1 - self.fee)) * (1 + self.fee)
        # Taker order
        return self.get_market_buy_price_for(key, self.arbitrar.amount * (1 - self.fee)) * (1 + self.fee)

    def get_sell_price(self):
        key = self.valueWallet.currency
        # Maker order
        # return self.getLowestAskPriceFor(key) * (1 - self.fee)) * (1 - self.fee)
        # Taker order
        return self.get_market_sell_price_for(key, self.wallets[key].amount * (1 - self.fee)) * (1 - self.fee)

    def get_highest_bid_price_for(self, key):
        symbol = key + "-" + self.arbitrar.currency
        pair = symbols[symbol]
        book = self.k.get_order_book(pair)[1].astype('float').sort_values(by=['price'], ascending=False)
        return float(book.iloc[0]['price'])

    def get_lowest_ask_price_for(self, key):
        symbol = key + "-" + self.arbitrar.currency
        pair = symbols[symbol]
        book = self.k.get_order_book(pair)[0].astype('float').sort_values(by=['price'])
        return float(book.iloc[0]['price'])

    def get_market_buy_price_for(self, key, amount):
        symbol = key + "-" + self.arbitrar.currency
        pair = symbols[symbol]
        book = self.k.get_order_book(pair)[0].astype('float').sort_values(by=['price'])
        full_amount = amount
        price = i = 0
        while amount > 0:
            volume = float(book.iloc[i]['volume'])
            this_price = float(book.iloc[i]['price'])
            this_amount = amount if amount < volume * this_price else volume * this_price
            price += this_price * this_amount / full_amount
            amount -= this_amount
            i += 1
        return price

    def get_market_sell_price_for(self, key, amount):
        symbol = key + "-" + self.arbitrar.currency
        pair = symbols[symbol]
        book = self.k.get_order_book(pair)[1].astype('float').sort_values(by=['price'], ascending=False)
        full_amount = amount
        price = i = 0
        while amount > 0:
            volume = float(book.iloc[i]['volume'])
            this_price = float(book.iloc[i]['price'])
            this_amount = amount if amount < volume else volume
            price += this_price * this_amount / full_amount
            amount -= this_amount
            i += 1
        return price

    def get_name(self):
        return "kraken"
