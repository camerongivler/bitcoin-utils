#!/usr/bin/env python3
import gdax
import json
import os
import time

public_client = gdax.PublicClient()

keys = json.load(open('apiKeys.json'))
auth_client = gdax.AuthenticatedClient(**keys)

# products = public_client.get_product_order_book('BTC-USD')
# asks = products["asks"][0]
# bids = products["bids"][0]

while True:

    wallets = []
    accounts = auth_client.get_accounts()

    for acc in accounts:
        currency = acc['currency']
        ticker = public_client.get_product_ticker(currency + '-USD')
        if ticker.get('message', 'found') != 'found':
            continue
        wallets.append({'currency': acc['currency'],
                        'balance': float(acc['balance']),
                        'value': float(acc['balance']) * float(ticker['price'])})
        time.sleep(0.34)

    os.system('clear')

    for w in wallets:
        print("You have", '{:.4f}'.format(w['balance']), w['currency'], "worth", w['value'])
