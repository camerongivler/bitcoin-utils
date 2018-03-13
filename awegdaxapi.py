#Import the necessary modules
import json
import requests

#Import the necessary classes
from exchangebase import ExchangeBase

#Let's try gdax first
class Gdax(ExchangeBase):
    def request(self, url):
        """Return json data from user specified url extension on gdax"""
        timeout = 5
        base_url = "https://www.gdax.com/trade/"
        response = requests.get(base_url + url,
                               timeout=timeout,
                               verify = True)
        if response.status_code != 200:
            print(f"error: {base_url}{url}")
        return response
        
    def GetLastTradePrice(self, symbol):
        """Return the last trade price of user specified coin"""
        pass
        

    def getName(self):
        return "gdax"
    
g = Gdax()
g.request("BCH-USD")