import requests
import base64
import hmac
import json
import time
from wallet import Wallet
from exchangebase import ExchangeBase
from hashlib import sha384

class Gemini(ExchangeBase):
    
    def __init__(self):
        #set up wallets
        self.wallets = {}
        self.wallets["ETH"] = Wallet("gemini", "ETH", 0)
        self.wallets["BTC"] = Wallet("gemini", "BTC", 0)
        self.wallets["USD"] = Wallet("gemini", "USD", 0)
        self.fee = 0.0025
        self.value = self.wallets["BTC"]
    
    def request(url):
        timeout = 5
        base_url = "https://api.gemini.com/v1"
        response = requests.get(base_url + "/" + url,
                                timeout=timeout,
                                verify=True)
        if response.status_code != 200:
            print("error:",base_url + "/" + url)
        return json.loads(response.content)

    def getLastTradePrice(self, symbol):
        mySymbol = symbol.replace("-","").lower()
        return float(Gemini.request("pubticker/" + mySymbol)["last"])

    def getName(self):
        return "gemini"

class Private:
    def test():
        timeout = 5

        key = json.load(open('geminiKey.json'))

        payload_nonce = int(round(time.time() * 1000))

        payload =  {"request": "/v1/mytrades", "nonce": payload_nonce}
        encoded_payload = json.dumps(payload).encode()
        b64 = base64.b64encode(encoded_payload)
        signature = hmac.new(key["gemini_api_secret"].encode(), b64, sha384).hexdigest()

        request_headers = {
            'Content-Type': "text/plain",
            'Content-Length': "0",
            'X-GEMINI-APIKEY': key["gemini_api_key"],
            'X-GEMINI-PAYLOAD': b64,
            'X-GEMINI-SIGNATURE': signature,
            'Cache-Control': "no-cache"
            }

        response = requests.post(key["url"], data=None, headers=request_headers, timeout=timeout, verify=True)
        print(response)
        assert response.status_code == 200
        print(response.content)
