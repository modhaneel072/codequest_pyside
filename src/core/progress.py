# -*- coding: utf-8 -*-
from pathlib import Path
from src.core.io import load_json, write_json

PROGRESS_PATH = Path("src/data/progress.json")

DEFAULT_PROGRESS = {
  "last_route": "boot",
  "unlocked_module": 1,
  "completed": {"lessons": [], "quizzes": [], "debugs": [], "problemsets": [], "hackathons": []},
  "hackathons_unlock_after_module": 3
}

def load_progress():
    if not PROGRESS_PATH.exists():
        write_json(PROGRESS_PATH.as_posix(), DEFAULT_PROGRESS)
    return load_json(PROGRESS_PATH.as_posix())

def save_progress(data: dict):
    write_json(PROGRESS_PATH.as_posix(), data)

def set_last_route(route: str):
    p = load_progress()
    p["last_route"] = route
    save_progress(p)

def mark_completed(kind: str, id_: str):
    p = load_progress()
    p["completed"].setdefault(kind, [])
    if id_ not in p["completed"][kind]:
        p["completed"][kind].append(id_)
    save_progress(p)

def unlock_next_module(current_module: int):
    p = load_progress()
    if p.get("unlocked_module", 1) <= current_module:
        p["unlocked_module"] = current_module + 1
    save_progress(p)

def hackathons_unlocked() -> bool:
    p = load_progress()
    return p.get("unlocked_module", 1) > p.get("hackathons_unlock_after_module", 3)
