import gdax
import json
import time

from exchangebase import ExchangeBase
from wallet import Wallet


class InsufficientFundsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Gdax(ExchangeBase):

    def __init__(self):
        super().__init__()
        args = json.load(open('gdaxKey.json'))
        self.auth_client = gdax.AuthenticatedClient(**args)
        self.public_client = gdax.PublicClient()

        accounts = self.auth_client.get_accounts()
        for account in accounts:
            currency = account['currency']
            balance = float(account['available'])
            self.wallets[currency] = Wallet(currency, balance)
            print(currency, balance)
            if balance > self.valueWallet.amount:
                self.valueWallet = self.wallets[currency]

        self.fee = 0.0025

    def get_last_trade_price(self, symbol):
        ticker = {}
        ticker = self.public_client.get_product_ticker(symbol)
        return float(ticker['price'])

    def buy(self, key):
        buySymbol = key + "-" + self.arbitrar.currency
        amount = str(self.arbitrar.amount // 0.01 / 100)
        order = self.auth_client.buy(product_id=buySymbol, type='market', funds=amount)
        if 'message' in order.keys():
            raise InsufficientFundsError(order['message'])

        settled = order['settled']
        while not settled:
            order = self.auth_client.get_order(order['id'])
            settled = order['settled']
            time.sleep(0.12)

        self.wallets[key].amount = float(order['filled_size'])
        self.arbitrar.amount = 0
        self.valueWallet = self.wallets[key]

        # NOTE: This includes the fee!
        rate = float(order['executed_value']) / float(order['filled_size'])

        return buySymbol, rate

    def sell(self):
        sellSymbol = self.valueWallet.currency + "-" + self.arbitrar.currency
        amount = str(self.valueWallet.amount)
        order = self.auth_client.sell(product_id=sellSymbol, type='market', size=amount)
        if 'message' in order.keys():
            raise InsufficientFundsError(order['message'])

        settled = order['settled']
        while not settled:
            order = self.auth_client.get_order(order['id'])
            settled = order['settled']
            time.sleep(0.12)

        self.arbitrar.amount = float(order['executed_value'])
        self.valueWallet.amount = 0
        self.valueWallet = self.arbitrar

        # NOTE: This includes the fee!
        rate = float(order['executed_value']) / float(order['filled_size'])

        return sellSymbol, rate

    def get_name(self):
        return "gdax"
