from datetime import datetime

def calculate_pnl(entry, current, quantity):
    return round((current - entry) * quantity, 2)

def check_exit(position, current_price):
    if not position:
        return {"close": False}

    if current_price >= position.get("tp", 0):
        return {"close": True, "reason": "TAKE_PROFIT"}

    if current_price <= position.get("sl", 0):
        return {"close": True, "reason": "STOP_LOSS"}

    return {"close": False}
