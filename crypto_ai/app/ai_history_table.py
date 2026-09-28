from runtime.live_state import load_state


def ai_history_html():
    state = load_state()
    history = state.get("ai_history", [])

    rows = ""
    for item in reversed(history[-20:]):
        signal = item.get("signal", "WAIT")
        emoji = "🟢" if signal == "BUY" else ("🔴" if signal == "SELL" else "🟡")

        rows += f"""
        <tr>
            <td>{item.get('time','')}</td>
            <td>{item.get('symbol','')}</td>
            <td>{emoji} {signal}</td>
            <td>{item.get('confidence',0)}%</td>
            <td>{item.get('ai_score',0)}</td>
            <td>{item.get('momentum_score',0)}/{25}</td>
            <td>{item.get('trend_score',0)}/{20}</td>
            <td>{item.get('volume_score',0)}/{15}</td>
            <td>{item.get('volatility_score',0)}/{10}</td>
            <td>{item.get('risk_level','')}</td>
            <td>{item.get('reason_text', item.get('reason',''))}</td>
            <td>{item.get('ai_explanation','')}</td>
            <td>{item.get('price',0)}</td>
            <td>{item.get('change','')}</td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='14'>No AI decisions yet</td></tr>"

    return f"""
    <div class='card'>
    <h2>🧠 AI History</h2>
    <table>
    <tr>
      <th>Time</th>
      <th>Symbol</th>
      <th>Signal</th>
      <th>Confidence</th>
      <th>Score</th>
      <th>Momentum</th>
      <th>Trend</th>
      <th>Volume</th>
      <th>Volatility</th>
      <th>Risk</th>
      <th>Reason</th>
      <th>AI Explanation</th>
      <th>Price</th>
      <th>Change</th>
    </tr>
    {rows}
    </table>
    </div>
    """