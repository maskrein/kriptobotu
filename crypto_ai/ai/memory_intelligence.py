
def analyze_memory(history):
    history = history or []

    total = len(history)
    buy = len([x for x in history if x.get("signal") == "BUY"])
    sell = len([x for x in history if x.get("signal") == "SELL"])
    wait = len([x for x in history if x.get("signal") == "WAIT"])

    scores = []
    risks = {}

    for item in history:
        scores.append(float(item.get("score", item.get("ai_score", 0))))
        risk = item.get("risk", item.get("risk_level", "Unknown"))
        risks[risk] = risks.get(risk, 0) + 1

    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    change = "INITIAL"
    if len(history) > 1:
        prev = history[-2].get("signal")
        curr = history[-1].get("signal")
        if prev and curr and prev != curr:
            change = f"{prev}->{curr}"

    return {
        "total_decisions": total,
        "buy_count": buy,
        "sell_count": sell,
        "wait_count": wait,
        "avg_score": avg_score,
        "last_change": change,
        "risk_distribution": risks
    }
