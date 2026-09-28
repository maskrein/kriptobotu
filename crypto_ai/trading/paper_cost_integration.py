from trading.cost_engine import TradingCostEngine

def apply_trade_costs(entry, exit, quantity):
    engine = TradingCostEngine()

    result = engine.calculate(
        entry,
        exit,
        quantity
    )

    return {
        "gross_pnl": result["gross_pnl"],
        "commission": result["commission"],
        "slippage": result["slippage"],
        "net_pnl": result["net_pnl"]
    }
