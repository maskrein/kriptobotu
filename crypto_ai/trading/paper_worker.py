from trading.auto_execution_loop import AutoExecutionLoop
from trading.paper_state_bridge import sync_paper_state


class PaperWorker:
    def __init__(self):
        self.engine = AutoExecutionLoop()

    def on_ai_decision(self, decision):
        result = self.engine.process_signal(decision)

        try:
            sync_paper_state(self.engine.get_state())
        except Exception:
            pass

        return result

    def state(self):
        state = self.engine.get_state()

        try:
            sync_paper_state(state)
        except Exception:
            pass

        return state
