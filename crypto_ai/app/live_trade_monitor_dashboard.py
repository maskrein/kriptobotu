def build_live_trade_monitor_dashboard(state):
    position = state.get("position")
    history = state.get("history", [])

    last = history[-1] if history else {}

    return {
        "title": "AI Trade Execution",
        "status": "OPEN" if position else "CLOSED",
        "position": position,
        "last_trade": last,
        "gross_pnl": last.get("gross_pnl", 0),
        "commission": last.get("commission", 0),
        "slippage": last.get("slippage", 0),
        "net_pnl": last.get("net_pnl", last.get("pnl", 0)),
        "result": "WIN" if last.get("net_pnl", last.get("pnl", 0)) > 0 else "LOSS"
    }
