def enrich_trade_history(trade):
    return {
        **trade,
        'gross_pnl': trade.get('gross_pnl', trade.get('pnl', 0)),
        'commission': trade.get('commission', 0),
        'slippage': trade.get('slippage', 0),
        'net_pnl': trade.get('net_pnl', trade.get('pnl', 0))
    }
