# V7.13.2_INTELLIGENCE_CONNECTED
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.price_engine import get_prices
from performance.paper_performance import get_performance
from runtime.live_state import load_state
from ai.decision_layer import build_decision_layer
from app.learning_memory_card import build_learning_memory
from trading.paper_trader import PaperTrader
from runtime.paper_shared_state import load_paper_state
from trading.paper_state_bridge import calculate_paper_account

paper_trader = PaperTrader()


def get_paper_performance_live(state):
    history = state.get("history", [])
    if not history:
        return {
            "gross_pnl": 0,
            "commission": 0,
            "slippage": 0,
            "net_pnl": 0
        }

    trade = history[-1]
    return {
        "gross_pnl": trade.get("gross_pnl", 0),
        "commission": trade.get("commission", 0),
        "slippage": trade.get("slippage", 0),
        "net_pnl": trade.get("net_pnl", trade.get("pnl", 0))
    }


app = FastAPI(title="CRYPTO AI V7.13.2 AI MEMORY ANALYTICS DASHBOARD")


# V7.16.1_PAPER_TRADING_CARD
def build_paper_trading_card():
    try:
        state = load_paper_state()
    except Exception:
        state = paper_trader.state()
    pos = state.get('position')
    return {
        'balance': state.get('balance', 0),
        'position': pos,
        'trades': len(state.get('history', [])),
        'history': state.get('history', []),
        'account': calculate_paper_account(
            state,
            current_price=(
                get_prices().get('BTCUSDT', {}).get('price', 0)
                if get_prices().get('BTCUSDT')
                else 0
            )
        )
    }


# V7.22.1 TRADE EXECUTION PAYLOAD
def get_trade_execution_payload(paper):
    paper = paper or {}
    position = paper.get("position")
    history = paper.get("history", [])
    last = history[-1] if history else {}

    # Open position takes priority over closed history
    if position:
        symbol = position.get("symbol", "-")
        entry = position.get("entry", "-")
        qty = position.get("quantity", 0)

        current = "-"
        try:
            current = get_prices().get(symbol, {}).get("price", "-")
        except Exception:
            pass

        live_pnl = 0
        try:
            if current != "-":
                live_pnl = round((float(current) - float(entry)) * float(qty), 4)
        except Exception:
            pass

        return {
            "status": "OPEN",
            "side": position.get("side", "LONG"),
            "symbol": symbol,
            "entry": entry,
            "exit": "-",
            "current": current,
            "live_pnl": live_pnl,
            "gross_pnl": 0,
            "commission": 0,
            "slippage": 0,
            "net_pnl": 0,
            "result": "RUNNING"
        }

    net = last.get("net_pnl", last.get("pnl", 0)) if last else 0

    return {
        "status": "CLOSED" if last else "-",
        "side": last.get("side", "-") if last else "-",
        "symbol": last.get("symbol", "-") if last else "-",
        "entry": last.get("entry", "-") if last else "-",
        "exit": last.get("exit", "-") if last else "-",
        "current": "-",
        "live_pnl": 0,
        "gross_pnl": last.get("gross_pnl", last.get("pnl", 0)) if last else 0,
        "commission": last.get("commission", 0) if last else 0,
        "slippage": last.get("slippage", 0) if last else 0,
        "net_pnl": net,
        "result": "WIN" if net > 0 else ("LOSS" if net < 0 else "-")
    }



@app.get("/api/paper")
def paper():
    return build_paper_trading_card()

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
        "ai_learning_memory": build_learning_memory(ai_history),
        "paper": build_paper_trading_card(),
        "trade_execution": get_trade_execution_payload(build_paper_trading_card()),
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
<title>CRYPTO AI LIVE PAPER TRADING V7.13.2</title>
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
.pnl-positive{color:#00d084!important}.pnl-negative{color:#ff4d4f!important}
.side-long{color:#00c853}.side-short{color:#ff1744}</style>
<!-- V7.13.2_CLEAN_MEMORY_STYLE -->
<style>
#history { display:block; overflow-x:auto; white-space:nowrap; font-size:12px; }
#history th { padding:8px; }
#history td { padding:8px; max-width:260px; }
</style>
</head>
<body>
<!-- V7.13.2_AI_HISTORY_CONNECTED -->
<h1>CRYPTO AI LIVE PAPER TRADING V7.13.2</h1>
<div class="card"><h2>💎 ACCOUNT SUMMARY</h2><div class="memory-grid">
<div class="memory-box">BALANCE<h3 id="sum_balance">-</h3></div>
<div class="memory-box">EQUITY<h3 id="sum_equity">-</h3></div>
<div class="memory-box">USED MARGIN<h3 id="sum_margin">-</h3></div>
<div class="memory-box">AVAILABLE<h3 id="sum_available">-</h3></div>
<div class="memory-box">UNREALIZED PNL<h3 id="sum_unrealized">-</h3></div>
</div></div>
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
<div class="card"><h2>🟢 Position</h2>
<div class="memory-grid">
<div class="memory-box">SYMBOL<h3 id="pos_symbol">-</h3></div>
<div class="memory-box">SIDE<h3 id="pos_side">-</h3></div>
<div class="memory-box">ENTRY<h3 id="pos_entry">-</h3></div>
<div class="memory-box">QUANTITY<h3 id="pos_qty">-</h3></div>
<div class="memory-box">STOP LOSS<h3 id="pos_sl">-</h3></div>
<div class="memory-box">TAKE PROFIT<h3 id="pos_tp">-</h3></div>
<div class="memory-box">CURRENT PRICE<h3 id="pos_current">-</h3></div>
<div class="memory-box">UNREALIZED PNL<h3 id="pos_unrealized">-</h3></div>
<div class="memory-box">ROI %<h3 id="pos_roi">-</h3></div>
<div class="memory-box">MARGIN<h3 id="pos_margin">-</h3></div>
</div></div>
<div class="card"><h2>📄 Trades</h2><div id="trades"></div></div>
<div class="card"><h2>🧠 AI Memory Analytics</h2><div class="memory-grid">
<div class="memory-box">TOTAL DECISIONS<h3 id="mem_total">-</h3></div>
<div class="memory-box">BUY<h3 id="mem_buy">-</h3></div>
<div class="memory-box">SELL<h3 id="mem_sell">-</h3></div>
<div class="memory-box">WAIT<h3 id="mem_wait">-</h3></div>
<div class="memory-box">AVG SCORE<h3 id="mem_avg">-</h3></div>
</div></div>\n<div class="card"><h2>💰 Paper Futures Account</h2><div class="memory-grid">
<div class="memory-box">WALLET BALANCE<h3 id="pf_wallet">-</h3></div>
<div class="memory-box">AVAILABLE<h3 id="pf_available">-</h3></div>
<div class="memory-box">POSITION VALUE<h3 id="pf_position_value">-</h3></div>
<div class="memory-box">ENTRY PRICE<h3 id="pf_entry">-</h3></div>
<div class="memory-box">CURRENT PRICE<h3 id="pf_current">-</h3></div>
<div class="memory-box">UNREALIZED PNL<h3 id="pf_unrealized">-</h3></div>
<div class="memory-box">REALIZED PNL<h3 id="pf_realized">-</h3></div>
<div class="memory-box">EQUITY<h3 id="pf_equity">-</h3></div>
</div></div>
<div class="card"><h2>🧠 AI Learning Memory</h2><div class="memory-grid">
<div class="memory-box">STATUS<h3 id="learn_status">-</h3></div>
<div class="memory-box">SAMPLES<h3 id="learn_samples">-</h3></div>
<div class="memory-box">BUY<h3 id="learn_buy">-</h3></div>
<div class="memory-box">SELL<h3 id="learn_sell">-</h3></div>
<div class="memory-box">WAIT<h3 id="learn_wait">-</h3></div>
<div class="memory-box">AVG SCORE<h3 id="learn_avg">-</h3></div>
</div></div>
<div class="card"><h2>🧠 AI History</h2>
<table id="history" style="width:100%;text-align:left"><tr><th>Time</th><th>Symbol</th><th>Signal</th><th>Confidence</th><th>Score</th><th>Momentum</th><th>Trend</th><th>Volume</th><th>Volatility</th><th>Risk</th><th>Reason</th><th>AI Explanation</th><th>Price</th><th>Change</th></tr></table></div>
<style>
.memory-grid{display:flex;gap:15px;flex-wrap:wrap}
.memory-box{background:#222;padding:15px;border-radius:12px;min-width:120px}
.memory-box h3{margin:8px 0 0}
#history{display:block;overflow-x:auto;white-space:nowrap}
</style>
<!-- V7.21.3_AI_TRADE_EXECUTION_CARD -->
<div class="card">
<h2>🤖 AI TRADE EXECUTION</h2>
<div class="memory-grid">
<div class="memory-box">STATUS<h3 id="trade_status">-</h3></div>
<div class="memory-box">SIDE<h3 id="trade_side">-</h3></div>
<div class="memory-box">SYMBOL<h3 id="trade_symbol">-</h3></div>
<div class="memory-box">ENTRY<h3 id="trade_entry">-</h3></div>
<div class="memory-box">EXIT<h3 id="trade_exit">-</h3></div>
<div class="memory-box">CURRENT<h3 id="trade_current">-</h3></div>
<div class="memory-box">LIVE PNL<h3 id="trade_live_pnl">-</h3></div>
<div class="memory-box">GROSS PNL<h3 id="trade_gross">-</h3></div>
<div class="memory-box">NET PNL<h3 id="trade_net">-</h3></div>
<div class="memory-box">RESULT<h3 id="trade_result">-</h3></div>
<div class="memory-box">AI CONFIDENCE<h3 id="trade_confidence">-</h3></div>
</div>
</div>

<script>
function setPnlColor(id,value){
 const el=document.getElementById(id);
 if(!el) return;
 el.innerText=value;
 const n=parseFloat(value);
 el.className = n>0 ? 'pnl-positive' : (n<0 ? 'pnl-negative' : '');
}
async function refresh(){
 const r=await fetch('/api/live');
 const d=await r.json();
 document.getElementById('balance').innerText=d.balance;
 document.getElementById('signal').innerText=d.decision.signal;
 document.getElementById('confidence').innerText=d.decision.confidence+'%';
 setPnlColor('pnl',d.performance.net_pnl);
 document.getElementById('ai_score').innerText=d.ai_score+'/100';
 document.getElementById('market_mood').innerText=d.market_mood;
 document.getElementById('risk_level').innerText=d.risk_level;
 document.getElementById('decision_explanation').innerText=d.decision_explanation;
 document.getElementById('momentum_score').innerText=d.ai_intelligence.momentum_score+'/25';
 document.getElementById('trend_score').innerText=d.ai_intelligence.trend_score+'/20';
 document.getElementById('volume_score').innerText=d.ai_intelligence.volume_score+'/15';
 document.getElementById('volatility_score').innerText=d.ai_intelligence.volatility_score+'/10';
 document.getElementById('ai_explanation').innerText=d.ai_intelligence.ai_explanation;
 const pos=d.position || {};
 document.getElementById('pos_symbol').innerText=pos.symbol || '-';
 document.getElementById('pos_side').innerText=pos.side || 'LONG';
 document.getElementById('pos_entry').innerText=pos.entry || '-';
 document.getElementById('pos_qty').innerText=pos.quantity || '-';
 document.getElementById('pos_sl').innerText=pos.sl || '-';
 document.getElementById('pos_tp').innerText=pos.tp || '-';
 const paper=d.paper || {};
 const pa = paper.account || {};
 const paperAccount = pa || d.paper_account || {};
 document.getElementById('pos_current').innerText = paperAccount.current_price || d.market?.BTCUSDT?.price || '-';
 setPnlColor('pos_unrealized',paperAccount.unrealized_pnl ?? '-');
 document.getElementById('pos_margin').innerText = paperAccount.position_value ?? '-';
 const roi = paperAccount.position_value ? ((paperAccount.unrealized_pnl || 0) / paperAccount.position_value * 100) : 0;
 document.getElementById('pos_roi').innerText = roi.toFixed(2)+'%';

 const trades=d.trades || [];
 document.getElementById('trades').innerHTML = trades.map(t =>
 `<div class="memory-box"> ${t.action || '-'} ${t.symbol || ''}<br>Entry: ${t.entry || '-'}<br>Quantity: ${t.quantity || '-'}</div>`
 ).join('');
 const ms=d.ai_memory_stats || {};
 document.getElementById('mem_total').innerText = ms.total ?? 0;
 document.getElementById('mem_buy').innerText = ms.buy ?? 0;
 document.getElementById('mem_sell').innerText = ms.sell ?? 0;
 document.getElementById('mem_wait').innerText = ms.wait ?? 0;
 document.getElementById('mem_avg').innerText = ms.avg_score ?? 0;

 document.getElementById('sum_balance').innerText=d.balance ?? '-';
document.getElementById('sum_equity').innerText=pa.equity ?? d.balance ?? '-';
document.getElementById('sum_margin').innerText=pa.position_value ?? '-';
document.getElementById('sum_available').innerText=pa.available_balance ?? '-';
setPnlColor('sum_unrealized',pa.unrealized_pnl ?? 0);

document.getElementById('pf_wallet').innerText = (pa.wallet_balance ?? 0).toFixed ? pa.wallet_balance.toFixed(2) : pa.wallet_balance;
document.getElementById('pf_available').innerText = (pa.available_balance ?? 0).toFixed ? pa.available_balance.toFixed(2) : pa.available_balance;
document.getElementById('pf_position_value').innerText = (pa.position_value ?? 0).toFixed ? pa.position_value.toFixed(2) : pa.position_value;
document.getElementById('pf_entry').innerText = paper.position?.entry ?? '-';
document.getElementById('pf_current').innerText = d.market?.BTCUSDT?.price ?? '-';
setPnlColor('pf_unrealized',(pa.unrealized_pnl ?? 0).toFixed ? pa.unrealized_pnl.toFixed(4) : pa.unrealized_pnl);
document.getElementById('pf_realized').innerText = (pa.realized_pnl ?? 0).toFixed ? pa.realized_pnl.toFixed(4) : pa.realized_pnl;
document.getElementById('pf_equity').innerText = (pa.equity ?? 0).toFixed ? pa.equity.toFixed(2) : pa.equity;

 const lm=d.ai_learning_memory || {};
 const te=d.trade_execution || {};
 const livePosition = (d.paper && d.paper.position) || d.position || null;
 const tradeSide=(livePosition || te).side || '-';
 document.getElementById('trade_side').innerText = tradeSide;
 document.getElementById('trade_side').className = tradeSide === 'LONG' ? 'side-long' : (tradeSide === 'SHORT' ? 'side-short' : '');

 document.getElementById('trade_status').innerText = livePosition ? 'OPEN' : (te.status || '-');
 document.getElementById('trade_symbol').innerText = (livePosition || te).symbol || '-';
 document.getElementById('trade_entry').innerText = (livePosition || te).entry || '-';
 document.getElementById('trade_current').innerText = d.market?.BTCUSDT?.price || '-';
 setPnlColor('trade_live_pnl',paperAccount.unrealized_pnl ?? '-');
 document.getElementById('trade_exit').innerText = livePosition ? '-' : (te.exit || '-');
 document.getElementById('trade_gross').innerText = te.gross_pnl || 0;
 document.getElementById('trade_net').innerText = te.net_pnl || 0;
 document.getElementById('trade_result').innerText = livePosition ? 'RUNNING' : (te.result || '-');
 document.getElementById('trade_confidence').innerText = d.confidence || d.decision?.confidence || '-';
 document.getElementById('learn_status').innerText = lm.status || '-';
 document.getElementById('learn_samples').innerText = lm.samples ?? 0;
 document.getElementById('learn_buy').innerText = lm.buy ?? 0;
 document.getElementById('learn_sell').innerText = lm.sell ?? 0;
 document.getElementById('learn_wait').innerText = lm.wait ?? 0;
 document.getElementById('learn_avg').innerText = lm.avg_score ?? 0;


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


# V7.19.3 DASHBOARD COST CARD HELPERS

def get_paper_cost_performance(state):
    history = state.get("history", []) if state else []
    return {
        "gross_pnl": round(sum(x.get("gross_pnl", 0) for x in history), 4),
        "commission": round(sum(x.get("commission", 0) for x in history), 4),
        "slippage": round(sum(x.get("slippage", 0) for x in history), 4),
        "net_pnl": round(sum(x.get("net_pnl", x.get("pnl", 0)) for x in history), 4)
    }

