"""Trade loop skeleton.
Connects AI decisions to PositionManager.
"""
import time

class TradeLoop:
    def __init__(self, engine, position_manager, interval=5):
        self.engine = engine
        self.position_manager = position_manager
        self.interval = interval
        self.running = False

    def run_once(self, state):
        decision = self.engine.get_decision()
        return self.position_manager.handle_decision(decision, state)

    def start(self, state_provider):
        self.running = True
        while self.running:
            state = state_provider()
            self.run_once(state)
            time.sleep(self.interval)

    def stop(self):
        self.running = False
