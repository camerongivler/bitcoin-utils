import time
from datetime import datetime, timedelta
import json
import gdax
from TraderBot.TradingInterface import TradingInterface


class HistoricTrader(TradingInterface):
    current_time = datetime.now()
    delta = 86400

    def __init__(self, public, auth):
        TradingInterface.__init__(self, public, auth)

    def get_current_time(self):
        return self.current_time.strftime("%m/%d/%y %H:%M")

    def set_current_time(self, time):
        self.current_time = time

    def get_current_price(self):
        curr_time = self.current_time

        ticker = self.public_client.get_product_historic_rates('BTC-USD', curr_time.isoformat(),
                                                               curr_time + timedelta(seconds=self.delta), self.delta)

        if 'message' in ticker:
            print(ticker['message'])
            return None

        return float(ticker[0][3]) if len(ticker) > 0 else None

    def increment_time(self):
        self.current_time += timedelta(seconds=self.delta)
        time.sleep(0.5)


if __name__ == '__main__':
    public_client = gdax.PublicClient()

    keys = json.load(open('gdaxKey.json'))

    # Sandbox API
    auth_client = gdax.AuthenticatedClient(**keys)

    trader = HistoricTrader(public_client, auth_client)

    current_time = datetime(2019, 1, 1, 12, 30)

    trader.set_current_time(current_time)
    try:
        while True:
            print(str(trader.get_current_time().strftime("%m/%d/%y %H:%M")) + ' - $' + str(trader.get_current_price()))
            trader.increment_time()
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass
