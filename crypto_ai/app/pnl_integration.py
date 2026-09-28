from app.pnl_hook import update_pnl

def apply_pnl_update(response_data, market):
    try:
        return update_pnl(response_data, market)
    except Exception:
        return response_data
