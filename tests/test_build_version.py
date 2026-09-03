"""Failing-first check: build.py prints its version via --version."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "build.py"), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_build_prints_version() -> None:
    proc = run("--version")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() != ""


def test_check_still_passes() -> None:
    proc = run("--check")
    assert proc.returncode == 0, proc.stderr
    assert "passed validation" in proc.stdout


if __name__ == "__main__":
    test_build_prints_version()
    test_check_still_passes()
    print("ok: build version tests passed")
