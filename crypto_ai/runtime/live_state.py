import json
from pathlib import Path

FILE = Path("runtime/live_state.json")

def load_state():
    if not FILE.exists():
        return {}
    return json.loads(FILE.read_text())

def save_state(state):
    FILE.write_text(json.dumps(state, indent=2))


def migrate_ai_history(state):
    history = state.get("ai_history", [])
    for item in history:
        item.setdefault("ai_score", item.get("confidence", 0))
        item.setdefault("risk_level", "Low" if item.get("confidence", 0) >= 70 else "Medium")
        item.setdefault("market_mood", "Bullish" if item.get("signal") == "BUY" else "Neutral")
        item.setdefault("reason_text", ", ".join(item.get("reason", [])))
    state["ai_history"] = history
    return state
