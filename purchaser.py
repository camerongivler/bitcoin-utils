#!/usr/bin/env python3
import gdax
import json
import sys

from TraderBot import TradingInterface

public_client = gdax.PublicClient()

keys = json.load(open('apiKeys.json'))

# Sandbox API
auth_client = gdax.AuthenticatedClient(**keys)

if len(sys.argv) != 3:
    print("Sorry, can't parse args")
    exit()

trade = TradingInterface.RealTimeTrader(public_client, auth_client)

trade.buy(sys.argv[2], str(sys.argv[1]))
