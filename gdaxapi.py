from exchangebase import ExchangeBase
import gdax

class Gdax(ExchangeBase):
    #GDAX
    g = gdax.PublicClient()

    def getLastTradePrice(self, symbol):
        ticker = {}
        ticker = self.g.get_product_ticker(symbol)
        while not 'price' in ticker.keys():
            sleep(0.34)
            ticker = self.g.get_product_ticker(symbol)
        return float(ticker['price'])

    def getName(self):
        return "gdax"
