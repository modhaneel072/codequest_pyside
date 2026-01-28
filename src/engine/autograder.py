from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from .runner import run_python

@dataclass
class GradeResult:
    passed: bool
    score: int
    feedback: str
    stdout: str
    stderr: str

def _norm(s: str) -> str:
    return s.replace("\r\n", "\n")

def grade_code(challenge: Dict[str, Any], code: str) -> GradeResult:
    """
    Simple safe autograder:
    - runs code
    - checks tests
    Supported tests:
      {"type":"stdout_exact","value":"..."}
      {"type":"stdout_contains","value":"..."}
      {"type":"exit_code","value":0}
    """
    res = run_python(code, timeout_sec=float(challenge.get("timeout_sec", 2.0)))
    stdout = res.stdout or ""
    stderr = res.stderr or ""

    tests = challenge.get("tests", [])
    if not tests:
        # If no tests provided, require no crash
        passed = (res.exit_code == 0)
        return GradeResult(passed=passed, score=(100 if passed else 0),
                           feedback=("No tests configured. Code must run without errors." if passed else "Your code crashed."),
                           stdout=stdout, stderr=stderr)

    total = len(tests)
    ok = 0
    msgs: List[str] = []

    for t in tests:
        ttype = t.get("type")
        val = t.get("value", "")
        if ttype == "stdout_exact":
            if _norm(stdout) == _norm(str(val)):
                ok += 1
            else:
                msgs.append(f"Expected exact output: {repr(val)}; got: {repr(stdout)}")
        elif ttype == "stdout_contains":
            if str(val) in stdout:
                ok += 1
            else:
                msgs.append(f"Expected output to contain: {repr(val)}")
        elif ttype == "exit_code":
            if res.exit_code == int(val):
                ok += 1
            else:
                msgs.append(f"Expected exit code {val}, got {res.exit_code}")
        else:
            msgs.append(f"Unknown test type: {ttype}")

    score = int(round((ok / total) * 100))
    passed = score >= int(challenge.get("pass_score", 90))

    feedback = f"Passed {ok}/{total} tests. Score={score}%."
    if msgs:
        feedback += "\n\nIssues:\n- " + "\n- ".join(msgs)

    # If code crashed, ensure fail
    if res.exit_code != 0:
        passed = False
        if "crash" not in feedback.lower():
            feedback += f"\n\nYour code crashed (exit code {res.exit_code})."

    return GradeResult(passed=passed, score=score, feedback=feedback, stdout=stdout, stderr=stderr)