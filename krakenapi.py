from exchangebase import ExchangeBase
import krakenex
from pykrakenapi import KrakenAPI

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
