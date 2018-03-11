#!/usr/bin/env python3

class Wallet:
    
    def __init__(self, exchange, currency, amount):
        self.exchange = exchange
        self.currency = currency
        self.amount = amount


class Exchange:

    # Takes [amount] out of [sellWallet], mutliplies it by [rate]
    # and deposits it into [buyWallet]
    def exchange(buyWallet, sellWallet, amount, rate):
        if sellWallet.amount < amount: return False
        sellWallet = sellWallet - amount
        buyWallet += amount * rate
        return True
