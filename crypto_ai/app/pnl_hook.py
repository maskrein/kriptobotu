from trading.paper_monitor import monitor_position

def update_pnl(state, market):
    position = state.get("position")

    if not position:
        return state

    symbol = position.get("symbol")
    price = market.get(symbol, {}).get("price", 0)

    result = monitor_position(position, price)

    state["gross_pnl"] = result.get("pnl", 0)
    state["net_pnl"] = result.get("pnl", 0)

    return state
