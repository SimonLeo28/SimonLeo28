from pathlib import Path


OUTPUT = Path("assets/info-card.svg")


WIDTH = 490
HEIGHT = 430


lines = [
    ("USER", "Simon Leo Alexander"),
    ("ROLE", "AI & Full Stack Developer"),
    ("EDUCATION", "Information Science Engineering"),
    ("FOCUS", "AI • Computer Vision • Web"),
    ("FRONTEND", "React • Next.js • Tailwind"),
    ("BACKEND", "Node.js • Express • Python"),
    ("DATABASE", "MongoDB"),
    ("AI/ML", "YOLO • OpenCV • TensorFlow"),
    ("CLOUD", "AWS"),
]


def escape_xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def create_svg():

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">'''
    )

    svg.append("""
<style>

.background {
    fill: #0d1117;
    stroke: #30363d;
    stroke-width: 1;
}

.header {
    fill: #161b22;
}

.title {
    font-family: monospace;
    font-size: 16px;
    font-weight: bold;
    fill: #58a6ff;
}

.prompt {
    font-family: monospace;
    font-size: 13px;
    fill: #8b949e;
}

.key {
    font-family: monospace;
    font-size: 13px;
    font-weight: bold;
    fill: #79c0ff;
}

.value {
    font-family: monospace;
    font-size: 13px;
    fill: #c9d1d9;
}

.dot {
    fill: #f85149;
}

.dot2 {
    fill: #d29922;
}

.dot3 {
    fill: #3fb950;
}

.row {
    opacity: 0;
    animation: appear 0.45s ease-out forwards;
}

@keyframes appear {

    from {
        opacity: 0;
        transform: translateY(7px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

</style>
""")

    # Main background
    svg.append(
        f'''
<rect
    class="background"
    x="0"
    y="0"
    width="{WIDTH}"
    height="{HEIGHT}"
    rx="12"
/>
'''
    )

    # Header
    svg.append(
        f'''
<rect
    class="header"
    x="0"
    y="0"
    width="{WIDTH}"
    height="48"
    rx="12"
/>
'''
    )

    # Fake terminal dots
    svg.append(
        '''
<circle class="dot" cx="20" cy="24" r="5"/>
<circle class="dot2" cx="38" cy="24" r="5"/>
<circle class="dot3" cx="56" cy="24" r="5"/>
'''
    )

    svg.append(
        '''
<text class="title" x="78" y="30">
simon@github ~ $ neofetch
</text>
'''
    )

    # Prompt
    svg.append(
        '''
<text class="prompt" x="22" y="75">
$ system --info
</text>
'''
    )

    start_y = 105
    spacing = 32

    for index, (key, value) in enumerate(lines):

        y = start_y + index * spacing
        delay = 0.4 + index * 0.12

        svg.append(
            f'''
<g
    class="row"
    style="animation-delay:{delay:.2f}s"
>
    <text
        class="key"
        x="22"
        y="{y}"
    >
        {escape_xml(key)}
    </text>

    <text
        class="value"
        x="145"
        y="{y}"
    >
        {escape_xml(value)}
    </text>
</g>
'''
        )

    svg.append(
        '''
<text
    class="prompt"
    x="22"
    y="402"
>
$ status: building intelligent software...
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

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    create_svg()