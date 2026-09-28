from trading.live_paper_binding import LivePaperBinding
from trading.tp_sl_manager import TPSLManager
from trading.scalping_engine import ScalpingEngine
from trading.scalping_manager import ScalpingManager


class AutoExecutionLoop:

    def __init__(self):
        self.binding = LivePaperBinding()
        self.tp_sl = TPSLManager()
        self.scalper = ScalpingEngine(cooldown_seconds=3, take_profit=0.0018, stop_loss=0.0012)
        self.scalping_manager = ScalpingManager()

    def _position_report(self, position, price):
        entry = position.get("entry", 0)
        quantity = position.get("quantity", 0)

        pnl = round((price - entry) * quantity, 4)

        return {
            "status": "HOLDING",
            "symbol": position.get("symbol"),
            "side": position.get("side"),
            "entry": entry,
            "current": price,
            "quantity": quantity,
            "tp": position.get("tp"),
            "sl": position.get("sl"),
            "unrealized_pnl": pnl
        }

    def process_signal(self, state):
        if not state:
            return {"status": "NO_SIGNAL"}

        signal = {
            "signal": state.get("signal", "WAIT"),
            "symbol": state.get("symbol", "BTCUSDT"),
            "price": state.get("price", 0),
            "quantity": state.get("quantity", 0.001)
        }

        current_position = self.binding.state().get("position")

        if current_position and signal["price"]:
            scalp_reason = self.scalping_manager.exit_signal(
                current_position,
                signal["price"]
            )

            if scalp_reason:
                result = self.binding.paper_trader.sell(
                    price=signal["price"],
                    exit_reason=scalp_reason
                )
                print(f"[SCALPER EXIT] {signal['symbol']} PRICE:{signal['price']} REASON:{scalp_reason}")
                return result

            reason = self.tp_sl.check(
                current_position,
                signal["price"]
            )

            if reason:
                result = self.binding.paper_trader.sell(
                    price=signal["price"],
                    exit_reason=reason
                )
                print(f"[TP/SL EXIT] {signal['symbol']} PRICE:{signal['price']} REASON:{reason}")
                return result

            return self._position_report(
                current_position,
                signal["price"]
            )

        if signal["signal"] == "BUY":
            if self.scalper.can_trade():
                result = self.binding.execute(signal)
                self.scalper.register_trade()
                print(f"[SCALPER ENTRY] {signal['symbol']} PRICE:{signal['price']}")
                return result

            return {
                "status": "SCALP_COOLDOWN"
            }

        return {
            "status": "WAIT"
        }

    def get_state(self):
        return self.binding.state()
