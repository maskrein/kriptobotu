import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ai.signal_engine import get_signal
from ai.signal_filter import check_execution
from trading.paper_worker import PaperWorker


worker = PaperWorker()


def start_trading_worker(interval=5):
    print("AI TRADING WORKER STARTED")

    while True:
        try:
            signal = get_signal()

            # Önce açık pozisyon yönetimine izin ver.
            # TP/SL ve AutoExecutionLoop mevcut pozisyonu burada kontrol eder.
            state = worker.state()
            position = state.get("position")

            if position:
                result = worker.on_ai_decision(signal)
                print(
                    f"[POSITION MANAGER] {signal.get('symbol')} "
                    f"PRICE:{signal.get('price')} "
                    f"RESULT:{result}"
                )

            else:
                # Yeni pozisyon açılışları filtrelerden geçer.
                decision = check_execution(signal)

                if decision["allowed"]:
                    result = worker.on_ai_decision(signal)
                    print(
                        f"[TRADE] {signal.get('symbol')} "
                        f"{signal.get('signal')} "
                        f"CONF:{signal.get('confidence')} "
                        f"RESULT:{result}"
                    )
                else:
                    print(
                        f"[FILTERED] {signal.get('symbol')} "
                        f"{signal.get('signal')} "
                        f"REASON:{decision['reason']}"
                    )

        except Exception as e:
            print("TRADING ERROR:", e)

        time.sleep(interval)


if __name__ == "__main__":
    start_trading_worker()
