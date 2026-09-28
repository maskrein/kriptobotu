import json
from pathlib import Path

STATE_FILE = Path('runtime/paper_shared_state.json')


def save_paper_state(state):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')


def load_paper_state():
    if not STATE_FILE.exists():
        return {
            'balance': 10000,
            'position': None,
            'history': []
        }

    return json.loads(STATE_FILE.read_text(encoding='utf-8'))
