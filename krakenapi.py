from exchangebase import ExchangeBase
import krakenex
from pykrakenapi import KrakenAPI

class Kraken(ExchangeBase):
    api = krakenex.API()
    k = KrakenAPI(api)

    def getLastTradePrice(self, symbol):
        try:
            mySymbol = symbol.replace("BTC", "XBT").replace("-","")
            krakenTicker = self.k.get_ticker_information(mySymbol)
            # c = last trade
            return float(krakenTicker['c'][0][0])
        except requests.exceptions.ConnectionError:
            sleep(3)
            return self.getLastTradePrice(symbol)

    def getName(self):
        return "kraken"
