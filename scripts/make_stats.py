#!/usr/bin/env python3
"""assets/stats.svg — metric tiles, language bars and weekly activity, from data/*.json."""

from datetime import date

from theme import C, esc, fmt, load_json, rng, svg_close, svg_open, window_chrome, write_svg

W, H = 1000, 432

SHORT_NAMES = {"Jupyter Notebook": "Jupyter", "Objective-C": "Obj-C", "Vim Script": "Vim"}

LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5", "HTML": "#e34c26",
    "CSS": "#663399", "Jupyter Notebook": "#DA5B0B", "EJS": "#a91e50", "Java": "#b07219",
    "C++": "#f34b7d", "C": "#8b949e", "Shell": "#89e051", "Go": "#00ADD8", "Rust": "#dea584",
}


def short_name(name: str) -> str:
    name = SHORT_NAMES.get(name, name)
    return name if len(name) <= 12 else name[:11] + "…"


def tile(x, y, w, h, label, value, sub, accent, idx) -> str:
    r = rng(f"tile{idx}")
    digits = len(str(value))
    frames = []
    for k in range(8):
        junk = "".join(str(r.randint(0, 9)) for _ in range(digits))
        frames.append(
            f'<text class="sc" style="animation-delay:{.15 + k * .09:.2f}s" x="{x + 20}" y="{y + 74}" '
            f'font-size="44" font-weight="800" fill="{accent}">{junk}</text>'
        )
    return f"""<g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{C['panel2']}" fill-opacity=".7" stroke="{C['line_dim']}"/>
<rect x="{x}" y="{y}" width="{w}" height="3" rx="1.5" fill="{accent}" opacity=".9"/>
<text x="{x + 20}" y="{y + 30}" font-size="11" letter-spacing="1.8" fill="{C['muted']}">{esc(label)}</text>
{''.join(frames)}
<text class="fin" x="{x + 20}" y="{y + 74}" font-size="44" font-weight="800" fill="{accent}" filter="url(#tglow)">{value}</text>
<text x="{x + 20}" y="{y + 98}" font-size="12" fill="{C['muted']}">{esc(sub)}</text>
</g>"""


def language_panel(x, y, w, h, stats) -> str:
    langs = stats.get("languages", [])[:6]
    total = sum(l["count"] for l in stats.get("languages", [])) or 1
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{C["panel2"]}" fill-opacity=".7" stroke="{C["line_dim"]}"/>',
           f'<text x="{x + 20}" y="{y + 30}" font-size="11" letter-spacing="1.8" fill="{C["muted"]}">TOP LANGUAGES · BY REPO</text>']
    label_w, track_x, track_w = 118, x + 20 + 118, w - 20 - 118 - 20 - 84
    top = max((l["count"] for l in langs), default=1)
    for i, lang in enumerate(langs):
        ry = y + 52 + i * 25
        color = LANG_COLORS.get(lang["name"], C["muted"])
        pct = round(100 * lang["count"] / total)
        bar = max(4, track_w * lang["count"] / top)
        out.append(
            f'<circle cx="{x + 26}" cy="{ry + 7}" r="4" fill="{color}"/>'
            f'<text x="{x + 38}" y="{ry + 11}" font-size="12.5" fill="{C["text"]}">{esc(short_name(lang["name"]))}</text>'
            f'<rect x="{track_x}" y="{ry + 2}" width="{fmt(track_w)}" height="10" rx="5" fill="{C["bg"]}" stroke="{C["line_dim"]}"/>'
            f'<rect class="grow" style="animation-delay:{.5 + i * .12:.2f}s" x="{track_x}" y="{ry + 2}" width="{fmt(bar)}" height="10" rx="5" fill="{color}" fill-opacity=".9"/>'
            f'<text x="{x + w - 20}" y="{ry + 11}" font-size="12" text-anchor="end" fill="{C["muted"]}">{lang["count"]} · {pct}%</text>'
        )
    return "\n".join(out)


def weekly_totals(days):
    """Sunday-anchored weekly sums, oldest → newest."""
    weeks, current, key = [], 0, None
    for d in days:
        y, m, dd = map(int, d["date"].split("-"))
        weekday = (date(y, m, dd).weekday() + 1) % 7  # Sunday = 0
        if weekday == 0 and key is not None:
            weeks.append(current)
            current = 0
        key = d["date"]
        current += d["count"]
    weeks.append(current)
    return weeks


def activity_panel(x, y, w, h, contrib) -> str:
    days = contrib["days"]
    weeks = weekly_totals(days)
    peak = max(weeks) or 1
    inner_w, base_y, max_h = w - 40, y + h - 46, h - 100
    pitch = inner_w / len(weeks)
    bw = max(3, pitch * .68)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{C["panel2"]}" fill-opacity=".7" stroke="{C["line_dim"]}"/>',
           f'<text x="{x + 20}" y="{y + 30}" font-size="11" letter-spacing="1.8" fill="{C["muted"]}">WEEKLY CONTRIBUTIONS · LAST 12 MONTHS</text>']
    for i, total in enumerate(weeks):
        bh = max(2, max_h * total / peak) if total else 2
        cls = "bar" if total else "bar zero"
        out.append(
            f'<rect class="{cls}" style="animation-delay:{i * .022:.2f}s,{2 + i * .07:.2f}s" x="{fmt(x + 20 + i * pitch)}" '
            f'y="{fmt(base_y - bh)}" width="{fmt(bw)}" height="{fmt(bh)}" rx="1.6"/>'
        )
    out.append(f'<path d="M{x + 20} {base_y + 4}H{x + w - 20}" stroke="{C["line"]}"/>')
    best = max(days, key=lambda d: d["count"])
    out.append(f'<text x="{x + 20}" y="{y + h - 16}" font-size="11.5" fill="{C["muted"]}">{esc(days[0]["date"])}</text>')
    out.append(f'<text x="{x + w - 20}" y="{y + h - 16}" font-size="11.5" text-anchor="end" fill="{C["muted"]}">{esc(days[-1]["date"])}</text>')
    if best["count"]:
        out.append(f'<text x="{x + w / 2}" y="{y + h - 16}" font-size="11.5" text-anchor="middle" fill="{C["green_soft"]}">'
                   f'peak day · {best["count"]} on {esc(best["date"])}</text>')
    return "\n".join(out)


def build() -> str:
    stats = load_json("stats.json", {"repos": 0, "languages": []})
    contrib = load_json("contributions.json")
    if not contrib or not contrib.get("days"):
        raise SystemExit("data/contributions.json missing — run fetch_contributions.py first")
    cs = contrib["stats"]

    css = f"""
.sc{{opacity:0;animation:fl .09s steps(1,end)}}
@keyframes fl{{from,to{{opacity:1}}}}
.fin{{animation:fin .01s .87s backwards}}
@keyframes fin{{from{{opacity:0}}to{{opacity:1}}}}
.grow{{transform-box:fill-box;transform-origin:left center;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) backwards}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.bar{{fill:{C['green']};fill-opacity:.78;transform-box:fill-box;transform-origin:center bottom;
animation:up .7s cubic-bezier(.2,.8,.2,1) backwards,wave 7s ease-in-out infinite}}
.bar.zero{{fill:{C['line']};fill-opacity:1}}
@keyframes up{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes wave{{0%,10%,100%{{fill-opacity:.78}}4%{{fill-opacity:1}}}}
"""
    p = [svg_open(W, H, "GitHub metrics",
                  f"{stats['repos']} public repositories, {cs['total']} contributions in the last year, "
                  f"{cs['active_days']} active days and a longest streak of {cs['longest_streak']} days.", css)]
    p.append(f'<defs><filter id="tglow" x="-20%" y="-30%" width="140%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/>'
             f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    p.append(window_chrome(W, H, "github_metrics.dat", f"synced {contrib.get('synced', '')}"))

    tw, gap, x0, y0, th = 227, 14, 24, 62, 112
    tiles = [
        ("REPOSITORIES", stats["repos"], "public on GitHub", C["green"]),
        ("CONTRIBUTIONS", cs["total"], "in the last year", C["blue"]),
        ("ACTIVE DAYS", cs["active_days"], f"out of {len(contrib['days'])} days", C["purple"]),
        ("LONGEST STREAK", cs["longest_streak"], f"days · current streak {cs['current_streak']}", C["amber"]),
    ]
    for i, (label, value, sub, accent) in enumerate(tiles):
        p.append(tile(x0 + i * (tw + gap), y0, tw, th, label, value, sub, accent, i))

    py, ph = y0 + th + 16, H - (y0 + th + 16) - 20
    p.append(language_panel(24, py, 470, ph, stats))
    p.append(activity_panel(506, py, 470, ph, contrib))
    p.append(svg_close())
    return "\n".join(p)


if __name__ == "__main__":
    write_svg("stats.svg", build())
