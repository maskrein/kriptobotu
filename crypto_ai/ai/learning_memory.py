from collections import Counter

def analyze_learning(history):
    history = history or []

    signals = Counter(
        item.get("signal", "WAIT")
        for item in history
    )

    scores = [
        float(item.get("score", item.get("confidence", 0)))
        for item in history
    ]

    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    return {
        "samples": len(history),
        "buy_count": signals.get("BUY", 0),
        "sell_count": signals.get("SELL", 0),
        "wait_count": signals.get("WAIT", 0),
        "average_score": avg_score,
    }
