from performance.pnl_engine import calculate_pnl, check_exit

def monitor_position(position, market_price):
    if not position:
        return {}

    pnl = calculate_pnl(
        position.get("entry", 0),
        market_price,
        position.get("quantity", 0)
    )

    exit_check = check_exit(position, market_price)

    return {
        "symbol": position.get("symbol"),
        "pnl": pnl,
        "exit": exit_check,
    }
