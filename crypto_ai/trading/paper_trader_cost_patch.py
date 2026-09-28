from trading.cost_engine import TradingCostEngine


def build_cost_aware_close(entry, exit, quantity):
    engine = TradingCostEngine()

    result = engine.calculate(
        entry,
        exit,
        quantity
    )

    return {
        "gross_pnl": result.get("gross_pnl", 0),
        "commission": result.get("commission", 0),
        "slippage": result.get("slippage", 0),
        "net_pnl": result.get("net_pnl", 0)
    }


# V7.18.8_COST_AWARE_PAPERTRADER
# PaperTrader.sell() should merge this result into history.
