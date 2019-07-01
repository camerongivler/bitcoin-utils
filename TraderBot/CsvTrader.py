import sys
import time
from datetime import datetime, timedelta
import json
import gdax
import csv
from TraderBot.TradingInterface import TradingInterface


class CsvTrader(TradingInterface):
    current_time = datetime.now()
    delta = 86400
    row = 0

    def __init__(self):
        TradingInterface.__init__(self, None, None)
        self.prices = self.read_prices('Coinbase_BTCUSD_1h.csv')

    def read_prices(self, filename):
        prices = []

        with open(filename) as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            for row in csv_reader:
                try:
                    datetime_o = datetime.strptime(row[0], '%Y-%m-%d %I-%p')
                except ValueError as e:
                    print("could not parse date: " + row[0])
                    print(e)
                    continue
                except:
                    print("could not parse date: " + row[0])
                    continue

                prices.insert(0, {})
                prices[0]['time'] = datetime_o
                prices[0]['price'] = float(row[5])
                prices[0]['vol'] = float(row[6])

        return prices

    def get_current_time(self):
        return self.prices[self.row]['time']

    def get_current_price(self):
        return self.prices[self.row]['price']

    def get_current_volume(self):
        return self.prices[self.row]['volume']

    def increment_time(self):
        self.row += 24

    def is_finished(self):
        return self.row >= len(self.prices)


if __name__ == '__main__':
    trader = CsvTrader()

    try:
        while True:
            print(str(trader.get_current_time().strftime("%m/%d/%y %H:%M")) + ' - $' + str(trader.get_current_price()))
            trader.increment_time()
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass
