from exchangebase import ExchangeBase
import gdax

class Gdax(ExchangeBase):
    g = gdax.PublicClient()

    def getLastTradePrice(self, symbol):
        ticker = {}
        try:
            ticker = self.g.get_product_ticker(symbol)
            while not 'price' in ticker.keys():
                sleep(0.34)
                ticker = self.g.get_product_ticker(symbol)
        except json.decoder.JSONDecodeError:
            sleep(1)
            return self.getLastTradePrice(symbol)

        return float(ticker['price'])

    def getName(self):
        return "gdax"
