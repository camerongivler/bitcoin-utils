#!/usr/bin/env python3

class Wallet:
    
    def __init__(self, exchange, currency, amount):
        self.exchange = exchange
        self.currency = currency
        self.amount = amount


class Exchange:

    # Takes [amount] out of [sellWallet], mutliplies it by [rate]
    # and deposits it into [buyWallet], fee is decimal percent
    def exchange(sellWallet, buyWallet, amount, rate, fee=0.0026):
        if sellWallet.amount < amount: return False
        sellWallet.amount -= amount
        buyWallet.amount += amount * (1-fee) * rate
        return True
