from exchangebase import ExchangeBase
import krakenex
from wallet import Wallet
from pykrakenapi import KrakenAPI
    
class Kraken(ExchangeBase):
    def __init__(self):
      #set up the wallets
        self.wallets = {}
        self.wallets["LTC"] = Wallet("kraken", "LTC", 2.840026170837398)
        self.wallets["ETH"] = Wallet("kraken", "ETH", 0)
        self.wallets["BCH"] = Wallet("kraken", "BCH", 0)
        self.wallets["BTC"] = Wallet("kraken", "BTC", 0)
        self.wallets["USD"] = Wallet("kraken", "USD", 0)
        self.fee = 0.0026
        self.value = self.wallets["LTC"]
        
    api = krakenex.API()
    k = KrakenAPI(api)
    
    def getLastTradePrice(self, symbol):
        mySymbol = symbol.replace("BTC", "XBT").replace("-","")
        krakenTicker = self.k.get_ticker_information(mySymbol)
        # c = last trade
        return float(krakenTicker['c'][0][0])

    def getName(self):
        return "kraken"
