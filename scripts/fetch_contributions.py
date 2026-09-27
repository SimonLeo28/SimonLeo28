#!/usr/bin/env python3
"""Fetch the public contribution calendar into data/contributions.json.

GitHub renders the per-day counts inside <tool-tip> elements that point at
each calendar cell (``for="contribution-day-component-…"``).  The previous
version of this script looked for an ``aria-label`` on the cell, which no
longer exists, so every day silently became 0.  This version reads the
tool-tips, cross-checks the total against the page headline, and refuses to
overwrite good cached data with a bad scrape.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

from theme import DATA, USERNAME

URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT = DATA / "contributions.json"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/141 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
COUNT_RE = re.compile(r"^\s*(\d[\d,]*)\s+contribution", re.I)


def fetch_page() -> str:
    last_error: Exception | None = None
    for _ in range(3):
        try:
            response = requests.get(URL, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as error:  # retry transient failures
            last_error = error
    raise RuntimeError(f"could not download {URL}: {last_error}")


def parse_contributions(markup: str) -> tuple[list[dict], int | None]:
    soup = BeautifulSoup(markup, "html.parser")

    tips: dict[str, int] = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if not target:
            continue
        match = COUNT_RE.match(tip.get_text(" ", strip=True))
        tips[target] = int(match.group(1).replace(",", "")) if match else 0

    days: list[dict] = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        try:
            level = int(cell.get("data-level", "0"))
        except ValueError:
            level = 0
        days.append(
            {
                "date": cell["data-date"],
                "count": tips.get(cell.get("id", ""), 0),
                "level": level,
            }
        )
    days.sort(key=lambda d: d["date"])

    headline = None
    heading = soup.select_one("h2#js-contribution-activity-description")
    if heading:
        match = re.search(r"(\d[\d,]*)\s+contributions?", heading.get_text(" ", strip=True))
        if match:
            headline = int(match.group(1).replace(",", ""))
    return days, headline


def calculate_stats(days: list[dict]) -> dict:
    if not days:
        return {
            "total": 0, "active_days": 0, "current_streak": 0,
            "longest_streak": 0, "best_day": None,
        }

    longest = run = 0
    for day in days:
        run = run + 1 if day["count"] > 0 else 0
        longest = max(longest, run)

    # Current streak: consecutive active days ending today — or yesterday, if
    # today simply has no commits *yet* (this is how GitHub itself counts it).
    by_date = {d["date"]: d["count"] for d in days}
    cursor = date.fromisoformat(days[-1]["date"])
    if by_date.get(cursor.isoformat(), 0) == 0:
        cursor -= timedelta(days=1)
    current = 0
    while by_date.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)

    best = max(days, key=lambda d: d["count"])
    return {
        "total": sum(d["count"] for d in days),
        "active_days": sum(1 for d in days if d["count"] > 0),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best if best["count"] > 0 else None,
    }


def main() -> int:
    print(f"Fetching contributions for {USERNAME} …")
    try:
        days, headline = parse_contributions(fetch_page())
        stats = calculate_stats(days)
        if len(days) < 300:
            raise RuntimeError(f"only {len(days)} calendar cells parsed (expected ~370)")
        if headline is not None and stats["total"] != headline:
            raise RuntimeError(
                f"parsed total {stats['total']} != page headline {headline}; markup changed?"
            )
    except Exception as error:  # never break the workflow, never write bad data
        print(f"::warning::contribution fetch failed, keeping cached data: {error}")
        return 0 if OUTPUT.exists() else 1

    payload = {
        "username": USERNAME,
        "synced": datetime.now(timezone.utc).date().isoformat(),
        "days": days,
        "stats": stats,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Saved {len(days)} days · {stats['total']} contributions · "
          f"longest streak {stats['longest_streak']} → {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
