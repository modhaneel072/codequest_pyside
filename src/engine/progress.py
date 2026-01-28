from datetime import datetime

def record_attempt(progress: dict, module_index: int, score: int) -> None:
    progress.setdefault("history", []).append({
        "module_index": module_index,
        "score": score,
        "ts": datetime.now().isoformat(timespec="seconds")
    })

def unlock_after_pass(progress: dict, module_index: int) -> None:
    # unlock more terminal commands as the user passes modules
    unlocked = progress.setdefault("terminal_unlocked", {"commands": ["help", "status"]})
    cmds = set(unlocked.get("commands", []))

    if module_index >= 0:
        cmds.update(["ls", "cat"])
    if module_index >= 1:
        cmds.update(["cd", "run"])
    unlocked["commands"] = sorted(cmds)

    progress["module_index"] = module_index + 1