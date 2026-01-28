# -*- coding: utf-8 -*-
import json
from pathlib import Path

def read_text_utf8(path: str) -> str:
    return Path(path).read_text(encoding="utf-8-sig")

def load_json(path: str) -> dict:
    return json.loads(read_text_utf8(path))

def write_json(path: str, data: dict):
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
