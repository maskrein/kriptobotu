def build_live_trade_monitor(state):
    position = state.get("position")

    if position:
        return {
            "status": "OPEN",
            "symbol": position.get("symbol"),
            "side": position.get("side"),
            "entry": position.get("entry"),
            "quantity": position.get("quantity")
        }

    history = state.get("history", [])
    last = history[-1] if history else {}

    return {
        "status": "CLOSED",
        "last_trade": last,
        "net_pnl": last.get("net_pnl", last.get("pnl", 0))
    }
