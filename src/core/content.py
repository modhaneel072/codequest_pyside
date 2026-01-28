# -*- coding: utf-8 -*-
import json
from pathlib import Path

def load_lesson(path: str) -> str:
    # ALWAYS read as UTF-8 to avoid ÂƒÂ¢Â€Â‹ issues
    return Path(path).read_text(encoding="utf-8-sig")

def load_problem(problem_id: str, base_dir: str = "src/data/problems") -> dict:
    p = Path(base_dir) / f"{problem_id}.json"
    return json.loads(p.read_text(encoding="utf-8-sig"))

