def build_decision_layer(signal):
    confidence = int(signal.get("confidence", 0))
    reasons = signal.get("reason", [])

    score = min(100, max(0, confidence))

    if signal.get("signal") == "BUY":
        mood = "Bullish"
    elif signal.get("signal") == "SELL":
        mood = "Bearish"
    else:
        mood = "Neutral"

    if score >= 75:
        risk = "Low"
    elif score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    explanation = ", ".join(reasons) if reasons else "No additional data"

    return {
        "ai_score": score,
        "market_mood": mood,
        "risk_level": risk,
        "decision_explanation": explanation
    }
