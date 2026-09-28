from trading.cost_engine import TradingCostEngine
from trading.paper_state_bridge import sync_paper_state


def close_with_cost_and_sync(state, symbol, entry, exit_price, quantity):
    engine = TradingCostEngine()

    cost = engine.calculate(
        entry,
        exit_price,
        quantity
    )

    record = {
        "symbol": symbol,
        "entry": entry,
        "exit": exit_price,
        "quantity": quantity,
        "gross_pnl": cost["gross_pnl"],
        "commission": cost["commission"],
        "slippage": cost["slippage"],
        "net_pnl": cost["net_pnl"]
    }

    state.setdefault("history", []).append(record)

    sync_paper_state(state)

    return record
