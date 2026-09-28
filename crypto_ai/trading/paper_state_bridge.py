from runtime.paper_shared_state import save_paper_state, load_paper_state


def calculate_paper_account(state, current_price=None):
    balance = state.get('balance', 0)
    position = state.get('position')
    realized = sum(
        x.get('net_pnl', x.get('pnl', 0))
        for x in state.get('history', [])
    )

    unrealized = 0
    position_value = 0

    if position:
        entry = position.get('entry', 0)
        qty = position.get('quantity', 0)
        price = current_price if current_price else entry
        position_value = price * qty
        unrealized = (price - entry) * qty

    return {
        'wallet_balance': round(balance, 4),
        'available_balance': round(balance, 4),
        'position_value': round(position_value, 4),
        'unrealized_pnl': round(unrealized, 4),
        'realized_pnl': round(realized, 4),
        'equity': round(balance + unrealized, 4)
    }


def sync_paper_state(state):
    save_paper_state(state)
    return state


def get_shared_paper_state():
    return load_paper_state()
