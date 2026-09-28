class PaperEngine:
    def __init__(self):
        pass

    def process_signal(self, signal):
        if signal.get("signal") != "BUY":
            return {}

        return {
            "symbol": signal.get("symbol"),
            "entry": signal.get("price"),
            "quantity": 1,
            "sl": signal.get("price") * 0.98,
            "tp": signal.get("price") * 1.04
        }
