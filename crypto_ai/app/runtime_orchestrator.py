import time

_RUNTIME = {
    "status": "READY",
    "mode": "LIVE_DEVELOPMENT_PAPER_TRADING",
    "orchestrator": "ACTIVE"
}


def start():
    return {
        "status": "RUNNING",
        "runtime": _RUNTIME
    }


def get_runtime_status():
    return _RUNTIME


def heartbeat():
    _RUNTIME["last_check"] = time.time()
    return _RUNTIME
