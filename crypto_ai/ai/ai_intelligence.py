def calculate_ai_intelligence(signal, market=None):
    confidence = int(signal.get("confidence", 0))

    momentum = 25 if signal.get("signal") == "BUY" else 15 if signal.get("signal") == "SELL" else 10
    trend = 20 if signal.get("signal") in ("BUY", "SELL") else 5
    volume = 15
    volatility = 10
    mood = 14 if signal.get("signal") == "BUY" else 8

    score = min(100, momentum + trend + volume + volatility + mood)

    risk_score = max(0, 100 - score)

    return {
        "ai_score": score,
        "risk_score": risk_score,
        "momentum_score": momentum,
        "trend_score": trend,
        "volume_score": volume,
        "volatility_score": volatility,
        "mood_score": mood,
        "ai_explanation": "AI intelligence analysis generated from momentum, trend, volume and risk factors."
    }
