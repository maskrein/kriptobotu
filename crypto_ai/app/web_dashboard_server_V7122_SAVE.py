# V7.13.2_INTELLIGENCE_CONNECTED
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.price_engine import get_prices
from performance.paper_performance import get_performance
from runtime.live_state import load_state
from ai.decision_layer import build_decision_layer

app = FastAPI(title="CRYPTO AI V7.12.2 AI MEMORY ANALYTICS DASHBOARD")

@app.get("/api/live")
def live():
    perf = get_performance()
    prices = get_prices()

    state = load_state()
    ai_history = state.get("ai_history", [])
    recent = ai_history[-10:]
    buy_count = sum(1 for x in recent if x.get("signal") == "BUY")
    sell_count = sum(1 for x in recent if x.get("signal") == "SELL")
    ai_trend = "BUY" if buy_count > sell_count else ("SELL" if sell_count > buy_count else "NEUTRAL")

    if ai_history:
        decision = ai_history[-1]
    else:
        decision = {
            "symbol": None,
            "signal": "WAIT",
            "confidence": 0,
            "reason": ["No AI decision yet"],
            "time": ""
        }

    decision.update(build_decision_layer(decision))

    return {
        "market": prices,
        "decision": decision,
        "balance": perf.get("balance", 10000),
        "performance": {
            "gross_pnl": perf.get("gross_pnl", 0),
            "fees": perf.get("fees", 0),
            "slippage": perf.get("slippage", 0),
            "net_pnl": perf.get("net_pnl", 0)
        },
        "position": perf.get("position", {}),
        "trades": perf.get("trades", []),
        "history": perf.get("history", []),
        "ai_history": ai_history,
        "ai_memory_stats": {
            "total": len(ai_history),
            "buy": len([x for x in ai_history if x.get("signal") == "BUY"]),
            "sell": len([x for x in ai_history if x.get("signal") == "SELL"]),
            "wait": len([x for x in ai_history if x.get("signal") == "WAIT"]),
            "avg_score": round(sum([float(x.get("score", x.get("ai_score",0))) for x in ai_history]) / len(ai_history), 2) if ai_history else 0
        },
        "ai_trend": ai_trend,
        "decision_metrics": {"buy_count": buy_count, "sell_count": sell_count},
        "ai_score": decision.get("ai_score", 0),
        "ai_intelligence": {
            "momentum_score": decision.get("momentum_score", 0),
            "trend_score": decision.get("trend_score", 0),
            "volume_score": decision.get("volume_score", 0),
            "volatility_score": decision.get("volatility_score", 0),
            "ai_explanation": decision.get("ai_explanation", "")
        },
        "market_mood": decision.get("market_mood", "Neutral"),
        "risk_level": decision.get("risk_level", "Medium"),
        "decision_explanation": decision.get("decision_explanation", ""),
        "system_version": "V7.13.2",
        "position_metrics": {
            "entry": perf.get("position", {}).get("entry", 0),
            "target": perf.get("position", {}).get("tp", 0),
            "stop": perf.get("position", {}).get("sl", 0)
        }
    }

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
<html>
<head>
<title>CRYPTO AI LIVE PAPER TRADING V7.12.2</title>
<!-- V7.13.2_AI_MEMORY_UI -->
<style>
body{background:#090909;color:white;font-family:Arial;padding:40px}
.card{background:#202020;padding:20px;border-radius:15px;margin:15px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px}
#history{width:100%;border-collapse:collapse;display:block;overflow-x:auto;white-space:nowrap}
#history th{padding:10px;text-align:left;color:#ddd;font-size:13px}
#history td{padding:10px;border-top:1px solid #333;font-size:12px;vertical-align:top}
#history td:nth-child(12){max-width:280px;white-space:normal}
#history tr:hover{background:#292929}
</style>
<!-- V7.12.2_AI_MEMORY_STYLE -->
<style>
#history { display:block; overflow-x:auto; white-space:nowrap; font-size:12px; }
#history th { padding:8px; }
#history td { padding:8px; max-width:260px; }
</style>
</head>
<body>
<!-- V7.13.2_AI_HISTORY_CONNECTED -->
<h1>CRYPTO AI LIVE PAPER TRADING V7.12.2</h1>
<div class="grid">
<div class="card">💰 Balance<h2 id="balance">-</h2></div>
<div class="card">📈 Signal<h2 id="signal">-</h2></div>
<div class="card">🎯 Confidence<h2 id="confidence">-</h2></div>
<div class="card">💎 Net PNL<h2 id="pnl">-</h2></div>
<div class="card">🧠 AI Score<h2 id="ai_score">-</h2></div>
<div class="card">📊 Market Mood<h2 id="market_mood">-</h2></div>
<div class="card">⚠️ Risk<h2 id="risk_level">-</h2></div>
<div class="card">📝 Decision<h2 id="decision_explanation">-</h2></div>
<div class="card">🧠 Momentum<h2 id="momentum_score">-</h2></div>
<div class="card">📈 Trend<h2 id="trend_score">-</h2></div>
<div class="card">📊 Volume<h2 id="volume_score">-</h2></div>
<div class="card">🌊 Volatility<h2 id="volatility_score">-</h2></div>
<div class="card">🤖 AI Explanation<h2 id="ai_explanation">-</h2></div>
</div>
<div class="card"><h2>🟢 Position</h2><pre id="position"></pre></div>
<div class="card"><h2>📄 Trades</h2><pre id="trades"></pre></div>
<div class="card"><h2>🧠 AI Memory Analytics</h2><div class="memory-grid">
<div class="memory-box">TOTAL DECISIONS<h3 id="mem_total">-</h3></div>
<div class="memory-box">BUY<h3 id="mem_buy">-</h3></div>
<div class="memory-box">SELL<h3 id="mem_sell">-</h3></div>
<div class="memory-box">WAIT<h3 id="mem_wait">-</h3></div>
<div class="memory-box">AVG SCORE<h3 id="mem_avg">-</h3></div>
</div></div>\n<div class="card"><h2>🧠 AI History</h2>
<table id="history" style="width:100%;text-align:left"><tr><th>Time</th><th>Symbol</th><th>Signal</th><th>Confidence</th><th>Score</th><th>Momentum</th><th>Trend</th><th>Volume</th><th>Volatility</th><th>Risk</th><th>Reason</th><th>AI Explanation</th><th>Price</th><th>Change</th></tr></table></div>
<style>
.memory-grid{display:flex;gap:15px;flex-wrap:wrap}
.memory-box{background:#222;padding:15px;border-radius:12px;min-width:120px}
.memory-box h3{margin:8px 0 0}
#history{display:block;overflow-x:auto;white-space:nowrap}
</style>
<script>
async function refresh(){
 const r=await fetch('/api/live');
 const d=await r.json();
 document.getElementById('balance').innerText=d.balance;
 document.getElementById('signal').innerText=d.decision.signal;
 document.getElementById('confidence').innerText=d.decision.confidence+'%';
 document.getElementById('pnl').innerText=d.performance.net_pnl;
 document.getElementById('ai_score').innerText=d.ai_score+'/100';
 document.getElementById('market_mood').innerText=d.market_mood;
 document.getElementById('risk_level').innerText=d.risk_level;
 document.getElementById('decision_explanation').innerText=d.decision_explanation;
 document.getElementById('momentum_score').innerText=d.ai_intelligence.momentum_score+'/25';
 document.getElementById('trend_score').innerText=d.ai_intelligence.trend_score+'/20';
 document.getElementById('volume_score').innerText=d.ai_intelligence.volume_score+'/15';
 document.getElementById('volatility_score').innerText=d.ai_intelligence.volatility_score+'/10';
 document.getElementById('ai_explanation').innerText=d.ai_intelligence.ai_explanation;
 document.getElementById('position').innerText=JSON.stringify(d.position,null,2);
 document.getElementById('trades').innerText=JSON.stringify(d.trades,null,2);
 const ms=d.ai_memory_stats || {};
 document.getElementById('mem_total').innerText = ms.total ?? 0;
 document.getElementById('mem_buy').innerText = ms.buy ?? 0;
 document.getElementById('mem_sell').innerText = ms.sell ?? 0;
 document.getElementById('mem_wait').innerText = ms.wait ?? 0;
 document.getElementById('mem_avg').innerText = ms.avg_score ?? 0;


 const h=document.getElementById('history');
h.innerHTML='<tr><th>Time</th><th>Symbol</th><th>Signal</th><th>Confidence</th><th>Score</th><th>Momentum</th><th>Trend</th><th>Volume</th><th>Volatility</th><th>Risk</th><th>Reason</th><th>AI Explanation</th><th>Price</th><th>Change</th></tr>';
(d.ai_history||d.history||[]).slice(-10).reverse().forEach(x=>{
h.innerHTML += `<tr><td>${x.time||''}</td><td>${x.symbol||''}</td><td>${x.signal||''}</td><td>${x.confidence||''}%</td><td>${x.score||x.ai_score||0}</td><td>${x.momentum_score||0}/25</td><td>${x.trend_score||0}/20</td><td>${x.volume_score||0}/15</td><td>${x.volatility_score||0}/10</td><td>${x.risk||x.risk_level||''}</td><td>${Array.isArray(x.reason) ? x.reason.join(', ') : x.reason||''}</td><td>${x.ai_explanation||''}</td><td>${x.price||''}</td><td>${x.change||''}</td></tr>`;
});
}
refresh(); setInterval(refresh,3000);
</script>
</body>
</html>
"""
