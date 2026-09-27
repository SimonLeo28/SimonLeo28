#!/usr/bin/env python3
"""assets/terminal.svg — a shell session that types itself out, beside a live neural net."""

from theme import C, esc, fmt, rng, svg_close, svg_open, window_chrome, write_svg

W, H = 1000, 410
CW, SIZE, LH = 9.7, 16, 27.5
X0, Y0 = 36, 96
TOTAL = 21.0

G, WH, BL, TX, MU = C["green"], C["white"], C["blue"], C["text"], C["muted"]

# (kind, [(text, colour), ...], start seconds)
SCRIPT = [
    ("cmd", [("$ ", G), ("whoami", WH)], 0.6),
    ("out", [("simon_leo_alexander", BL), (" — ", MU), ("AI × Full-Stack Developer", C["green_soft"])], 1.8),
    ("cmd", [("$ ", G), ("cat ", WH), ("about.txt", C["amber"])], 3.2),
    ("out", [("Final-year Information Science & Engineering student.", TX)], 4.4),
    ("out", [("Forging intelligent systems through ", TX), ("full-stack engineering", C["green_soft"]), (",", TX)], 5.2),
    ("out", [("computer vision", C["green_soft"]), (", and ", TX), ("automation", C["green_soft"]), (".", TX)], 6.0),
    ("cmd", [("$ ", G), ("ls ", WH), ("~/focus", C["amber"])], 7.6),
    ("out", [("computer_vision/  full_stack/  automation/  ai_systems/", BL)], 8.8),
    ("cmd", [("$ ", G), ("echo ", WH), ("$STATUS", C["amber"])], 10.4),
    ("out", [("● ", G), ("open to software development opportunities", WH)], 11.6),
    ("cmd", [("$ ", G)], 13.2),
]


def line_svg(idx: int, kind: str, segs, start: float) -> str:
    y = Y0 + idx * LH
    text = "".join(t for t, _ in segs)
    n = len(text)
    tw = n * CW
    spans = "".join(f'<tspan fill="{col}">{esc(t)}</tspan>' for t, col in segs)
    last = idx == len(SCRIPT) - 1

    if kind == "cmd":
        dur = max(0.35, n * 0.055)
        pts = [(0.0, 0.0)] + [(start + k * dur / n, k * CW) for k in range(1, n + 1)]
        times = ";".join(f"{t / TOTAL:.5f}" for t, _ in pts)
        widths = ";".join(fmt(w) for _, w in pts)
        cursor_x = ";".join(fmt(X0 + w) for _, w in pts)
        clip_anim = (f'<animate attributeName="width" calcMode="discrete" dur="{TOTAL}s" repeatCount="indefinite" '
                     f'keyTimes="{times}" values="{widths}"/>')
        end_vis = TOTAL if last else start + dur + 0.45
        vis_t = f"0;{start / TOTAL:.5f};{min(end_vis / TOTAL, 0.9999):.5f}"
        vis_v = "0;1;0" if not last else "0;1;1"
        cursor = (f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" dur="{TOTAL}s" '
                  f'repeatCount="indefinite" keyTimes="{vis_t}" values="{vis_v}"/>'
                  f'<rect class="blink" x="{X0}" y="{fmt(y - 14)}" width="9" height="19" fill="{G}">'
                  f'<animate attributeName="x" calcMode="discrete" dur="{TOTAL}s" repeatCount="indefinite" '
                  f'keyTimes="{times}" values="{cursor_x}"/></rect></g>')
        base_w = fmt(tw)
    else:
        wipe = 0.55
        clip_anim = (f'<animate attributeName="width" dur="{TOTAL}s" repeatCount="indefinite" '
                     f'keyTimes="0;{start / TOTAL:.5f};{(start + wipe) / TOTAL:.5f};1" '
                     f'values="0;0;{fmt(tw + 4)};{fmt(tw + 4)}"/>')
        cursor = ""
        base_w = fmt(tw + 4)

    return (
        f'<clipPath id="c{idx}"><rect x="{X0}" y="{fmt(y - 18)}" width="{base_w}" height="26">{clip_anim}</rect></clipPath>'
        f'<text clip-path="url(#c{idx})" x="{X0}" y="{fmt(y)}" font-size="{SIZE}" textLength="{fmt(tw)}" '
        f'lengthAdjust="spacing" xml:space="preserve">{spans}</text>{cursor}'
    )


def neural_net() -> str:
    r = rng("terminal-net")
    px, py, pw, ph = 690, 66, 284, 322
    layers = [4, 6, 6, 3]
    xs = [px + 42 + i * 66 for i in range(len(layers))]
    nodes = []
    for li, count in enumerate(layers):
        top, bottom = py + 70, py + ph - 52
        gap = (bottom - top) / (count - 1) if count > 1 else 0
        nodes.append([(xs[li], top + gap * k) for k in range(count)])

    out = [f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{C["panel2"]}" fill-opacity=".55" stroke="{C["line_dim"]}"/>',
           f'<text x="{px + 16}" y="{py + 26}" font-size="11" letter-spacing="2" fill="{C["muted"]}">VISION.MODEL</text>',
           f'<circle class="pulse" cx="{px + pw - 22}" cy="{py + 22}" r="4" fill="{G}"/>',
           f'<text x="{px + pw - 32}" y="{py + 26}" font-size="11" text-anchor="end" fill="{C["green_soft"]}">ACTIVE</text>']
    for a, b in zip(nodes, nodes[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                out.append(f'<path d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}" stroke="{G}" stroke-opacity=".13" stroke-width="1"/>')
    # signals hop through all four layers
    for s in range(9):
        picks = [r.choice(layer) for layer in nodes]
        d = "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in picks)
        dur = r.uniform(2.4, 3.6)
        out.append(
            f'<circle r="3" fill="#eafff0"><animateMotion path="{d}" dur="{dur:.2f}s" begin="{-r.uniform(0, dur):.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.12;.86;1" dur="{dur:.2f}s" begin="0s" repeatCount="indefinite"/></circle>'
        )
    for li, layer in enumerate(nodes):
        for (x, y) in layer:
            out.append(f'<circle class="nd" style="animation-delay:{li * .45:.2f}s" cx="{fmt(x)}" cy="{fmt(y)}" r="6" fill="{C["bg"]}" stroke="{G}" stroke-width="1.6"/>')
    for li, label in enumerate(("input", "hidden", "hidden", "output")):
        out.append(f'<text x="{xs[li]}" y="{py + ph - 22}" font-size="10" text-anchor="middle" fill="{C["muted"]}">{label}</text>')
    return "\n".join(out)


def build() -> str:
    css = """
.nd{animation:nd 2.8s ease-in-out infinite}
@keyframes nd{0%,100%{fill:#0d1117}45%{fill:#00ff41}}
"""
    parts = [svg_open(W, H, "About Simon Leo Alexander — terminal",
                      "A terminal that types: whoami, cat about.txt, ls ~/focus and echo $STATUS, next to an animated neural network.", css)]
    parts.append(window_chrome(W, H, "simon@github: ~/profile", "zsh — 80×24"))
    parts.append(f'<g><animate attributeName="opacity" dur="{TOTAL}s" repeatCount="indefinite" '
                 f'keyTimes="0;.9;.945;.985;1" values="1;1;0;0;1"/>')
    parts.extend(line_svg(i, k, s, t) for i, (k, s, t) in enumerate(SCRIPT))
    parts.append("</g>")
    parts.append(neural_net())  # stays visible while the shell clears and restarts
    parts.append(svg_close())
    return "\n".join(parts)


if __name__ == "__main__":
    write_svg("terminal.svg", build())
