"""Minimal AI_FACTORY_OS V2 runtime entrypoint.

Provides health-check / startup only. Does not import or depend on
retired Entry-driven runtime under 99_ARCHIVE/legacy_runtime/.
"""

from __future__ import annotations

OK_MESSAGE = "AI_FACTORY_OS V2 runtime: OK"


def healthcheck() -> str:
    """Return the canonical V2 runtime health message."""
    return OK_MESSAGE


def main() -> int:
    print(healthcheck())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
