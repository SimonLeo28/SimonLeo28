import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "SimonLeo28"

URL = (
    f"https://github.com/users/"
    f"{USERNAME}/contributions"
)

OUTPUT = Path("data/contributions.json")


def fetch_page():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/140 Safari/537.36"
        )
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def parse_contributions(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    days = []

    for cell in soup.select(
        "td.ContributionCalendar-day"
    ):

        date = cell.get("data-date")

        if not date:
            continue

        level = cell.get(
            "data-level",
            "0"
        )

        try:
            level = int(level)
        except ValueError:
            level = 0

        aria = cell.get(
            "aria-label",
            ""
        )

        match = re.search(
            r"(\d[\d,]*) contribution",
            aria
        )

        count = 0

        if match:
            count = int(
                match.group(1).replace(",", "")
            )

        days.append(
            {
                "date": date,
                "count": count,
                "level": level
            }
        )

    return days


def calculate_stats(days):

    if not days:
        return {
            "total": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": None
        }

    total = sum(
        day["count"]
        for day in days
    )

    best = max(
        days,
        key=lambda x: x["count"]
    )

    longest = 0
    current = 0

    sorted_days = sorted(
        days,
        key=lambda x: x["date"]
    )

    for day in sorted_days:

        if day["count"] > 0:
            current += 1
            longest = max(
                longest,
                current
            )
        else:
            current = 0

    current_streak = 0

    for day in reversed(sorted_days):

        if day["count"] > 0:
            current_streak += 1
        else:
            break

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest,
        "best_day": best
    }


def main():

    print(
        f"Fetching contributions for "
        f"{USERNAME}..."
    )

    html = fetch_page()

    days = parse_contributions(
        html
    )

    print(
        f"Found {len(days)} contribution days."
    )

    stats = calculate_stats(days)

    output = {
        "username": USERNAME,
        "generated_at": datetime.utcnow().isoformat(),
        "days": days,
        "stats": stats
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            output,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Saved contributions to {OUTPUT}"
    )


if __name__ == "__main__":
    main()