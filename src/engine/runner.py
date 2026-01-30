"""Python code execution runner with timeout and error handling."""

from __future__ import annotations

import logging
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RunResult:
    """Result of running Python code."""
    ok: bool
    stdout: str
    stderr: str
    exit_code: int

    def __str__(self) -> str:
        """String representation of result."""
        return f"RunResult(ok={self.ok}, exit_code={self.exit_code}, stdout_len={len(self.stdout)}, stderr_len={len(self.stderr)})"


def run_python(code: str, timeout_sec: float = 2.0) -> RunResult:
    """
    Run user code in a temporary file using the current interpreter.
    Captures stdout/stderr. Hard timeout to avoid infinite loops.
    
    Args:
        code: Python code to execute
        timeout_sec: Timeout in seconds (default: 2.0)
        
    Returns:
        RunResult with execution status and output
    """
    if not code or not isinstance(code, str):
        logger.error(f"Invalid code: {type(code)}")
        return RunResult(
            ok=False,
            stdout="",
            stderr="Error: No valid code provided",
            exit_code=1
        )
    
    temp_path: Optional[str] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_path = f.name
        
        logger.debug(f"Running code with timeout {timeout_sec}s")
        p = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        
        result = RunResult(
            ok=(p.returncode == 0),
            stdout=p.stdout or "",
            stderr=p.stderr or "",
            exit_code=p.returncode,
        )
        logger.info(f"Code execution completed: {result}")
        return result
        
    except subprocess.TimeoutExpired as e:
        logger.warning(f"Code execution timed out after {timeout_sec}s")
        return RunResult(
            ok=False,
            stdout=(e.stdout or ""),
            stderr="Timeout: your code took too long (possible infinite loop).\n",
            exit_code=124,
        )
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        return RunResult(
            ok=False,
            stdout="",
            stderr=f"Error: {str(e)}",
            exit_code=1,
        )
    finally:
        # Clean up temporary file
        if temp_path:
            try:
                Path(temp_path).unlink()
            except Exception as e:
                logger.warning(f"Could not delete temp file {temp_path}: {e}")