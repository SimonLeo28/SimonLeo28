import json
import math
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
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0"
]


def load_data():

    if not INPUT.exists():
        raise FileNotFoundError(
            "contributions.json not found."
        )

    return json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )


def group_by_date(days):

    result = {}

    for day in days:

        result[
            day["date"]
        ] = day

    return result


def get_start_date(days):

    dates = [
        datetime.strptime(
            day["date"],
            "%Y-%m-%d"
        ).date()
        for day in days
    ]

    latest = max(dates)

    # Go backwards approximately one year
    start = latest - timedelta(
        days=364
    )

    # Align to Sunday
    start -= timedelta(
        days=(start.weekday() + 1) % 7
    )

    return start


def create_cells(days):

    lookup = group_by_date(days)

    start = get_start_date(days)

    cells = []

    for week in range(53):

        for day_index in range(7):

            date = start + timedelta(
                days=week * 7 + day_index
            )

            date_string = date.isoformat()

            info = lookup.get(
                date_string,
                {
                    "count": 0,
                    "level": 0
                }
            )

            x = (
                LEFT
                + week * (CELL + GAP)
            )

            y = (
                TOP
                + day_index * (CELL + GAP)
            )

            cells.append(
                {
                    "x": x,
                    "y": y,
                    "date": date_string,
                    "count": info["count"],
                    "level": info["level"]
                }
            )

    return cells


def escape(text):

    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def generate_svg(data):

    cells = create_cells(
        data["days"]
    )

    stats = data["stats"]

    svg = []

    svg.append(
        f'''
<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
>
'''
    )

    svg.append(
        '''
<style>

.cell {
    opacity: 0;
    animation: reveal 0.35s ease-out forwards;
}

@keyframes reveal {

    from {
        opacity: 0;
        transform: translateY(-5px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

.title {
    font-family: monospace;
    font-size: 15px;
    font-weight: bold;
    fill: #c9d1d9;
}

.subtitle {
    font-family: monospace;
    font-size: 11px;
    fill: #8b949e;
}

.legend {
    font-family: monospace;
    font-size: 10px;
    fill: #8b949e;
}

</style>
'''
    )

    # Background
    svg.append(
        f'''
<rect
    width="{WIDTH}"
    height="{HEIGHT}"
    rx="12"
    fill="#0d1117"
/>
'''
    )

    # Title
    svg.append(
        '''
<text
    class="title"
    x="20"
    y="20"
>
SimonLeo28 — contribution activity
</text>
'''
    )

    # Cells
    for index, cell in enumerate(cells):

        level = int(
            max(
                0,
                min(
                    cell["level"],
                    len(PALETTE) - 1
                )
            )
        )

        color = PALETTE[level]

        delay = (
            index * 0.008
        )

        svg.append(
            f'''
<rect
    class="cell"
    x="{cell["x"]}"
    y="{cell["y"]}"
    width="{CELL}"
    height="{CELL}"
    rx="2"
    fill="{color}"
    style="animation-delay:{delay:.3f}s"
>
<title>
{escape(cell["date"])}:
{cell["count"]} contributions
</title>
</rect>
'''
        )

    # Stats
    total = stats.get(
        "total",
        0
    )

    current = stats.get(
        "current_streak",
        0
    )

    longest = stats.get(
        "longest_streak",
        0
    )

    footer = (
        f"{total:,} contributions"
        f" • Current streak: {current}"
        f" • Longest streak: {longest}"
    )

    svg.append(
        f'''
<text
    class="subtitle"
    x="20"
    y="157"
>
{escape(footer)}
</text>
'''
    )

    # Legend
    legend_y = 177

    svg.append(
        f'''
<text
    class="legend"
    x="20"
    y="{legend_y}"
>
Less
</text>
'''
    )

    start_x = 58

    for index, color in enumerate(PALETTE):

        x = (
            start_x
            + index * 16
        )

        svg.append(
            f'''
<rect
    x="{x}"
    y="{legend_y - 9}"
    width="11"
    height="11"
    rx="2"
    fill="{color}"
/>
'''
        )

    svg.append(
        f'''
<text
    class="legend"
    x="{start_x + len(PALETTE) * 16 + 5}"
    y="{legend_y}"
>
More
</text>
'''
    )

    svg.append("</svg>")

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print(
        f"Created: {OUTPUT}"
    )


def main():

    data = load_data()

    generate_svg(
        data
    )


if __name__ == "__main__":
    main()