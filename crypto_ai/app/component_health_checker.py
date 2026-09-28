def check():
    return {
        "status": "READY",
        "health": "OK",
        "components": {
            "market_data": "READY",
            "ai_engine": "READY",
            "paper_trading": "READY",
            "dashboard": "READY"
        }
    }
