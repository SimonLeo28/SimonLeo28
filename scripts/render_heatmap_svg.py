import json
from datetime import datetime, timedelta
from pathlib import Path


INPUT = Path("data/contributions.json")
OUTPUT = Path("assets/contrib-heatmap.svg")

WIDTH = 860
HEIGHT = 190
CELL = 10
GAP = 3
LEFT = 35
TOP = 35

PALETTE = [
    "#0d1117",
    "#102b2d",
    "#0f4d4d",
    "#1d7f7a",
    "#3ec3bf",
    "#7dd3fc",
]


def load_data():
    if not INPUT.exists():
        raise FileNotFoundError("contributions.json not found.")
    return json.loads(INPUT.read_text(encoding="utf-8"))


def group_by_date(days):
    result = {}
    for day in days:
        result[day["date"]] = day
    return result


def get_start_date(days):
    dates = [datetime.strptime(day["date"], "%Y-%m-%d").date() for day in days]
    latest = max(dates)
    start = latest - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    return start


def create_cells(days):
    lookup = group_by_date(days)
    start = get_start_date(days)
    cells = []

    for week in range(53):
        for day_index in range(7):
            date = start + timedelta(days=week * 7 + day_index)
            date_string = date.isoformat()
            info = lookup.get(date_string, {"count": 0, "level": 0})
            cells.append(
                {
                    "x": LEFT + week * (CELL + GAP),
                    "y": TOP + day_index * (CELL + GAP),
                    "date": date_string,
                    "count": info["count"],
                    "level": info["level"],
                }
            )
    return cells


def escape(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_svg(data):
    cells = create_cells(data["days"])
    stats = data["stats"]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<style>',
        '.cell { opacity: 0; animation: reveal 0.35s ease-out forwards; }',
        '@keyframes reveal { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }',
        '.title { font-family: monospace; font-size: 15px; font-weight: 700; fill: #dfeaf5; }',
        '.meta { font-family: monospace; font-size: 11px; fill: #8ea4b8; }',
        '.legend { font-family: monospace; font-size: 10px; fill: #8ea4b8; }',
        '</style>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#08141d" stroke="#1d2d3d" />',
        '<rect x="18" y="18" width="824" height="154" rx="14" fill="#0b1621" stroke="#203345" />',
        '<text class="title" x="30" y="38">SYSTEM ACTIVITY</text>',
        '<text class="meta" x="30" y="55">SimonLeo28 • contribution monitor</text>',
    ]

    for index, cell in enumerate(cells):
        level = max(0, min(int(cell["level"]), len(PALETTE) - 1))
        color = PALETTE[level]
        svg.append(
            f'<rect class="cell" x="{cell["x"]}" y="{cell["y"]}" width="{CELL}" height="{CELL}" rx="2" fill="{color}" style="animation-delay:{index * 0.006:.3f}s">'
            f'<title>{escape(cell["date"])}: {cell["count"]} contributions</title>'
            f'</rect>'
        )

    total = stats.get("total", 0)
    current = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    footer = f"{total:,} contributions • current streak: {current} • longest streak: {longest}"
    svg.append(f'<text class="meta" x="30" y="160">{escape(footer)}</text>')

    svg.append('<text class="legend" x="30" y="177">Less</text>')
    for i, color in enumerate(PALETTE):
        x = 70 + i * 16
        svg.append(f'<rect x="{x}" y="168" width="11" height="11" rx="2" fill="{color}" />')
    svg.append(f'<text class="legend" x="{70 + len(PALETTE) * 16 + 8}" y="177">More</text>')
    svg.append('</svg>')

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"Created: {OUTPUT}")


def main():
    data = load_data()
    generate_svg(data)


if __name__ == "__main__":
    main()