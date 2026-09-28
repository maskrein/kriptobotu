
# CRYPTO AI V7.6 helper
# Dashboard tarafında kullanılacak otomatik yenileme ve AI history yardımcıları

import json
from datetime import datetime
from runtime.live_state import load_state, save_state


def add_ai_history(event):
    state = load_state()
    history = state.get("ai_history", [])

    history.append({
        "time": str(datetime.now()),
        **event
    })

    state["ai_history"] = history[-50:]
    save_state(state)
    return state
