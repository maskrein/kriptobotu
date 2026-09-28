from trading.paper_trader import PaperTrader


class LivePaperBinding:

    def __init__(self):
        self.paper_trader = PaperTrader()

    def execute(self, signal):
        action = signal.get("signal")

        if action == "BUY":
            return self.paper_trader.buy(
                symbol=signal["symbol"],
                price=signal["price"],
                quantity=signal.get("quantity", 0.001)
            )

        if action == "SELL":
            return self.paper_trader.sell(
                price=signal["price"]
            )

        return {
            "status": "WAIT"
        }

    def state(self):
        return self.paper_trader.state()