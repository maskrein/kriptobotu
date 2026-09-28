from ai.trade_feedback_loop import performance


def get_feedback_score():
    result = performance()

    if result["samples"] == 0:
        return 50

    return min(
        100,
        max(
            0,
            int(result["win_rate"])
        )
    )
