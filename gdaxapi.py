from exchangebase import ExchangeBase
import gdax

class Gdax(ExchangeBase):
    g = gdax.PublicClient()
    fee = 0.0025
    
    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
