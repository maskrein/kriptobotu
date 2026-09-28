import time

_last_signal = None
_last_price = None
_last_time = 0
_last_closed_time = 0


def should_record(signal):
    global _last_signal, _last_price, _last_time

    now = time.time()

    if _last_signal == signal.get("signal"):
        if _last_price is not None:
            change = abs(signal.get("price", 0) - _last_price)

            # Aynı yönde çok yakın sinyalleri engelle
            # Scalping modu için daha kısa tutuldu
            if change < 30 and now - _last_time < 30:
                return False

    _last_signal = signal.get("signal")
    _last_price = signal.get("price")
    _last_time = now

    return True


def can_scalp_trade():
    """
    Scalping modunda yeni fırsatlara izin verir.
    Eski uzun cooldown kaldırıldı.
    """
    return True


def register_position_closed():
    global _last_closed_time
    _last_closed_time = time.time()


def last_close_time():
    return _last_closed_time


def check_execution(signal):
    """
    Trade açılmadan önce son kontrol katmanı.
    """

    if not signal:
        return {
            "allowed": False,
            "reason": "EMPTY_SIGNAL"
        }

    action = signal.get("signal")
    confidence = signal.get("confidence", 0)

    if action not in ("BUY", "SELL"):
        return {
            "allowed": False,
            "reason": "INVALID_SIGNAL"
        }

    if confidence < 70:
        return {
            "allowed": False,
            "reason": "LOW_CONFIDENCE"
        }

    if not can_scalp_trade():
        return {
            "allowed": False,
            "reason": "SCALP_LOCK"
        }

    return {
        "allowed": True,
        "reason": "EXECUTION_APPROVED"
    }
