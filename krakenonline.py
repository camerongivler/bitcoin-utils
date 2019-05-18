import json
import krakenex
import time
from abc import ABC

from pykrakenapi import KrakenAPI

from exchangebase import ExchangeBase


class InsufficientFundsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Kraken(ExchangeBase, ABC):

    def __init__(self):
        super().__init__()
        args = json.load(open('krakenKey.json'))
        api = krakenex.API(**args)
        self.kraken = KrakenAPI(api)

        accounts = self.kraken.get_account_balance()
        print(accounts)
        return
        # for account in accounts:
        #     currency = account['currency']
        #     balance = float(account['available'])
        #     self.wallets[currency] = Wallet(currency, balance)
        #     print(currency, balance)
        #     if balance > self.valueWallet.amount:
        #         self.valueWallet = self.wallets[currency]

        # self.fee = 0.0025

    def get_last_trade_price(self, symbol):
        ticker = self.kraken.get_product_ticker(symbol)
        return float(ticker['price'])

    def buy(self, key):
        buy_symbol = (key + "-" + self.arbitrar.currency).replace("BTC", "XBT").replace("-", "")
        amount = str(self.arbitrar.amount // 0.01 / 100)
        order = self.kraken.buy(product_id=buy_symbol, type='market', funds=amount)
        if 'message' in order.keys():
            raise InsufficientFundsError(order['message'])

        settled = order['settled']
        while not settled:
            order = self.kraken.get_order(order['id'])
            settled = order['settled']
            time.sleep(0.12)

        self.wallets[key].amount = float(order['filled_size'])
        self.arbitrar.amount = 0
        self.valueWallet = self.wallets[key]

        # NOTE: This includes the fee!
        rate = float(order['executed_value']) / float(order['filled_size'])

        return buy_symbol, rate

    def sell(self):
        sell_symbol = (self.valueWallet.currency + "-" + self.arbitrar.currency).replace("BTC", "XBT").replace("-", "")
        amount = str(self.valueWallet.amount)
        order = self.kraken.sell(product_id=sell_symbol, type='market', size=amount)
        if 'message' in order.keys():
            raise InsufficientFundsError(order['message'])

        settled = order['settled']
        while not settled:
            order = self.kraken.get_order(order['id'])
            settled = order['settled']
            time.sleep(0.12)

        self.arbitrar.amount = float(order['executed_value'])
        self.valueWallet.amount = 0
        self.valueWallet = self.arbitrar

        # NOTE: This includes the fee!
        rate = float(order['executed_value']) / float(order['filled_size'])

        return sell_symbol, rate

    def get_name(self):
        return "kraken"


k = Kraken()
