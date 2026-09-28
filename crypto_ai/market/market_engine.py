import ccxt
import time

_EXCHANGE = None

def _get_exchange():
    global _EXCHANGE
    if _EXCHANGE is None:
        _EXCHANGE = ccxt.binance({
            "enableRateLimit": True
        })
    return _EXCHANGE


def get_market():
    symbols = ["BTC/USDT", "ETH/USDT"]
    result = {}

    try:
        exchange = _get_exchange()

        for symbol in symbols:
            ticker = exchange.fetch_ticker(symbol)
            key = symbol.replace("/", "")

            result[key] = {
                "price": float(ticker.get("last") or 0),
                "change": float(ticker.get("percentage") or 0),
                "volume": float(ticker.get("baseVolume") or 0),
                "time": time.time()
            }

    except Exception:
        return {}

    return result
