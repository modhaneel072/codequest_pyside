from __future__ import annotations
import subprocess
import sys
import tempfile
from dataclasses import dataclass

@dataclass
class RunResult:
    ok: bool
    stdout: str
    stderr: str
    exit_code: int

def run_python(code: str, timeout_sec: float = 2.0) -> RunResult:
    """
    Run user code in a temporary file using the current interpreter.
    Captures stdout/stderr. Hard timeout to avoid infinite loops.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        temp_path = f.name

    try:
        p = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return RunResult(
            ok=(p.returncode == 0),
            stdout=p.stdout or "",
            stderr=p.stderr or "",
            exit_code=p.returncode,
        )
    except subprocess.TimeoutExpired as e:
        return RunResult(
            ok=False,
            stdout=(e.stdout or ""),
            stderr="Timeout: your code took too long (possible infinite loop).\n",
            exit_code=124,
        )