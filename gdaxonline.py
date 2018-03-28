from exchangebase import ExchangeBase
from wallet import Wallet
import gdax, json, time

class InsufficientFundsError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Gdax(ExchangeBase):

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC", 0)
        self.wallets["ETH"] = Wallet("ETH", 0)
        self.wallets["BCH"] = Wallet("BCH", 0)
        self.wallets["BTC"] = Wallet("BTC", 0)
        self.wallets["USD"] = Wallet("USD", 500)
        self.valueWallet = self.wallets["USD"]

        args = json.load(open('gdaxKey.json'))
        self.auth_client = gdax.AuthenticatedClient(**args)
        self.public_client = gdax.PublicClient()

        self.fee = 0.0025

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.public_client.get_product_ticker(symbol)
        return float(ticker['price'])

    def buy(self, key):
        buySymbol = key + "-" + self.arbitrar.currency
        amount = str(round(self.arbitrar.amount, 2))
        order = self.auth_client.buy(product_id=buySymbol, type='market', funds=amount)
        if 'message' in order.keys():
            raise InsufficientFundsError(order['message'])
        
        settled = order['settled']
        while not settled:
            order = self.auth_client.get_order(order['id'])
            settled = order['settled']
            time.sleep(0.2)

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
            time.sleep(0.2)

        self.arbitrar.amount = float(order['executed_value'])
        self.valueWallet.amount = 0
        self.valueWallet = self.arbitrar

        # NOTE: This includes the fee!
        rate = float(order['executed_value']) / float(order['filled_size'])
        
        return sellSymbol, rate

    def getName(self):
        return "gdax"
