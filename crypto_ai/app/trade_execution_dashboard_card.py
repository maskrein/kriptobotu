def build_trade_execution_card(state):
    position = state.get("position")
    history = state.get("history", [])
    last = history[-1] if history else {}

    return {
        "title": "AI Trade Execution",
        "status": "OPEN" if position else "CLOSED",
         "side": (position or last).get("side", "LONG"),
        "symbol": (position or last).get("symbol"),
        "entry": (position or last).get("entry"),
        "exit": last.get("exit"),
        "gross_pnl": last.get("gross_pnl", 0),
        "commission": last.get("commission", 0),
        "slippage": last.get("slippage", 0),
        "net_pnl": last.get("net_pnl", last.get("pnl", 0)),
        "result": "WIN" if last.get("net_pnl", last.get("pnl", 0)) > 0 else "LOSS"
    }
