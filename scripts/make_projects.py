from pathlib import Path

OUTPUT = Path("assets/projects-showcase.svg")

WIDTH = 1200
HEIGHT = 620


PROJECTS = [
    (
        "AI Pallet & Case Detection",
        "Python · YOLO · OpenCV · PyAV · TensorRT · Flask · Electron · MongoDB",
        "#2dd4bf",
    ),
    (
        "AI Currency Object Detector",
        "Python · TensorFlow · OpenCV · Streamlit · Computer Vision",
        "#60a5fa",
    ),
    (
        "Plate Smart",
        "React · Vite · Tailwind · Product Experience",
        "#a78bfa",
    ),
    (
        "My LifeLine",
        "React · Node.js · Express · MongoDB · Safety Systems",
        "#f472b6",
    ),
    (
        "Nexora 2026",
        "React · Vite · Tailwind · GSAP · Framer Motion",
        "#f59e0b",
    ),
    (
        "KwickStack",
        "React · Vite · Tailwind · Modern Web UI",
        "#34d399",
    ),
]


def escape_xml(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg():
    card_width = 330
    card_height = 170
    x_positions = [50, 420, 790]
    y_positions = [90, 290]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '<linearGradient id="darkBg" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#08131e" />',
        '<stop offset="100%" stop-color="#0f172a" />',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="24" fill="url(#darkBg)" stroke="#253447" />',
        '<text x="52" y="52" font-size="22" font-family="monospace" font-weight="700" fill="#dbeafe">FEATURED PROJECTS</text>',
        '<text x="52" y="76" font-size="13" font-family="monospace" fill="#94a3b8">AI + full stack portfolio</text>',
    ]

    for index, (title, stack, accent) in enumerate(PROJECTS):
        col = index % 3
        row = index // 3
        x = x_positions[col]
        y = y_positions[row]

        svg.append(f'<g>')
        svg.append(f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="18" fill="#0b1724" stroke="{accent}" stroke-width="1.2" />')
        svg.append(f'<rect x="{x + 18}" y="{y + 20}" width="60" height="4" rx="2" fill="{accent}" />')
        svg.append(f'<text x="{x + 18}" y="{y + 52}" font-size="23" font-family="Segoe UI, Arial, sans-serif" font-weight="700" fill="#f8fafc">{escape_xml(title)}</text>')
        svg.append(f'<text x="{x + 18}" y="{y + 94}" font-size="13" font-family="monospace" fill="#cbd5e1">{escape_xml(stack)}</text>')
        svg.append(f'<line x1="{x + 18}" y1="{y + 118}" x2="{x + 310}" y2="{y + 118}" stroke="#1e293b" />')
        svg.append(f'<text x="{x + 18}" y="{y + 148}" font-size="15" font-family="monospace" fill="{accent}">VIEW PROJECT →</text>')
        svg.append('</g>')

    svg.append('</svg>')

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    build_svg()
