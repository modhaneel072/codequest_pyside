# -*- coding: utf-8 -*-
import io, contextlib, traceback

def run_code_capture_stdout(code: str):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {})
        return True, buf.getvalue()
    except Exception:
        return False, buf.getvalue() + "\n" + traceback.format_exc()

def grade_problem(code: str, spec: dict):
    env = {}
    try:
        exec(code, {}, env)
    except Exception as e:
        return False, f"❌ Your code crashed before tests ran:\n{e}"

    fn_name = spec.get("function")
    if fn_name and fn_name not in env:
        return False, f"❌ Missing required function: {fn_name}()"

    func = env.get(fn_name) if fn_name else None

    # Optional: forbid early features (simple keyword checks)
    forbidden = spec.get("forbidden_keywords", [])
    lowered = code.lower()
    for kw in forbidden:
        if kw.lower() in lowered:
            return False, f"❌ This problem forbids using: {kw}"

    tests = spec.get("tests", [])
    for t in tests:
        inp = t.get("input")
        expected = t.get("expected")
        try:
            out = func(*inp) if isinstance(inp, (list, tuple)) else func(inp)
        except Exception as e:
            return False, f"❌ Failed on input {inp}. Error: {e}"
        if out != expected:
            return False, f"❌ Failed on input {inp}. Expected {expected}, got {out}"

    return True, "✅ All tests passed!"
