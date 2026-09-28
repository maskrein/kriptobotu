from trading.paper_cost_integration import apply_trade_costs


def build_trade_record(symbol, entry, exit, quantity):
    costs = apply_trade_costs(
        entry,
        exit,
        quantity
    )

    return {
        "symbol": symbol,
        "entry": entry,
        "exit": exit,
        "quantity": quantity,
        "gross_pnl": costs["gross_pnl"],
        "commission": costs["commission"],
        "slippage": costs["slippage"],
        "net_pnl": costs["net_pnl"]
    }
