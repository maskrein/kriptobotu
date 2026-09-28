from trading.paper_state_store import load_state

def get_trade_execution():
    state = load_state()
    history = state.get('history', [])
    position = state.get('position')

    last = history[-1] if history else {}

    return {
        'status': 'OPEN' if position else 'CLOSED',
        'side': (position or last).get('side', 'LONG'),
        'symbol': (position or last).get('symbol', '-'),
        'entry': (position or last).get('entry', '-'),
        'exit': last.get('exit', '-'),
        'current': (position or last).get('current', (position or last).get('current_price', '-')),
        'live_pnl': (position or last).get('live_pnl', (position or last).get('unrealized_pnl', 0)),
        'gross_pnl': last.get('gross_pnl', last.get('pnl', 0)),
        'commission': last.get('commission', 0),
        'slippage': last.get('slippage', 0),
        'net_pnl': last.get('net_pnl', last.get('pnl', 0)),
        'result': 'RUNNING' if position else ('WIN' if last.get('net_pnl', last.get('pnl', 0)) > 0 else '-')
    }
