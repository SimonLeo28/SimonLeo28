#!/usr/bin/env python3
"""assets/header.svg — matrix rain, glitching name, self-typing tagline."""

from theme import C, DISPLAY_NAME, border_runner, esc, fmt, rng, svg_close, svg_open, typing_timeline, write_svg

W, H = 1000, 340
LINES = [
    "> AI × FULL_STACK_DEVELOPER",
    "> COMPUTER_VISION_ENGINEER",
    "> AUTOMATION_SPECIALIST",
    "> BUILDING_INTELLIGENT_SYSTEMS",
]
GLYPHS = "01<>/{}[]()=+*#$%&;:|~^ABCDEFXYZ"


def matrix_rain() -> str:
    r = rng("header-rain")
    cols, lh = 62, 17
    step = W / cols
    out = []
    for i in range(cols):
        n = r.randint(7, 15)
        dur = r.uniform(5.5, 11.5)
        begin = -r.uniform(0, dur)
        rest_y = r.randint(-n * lh // 2, H)  # resting frame = scattered rain
        chars = []
        for k in range(n):
            glyph = esc(r.choice(GLYPHS))
            head = k == n - 1
            alpha = 1 if head else 0.05 + 0.62 * (k / (n - 1)) ** 1.7
            fill = ' fill="#d9ffe4"' if head else ""
            chars.append(f'<text y="{k * lh}" fill-opacity="{alpha:.2f}"{fill}>{glyph}</text>')
        out.append(
            f'<g transform="translate({fmt(step * (i + .5))} 0)"><g transform="translate(0 {rest_y})">'
            f'<animateTransform attributeName="transform" type="translate" from="0 {-n * lh}" to="0 {H + lh}" '
            f'dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/>' + "".join(chars) + "</g></g>"
        )
    return '<g font-size="14" fill="#00ff41" text-anchor="middle" opacity=".62">' + "".join(out) + "</g>"


def tagline() -> str:
    size, cw = 26, 15.7
    y = 262
    slot = 4.4
    total = slot * len(LINES)
    defs, body = [], []
    for i, line in enumerate(LINES):
        n = len(line)
        tw = n * cw
        x0 = (W - tw) / 2
        start = i * slot
        times, widths, end = typing_timeline(n, cw, total, start, 1.7, 1.6, 0.9)
        # cursor visibility window for this slot
        vis_times = "0;" + f"{end / total:.5f}" if i == 0 else f"0;{start / total:.5f};{end / total:.5f}"
        vis_vals = "1;0" if i == 0 else "0;1;0"
        cursor_x = ";".join(fmt(x0 + float(w)) for w in widths.split(";"))
        base_w = fmt(tw) if i == 0 else "0"
        defs.append(
            f'<clipPath id="tc{i}"><rect x="{fmt(x0)}" y="{y - 30}" height="42" width="{base_w}">'
            f'<animate attributeName="width" calcMode="discrete" dur="{total:.1f}s" repeatCount="indefinite" '
            f'keyTimes="{times}" values="{widths}"/></rect></clipPath>'
        )
        body.append(
            f'<text clip-path="url(#tc{i})" x="{fmt(x0)}" y="{y}" font-size="{size}" font-weight="700" '
            f'fill="#eafff0" textLength="{fmt(tw)}" lengthAdjust="spacing">{esc(line)}</text>'
            f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" calcMode="discrete" '
            f'dur="{total:.1f}s" repeatCount="indefinite" keyTimes="{vis_times}" values="{vis_vals}"/>'
            f'<rect class="blink" y="{y - 24}" width="11" height="28" fill="#00ff41" x="{fmt(x0 + tw if i == 0 else x0)}">'
            f'<animate attributeName="x" calcMode="discrete" dur="{total:.1f}s" repeatCount="indefinite" '
            f'keyTimes="{times}" values="{cursor_x}"/></rect></g>'
        )
    return "<defs>" + "".join(defs) + "</defs>" + "".join(body)


def build() -> str:
    css = """
.gh{opacity:0;transform-box:fill-box;transform-origin:center}
.g1{animation:gl1 5.4s infinite}
.g2{animation:gl2 5.4s infinite}
@keyframes gl1{0%,85%,100%{opacity:0;transform:translate(0,0)}87%{opacity:.9;transform:translate(-7px,1px)}89%{opacity:.9;transform:translate(6px,-2px)}91%{opacity:.9;transform:translate(-3px,2px)}93%{opacity:0}}
@keyframes gl2{0%,86%,100%{opacity:0;transform:translate(0,0)}88%{opacity:.85;transform:translate(7px,-1px)}90%{opacity:.85;transform:translate(-6px,2px)}92%{opacity:.85;transform:translate(3px,-1px)}94%{opacity:0}}
.mn{transform-box:fill-box;transform-origin:center;animation:jit 5.4s infinite}
@keyframes jit{0%,86%,100%{transform:none}88%{transform:translate(2px,0) skewX(-5deg)}90%{transform:translate(-2px,0) skewX(4deg)}92%{transform:none}}
.scan{animation:scan 5s linear infinite}
@keyframes scan{from{transform:translateY(-70px)}to{transform:translateY(400px)}}
.rise{animation:rise 3.2s ease-out both}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
"""
    name = DISPLAY_NAME.upper()
    title_len = 800
    parts = [svg_open(W, H, f"{DISPLAY_NAME} — AI × Full-Stack Developer",
                      "Animated banner: falling matrix code, a glitching name and a self-typing list of roles.", css)]
    parts.append(f"""<defs>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<radialGradient id="vig"><stop offset="0" stop-color="{C['bg']}" stop-opacity=".93"/><stop offset=".62" stop-color="{C['bg']}" stop-opacity=".72"/><stop offset="1" stop-color="{C['bg']}" stop-opacity="0"/></radialGradient>
<linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="#00ff41" stop-opacity="0"/><stop offset=".5" stop-color="#00ff41" stop-opacity=".9"/><stop offset="1" stop-color="#00ff41" stop-opacity="0"/></linearGradient>
<linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#eafff0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00ff41" stop-opacity="0"/><stop offset=".5" stop-color="#00ff41" stop-opacity=".16"/><stop offset="1" stop-color="#00ff41" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{C['bg']}"/>
<g clip-path="url(#frame)">
{matrix_rain()}
<ellipse cx="500" cy="196" rx="480" ry="176" fill="url(#vig)"/>
<rect class="scan" width="{W}" height="70" fill="url(#scanG)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{C['line']}"/>
{border_runner(1, 1, W - 2, H - 2, 17, C['green'], dur=8, dash=260, width=2)}
""")
    # corner brackets
    b, m = 16, 26
    for (x, y, dx, dy) in ((m, m + 6, 1, 1), (W - m, m + 6, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        parts.append(
            f'<path class="pulse" d="M{x} {y + dy * b}V{y}H{x + dx * b}" fill="none" stroke="#00ff41" stroke-width="2" opacity=".8"/>'
        )
    # status row
    parts.append(f"""<circle class="pulse" cx="52" cy="46" r="4" fill="#00ff41"/>
<text x="64" y="50" font-size="12" letter-spacing="2" fill="{C['muted']}">SYS.ONLINE</text>
<text x="{W - 52}" y="50" font-size="12" letter-spacing="2" text-anchor="end" fill="{C['muted']}">BENGALURU // IN</text>""")
    # title with glitch ghosts
    tattrs = (f'x="500" y="186" text-anchor="middle" font-size="66" font-weight="800" '
              f'textLength="{title_len}" lengthAdjust="spacing"')
    parts.append(f"""<text class="gh g1" {tattrs} fill="{C['cyan']}">{esc(name)}</text>
<text class="gh g2" {tattrs} fill="{C['magenta']}">{esc(name)}</text>
<g filter="url(#glow)"><text class="mn" {tattrs} fill="#00ff41">{esc(name)}</text></g>
<rect x="100" y="210" width="800" height="1.6" fill="url(#rule)"/>
<rect y="208.5" width="120" height="4.5" rx="2" fill="url(#beam)" x="100">
<animate attributeName="x" values="100;780;100" keyTimes="0;.5;1" dur="4.4s" repeatCount="indefinite"/></rect>""")
    parts.append(tagline())
    # availability line
    tl = 480
    parts.append(f"""<circle class="pulse" cx="{500 - tl / 2 - 14}" cy="309" r="4" fill="#00ff41"/>
<text x="{500 - tl / 2}" y="313" font-size="13" letter-spacing="2" fill="{C['green_soft']}" fill-opacity=".85"
 textLength="{tl}" lengthAdjust="spacing">AVAILABLE FOR SOFTWARE DEVELOPMENT OPPORTUNITIES</text>""")
    parts.append(svg_close())
    return "\n".join(parts)


if __name__ == "__main__":
    write_svg("header.svg", build())
