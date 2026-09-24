from pathlib import Path


OUTPUT = Path("assets/info-card.svg")

WIDTH = 540
HEIGHT = 430

lines = [
    ("USER", "Simon Leo Alexander"),
    ("ROLE", "AI & Full Stack Developer"),
    ("LOCATION", "Bengaluru, Karnataka"),
    ("STACK", "AI • Full Stack • Vision"),
    ("FRONTEND", "React • Next.js • Tailwind"),
    ("BACKEND", "Node.js • Express • Python"),
    ("AI / ML", "TensorFlow • PyTorch • YOLO"),
    ("VISION", "OpenCV • PyAV • TensorRT"),
    ("TOOLS", "AWS • Docker • Git • Linux"),
]


def escape_xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def create_svg():
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '<linearGradient id="panel" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#0b1220" />',
        '<stop offset="100%" stop-color="#0f172a" />',
        '</linearGradient>',
        '</defs>',
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="18" fill="url(#panel)" stroke="#233548" stroke-width="1.2" />',
        '<rect x="0" y="0" width="540" height="46" rx="18" fill="#0d1724" stroke="#233548" stroke-width="1.2" />',
        '<circle cx="20" cy="23" r="5" fill="#f87171" />',
        '<circle cx="38" cy="23" r="5" fill="#fbbf24" />',
        '<circle cx="56" cy="23" r="5" fill="#4ade80" />',
        '<text x="82" y="30" font-size="15" font-family="monospace" fill="#7dd3fc">simon@github ~ $ whoami</text>',
        '<text x="22" y="82" font-size="12" font-family="monospace" fill="#8ba0b6">$ system --info</text>',
    ]

    start_y = 108
    for index, (key, value) in enumerate(lines):
        y = start_y + index * 28
        svg.append(
            f'<text x="22" y="{y}" font-size="11" font-family="monospace" fill="#7dd3fc" font-weight="700">{escape_xml(key)}</text>'
        )
        svg.append(
            f'<text x="150" y="{y}" font-size="12" font-family="monospace" fill="#e2e8f0">{escape_xml(value)}</text>'
        )

    svg.extend([
        '<text x="22" y="398" font-size="12" font-family="monospace" fill="#8ba0b6">$ status: building intelligent software...</text>',
        '<rect x="22" y="406" width="240" height="8" rx="4" fill="#0b1420" stroke="#263b4d" stroke-width="1" />',
        '<rect x="26" y="410" width="160" height="4" rx="2" fill="#34d399" opacity="0.9">',
        '<animate attributeName="width" values="160;210;160" dur="2.6s" repeatCount="indefinite" />',
        '</rect>',
        '</svg>',
    ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    create_svg()