from exchangebase import ExchangeBase
import gdax

class Gdax(ExchangeBase):
    #GDAX
    g = gdax.PublicClient()

    def getLastTradePrice(self, symbol):
        ticker = {}
        while not 'price' in ticker.keys():
            ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
