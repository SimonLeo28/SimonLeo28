#!/usr/bin/env python3
"""assets/stack.svg — brand-icon tech wall with a sweeping scan and a live ticker.

Brand icon paths come from the CC0 `simple-icons` set (scripts/icons.json),
embedded directly so nothing is fetched at view time.
"""

from theme import C, esc, fmt, icon_color, load_icons, svg_close, svg_open, window_chrome, write_svg

W = 1000
CHIP_W, CHIP_H, GAP = 124, 50, 10
CHIP_X0 = 176
ROW_Y0, ROW_PITCH = 72, 68

# AWS's mark is not part of simple-icons any more, so it gets a neutral cloud glyph.
CLOUD = {"title": "AWS", "hex": "FF9900",
         "path": "M17.5 19H7a5 5 0 0 1-.9-9.92A6 6 0 0 1 17.6 8.3 5.4 5.4 0 0 1 17.5 19z"}

ROWS = [
    ("// LANGUAGES", [("python", "Python"), ("typescript", "TypeScript"), ("javascript", "JavaScript"), ("html5", "HTML5")]),
    ("// FRONTEND", [("react", "React"), ("nextjs", "Next.js"), ("tailwind", "Tailwind"), ("vite", "Vite"), ("gsap", "GSAP")]),
    ("// BACKEND", [("nodejs", "Node.js"), ("express", "Express"), ("flask", "Flask"), ("mongodb", "MongoDB"),
                    ("postgresql", "PostgreSQL"), ("redis", "Redis")]),
    ("// AI_VISION", [("yolo", "YOLO"), ("opencv", "OpenCV"), ("tensorflow", "TensorFlow"), ("pytorch", "PyTorch"),
                      ("tensorrt", "TensorRT"), ("streamlit", "Streamlit")]),
    ("// DEVOPS", [("docker", "Docker"), ("git", "Git"), ("linux", "Linux"), ("aws", "AWS"), ("electron", "Electron")]),
]

TICKER = ("PYTHON • TYPESCRIPT • JAVASCRIPT • REACT • NEXT.JS • TAILWIND • NODE.JS • EXPRESS • MONGODB • "
          "YOLO • OPENCV • TENSORFLOW • PYTORCH • TENSORRT • PYAV • FLASK • ELECTRON • STREAMLIT • "
          "DOCKER • LINUX • AWS • GSAP • FRAMER MOTION • ")


def chip(icon: dict, label: str, x: float, y: float, idx: int) -> str:
    color = icon_color(icon["hex"])
    # outer <g> positions, inner <g> animates: a CSS transform would otherwise
    # override the SVG transform attribute and throw the chip to the origin.
    return (
        f'<g transform="translate({fmt(x)} {fmt(y)})"><g class="chip" style="animation-delay:{idx * 0.05:.2f}s">'
        f'<rect class="cb" style="animation-delay:{idx * 0.16 + 2.6:.2f}s" width="{CHIP_W}" height="{CHIP_H}" rx="9"/>'
        f'<g transform="translate(13 14) scale(.92)" fill="{color}"><path d="{icon["path"]}"/></g>'
        f'<text x="43" y="30" font-size="12.5" fill="{C["text"]}">{esc(label)}</text></g></g>'
    )


def build() -> str:
    icons = load_icons()
    icons["aws"] = CLOUD
    total = sum(len(r[1]) for r in ROWS)
    rows_bottom = ROW_Y0 + len(ROWS) * ROW_PITCH
    H = rows_bottom + 66

    ticker_w = len(TICKER) * 8.0
    css = f"""
.chip{{transform-box:fill-box;transform-origin:center;animation:pop .55s cubic-bezier(.2,.9,.3,1.25) backwards}}
@keyframes pop{{from{{opacity:0;transform:translateY(14px) scale(.7)}}to{{opacity:1;transform:none}}}}
.cb{{fill:{C['panel2']};stroke:{C['line']};animation:scan 7.5s ease-in-out infinite}}
@keyframes scan{{0%,9%,100%{{stroke:{C['line']};fill:{C['panel2']}}}3.5%{{stroke:#00ff41;fill:#0b2a17}}}}
.tick{{animation:tick 46s linear infinite}}
@keyframes tick{{from{{transform:translateX(0)}}to{{transform:translateX(-{fmt(ticker_w)}px)}}}}
"""
    p = [svg_open(W, H, "Tech stack",
                  "Languages, frontend, backend, AI and vision, and DevOps tools: "
                  + ", ".join(lbl for _, items in ROWS for _, lbl in items) + ".", css)]
    p.append(window_chrome(W, H, "tech_stack.exe", f"{total}/{total} modules"))
    p.append(f"""<defs>
<clipPath id="tk"><rect x="18" y="{rows_bottom + 14}" width="{W - 36}" height="34" rx="8"/></clipPath>
<linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="{C['panel']}"/><stop offset="1" stop-color="{C['panel']}" stop-opacity="0"/></linearGradient>
<linearGradient id="fadeR" x1="1" x2="0"><stop offset="0" stop-color="{C['panel']}"/><stop offset="1" stop-color="{C['panel']}" stop-opacity="0"/></linearGradient>
</defs>""")
    idx = 0
    for r, (label, items) in enumerate(ROWS):
        y = ROW_Y0 + r * ROW_PITCH
        p.append(f'<text x="32" y="{y + 30}" font-size="12.5" fill="{C["green"]}" letter-spacing="1">{esc(label)}</text>')
        for c, (key, name) in enumerate(items):
            p.append(chip(icons[key], name, CHIP_X0 + c * (CHIP_W + GAP), y, idx))
            idx += 1

    ty = rows_bottom + 14
    p.append(f'<rect x="18" y="{ty}" width="{W - 36}" height="34" rx="8" fill="#070b0f" stroke="{C["line_dim"]}"/>')
    p.append(f'<g clip-path="url(#tk)"><g class="tick" fill="{C["green_soft"]}" font-size="13" fill-opacity=".85">'
             f'<text x="24" y="{ty + 22}" textLength="{fmt(ticker_w)}" lengthAdjust="spacing" xml:space="preserve">{esc(TICKER)}</text>'
             f'<text x="{fmt(24 + ticker_w)}" y="{ty + 22}" textLength="{fmt(ticker_w)}" lengthAdjust="spacing" xml:space="preserve">{esc(TICKER)}</text>'
             f'</g><rect x="18" y="{ty}" width="70" height="34" fill="url(#fadeL)"/>'
             f'<rect x="{W - 88}" y="{ty}" width="70" height="34" fill="url(#fadeR)"/></g>')
    p.append(svg_close())
    return "\n".join(p)


if __name__ == "__main__":
    write_svg("stack.svg", build())
