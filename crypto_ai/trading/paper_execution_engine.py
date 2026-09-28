from trading.paper_trader import PaperTrader

class PaperExecutionEngine:
    def __init__(self):
        self.trader = PaperTrader()

    def execute_signal(self, signal):
        action = signal.get("signal", "").upper()
        symbol = signal.get("symbol", "BTCUSDT")
        price = float(signal.get("price", 0))
        quantity = float(signal.get("quantity", 0.001))

        if action == "BUY":
            return self.trader.buy(symbol, price, quantity)

        if action == "SELL":
            return self.trader.sell(price)

        return {"status": "NO_ACTION"}

    def state(self):
        return self.trader.state()
