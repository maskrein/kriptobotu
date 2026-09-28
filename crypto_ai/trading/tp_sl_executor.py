from trading.tp_sl_manager import TPSLManager

class TPSLExecutor:
    def __init__(self):
        self.manager = TPSLManager()

    def check(self, position, price):
        return self.manager.check(position, price)
