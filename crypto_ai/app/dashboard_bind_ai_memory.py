from runtime.live_state import load_state


def get_ai_memory_html():
    state = load_state()
    history = state.get("ai_history", [])

    rows = ""
    for item in reversed(history[-20:]):
        signal = item.get("signal", "WAIT")
        icon = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"

        rows += f"""
        <tr>
          <td>{item.get('time','')}</td>
          <td>{item.get('symbol','')}</td>
          <td>{icon} {signal}</td>
          <td>{item.get('confidence',0)}%</td>
          <td>{item.get('price',0)}</td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='5'>No AI decisions</td></tr>"

    return f"""
    <div class="card">
      <h2>🧠 AI MEMORY</h2>
      <table>
        <tr>
          <th>TIME</th>
          <th>SYMBOL</th>
          <th>SIGNAL</th>
          <th>CONF</th>
          <th>PRICE</th>
        </tr>
        {rows}
      </table>
    </div>
    """