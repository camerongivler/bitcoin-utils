

class TradingAlgorithm:

    @staticmethod
    def how_much_btc_to_buy(current, previous, btc, usd):
        if current is None or previous is None:
            return 0
        if current < previous:
            return (usd * 0.1) / current
        return 0

    @staticmethod
    def how_much_btc_to_sell(current, previous, btc, usd):
        if current is None or previous is None:
            return 0
        if current > previous:
            return btc * 0.1
        return 0

