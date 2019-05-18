#!/usr/bin/env python3


# The purpose of this class is to provide a common interface for buying and selling bitcoin,
# either now, or at any time in the past.  The rate of time is irrelevant to this interface
# which will allow for rapid modeling of algorithmic performance on past data

class TradingInterface:

    def __init__(self, public_client, auth_client):
        self.public_client = public_client
        self.auth_client = auth_client

    def get_current_time(self):
        pass

    def set_current_time(self, datetime):
        pass

    def get_current_price(self):
        pass

    def get_bitcoin_balance(self):
        pass

    def get_usd_balance(self):
        pass

    def buy(self, amount):
        pass

    def sell(self, amount):
        pass


class RealTimeTrader(TradingInterface):

    def __init__(self, public_client, auth_client):
        TradingInterface.__init__(self, public_client, auth_client)

    def get_current_time(self):
        return self.public_client.getTime()["epoch"]

    def get_current_price(self):
        ticker = self.public_client.get_product_ticker('BTC-USD')
        if ticker.get('message', 'found') != 'found':
            return None
        return float(ticker['price'])

    def get_bitcoin_balance(self):
        acc = self.auth_client.get_accounts()
        return float(acc['BTC']['balance'])

    def get_usd_balance(self):
        acc = self.auth_client.get_accounts()
        return float(acc['USD']['balance'])

    def buy(self, amount, price):
        self.auth_client.buy(price=price,
                             size=amount,
                             product_id='BTC-USD')

    def sell(self, amount, price):
        self.auth_client.sell(price=price,
                              size=amount,
                              product_id='BTC-USD')
