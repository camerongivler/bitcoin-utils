#!/usr/bin/env python3
import gdax

# The purpose of this class is to provide a common interface for buying and selling bitcoin,
# either now, or at any time in the past.  The rate of time is irrelevant to this interface
# which will allow for rapid modeling of algorithmic performance on past data

class TradingInterface:

    def __init__(self, public_client, auth_client):
        self.public_client = public_client
        self.auth_client = auth_client


    def getCurrentTime(self):
        pass

    def getCurrentBitcoinPrice(self):
        pass

    def getBitcoinBalance(self):
        pass

    def getUsdBalance(self):
        pass

    def buy(self, numBitcoin):
        pass

    def sell(self, numBitcoin):
        pass


class RealTimeTrader(TradingInterface):

    def __init__(self, public_client, auth_client):
        TradingInterface.__init__(self, public_client, auth_client)


    def getCurrentTime(self):
        return self.public_client.getTime()["epoch"]

    def getCurrentBitcoinPrice(self):
        ticker = self.public_client.get_product_ticker(currency+'-USD')
        if ticker.get('message', 'found') != 'found':
            return None
        return float(ticker['price'])

    def getBitcoinBalance(self):
        accounts = self.auth_client.get_accounts()
        return float(acc['BTC']['balance'])

    def getUsdBalance(self):
        accounts = self.auth_client.get_accounts()
        return float(acc['USD']['balance'])

    def buy(self, numBitcoin, price):
        self.auth_client.buy(price=price,
               size=numBitcoin,
               product_id='BTC-USD')

    def sell(self, numBitcoin, price):
        self.auth_client.sell(price=price,
               size=numBitcoin,
               product_id='BTC-USD')
