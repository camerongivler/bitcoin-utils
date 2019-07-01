

class TradingAlgorithm:

    @staticmethod
    def how_much_btc_to_buy(current, previous, btc, usd):
        if current is None or previous is None:
            return 0

        buy = 0
        if current < previous * 0.4:
            return (usd * (1 - current / previous) * 2) / current

        if buy > usd / current * 0.5:
            buy = usd / current * 0.5

        return buy

    @staticmethod
    def how_much_btc_to_sell(current, previous, btc, usd):
        if current is None or previous is None:
            return 0

        sell = 0
        if current > previous * 1.08:
            sell = btc * (current / previous - 1)

        if sell > btc * 0.5:
            sell = btc * 0.5

        return sell

