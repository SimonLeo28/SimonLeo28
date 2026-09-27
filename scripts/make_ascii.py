#!/usr/bin/env python3
"""assets/simon-ascii.svg — the prepped photo, rendered as animated ASCII art.

Reads source-prepped.png (produced by prep_photo.py) and converts brightness
to characters from a density ramp. The whole portrait fades/types in row by
row, and a soft green scanline sweeps over it afterwards.
"""

from pathlib import Path

from PIL import Image

from theme import C, esc, fmt, svg_close, svg_open, window_chrome, write_svg

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "source-prepped.png"

RAMP = " .`:-=+*cs#%@"
GRID_W, GRID_H = 100, 53
FONT_SIZE = 8
CHAR_W, LINE_H = 6.2, 8.5
PAD = 28
W = GRID_W * CHAR_W + PAD * 2
H = GRID_H * LINE_H + PAD * 2 + 46  # + window titlebar


def brightness_to_char(value: float) -> str:
    index = int((value / 255) * (len(RAMP) - 1))
    return RAMP[index]


def load_grid() -> list[str]:
    image = Image.open(INPUT).convert("L")
    image.thumbnail((GRID_W, GRID_H))
    canvas = Image.new("L", (GRID_W, GRID_H), 255)
    x, y = (GRID_W - image.width) // 2, (GRID_H - image.height) // 2
    canvas.paste(image, (x, y))
    pixels = canvas.load()
    rows = []
    for row in range(GRID_H):
        rows.append("".join(brightness_to_char(pixels[col, row]) for col in range(GRID_W)))
    return rows


def build() -> str:
    if not INPUT.exists():
        raise SystemExit(f"{INPUT} not found — run scripts/prep_photo.py first")
    rows = load_grid()

    css = f"""
.row{{opacity:0;animation:rowin .5s ease-out forwards}}
@keyframes rowin{{to{{opacity:1}}}}
.sweep{{animation:sweep 6s ease-in-out infinite}}
@keyframes sweep{{0%,100%{{transform:translateY(-10px)}}50%{{transform:translateY({GRID_H * LINE_H:.1f}px)}}}}
"""
    title_y = 46
    p = [svg_open(round(W), round(H), "Simon Leo Alexander — ASCII portrait",
                  "A photo of Simon rendered as ASCII art that fades in row by row, "
                  "with a soft scanline sweeping over it.", css)]
    p.append(window_chrome(round(W), round(H), "portrait.ascii", "100x53 · density-ramp render"))
    p.append(f'<g font-size="{FONT_SIZE}" font-family="ui-monospace,Consolas,monospace" fill="{C["green"]}" '
             f'transform="translate({PAD} {title_y + PAD})">')
    for r, row in enumerate(rows):
        delay = 0.35 + r * 0.024
        y = r * LINE_H + FONT_SIZE
        opacity = 0.22 + 0.68 * (sum(RAMP.index(ch) for ch in row) / (len(row) * (len(RAMP) - 1)))
        p.append(
            f'<text class="row" style="animation-delay:{delay:.2f}s" x="0" y="{fmt(y)}" '
            f'fill-opacity="{opacity:.2f}" xml:space="preserve">{esc(row)}</text>'
        )
    p.append(f'<rect class="sweep" x="0" y="-10" width="{fmt(GRID_W * CHAR_W)}" height="26" '
             f'fill="{C["green"]}" opacity=".07"/>')
    p.append("</g>")
    p.append(svg_close())
    return "\n".join(p)


if __name__ == "__main__":
    write_svg("simon-ascii.svg", build())
