import json
from pathlib import Path

STATE_FILE = Path('paper_state.json')

DEFAULT_STATE = {
    'balance': 10000,
    'position': None,
    'history': []
}

def load_state():
    if not STATE_FILE.exists():
        return DEFAULT_STATE.copy()
    return json.loads(STATE_FILE.read_text(encoding='utf-8'))

def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, indent=2),
        encoding='utf-8'
    )
    return state

def update_history(trade):
    state = load_state()
    state.setdefault('history', []).append(trade)
    save_state(state)
    return state
