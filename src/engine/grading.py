def grade_quiz(quiz: dict, answers: dict) -> tuple[int, dict]:
    """
    Policy: 2 MCQ + 1 FRQ, total 100.
      - each MCQ = 40 pts (80 total)
      - FRQ = 20 pts

    FRQ grading:
      - keyword rubric (partial credit)
      - AND must contain a valid fix line if expected_fix_contains is provided
    """
    points = 0
    detail = {"mcq": [], "frq": {"points": 0, "matched": [], "fix_ok": False}}

    mcq_items = quiz.get("mcq", [])
    chosen = answers.get("mcq", [])

    for i, q in enumerate(mcq_items):
        corr = int(q.get("correct_index", 0))
        pick = chosen[i] if i < len(chosen) else None
        ok = (pick == corr)
        earned = 40 if ok else 0
        points += earned
        detail["mcq"].append({"ok": ok, "earned": earned, "picked": pick, "correct": corr})

    frq = quiz.get("frq", {})
    txt = (answers.get("frq", "") or "").lower().strip()

    # keyword partial credit
    keywords = [k.lower() for k in frq.get("keywords", [])]
    matched = [k for k in keywords if k in txt]
    detail["frq"]["matched"] = matched

    base = 0
    if keywords:
        ratio = len(matched) / max(1, len(keywords))
        base = int(round(20 * ratio))
    else:
        base = 20 if len(txt) >= 20 else 0

    # fix requirement (must include one acceptable fix string)
    expected_fix = [s.lower() for s in frq.get("expected_fix_contains", [])]
    fix_ok = True
    if expected_fix:
        fix_ok = any(s in txt for s in expected_fix)

    detail["frq"]["fix_ok"] = fix_ok

    if expected_fix and not fix_ok:
        # If they didn't provide a fix, cap FRQ to 0 (strict, as requested)
        earned = 0
    else:
        earned = base

    detail["frq"]["points"] = earned
    points += earned

    return points, detail

def passed(score: int) -> bool:
    return score >= 90