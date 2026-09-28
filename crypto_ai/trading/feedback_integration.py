from ai.trade_feedback_loop import record_trade


def save_closed_trade(result):
    """
    Sends completed paper trades to feedback memory.
    """

    if not result:
        return

    trade = {
        "symbol": result.get("symbol"),
        "side": result.get("side"),
        "entry": result.get("entry"),
        "exit": result.get("exit"),
        "pnl": result.get("pnl", 0),
        "exit_reason": result.get("exit_reason", "UNKNOWN"),
        "result": "WIN" if result.get("pnl", 0) > 0 else "LOSS"
    }

    record_trade(trade)
