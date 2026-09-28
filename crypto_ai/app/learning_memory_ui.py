def get_learning_memory_view(history=None):
    history = history or []

    total = len(history)
    buy = sum(1 for x in history if x.get('signal') == 'BUY')
    sell = sum(1 for x in history if x.get('signal') == 'SELL')
    wait = sum(1 for x in history if x.get('signal') == 'WAIT')

    scores = [float(x.get('score', 0)) for x in history]
    avg = round(sum(scores) / len(scores), 2) if scores else 0

    return {
        'learning_status': 'ACTIVE',
        'samples': total,
        'buy': buy,
        'sell': sell,
        'wait': wait,
        'average_score': avg
    }
