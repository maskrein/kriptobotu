from trading.paper_history_cost import build_trade_record


def close_trade_with_cost_history(position, exit_price):
    return build_trade_record(
        symbol=position.get("symbol"),
        entry=position.get("entry"),
        exit=exit_price,
        quantity=position.get("quantity", 0)
    )
