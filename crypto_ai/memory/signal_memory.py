import json
import os
import time
from datetime import datetime

MEMORY_FILE = "memory/signal_memory.json"

def safe_save(path, data):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    tmp = path + ".tmp_" + str(os.getpid())

    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        for _ in range(10):
            try:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except PermissionError:
                        pass
                os.replace(tmp, path)
                return True
            except (PermissionError, FileNotFoundError):
                time.sleep(0.2)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass

    return False


def save_signal(signal):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    data = []

    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

    data.append({
        "timestamp": datetime.now().isoformat(),
        "signal": signal
    })

    if len(data) > 5000:
        data = data[-5000:]

    safe_save(MEMORY_FILE, data)
    return True


def get_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
