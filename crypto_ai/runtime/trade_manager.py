from runtime.live_state import load_state, save_state
from performance.pnl_engine import check_exit

def manage_trade(price):
    state = load_state()
    position = state.get("position")

    if not position:
        return state

    result = check_exit(position, price)

    if result.get("close"):
        state.setdefault("trades", []).append({
            "action": "CLOSE",
            "reason": result.get("reason"),
            "symbol": position.get("symbol"),
            "price": price
        })

        state["position"] = None
        save_state(state)

    return state
