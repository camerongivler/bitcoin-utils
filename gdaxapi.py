from exchangebase import ExchangeBase
import gdax

class Gdax(ExchangeBase):
    #GDAX
    g = gdax.PublicClient()

    def getLastTradePrice(self, symbol):
        return float(self.g.get_product_ticker(symbol)['price'])

    def getName(self):
        return "gdax"
