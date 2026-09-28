class TradingCostEngine:
    def __init__(self, commission_rate=0.001, slippage_rate=0.0001):
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate

    def calculate(self, entry, exit, quantity):
        gross_pnl = (exit - entry) * quantity

        buy_value = entry * quantity
        sell_value = exit * quantity

        commission = (buy_value + sell_value) * self.commission_rate
        slippage = sell_value * self.slippage_rate

        net_pnl = gross_pnl - commission - slippage

        return {
            "gross_pnl": round(gross_pnl, 4),
            "commission": round(commission, 4),
            "slippage": round(slippage, 4),
            "net_pnl": round(net_pnl, 4)
        }
