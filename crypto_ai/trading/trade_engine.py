"""
AI Trade Engine - V8 Step 1
Automatic decision loop foundation.

This module manages:
- signal evaluation
- position open/close decisions
- repeated AI cycle handling

It does not send real exchange orders.
"""

import time


class TradeEngine:
    def __init__(self, worker=None):
        self.worker = worker
        self.last_signal = None
        self.last_action_time = 0

    def evaluate(self, ai_decision):
        if not ai_decision:
            return {"status": "NO_DECISION"}

        signal = str(ai_decision.get("signal", "WAIT")).upper()

        payload = {
            "signal": signal,
            "symbol": ai_decision.get("symbol", "BTCUSDT"),
            "price": ai_decision.get("price", 0),
            "quantity": ai_decision.get("quantity", 0.001),
            "time": time.time()
        }

        self.last_signal = payload
        self.last_action_time = time.time()

        if self.worker:
            return self.worker.on_ai_decision(payload)

        return {
            "status": "READY",
            "decision": payload
        }

    def status(self):
        return {
            "last_signal": self.last_signal,
            "last_action_time": self.last_action_time
        }
