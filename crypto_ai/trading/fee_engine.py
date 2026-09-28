
class FeeEngine:
    def __init__(self, rate=0.001):
        self.rate = rate

    def fee(self, amount):
        return amount * self.rate

    def net_profit(self, buy_value, sell_value):
        buy_fee = self.fee(buy_value)
        sell_fee = self.fee(sell_value)
        return {
            "gross_profit": sell_value - buy_value,
            "buy_fee": buy_fee,
            "sell_fee": sell_fee,
            "total_fee": buy_fee + sell_fee,
            "net_profit": sell_value - buy_value - buy_fee - sell_fee
        }
