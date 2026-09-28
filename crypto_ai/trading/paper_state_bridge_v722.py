from trading.paper_state_store import load_state, save_state

def sync_paper_state(paper_state):
    save_state(paper_state)
    return load_state()
