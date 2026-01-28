# -*- coding: utf-8 -*-
import traceback

def run_debug(spec: dict, code: str):
    """
    spec fields:
      - required_function (optional)
      - tests: [{"input":[...], "expected": ...}, ...]
      - mode: "return" (expects function return)
    """
    env = {}
    try:
        exec(code, {}, env)
    except Exception:
        return False, "❌ Crash while running your code:\n" + traceback.format_exc()

    fn = spec.get("required_function")
    if fn and fn not in env:
        return False, f"❌ Missing required function: {fn}()"

    func = env.get(fn) if fn else None
    tests = spec.get("tests", [])
    mode = spec.get("mode", "return")

    for t in tests:
        inp = t.get("input", [])
        expected = t.get("expected")
        try:
            if mode == "return" and func:
                out = func(*inp)
            else:
                return False, "❌ Debug spec misconfigured."
        except Exception as e:
            return False, f"❌ Failed on input {inp}. Error: {e}"
        if out != expected:
            return False, f"❌ Failed on input {inp}. Expected {expected}, got {out}"

    return True, "✅ Debug mission passed!"
