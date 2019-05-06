import base64
import hmac
import json
import time
from hashlib import sha384

import requests

from exchangebase import ExchangeBase
from wallet import Wallet


# For public API entry points, we limit requests to 120 requests per minute,
#   and recommend that you do not exceed 1 request per second.
# For private API entry points, we limit requests to 600 requests per minute,
#   and recommend that you not exceed 5 requests per second.
class Gemini(ExchangeBase):

    def __init__(self):
        # set up wallets
        self.wallets = {}
        self.wallets["ETH"] = Wallet("ETH", 0)
        self.wallets["BTC"] = Wallet("BTC", 0)
        self.wallets["USD"] = Wallet("USD", 500)
        self.valueWallet = self.wallets["USD"]
        self.fee = 0.0025

    def request(url):
        timeout = 5
        base_url = "https://api.gemini.com/v1"
        response = requests.get(base_url + "/" + url,
                                timeout=timeout,
                                verify=True)
        if response.status_code != 200:
            print("error:", base_url + "/" + url)
        return json.loads(response.content)

    def get_last_trade_price(self, symbol):
        mySymbol = symbol.replace("-", "").lower()
        return float(Gemini.request("pubticker/" + mySymbol)["last"])

    def get_name(self):
        return "gemini"


class Private:
    def test(self):
        timeout = 5

        key = json.load(open('geminiKey.json'))

        payload_nonce = int(round(time.time() * 1000))

        payload = {"request": "/v1/mytrades", "nonce": payload_nonce}
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


p = Private()
p.test()
