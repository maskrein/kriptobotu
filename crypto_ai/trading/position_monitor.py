import json
from pathlib import Path

STATE = Path("runtime/live_state.json")

def update_position(price):
    if not STATE.exists():
        return {}

    data = json.loads(STATE.read_text())

    pos = data.get("position")
    if pos:
        pnl = (float(price) - float(pos["entry"])) * float(pos["quantity"])
        data["gross_pnl"] = round(pnl, 4)
        data["net_pnl"] = round(
            pnl - float(data.get("fees",0)) - float(data.get("slippage",0)),
            4
        )

    STATE.write_text(json.dumps(data, indent=2))
    return data
