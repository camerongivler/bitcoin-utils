#Import the necessary modules
import json
import requests

#Import the necessary classes
from exchangebase import ExchangeBase

#Kraken url does not change based on the coin
class Kraken(ExchangeBase):
    def request(self):
        """Return json data from kraken
        Important note: kraken URL does not change based on
        what coin is being displayed, no need for user-defined extension(?)"""
        fee = 0.0026
        timeout = 5
        base_url = "http://api.kraken.com/0/public/ticker"
        response = requests.get(base_url,
                               timeout=timeout,
                               verify = True)
        if response.status_code != 200:
            print(f"error: {base_url}")
        return response
    
    def GetLastTradePrice(self, symbol):
        """Return the last trade price of user specified coin"""
        pass
        

    def getName(self):
        return "kraken"
    
k = Kraken()
k.request()