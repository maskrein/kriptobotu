def build_ai_learning_feedback_card(history):
    total = len(history)
    wins = sum(1 for x in history if x.get("net_pnl", x.get("pnl", 0)) > 0)

    avg = (
        sum(x.get("net_pnl", x.get("pnl", 0)) for x in history) / total
        if total else 0
    )

    return {
        "title": "AI Performance Learning",
        "total_closed_trades": total,
        "winning_trades": wins,
        "win_rate": round((wins / total) * 100, 2) if total else 0,
        "average_net_pnl": round(avg, 4),
        "status": "ACTIVE"
    }
