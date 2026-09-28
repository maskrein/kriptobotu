def build_paper_analytics(state=None):
    state = state or {}

    history = state.get("history", [])
    balance = state.get("balance", 0)

    wins = sum(
        1 for t in history
        if float(t.get("pnl", 0)) > 0
    )

    losses = sum(
        1 for t in history
        if float(t.get("pnl", 0)) < 0
    )

    total_pnl = round(
        sum(float(t.get("pnl", 0)) for t in history),
        4
    )

    return {
        "balance": balance,
        "total_trades": len(history),
        "winning_trades": wins,
        "losing_trades": losses,
        "total_pnl": total_pnl
    }
