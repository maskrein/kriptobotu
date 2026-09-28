def build_ai_evolution(history=None):
    history = history or []

    total = len(history)

    buy = sum(1 for x in history if x.get("signal") == "BUY")
    sell = sum(1 for x in history if x.get("signal") == "SELL")
    wait = sum(1 for x in history if x.get("signal") == "WAIT")

    scores = [
        float(x.get("score", 0))
        for x in history
        if isinstance(x, dict)
    ]

    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    confidence = [
        float(x.get("confidence", 0))
        for x in history
        if isinstance(x, dict)
    ]

    avg_confidence = round(
        sum(confidence) / len(confidence), 2
    ) if confidence else 0

    return {
        "status": "LEARNING",
        "total_decisions": total,
        "buy_count": buy,
        "sell_count": sell,
        "wait_count": wait,
        "average_score": avg_score,
        "average_confidence": avg_confidence
    }
