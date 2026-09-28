class TPSLManager:

    def __init__(
        self,
        tp_percent=0.0035,
        sl_percent=0.002,
        trailing_trigger=0.01,
        trailing_distance=0.005
    ):
        self.tp_percent = tp_percent
        self.sl_percent = sl_percent
        self.trailing_trigger = trailing_trigger
        self.trailing_distance = trailing_distance


    def apply(self, position):
        if not position:
            return position

        entry = position.get("entry", 0)
        side = position.get("side", "LONG")

        if side == "LONG":
            position["tp"] = round(
                entry * (1 + self.tp_percent),
                2
            )

            position["sl"] = round(
                entry * (1 - self.sl_percent),
                2
            )

        return position


    def update_trailing_stop(self, position, price):
        if not position:
            return position

        entry = position.get("entry", 0)
        side = position.get("side", "LONG")

        if side != "LONG":
            return position

        profit = (price - entry) / entry

        if profit >= self.trailing_trigger:
            new_sl = round(
                price * (1 - self.trailing_distance),
                2
            )

            old_sl = position.get("sl", 0)

            if new_sl > old_sl:
                position["sl"] = new_sl
                position["trailing_active"] = True

        return position


    def check(self, position, price):
        if not position:
            return None

        if price >= position.get(
            "tp",
            float("inf")
        ):
            return "TAKE_PROFIT"

        if price <= position.get(
            "sl",
            0
        ):
            return "STOP_LOSS"

        return None
