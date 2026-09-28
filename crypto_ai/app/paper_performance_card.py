def build_paper_performance_card(state=None):
    state = state or {}

    history = state.get("history", [])

    wins = sum(1 for x in history if float(x.get("pnl", 0)) > 0)
    losses = sum(1 for x in history if float(x.get("pnl", 0)) < 0)

    total_pnl = round(
        sum(float(x.get("pnl", 0)) for x in history),
        4
    )

    return {
        "title": "Paper Trading Performance",
        "balance": state.get("balance", 0),
        "total_trades": len(history),
        "winning_trades": wins,
        "losing_trades": losses,
        "net_pnl": total_pnl
    }
