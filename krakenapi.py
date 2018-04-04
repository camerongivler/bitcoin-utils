from exchangebase import ExchangeBase
import krakenex
from wallet import Wallet
from pykrakenapi import KrakenAPI
    
# Every user of our API has a "call counter" which starts at 0.

# Ledger/trade history calls increase the counter by 2.

# Place/cancel order calls do not affect the counter.

# All other API calls increase the counter by 1.

# The user's counter is reduced every couple of seconds, and if the counter exceeds the user's maximum API access is suspended for 15 minutes. Tier 2 users have a maximum of 15 and their count gets reduced by 1 every 3 seconds. Tier 3 and 4 users have a maximum of 20; the count is reduced by 1 every 2 seconds for tier 3 users, and is reduced by 1 every 1 second for tier 4 users.

# I am tier 2 - 1 call every 3 seconds
class Kraken(ExchangeBase):
    api = krakenex.API()
    k = KrakenAPI(api)

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC", 0)
        self.wallets["ETH"] = Wallet("ETH", 0)
        self.wallets["BCH"] = Wallet("BCH", 0)
        self.wallets["BTC"] = Wallet("BTC", 0)
        self.wallets["USD"] = Wallet("USD", 500)
        self.valueWallet = self.wallets["USD"]

        self.fee = 0.0026
    
    def getLastTradePrice(self, symbol):
        mySymbol = symbol.replace("BTC", "XBT").replace("-","")
        krakenTicker = self.k.get_ticker_information(mySymbol)
        # c = last trade
        return float(krakenTicker['c'][0][0])

    def getName(self):
        return "kraken"
