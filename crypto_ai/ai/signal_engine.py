from datetime import datetime

from app.price_engine import get_prices
from runtime.live_state import load_state, save_state

from ai.confidence_engine import adjust_confidence
from ai.decision_layer import build_decision_layer
from ai.signal_filter import should_record
from ai.ai_intelligence import calculate_ai_intelligence


def add_ai_history(result):
    state = load_state()

    history = state.get("ai_history", [])

    history.append({
        "symbol": result.get("symbol"),
        "price": result.get("price"),

        "signal": result.get("signal"),
        "confidence": result.get("confidence"),

        "momentum_score": result.get("momentum_score", 0),
        "trend_score": result.get("trend_score", 0),
        "volume_score": result.get("volume_score", 0),
        "volatility_score": result.get("volatility_score", 0),
        "ai_explanation": result.get("ai_explanation", ""),

        "score": result.get(
            "ai_score",
            result.get("confidence", 0)
        ),

        "risk": result.get(
            "risk_level",
            "Medium"
        ),

        "market_mood": result.get(
            "market_mood",
            "Neutral"
        ),

        "reason": result.get(
            "reason",
            []
        ),

        "decision": result.get(
            "decision_explanation",
            ""
        ),

        "time": result.get(
            "time",
            str(datetime.now())
        )
    })

    state["ai_history"] = history[-100:]

    save_state(state)


def get_signal():

    prices = get_prices()

    btc = prices.get(
        "BTCUSDT",
        {}
    )

    price = btc.get(
        "price",
        0
    )

    change = btc.get(
        "change",
        0
    )


    reasons = []


    if change > 0:
        signal = "BUY"
        reasons.append(
            "Positive momentum"
        )

    elif change < 0:
        signal = "SELL"
        reasons.append(
            "Negative momentum"
        )

    else:

        signal = "WAIT"
        reasons.append(
            "No clear momentum"
        )


    reasons.append(
        "Live price"
    )


    confidence = 80 if signal != "WAIT" else 50

    confidence = adjust_confidence(
        confidence
    )


    result = {
        "symbol": "BTCUSDT",
        "price": price,

        "signal": signal,

        "confidence": confidence,

        "reason": reasons,

        "time": str(
            datetime.now()
        )
    }


    decision = build_decision_layer(
        result
    )

    result.update(
        decision
    )

    intelligence = calculate_ai_intelligence(result, prices)
    result.update(intelligence)


    if should_record(result):
        add_ai_history(result)


    return result