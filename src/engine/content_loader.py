import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load_course() -> dict:
    p = DATA / "course.json"
    return json.loads(p.read_text(encoding="utf-8-sig"))

def load_progress() -> dict:
    p = DATA / "progress.json"
    if not p.exists():
        return {"module_index": 0, "history": [], "terminal_unlocked": {"commands": ["help", "status"]}}
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return {"module_index": 0, "history": [], "terminal_unlocked": {"commands": ["help", "status"]}}

def save_progress(progress: dict) -> None:
    p = DATA / "progress.json"
    p.write_text(json.dumps(progress, indent=2), encoding="utf-8")