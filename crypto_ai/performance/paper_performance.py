
from runtime.live_state import load_state
def get_performance():
    s=load_state()
    return {
        "balance": s.get("balance",10000),
        "gross_pnl": s.get("gross_pnl",0),
        "fees": s.get("fees",0),
        "slippage": s.get("slippage",0),
        "net_pnl": s.get("net_pnl",0),
        "position": s.get("position",{}),
        "trades": s.get("trades",[]),
        "history": s.get("ai_history",[])
    }
