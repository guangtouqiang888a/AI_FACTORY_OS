"""Single verification entry for V2 baseline.

Usage (from repo root):
    python -m tests.verify_v2
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    from app.main import healthcheck
    from database.db import initialize, reset, verify

    print("== V2 runtime health ==")
    msg = healthcheck()
    print(msg)
    if msg != "AI_FACTORY_OS V2 runtime: OK":
        print("FAIL: unexpected health message")
        return 1

    print("== V2 database fresh init ==")
    path = initialize()
    print(f"initialized: {path}")
    info = verify()
    print(
        f"schema_identity={info['schema_identity']} "
        f"schema_version={info['schema_version']} "
        f"status={info['initialization_status']}"
    )

    print("== V2 database reset + reinitialize ==")
    path = reset()
    info = verify()
    print(f"reset path: {path}")
    print(
        f"schema_identity={info['schema_identity']} "
        f"schema_version={info['schema_version']} "
        f"status={info['initialization_status']}"
    )

    print("== unittest suite ==")
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=str(REPO_ROOT),
        check=False,
    )
    if proc.returncode != 0:
        print("FAIL: unittest")
        return proc.returncode

    print("ALL VERIFICATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
