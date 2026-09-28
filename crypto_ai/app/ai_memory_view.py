import json
from runtime.live_state import load_state


def get_ai_memory():
    state = load_state()
    history = state.get("ai_history", [])

    return {
        "total_decisions": len(history),
        "latest": history[-20:],
        "buy_count": len([x for x in history if x.get("signal") == "BUY"]),
        "wait_count": len([x for x in history if x.get("signal") == "WAIT"]),
        "sell_count": len([x for x in history if x.get("signal") == "SELL"]),
    }