import time

class ScalpingManager:
    def __init__(self, cooldown=3, take_profit=0.0018, stop_loss=0.0012):
        self.cooldown = cooldown
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.last_trade = 0

    def can_enter(self):
        return time.time() - self.last_trade >= self.cooldown

    def register(self):
        self.last_trade = time.time()

    def exit_signal(self, position, price):
        if not position:
            return None
        entry = position.get("entry", 0)
        if not entry:
            return None
        change = (price-entry)/entry
        if change >= self.take_profit:
            return "SCALP_TAKE_PROFIT"
        if change <= -self.stop_loss:
            return "SCALP_STOP_LOSS"
        return None
