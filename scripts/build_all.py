#!/usr/bin/env python3
"""Regenerate every generated asset in data → art order.

Run this after fetch_contributions.py / fetch_stats.py have refreshed the
data files, or any time you edit a make_*.py script.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

# Data first (each fetcher is self-healing and never hard-fails the run),
# then every asset generator that reads data/*.json or scripts/icons.json.
STEPS = [
    "fetch_contributions.py",
    "fetch_stats.py",
    "make_header.py",
    "make_terminal.py",
    "make_stack.py",
    "make_projects.py",
    "make_stats.py",
    "make_activity.py",
    "make_footer.py",
    "make_buttons.py",
    "make_ascii.py",
]


def main() -> int:
    for step in STEPS:
        print(f"\n== {step} ==")
        result = subprocess.run([sys.executable, str(SCRIPTS_DIR / step)], cwd=SCRIPTS_DIR)
        if result.returncode != 0:
            print(f"::error::{step} failed (exit {result.returncode})")
            return result.returncode
    print("\nAll assets regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
