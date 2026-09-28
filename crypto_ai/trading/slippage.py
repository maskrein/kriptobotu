
def apply_slippage(price, rate=0.0005, side="BUY"):
    if side == "BUY":
        return price * (1 + rate)
    return price * (1 - rate)
