import os
import time

from wallet import Wallet


class ExchangeBase:

    def __init__(self):
        self.wallets = {}
        self.fee = 0
        # Value of all wallets, in arbiter currency (USD)
        self.value = 0
        # Wallet that contains the value
        self.valueWallet = Wallet("null", 0)
        self.arbitrar = Wallet("null", 0)

    # The symbols will be taken in GDAX form (BTC-USD) and converted appropriately
    def get_last_trade_price(self, symbol):
        raise NotImplementedError("Need to implement this in exchange subclass")

    def get_buy_price_for(self, key):
        raise NotImplementedError("Need to implement this in exchange subclass")

    def get_sell_price(self):
        raise NotImplementedError("Need to implement this in exchange subclass")

    def get_highest_bid_price_for(self, key):
        raise NotImplementedError("Need to implement this in exchange subclass")

    def get_lowest_ask_price_for(self, key):
        raise NotImplementedError("Need to implement this in exchange subclass")

    def get_market_buy_price_for(self, key, amount):
        raise NotImplementedError("Need to implement this in exchange subclass")

    def get_market_sell_price_for(self, key, amount):
        raise NotImplementedError("Need to implement this in exchange subclass")

    # The name of the exchange
    def get_name(self):
        raise NotImplementedError("Need to implement this in exchange subclass")

    # The name of the exchange, in percent
    def get_fee(self):
        return self.fee * 100

    # The value of the exchange, in arbitrar currency
    # NOTE: This value will be 0 until first transaction
    def get_value(self):
        return self.value

    # The arbitrar
    def set_arbitrar(self, arbitrar_name):
        self.arbitrar = self.wallets[arbitrar_name]

    def buy(self, key):
        buy_symbol = key + "-" + self.arbitrar.currency
        rate = self.get_buy_price_for(key)
        # rate = self.buy_wait(buy_symbol, rate);
        self.transact(self.arbitrar, self.wallets[key], 1 / rate)
        return buy_symbol, rate

    def sell(self):
        key = self.valueWallet.currency
        sell_symbol = key + "-" + self.arbitrar.currency
        rate = self.get_sell_price()
        # rate = self.sell_wait(sell_symbol, rate);
        self.transact(self.valueWallet, self.arbitrar, rate)
        return sell_symbol, rate

    def buy_wait(self, buy_symbol, rate):
        last = -1
        while True:
            time.sleep(2)
            try:
                current = self.get_last_trade_price(buy_symbol)
                os.system('clear')
                print("Waiting for", buy_symbol, "ticker on", self.get_name(), "to be less than", "%.4f" % rate)
                print("Ticker:", current)
                if current < rate:
                    break
                if last != -1 and current > last and current / rate > 1.002:
                    rate = current / 1.002
                last = current
            except Exception:
                pass
        self.transact(self.arbitrar, self.wallets[key], 1 / rate)
        return rate

    def sell_wait(self, sell_symbol, rate):
        last = -1
        while True:
            time.sleep(2)
            try:
                os.system('clear')
                current = self.get_last_trade_price(sell_symbol)
                print("Waiting for", sell_symbol, "ticker on", self.get_name(), "to be greater than", "%.4f" % rate)
                print("Ticker:", current)
                if current > rate:
                    break
                if last != -1 and current < last and rate / current > 1.002:
                    rate = current * 1.002
                last = current
            except Exception:
                pass
        return rate

    # exchange method that takes money from the sellWallet and adds
    # it to the buy wallet taking out the fee and multiplied by the rate
    def transact(self, sell_wallet, buy_wallet, rate):
        if sell_wallet == self.arbitrar:
            self.value = sell_wallet.amount * (1 - self.fee)

        buy_wallet.amount += sell_wallet.amount * rate
        sell_wallet.amount = 0
        self.valueWallet = buy_wallet

        if buy_wallet == self.arbitrar:
            self.value = buy_wallet.amount
