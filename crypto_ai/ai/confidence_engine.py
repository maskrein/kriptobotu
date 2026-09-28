def adjust_confidence(value):
    return max(0, min(100, int(value)))
