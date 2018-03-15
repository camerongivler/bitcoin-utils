from exchangebase import ExchangeBase
import krakenex
from wallet import Wallet
from pykrakenapi import KrakenAPI

krakenWallets = {}    
krakenWallets["LTC"] = Wallet("kraken", "LTC", 2.840026170837398)
krakenWallets["ETH"] = Wallet("kraken", "ETH", 0)
krakenWallets["BCH"] = Wallet("kraken", "BCH", 0)
krakenWallets["BTC"] = Wallet("kraken", "BTC", 0)
krakenWallets["USD"] = Wallet("kraken", "USD", 0)
krakenWallets["value"] = krakenWallets["LTC"]
    
class Kraken(ExchangeBase):
    api = krakenex.API()
    k = KrakenAPI(api)
    fee = 0.0026
    
    def getLastTradePrice(self, symbol):
        mySymbol = symbol.replace("BTC", "XBT").replace("-","")
        krakenTicker = self.k.get_ticker_information(mySymbol)
        # c = last trade
        return float(krakenTicker['c'][0][0])

    def getName(self):
        return "kraken"
