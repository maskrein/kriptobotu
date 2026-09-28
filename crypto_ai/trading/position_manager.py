"""Position manager for AI trade engine v1.
Controls whether BUY/SELL actions are allowed based on current paper position.
"""
class PositionManager:
    def __init__(self, paper_worker=None):
        self.paper_worker = paper_worker

    def has_position(self, state):
        return bool(state and state.get("position"))

    def handle_decision(self, decision, state):
        signal = str(decision.get("signal", "WAIT")).upper()

        if signal == "BUY":
            if self.has_position(state):
                return {"action": "HOLD", "reason": "POSITION_ALREADY_OPEN"}
            return {"action": "OPEN", "decision": decision}

        if signal == "SELL":
            if not self.has_position(state):
                return {"action": "WAIT", "reason": "NO_POSITION"}
            return {"action": "CLOSE", "decision": decision}

        return {"action": "WAIT", "reason": "NO_ACTION"}
