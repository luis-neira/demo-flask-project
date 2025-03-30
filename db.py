from pathlib import Path
import json


def init_db():
    raw_data = Path("data.json").read_text()
    store = json.loads(raw_data)
    return store


store = init_db()
