#!/usr/bin/env python3
"""Fetch profile statistics into data/stats.json.

Strategy (each step only runs if the previous one failed):
  1. GitHub REST API — authenticated with $GITHUB_TOKEN inside Actions.
  2. Scrape the public repositories page.
  3. Keep the previously cached data/stats.json.

The workflow therefore never fails because of a transient outage or a
rate limit, and it never overwrites good data with an empty result.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

from theme import DATA, USERNAME

OUTPUT = DATA / "stats.json"
API = "https://api.github.com"
WEB = "https://github.com"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/141 Safari/537.36"
)


# ── 1. REST API ────────────────────────────────────────────────────────
def via_api() -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-art"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    user = requests.get(f"{API}/users/{USERNAME}", headers=headers, timeout=30)
    user.raise_for_status()
    user = user.json()

    repos: list[dict] = []
    page = 1
    while True:
        response = requests.get(
            f"{API}/users/{USERNAME}/repos",
            headers=headers,
            params={"per_page": 100, "page": page, "type": "owner"},
            timeout=30,
        )
        response.raise_for_status()
        chunk = response.json()
        if not isinstance(chunk, list):
            raise RuntimeError(f"unexpected repos payload: {chunk!r:.120}")
        repos.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1

    owned = [r for r in repos if not r.get("fork")]
    return build_payload(
        repos=user["public_repos"],
        followers=user["followers"],
        following=user["following"],
        stars=sum(r.get("stargazers_count", 0) for r in owned),
        forks=sum(r.get("forks_count", 0) for r in owned),
        languages=[r.get("language") for r in owned],
        source="api",
    )


# ── 2. HTML fallback ───────────────────────────────────────────────────
def via_html() -> dict:
    headers = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    profile = requests.get(f"{WEB}/{USERNAME}", headers=headers, timeout=30)
    profile.raise_for_status()
    soup = BeautifulSoup(profile.text, "html.parser")

    def number_near(href_suffix: str) -> int:
        link = soup.select_one(f'a[href$="{href_suffix}"]')
        match = re.search(r"([\d,.]+)\s*([kK]?)", link.get_text(" ", strip=True)) if link else None
        if not match:
            return 0
        value = float(match.group(1).replace(",", ""))
        return int(value * 1000) if match.group(2) else int(value)

    followers = number_near("?tab=followers")
    following = number_near("?tab=following")

    languages: list[str | None] = []
    stars = forks = 0
    total_repos = 0
    url = f"{WEB}/{USERNAME}?tab=repositories"
    for _ in range(10):  # hard stop on pagination
        page = requests.get(url, headers=headers, timeout=30)
        page.raise_for_status()
        listing = BeautifulSoup(page.text, "html.parser")
        for item in listing.select("li[itemprop='owns']"):
            if "Forked from" in item.get_text(" ", strip=True):
                continue
            total_repos += 1
            lang = item.select_one("[itemprop='programmingLanguage']")
            languages.append(lang.get_text(strip=True) if lang else None)
            star = item.select_one("a[href$='/stargazers']")
            fork = item.select_one("a[href$='/forks']")
            stars += int(re.sub(r"\D", "", star.get_text()) or 0) if star else 0
            forks += int(re.sub(r"\D", "", fork.get_text()) or 0) if fork else 0
        nxt = listing.select_one("a.next_page[href]")
        if not nxt:
            break
        url = WEB + nxt["href"]

    if total_repos == 0:
        raise RuntimeError("repository listing parsed as empty")
    return build_payload(
        repos=total_repos, followers=followers, following=following,
        stars=stars, forks=forks, languages=languages, source="html",
    )


def build_payload(*, repos, followers, following, stars, forks, languages, source) -> dict:
    counts = Counter(lang for lang in languages if lang)
    return {
        "username": USERNAME,
        "synced": datetime.now(timezone.utc).date().isoformat(),
        "source": source,
        "repos": repos,
        "followers": followers,
        "following": following,
        "stars": stars,
        "forks": forks,
        "languages": [
            {"name": name, "count": count} for name, count in counts.most_common()
        ],
    }


def main() -> int:
    print(f"Fetching profile stats for {USERNAME} …")
    payload = None
    for label, fn in (("REST API", via_api), ("HTML fallback", via_html)):
        try:
            payload = fn()
            print(f"  {label}: ok")
            break
        except Exception as error:
            print(f"  {label} failed: {error}")

    if payload is None:
        print("::warning::stats fetch failed everywhere, keeping cached data")
        return 0 if OUTPUT.exists() else 1

    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Saved → {OUTPUT}: {payload['repos']} repos, "
          f"{len(payload['languages'])} languages ({payload['source']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
