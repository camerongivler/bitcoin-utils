from exchangebase import ExchangeBase
import krakenex
from wallet import Wallet
from pykrakenapi import KrakenAPI
    
class Kraken(ExchangeBase):
    api = krakenex.API()
    k = KrakenAPI(api)

    def __init__(self):
        super().__init__()
        self.wallets["LTC"] = Wallet("LTC")
        self.wallets["ETH"] = Wallet("ETH")
        self.wallets["BCH"] = Wallet("BCH")
        self.wallets["BTC"] = Wallet("BTC")
        self.wallets["USD"] = Wallet("USD")
        self.valueWallet = self.wallets["USD"]

        self.fee = 0.0026
    
    def getLastTradePrice(self, symbol):
        mySymbol = symbol.replace("BTC", "XBT").replace("-","")
        krakenTicker = self.k.get_ticker_information(mySymbol)
        # c = last trade
        return float(krakenTicker['c'][0][0])

    def getName(self):
        return "kraken"
