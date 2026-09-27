#!/usr/bin/env python3
"""assets/activity.svg — the real contribution graph, eaten by an animated snake.

No external action or `output` branch is needed: the snake is a stroked path
whose dash slides along the grid (so it is one continuous, rounded body) and
every active cell fades out at the exact moment the head reaches it.
"""

from datetime import date

from theme import C, esc, fmt, load_json, svg_close, svg_open, window_chrome, write_svg

W = 1000
CELL, PITCH = 13, 17
X0, Y0 = 58, 106
LEVEL_FILL = ["#141b23", "#0e4429", "#006d32", "#26a641", "#00ff41"]

SNAKE_LEN = 104          # px of body
MOVE = 26.0              # seconds the snake needs to cross the whole graph
PAUSE = 4.0              # rest at the end, then everything re-grows
TOTAL = MOVE + PAUSE


def sunday_index(day: str) -> int:
    y, m, d = map(int, day.split("-"))
    return (date(y, m, d).weekday() + 1) % 7  # Sunday = 0


def layout(days):
    """→ dict[(col,row)] = day, number of columns."""
    cells, col = {}, 0
    for i, day in enumerate(days):
        row = sunday_index(day["date"])
        if i > 0 and row == 0:
            col += 1
        cells[(col, row)] = day
    return cells, col + 1


def cx(col): return X0 + col * PITCH + CELL / 2
def cy(row): return Y0 + row * PITCH + CELL / 2


def snake_route(cells, ncols):
    """Axis-aligned vertices: down even columns, up odd ones, then off-screen."""
    pts = [(X0 - 220, cy(0)), (cx(0), cy(0))]
    for c in range(ncols):
        rows = [r for (cc, r) in cells if cc == c]
        last = max(rows)
        pts.append((cx(c), cy(last) if c % 2 == 0 else cy(0)))
        if c < ncols - 1:
            pts.append((cx(c + 1), pts[-1][1]))
    pts.append((W + 260, pts[-1][1]))
    return pts


def cumulative(pts):
    dist, total = [0.0], 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        total += abs(x2 - x1) + abs(y2 - y1)
        dist.append(total)
    return dist, total


def distance_of(pts, dist, x, y) -> float:
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        if min(x1, x2) - 1e-6 <= x <= max(x1, x2) + 1e-6 and min(y1, y2) - 1e-6 <= y <= max(y1, y2) + 1e-6:
            return dist[i] + abs(x - x1) + abs(y - y1)
    raise ValueError(f"cell centre ({x},{y}) is not on the snake route")


def month_labels(cells, ncols):
    out, prev = [], None
    for c in range(ncols):
        first = cells.get((c, 0)) or next((cells[(c, r)] for r in range(7) if (c, r) in cells), None)
        if not first:
            continue
        y, m, _ = map(int, first["date"].split("-"))
        if prev is None or m != prev:
            name = date(y, m, 1).strftime("%b")
            if not out or c - out[-1][0] >= 3:
                out.append((c, name))
            prev = m
    return out


def build() -> str:
    data = load_json("contributions.json")
    if not data or not data.get("days"):
        raise SystemExit("data/contributions.json missing — run fetch_contributions.py first")
    days, stats = data["days"], data["stats"]
    cells, ncols = layout(days)
    pts = snake_route(cells, ncols)
    dist, path_len = cumulative(pts)
    d_attr = "M" + " L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)

    reach = path_len + SNAKE_LEN                  # head+body must clear the path
    m = MOVE / TOTAL                              # fraction of the cycle spent moving
    head_done = m * path_len / reach              # when the head reaches the path end
    dash_anim = (f'<animate attributeName="stroke-dashoffset" dur="{TOTAL}s" repeatCount="indefinite" '
                 f'keyTimes="0;{m:.5f};1" values="{SNAKE_LEN};{-fmt_num(path_len)};{-fmt_num(path_len)}"/>')
    gap = reach + 80

    css = """
.ring{animation:ring 3.2s ease-in-out infinite}
@keyframes ring{0%,100%{opacity:.35}50%{opacity:1}}
.lick{animation:lick 1.1s steps(1,end) infinite}
@keyframes lick{0%,60%{opacity:1}61%,100%{opacity:0}}
"""
    p = [svg_open(W, 276, "Contribution activity — snake game",
                  f"{stats['total']} contributions in the last year across {stats['active_days']} active days. "
                  f"An animated snake eats the contribution graph.", css)]
    H = 276
    p.append(window_chrome(W, H, "activity_feed.sh", f"synced {data.get('synced', '')}"))
    # command line
    p.append(f"""<text x="28" y="74" font-size="14" fill="{C['green']}">$</text>
<text x="44" y="74" font-size="14" fill="{C['white']}" textLength="229" lengthAdjust="spacing">./snake --eat contributions</text>
<rect class="blink" x="280" y="61" width="8" height="16" fill="{C['green']}"/>
<text x="{W - 28}" y="74" font-size="13" text-anchor="end" fill="{C['muted']}"><tspan fill="{C['green']}" font-weight="700">{stats['total']}</tspan> contributions in the last year</text>""")

    # month + weekday labels
    for c, name in month_labels(cells, ncols):
        p.append(f'<text x="{fmt(X0 + c * PITCH)}" y="{Y0 - 10}" font-size="10.5" fill="{C["muted"]}">{name}</text>')
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text x="24" y="{fmt(cy(row) + 3.5)}" font-size="10" fill="{C["muted"]}">{name}</text>')

    # cells
    for (c, r), day in sorted(cells.items()):
        level = max(0, min(4, day["level"]))
        base = (f'<rect x="{fmt(X0 + c * PITCH)}" y="{fmt(Y0 + r * PITCH)}" width="{CELL}" height="{CELL}" '
                f'rx="3" fill="{LEVEL_FILL[level]}"')
        if level == 0:
            p.append(base + "/>")
            continue
        eaten = MOVE * distance_of(pts, dist, cx(c), cy(r)) / reach
        a = eaten / TOTAL
        e = 0.4 / TOTAL
        back1, back2 = (MOVE + 1.6) / TOTAL, (MOVE + 2.6) / TOTAL
        p.append(
            base + f'><title>{day["count"]} contribution{"s" if day["count"] != 1 else ""} on {esc(day["date"])}</title>'
            f'<animate attributeName="opacity" dur="{TOTAL}s" repeatCount="indefinite" '
            f'keyTimes="0;{a:.5f};{a + e:.5f};{back1:.5f};{back2:.5f};1" '
            f'values="1;1;.08;.08;1;1"/></rect>'
        )

    # the snake
    p.append(f"""<defs><clipPath id="arena"><rect x="{X0 - 12}" y="{Y0 - 14}" width="{W - X0 - 8}" height="{7 * PITCH + 20}"/></clipPath>
<filter id="sglow" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g clip-path="url(#arena)"><g filter="url(#sglow)">
<path d="{d_attr}" fill="none" stroke="{C['green']}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"
 stroke-dasharray="{SNAKE_LEN} {fmt(gap)}" stroke-dashoffset="{SNAKE_LEN}">{dash_anim}</path>
<path d="{d_attr}" fill="none" stroke="#04310f" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".75"
 stroke-dasharray="{SNAKE_LEN - 18} {fmt(gap + 18)}" stroke-dashoffset="{SNAKE_LEN - 9}">
<animate attributeName="stroke-dashoffset" dur="{TOTAL}s" repeatCount="indefinite" keyTimes="0;{m:.5f};1" values="{SNAKE_LEN - 9};{-fmt_num(path_len) - 9};{-fmt_num(path_len) - 9}"/></path>
</g>
<g>
<animateMotion dur="{TOTAL}s" repeatCount="indefinite" rotate="auto" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{head_done:.5f};1" path="{d_attr}"/>
<circle r="6.6" fill="#7dffa0"/>
<circle cx="2.6" cy="-2.7" r="1.7" fill="#04310f"/><circle cx="2.6" cy="2.7" r="1.7" fill="#04310f"/>
<path class="lick" d="M6.2 0H10.5M10.5 0l2.6-1.8M10.5 0l2.6 1.8" stroke="{C['red']}" stroke-width="1.3" stroke-linecap="round" fill="none"/>
</g></g>""")

    # footer: streak + legend
    fy = Y0 + 7 * PITCH + 34
    p.append(f'<text x="28" y="{fy}" font-size="12" fill="{C["muted"]}">current streak <tspan fill="{C["green"]}">{stats["current_streak"]}d</tspan>'
             f' · longest <tspan fill="{C["green"]}">{stats["longest_streak"]}d</tspan>'
             f' · active <tspan fill="{C["green"]}">{stats["active_days"]}</tspan> of {len(days)} days</text>')
    lx = W - 28 - 5 * (CELL + 4) - 66
    p.append(f'<text x="{lx}" y="{fy}" font-size="11" text-anchor="end" fill="{C["muted"]}">Less</text>')
    for i, fill in enumerate(LEVEL_FILL):
        p.append(f'<rect x="{lx + 10 + i * (CELL + 4)}" y="{fy - 11}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}"/>')
    p.append(f'<text x="{lx + 16 + 5 * (CELL + 4)}" y="{fy}" font-size="11" fill="{C["muted"]}">More</text>')
    p.append(svg_close())
    return "\n".join(p)


def fmt_num(x: float) -> float:
    return round(x, 2)


if __name__ == "__main__":
    write_svg("activity.svg", build())
