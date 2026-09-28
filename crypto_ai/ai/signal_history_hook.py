from ai.signal_filter import should_record
from runtime.live_state import load_state, save_state

def record_ai_signal(signal):
    if not should_record(signal):
        return False

    state = load_state()
    from runtime.live_state import migrate_ai_history
    state = migrate_ai_history(state)
    history = state.get("ai_history", [])

    # V7.9.2 duplicate protection:
    # Same symbol + same signal + almost same price is not a new AI decision.
    if history:
        last = history[-1]
        same_symbol = last.get("symbol") == signal.get("symbol")
        same_signal = last.get("signal") == signal.get("signal")
        try:
            same_price = abs(float(last.get("price", 0)) - float(signal.get("price", 0))) < 1
        except Exception:
            same_price = False

        if same_symbol and same_signal and same_price:
            return False

    if history:\n        prev = history[-1].get("signal")\n        curr = signal.get("signal")\n        if prev and curr and prev != curr:\n            signal["change"] = f"{prev}->{curr}"\n    else:\n        signal["change"] = "INITIAL"\n\n    # V7.9.6 AI memory enrichment
    try:
        from ai.decision_layer import build_decision_layer
        signal.update(build_decision_layer(signal))
        signal["reason_text"] = ", ".join(signal.get("reason", []))
    except Exception:
        signal.setdefault("ai_score", signal.get("confidence", 0))
        signal.setdefault("risk_level", "Unknown")
        signal.setdefault("market_mood", "Unknown")
        signal.setdefault("reason_text", ", ".join(signal.get("reason", [])))

    history.append({
        "symbol": signal.get("symbol", "BTCUSDT"),
        "price": signal.get("price", 0),
        "signal": signal.get("signal", "HOLD"),
        "confidence": signal.get("confidence", 0),
        "score": signal.get("ai_score", signal.get("confidence", 0)),
        "risk": (
            "Low"
            if signal.get("confidence", 0) >= 75
            else "Medium"
            if signal.get("confidence", 0) >= 50
            else "High"
        ),
        "reason": signal.get("reason", ["AI analysis"]),
        "decision": ", ".join(signal.get("reason", ["AI decision"])),
        "market_mood": (
            "Bullish"
            if signal.get("signal") == "BUY"
            else "Bearish"
            if signal.get("signal") == "SELL"
            else "Neutral"
        ),
        "time": signal.get("time")
    })
    state["ai_history"] = history[-100:]
    save_state(state)
    return True
