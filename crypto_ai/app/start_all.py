import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.system_launcher import launch
from app.component_health_checker import check
from app.runtime_orchestrator import start

def run():
    return {
        "launch": launch(),
        "health": check(),
        "runtime": start(),
        "status": "READY"
    }

if __name__ == "__main__":
    print(run())
