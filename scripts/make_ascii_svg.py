from pathlib import Path
from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("assets/simon-ascii.svg")

# ASCII density ramp
RAMP = " .`:-=+*cs#%@"

# Character grid
WIDTH = 100
HEIGHT = 53

# SVG settings
FONT_SIZE = 8
CHAR_WIDTH = 6.2
LINE_HEIGHT = 8.5

SVG_WIDTH = int(WIDTH * CHAR_WIDTH)
SVG_HEIGHT = int(HEIGHT * LINE_HEIGHT)


def brightness_to_char(value):
    index = int((value / 255) * (len(RAMP) - 1))
    return RAMP[index]


def load_image():
    image = Image.open(INPUT).convert("L")

    # Preserve portrait proportions while compensating
    # for terminal characters being taller than wide.
    image.thumbnail((WIDTH, HEIGHT))

    canvas = Image.new(
        "L",
        (WIDTH, HEIGHT),
        255
    )

    x = (WIDTH - image.width) // 2
    y = (HEIGHT - image.height) // 2

    canvas.paste(image, (x, y))

    return canvas


def escape_xml(text):
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def generate_svg():
    if not INPUT.exists():
        raise FileNotFoundError(
            "source-prepped.png not found. "
            "Run prep_photo.py first."
        )

    image = load_image()

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{SVG_WIDTH}"
        height="{SVG_HEIGHT}"
        viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'''
    )

    svg.append("""
<style>
.ascii {
    font-family: "Courier New", monospace;
    font-size: 8px;
    font-weight: 600;
    fill: #8b949e;
}

@keyframes reveal {
    from {
        opacity: 0;
        transform: translateX(-10px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.row {
    opacity: 0;
    animation: reveal 0.45s ease-out forwards;
}
</style>
""")

    svg.append(
        '<rect width="100%" height="100%" fill="#0d1117"/>'
    )

    for y in range(HEIGHT):

        characters = []

        for x in range(WIDTH):
            value = image.getpixel((x, y))
            char = brightness_to_char(value)

            characters.append(char)

        line = "".join(characters)

        # Skip completely blank lines
        if not line.strip():
            continue

        escaped = escape_xml(line)

        y_position = (y + 1) * LINE_HEIGHT

        delay = y * 0.045

        svg.append(
            f'''
<text
    class="ascii row"
    x="4"
    y="{y_position}"
    style="animation-delay:{delay:.3f}s"
>{escaped}</text>
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
    generate_svg()