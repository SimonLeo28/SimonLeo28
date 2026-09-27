#!/usr/bin/env python3
"""assets/footer.svg (waves, rising particles, typed sign-off) and assets/divider.svg."""

import math

from theme import C, border_runner, esc, fmt, rng, svg_close, svg_open, typing_timeline, write_svg

W, H = 1000, 210
LINES = ["> thanks_for_stopping_by();", "> ship_something_intelligent();"]


def wave(base, amp, cycles, phase, opacity, dur, cls, uid):
    """A seamless sine wave: 2000px wide, slides exactly one 1000px period."""
    pts = []
    for i in range(0, 2001, 10):
        y = base + amp * math.sin(2 * math.pi * cycles * i / 1000 + phase)
        pts.append(f"{i} {fmt(y)}")
    d = "M" + " L".join(pts) + f" L2000 {H} L0 {H} Z"
    return (f'<path class="{cls}" d="{d}" fill="url(#{uid})" fill-opacity="{opacity}" '
            f'style="animation-duration:{dur}s"/>')


def particles() -> str:
    r = rng("footer-particles")
    out = []
    for _ in range(26):
        x = r.uniform(20, W - 20)
        size = r.uniform(1.2, 2.8)
        dur = r.uniform(4.5, 9)
        y0 = r.uniform(150, 200)
        out.append(
            f'<circle cx="{fmt(x)}" cy="{fmt(y0)}" r="{size:.1f}" fill="#00ff41">'
            f'<animate attributeName="cy" values="{fmt(y0)};{fmt(y0 - r.uniform(110, 170))}" dur="{dur:.1f}s" '
            f'begin="{-r.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.85;0" dur="{dur:.1f}s" begin="{-r.uniform(0, dur):.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


def signoff() -> str:
    size, cw, y = 27, 16.4, 98
    slot = 5.2
    total = slot * len(LINES)
    defs, body = [], []
    for i, line in enumerate(LINES):
        n = len(line)
        tw = n * cw
        x0 = (W - tw) / 2
        start = i * slot
        times, widths, end = typing_timeline(n, cw, total, start, 1.6, 2.0, 0.9)
        cursor_x = ";".join(fmt(x0 + float(w)) for w in widths.split(";"))
        vis_t = f"0;{end / total:.5f}" if i == 0 else f"0;{start / total:.5f};{end / total:.5f}"
        vis_v = "1;0" if i == 0 else "0;1;0"
        defs.append(
            f'<clipPath id="so{i}"><rect x="{fmt(x0)}" y="{y - 32}" height="44" width="{fmt(tw) if i == 0 else 0}">'
            f'<animate attributeName="width" calcMode="discrete" dur="{total}s" repeatCount="indefinite" '
            f'keyTimes="{times}" values="{widths}"/></rect></clipPath>'
        )
        body.append(
            f'<text clip-path="url(#so{i})" x="{fmt(x0)}" y="{y}" font-size="{size}" font-weight="700" fill="#00ff41" '
            f'filter="url(#fglow)" textLength="{fmt(tw)}" lengthAdjust="spacing">{esc(line)}</text>'
            f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" calcMode="discrete" dur="{total}s" '
            f'repeatCount="indefinite" keyTimes="{vis_t}" values="{vis_v}"/>'
            f'<rect class="blink" y="{y - 25}" width="11" height="29" fill="#00ff41" x="{fmt(x0 + (tw if i == 0 else 0))}">'
            f'<animate attributeName="x" calcMode="discrete" dur="{total}s" repeatCount="indefinite" '
            f'keyTimes="{times}" values="{cursor_x}"/></rect></g>'
        )
    return "<defs>" + "".join(defs) + "</defs>" + "".join(body)


def build_footer() -> str:
    css = """
.w1{animation:slide 14s linear infinite}
.w2{animation:slide 22s linear infinite reverse}
.w3{animation:slide 9s linear infinite}
@keyframes slide{from{transform:translateX(0)}to{transform:translateX(-1000px)}}
"""
    p = [svg_open(W, H, "Footer — thanks for stopping by",
                  "Animated waves and rising particles behind a typed sign-off.", css)]
    p.append(f"""<defs>
<clipPath id="fr"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<linearGradient id="wg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00ff41" stop-opacity=".55"/><stop offset="1" stop-color="#00ff41" stop-opacity="0"/></linearGradient>
<linearGradient id="wg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#79c0ff" stop-opacity=".45"/><stop offset="1" stop-color="#79c0ff" stop-opacity="0"/></linearGradient>
<linearGradient id="wg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00ff41" stop-opacity=".35"/><stop offset="1" stop-color="#00ff41" stop-opacity="0"/></linearGradient>
<filter id="fglow" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{C['bg']}"/>
<g clip-path="url(#fr)">
{wave(150, 14, 2, 0.0, .55, 14, 'w1', 'wg2')}
{wave(158, 11, 3, 1.6, .7, 22, 'w2', 'wg3')}
{wave(168, 9, 1, 3.1, .9, 9, 'w3', 'wg1')}
{particles()}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{C['line']}"/>
{border_runner(1, 1, W - 2, H - 2, 17, C['green'], dur=9, dash=240, width=2, begin=-3)}
{signoff()}
<text x="500" y="146" font-size="12.5" letter-spacing="3" text-anchor="middle" fill="{C['muted']}">SIMON LEO ALEXANDER  //  BENGALURU, IN  //  2026</text>""")
    p.append(svg_close())
    return "\n".join(p)


def build_divider() -> str:
    dw, dh = 1000, 30
    p = [svg_open(dw, dh, "Divider", "Decorative animated divider line.")]
    p.append(f"""<defs>
<linearGradient id="dl" x1="0" x2="1"><stop offset="0" stop-color="#00ff41" stop-opacity="0"/><stop offset=".5" stop-color="#00ff41" stop-opacity=".7"/><stop offset="1" stop-color="#00ff41" stop-opacity="0"/></linearGradient>
<filter id="dg" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="0" y="14.5" width="{dw}" height="1.2" fill="url(#dl)"/>
<circle r="2.6" cy="15" fill="#eafff0" filter="url(#dg)"><animate attributeName="cx" values="60;940" dur="5.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="5.5s" repeatCount="indefinite"/></circle>
<circle r="2.6" cy="15" fill="#79c0ff" filter="url(#dg)"><animate attributeName="cx" values="940;60" dur="7s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="7s" repeatCount="indefinite"/></circle>
<g><animateTransform attributeName="transform" type="rotate" from="0 500 15" to="360 500 15" dur="9s" repeatCount="indefinite"/>
<rect x="491" y="6" width="18" height="18" rx="3" fill="{C['bg']}" stroke="#00ff41" stroke-width="1.4" transform="rotate(45 500 15)"/></g>
<rect class="pulse" x="496" y="11" width="8" height="8" rx="1.5" fill="#00ff41" transform="rotate(45 500 15)"/>""")
    p.append(svg_close())
    return "\n".join(p)


if __name__ == "__main__":
    write_svg("footer.svg", build_footer())
    write_svg("divider.svg", build_divider())
