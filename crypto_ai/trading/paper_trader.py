import time
from trading.paper_state_bridge import get_shared_paper_state, sync_paper_state
from trading.tp_sl_manager import TPSLManager

class PaperTrader:
    def __init__(self, balance=10000):
        self.balance = balance
        self.position = None
        self.history = []
        self.tp_sl = TPSLManager()
        self._load_shared_state()


    def _load_shared_state(self):
        try:
            shared = get_shared_paper_state()
            if shared:
                self.balance = shared.get("balance", self.balance)
                self.position = shared.get("position")
                self.history = shared.get("history", [])
        except Exception:
            pass

    def buy(self, symbol, price, quantity):
        if self.position is not None:
            return {"status": "POSITION_EXISTS"}

        cost = price * quantity

        if cost > self.balance:
            return {"status": "INSUFFICIENT_BALANCE"}

        self.balance -= cost

        self.position = {
            "symbol": symbol,
            "side": "LONG",
            "entry": price,
            "quantity": quantity,
            "time": time.time()
        }

        self.position = self.tp_sl.apply(self.position)

        try:
            sync_paper_state(self.state())
        except Exception:
            pass
        return self.position

    def sell(self, price, exit_reason=None):
        if self.position is None:
            return {"status": "NO_POSITION"}

        p = self.position

        pnl = (price - p["entry"]) * p["quantity"]

        trade = {
            **p,
            "exit": price,
            "pnl": round(pnl, 4),
            "closed_time": time.time(),
            "exit_reason": exit_reason or "MANUAL"
        }

        # V7.2 Feedback Loop integration
        try:
            from trading.feedback_integration import save_closed_trade
            save_closed_trade(trade)
        except Exception:
            pass

        self.balance += price * p["quantity"]
        self.history.append(trade)
        self.position = None

        try:
            sync_paper_state(self.state())
        except Exception:
            pass
        return trade

    def state(self):
        return {
            "balance": self.balance,
            "position": self.position,
            "history": self.history
        }
