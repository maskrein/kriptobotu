def build_live_trade_monitor_card(state):
    monitor = {
        "title": "AI Trade Execution Monitor",
        "trade": state.get("position"),
        "last_result": state.get("history", [])[-1] if state.get("history") else None
    }

    return monitor
