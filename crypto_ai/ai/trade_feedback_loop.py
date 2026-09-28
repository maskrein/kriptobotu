import json
import os
from datetime import datetime

FILE = "runtime/trade_feedback.json"


def _load():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def record_trade(trade):
    data = _load()
    data.append({
        "time": str(datetime.now()),
        **trade
    })

    os.makedirs("runtime", exist_ok=True)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def performance():
    data = _load()

    wins = len([x for x in data if x.get("pnl", 0) > 0])
    losses = len([x for x in data if x.get("pnl", 0) < 0])

    return {
        "samples": len(data),
        "wins": wins,
        "losses": losses,
        "win_rate": round(
            (wins / len(data)) * 100, 2
        ) if data else 0
    }
