import time
import threading

from app.price_engine import get_prices
from runtime.live_state import load_state, save_state
from performance.pnl_engine import calculate_pnl


def update_pnl_once():
    state = load_state()
    position = state.get("position")

    if not position:
        return state

    market = get_prices()
    symbol = position.get("symbol")
    current = market.get(symbol, {}).get("price")

    if not current:
        return state

    pnl = calculate_pnl(
        position.get("entry", 0),
        current,
        position.get("quantity", 0)
    )

    state["gross_pnl"] = pnl
    state["net_pnl"] = pnl

    save_state(state)
    return state


def update_pnl():
    return update_pnl_once()


def start_pnl_worker():
    def loop():
        while True:
            try:
                update_pnl_once()
            except Exception:
                pass
            time.sleep(5)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
