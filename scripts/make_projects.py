#!/usr/bin/env python3
"""assets/project-*.svg — one animated card per project (each is linkable from the README)."""

from theme import C, USERNAME, border_runner, esc, fmt, icon_color, load_icons, rng, svg_close, svg_open, write_svg

W, H = 480, 218

PROJECTS = [
    {
        "file": "project-gods-eye.svg", "repo": "God-s-Eye", "title": "AI Pallet & Case Detection",
        "lines": ["Computer-vision system that detects pallets and", "cases from video streams using YOLO + TensorRT."],
        "tags": ["Python", "YOLO", "OpenCV", "TensorRT", "PyAV", "Flask", "Electron", "MongoDB"],
        "icons": ["python", "opencv"], "accent": C["green"],
    },
    {
        "file": "project-currency-detector.svg", "repo": "ai-currency-object-detector",
        "title": "AI Currency Object Detector",
        "lines": ["Detects currency with a TensorFlow + OpenCV", "pipeline, served through a Streamlit app."],
        "tags": ["Python", "TensorFlow", "OpenCV", "Streamlit"],
        "icons": ["tensorflow", "opencv"], "accent": C["blue"],
    },
    {
        "file": "project-plate-smart.svg", "repo": "Plate_Smart", "title": "Plate Smart",
        "lines": ["A modern product experience crafted with React,", "Vite and Tailwind CSS."],
        "tags": ["React", "Vite", "Tailwind CSS"],
        "icons": ["react", "vite"], "accent": C["purple"],
    },
    {
        "file": "project-mylifeline.svg", "repo": "MyLifeLine", "title": "My LifeLine",
        "lines": ["Safety-focused platform with a React front end", "and a Node.js, Express & MongoDB backend."],
        "tags": ["React", "Node.js", "Express", "MongoDB"],
        "icons": ["react", "nodejs"], "accent": C["red"],
    },
    {
        "file": "project-nexora-2026.svg", "repo": "Nexora-2026", "title": "Nexora 2026",
        "lines": ["A motion-rich web experience animated with GSAP", "and Framer Motion on a React + Vite stack."],
        "tags": ["React", "Vite", "Tailwind CSS", "GSAP", "Framer Motion"],
        "icons": ["gsap", "react"], "accent": C["amber"],
    },
    {
        "file": "project-kwickstack.svg", "repo": "kwickstack", "title": "KwickStack",
        "lines": ["A clean, fast and modern web interface built", "with React, Vite and Tailwind CSS."],
        "tags": ["React", "Vite", "Tailwind CSS"],
        "icons": ["react", "tailwind"], "accent": C["teal"],
    },
]


def pills(tags, x0, y, accent, limit) -> str:
    out, x = [], x0
    shown = 0
    for i, tag in enumerate(tags):
        w = len(tag) * 7.1 + 18
        remaining = len(tags) - i
        reserve = 0 if remaining == 1 else 40  # keep room for a "+N" pill
        if x + w > limit - reserve and remaining > 1:
            break
        out.append(f'<rect x="{fmt(x)}" y="{y}" width="{fmt(w)}" height="24" rx="12" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".45"/>'
                   f'<text x="{fmt(x + w / 2)}" y="{y + 16}" font-size="11.5" text-anchor="middle" fill="{C["text"]}">{esc(tag)}</text>')
        x += w + 8
        shown += 1
    if shown < len(tags):
        extra = len(tags) - shown
        label = f"+{extra}"
        w = len(label) * 7.1 + 18
        out.append(f'<rect x="{fmt(x)}" y="{y}" width="{fmt(w)}" height="24" rx="12" fill="none" stroke="{C["faint"]}" stroke-dasharray="3 3"/>'
                   f'<text x="{fmt(x + w / 2)}" y="{y + 16}" font-size="11.5" text-anchor="middle" fill="{C["muted"]}">{label}</text>')
    return "".join(out)


def build(project: dict, icons: dict) -> str:
    a = project["accent"]
    r = rng(project["file"])
    css = """
.arrow{animation:nudge 1.6s ease-in-out infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
.rise{animation:rise .7s cubic-bezier(.2,.8,.3,1) backwards}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
"""
    url_path = f"{USERNAME}/{project['repo']}"
    p = [svg_open(W, H, f"{project['title']} — project card",
                  f"{project['title']}: {' '.join(project['lines'])} Built with {', '.join(project['tags'])}.", css)]
    p.append(f"""<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{a}" stroke-opacity=".07"/></pattern>
<linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}" stop-opacity=".16"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{C['panel']}" stroke="{C['line_dim']}"/>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect y="0" width="90" height="{H}" fill="url(#sweep)" x="-90"><animate attributeName="x" values="-90;{W};{W}" keyTimes="0;.62;1" dur="{r.uniform(6.2, 7.6):.1f}s" begin="{r.uniform(0, 3):.1f}s" repeatCount="indefinite"/></rect>
<rect x="0" y="0" width="5" height="{H}" fill="{a}"/>
</g>
{border_runner(1, 1, W - 2, H - 2, 11, a, dur=r.uniform(6, 8), dash=150, width=2, begin=-r.uniform(0, 6))}
<g class="rise">
<text x="26" y="34" font-size="11.5" fill="{C['muted']}">~/{esc(url_path)}</text>""")
    # tech icons top-right
    for i, key in enumerate(project["icons"]):
        ic = icons[key]
        x = W - 30 - 22 - i * 32
        p.append(f'<g transform="translate({x} 18) scale(.92)" fill="{icon_color(ic["hex"])}"><path d="{ic["path"]}"/></g>')
    p.append(f"""<text x="26" y="76" font-size="21" font-weight="700" fill="{a}">{esc(project['title'])}</text>
<text x="26" y="106" font-size="13" fill="#a9b7c6">{esc(project['lines'][0])}</text>
<text x="26" y="126" font-size="13" fill="#a9b7c6">{esc(project['lines'][1])}</text>
{pills(project['tags'], 26, 146, a, W - 26)}
<circle class="pulse" cx="32" cy="196" r="3.5" fill="{a}"/>
<text x="43" y="200" font-size="11" fill="{C['muted']}" letter-spacing="1">PUBLIC REPO</text>
<text x="{W - 46}" y="200" font-size="11.5" text-anchor="end" fill="{a}" letter-spacing="1">VIEW REPO</text>
<text class="arrow" x="{W - 40}" y="200" font-size="12" fill="{a}">→</text>
</g>""")
    p.append(svg_close())
    return "\n".join(p)


def main() -> None:
    icons = load_icons()
    for project in PROJECTS:
        write_svg(project["file"], build(project, icons))


if __name__ == "__main__":
    main()
