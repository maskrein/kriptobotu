import time


class ScalpingEngine:
    def __init__(self, cooldown_seconds=3, take_profit=0.0018, stop_loss=0.0012):
        self.cooldown_seconds = cooldown_seconds
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.last_trade_time = 0

    def can_trade(self):
        return time.time() - self.last_trade_time >= self.cooldown_seconds

    def register_trade(self):
        self.last_trade_time = time.time()

    def should_close(self, position, price):
        if not position:
            return None

        entry = position.get("entry", 0)
        if not entry:
            return None

        change = (price - entry) / entry

        if position.get("side", "LONG") == "LONG":
            if change >= self.take_profit:
                return "SCALP_TAKE_PROFIT"

            if change <= -self.stop_loss:
                return "SCALP_STOP_LOSS"

        return None
