from pathlib import Path

OUTPUT = Path("assets/stack-architecture.svg")

WIDTH = 1200
HEIGHT = 420


def escape_xml(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg():
    nodes = [
        (180, 80, "AI / ML", "YOLO\nPyTorch\nTensorFlow\nOpenCV", "#1d4ed8"),
        (470, 80, "BACKEND", "Node.js\nFlask\nREST APIs\nFast prototyping", "#8b5cf6"),
        (760, 80, "DATABASE", "MongoDB\nPostgreSQL\nSQL", "#10b981"),
        (1015, 80, "FRONTEND", "React\nNext.js\nTailwind\nUI systems", "#f59e0b"),
    ]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '<linearGradient id="panelGlow" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#09141f" />',
        '<stop offset="100%" stop-color="#0d172a" />',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="22" fill="url(#panelGlow)" stroke="#253447" />',
        '<g opacity="0.2">',
        '<path d="M 0 210 H 1200" stroke="#2dd4bf" stroke-width="1" />',
        '</g>',
    ]

    for x, y, title, body, color in nodes:
        svg.append(f'<g>')
        svg.append(f'<rect x="{x}" y="{y}" width="220" height="165" rx="18" fill="#0f172a" stroke="{color}" stroke-width="1.2" />')
        svg.append(f'<rect x="{x + 18}" y="{y + 15}" width="54" height="4" rx="2" fill="{color}" opacity="0.9" />')
        svg.append(f'<text x="{x + 20}" y="{y + 48}" font-size="18" font-family="monospace" font-weight="700" fill="#e2e8f0">{escape_xml(title)}</text>')
        body_lines = body.split("\n")
        for idx, line in enumerate(body_lines):
            svg.append(f'<text x="{x + 20}" y="{y + 82 + idx * 22}" font-size="14" font-family="monospace" fill="#cbd5e1">{escape_xml(line)}</text>')
        svg.append('</g>')

    for x in [390, 690, 970]:
        svg.append(f'<path d="M {x + 220} 160 C {x + 280} 160, {x + 280} 160, {x + 310} 160" stroke="#67e8f9" stroke-width="2" fill="none" opacity="0.7" />')
        svg.append(f'<path d="M {x + 310} 160 L {x + 325} 160 L {x + 315} 155 M {x + 325} 160 L {x + 315} 165" stroke="#67e8f9" stroke-width="2" fill="none" opacity="0.7" />')

    svg.extend([
        '<text x="510" y="330" font-size="24" font-family="monospace" fill="#cbd5e1">AI → BACKEND → DATABASE → FRONTEND</text>',
        '<text x="420" y="365" font-size="16" font-family="monospace" fill="#94a3b8">building systems that combine intelligence, infrastructure, and user experience</text>',
        '</svg>',
    ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    build_svg()
