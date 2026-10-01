"""Shared theme + helpers for every generated profile asset.

Everything the README shows is a self-contained SVG written by the
`make_*.py` scripts in this folder.  No third-party image services are
used, so nothing on the profile can break because somebody else's
server is down or rate-limited.

Rules every SVG follows (so it renders + animates on github.com):
  * no <script>, no <foreignObject>, no external URLs
  * system font stack only (webfonts cannot load inside <img> SVGs)
  * the *resting* state of every element is the finished/visible state;
    animations only borrow a hidden "from" state, so a browser that
    disables animation still shows a complete picture
  * output is deterministic (seeded RNG, no timestamps besides the
    data-sync date) so the daily bot commit only happens on real changes
"""

from __future__ import annotations

import html
import json
import math
import random
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = ROOT / "data"

USERNAME = "SimonLeo28"
DISPLAY_NAME = "Simon Leo Alexander"

# ── palette ────────────────────────────────────────────────────────────
C = {
    "bg": "#0d1117",
    "panel": "#0a0f14",
    "panel2": "#0f1720",
    "line": "#194569",
    "line_dim": "#102a43",
    "green": "#00e5ff",
    "green_soft": "#80f2ff",
    "green_dim": "#0a3654",
    "blue": "#79c0ff",
    "purple": "#d2a8ff",
    "amber": "#f0b429",
    "red": "#ff7b72",
    "teal": "#56d4dd",
    "cyan": "#00e5ff",
    "magenta": "#ff2bd6",
    "text": "#c9d1d9",
    "white": "#e6edf3",
    "muted": "#8b949e",
    "faint": "#4d5966",
}

FONT = (
    "'JetBrains Mono','Fira Code','SF Mono',SFMono-Regular,ui-monospace,"
    "Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
)

# average advance width of the monospace fallbacks, as a fraction of size
CHAR_W = 0.61


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def rng(name: str) -> random.Random:
    """Deterministic RNG per asset name."""
    return random.Random(f"{USERNAME}:{name}")


def fmt(n: float) -> str:
    """Compact float formatting for SVG attribute values."""
    text = f"{n:.2f}".rstrip("0").rstrip(".")
    return text if text not in ("-0", "") else "0"


def text_w(text: str, size: float, factor: float = CHAR_W) -> float:
    return len(text) * size * factor


# ── data ───────────────────────────────────────────────────────────────
def load_json(name: str, default=None):
    path = DATA / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_icons() -> dict:
    return json.loads((ROOT / "scripts" / "icons.json").read_text(encoding="utf-8"))


def icon_color(hex_code: str) -> str:
    """Brand colour, lifted when it would vanish on the dark background."""
    r, g, b = (int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#e6edf3" if luminance < 0.32 else f"#{hex_code}"


# ── svg scaffolding ────────────────────────────────────────────────────
BASE_CSS = f"""
svg{{font-family:{FONT}}}
text{{font-family:{FONT}}}
.blink{{animation:blink 1.06s steps(1,end) infinite}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.28}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def svg_open(width: int, height: int, title: str, desc: str, css: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">\n'
        f'<title id="t">{esc(title)}</title>\n<desc id="d">{esc(desc)}</desc>\n'
        f"<style>{BASE_CSS}{css}</style>\n"
    )


def svg_close() -> str:
    return "</svg>\n"


FORBIDDEN = ("<script", "<foreignobject", "http://", "https://", "@import", "javascript:")


def write_svg(name: str, content: str) -> Path:
    """Validate + write an SVG. Raises on anything GitHub would choke on."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    body = content.replace('xmlns="http://www.w3.org/2000/svg"', "")
    lowered = body.lower()
    for bad in FORBIDDEN:
        if bad in lowered:
            raise ValueError(f"{name}: forbidden construct {bad!r}")
    etree.fromstring(content.encode("utf-8"))  # must be well-formed XML
    ids = [el.get("id") for el in etree.fromstring(content.encode()).iter() if el.get("id")]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"{name}: duplicate ids {sorted(dupes)}")
    path = ASSETS / name
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote assets/{name}  ({path.stat().st_size / 1024:.1f} KB)")
    return path


def window_chrome(width: int, height: int, title: str, right: str = "", accent: str | None = None) -> str:
    """macOS-style terminal window frame used by several panels."""
    accent = accent or C["line"]
    out = [
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="14" fill="{C["panel"]}" stroke="{accent}"/>',
        f'<path d="M.5 44.5H{width - .5}" stroke="{C["line_dim"]}"/>',
        f'<path d="M.5 44.5V15a14.5 14.5 0 0 1 14.5-14.5H{width - 15}a14.5 14.5 0 0 1 14.5 14.5v29.5z" fill="{C["panel2"]}" opacity=".9"/>',
        f'<circle cx="26" cy="23" r="6" fill="#ff5f56"/><circle cx="48" cy="23" r="6" fill="#ffbd2e"/><circle cx="70" cy="23" r="6" fill="#27c93f"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="13" fill="{C["muted"]}">{esc(title)}</text>',
    ]
    if right:
        out.append(
            f'<text x="{width - 24}" y="28" text-anchor="end" font-size="12" fill="{C["faint"]}">{esc(right)}</text>'
        )
    return "\n".join(out)


def perimeter(w: float, h: float, r: float) -> float:
    return 2 * (w - 2 * r) + 2 * (h - 2 * r) + 2 * math.pi * r


def border_runner(x, y, w, h, r, color, dur=7.0, dash=200, width=2, begin=0.0, opacity=1.0) -> str:
    """A bright streak that endlessly circles a rounded rectangle."""
    p = perimeter(w, h, r)
    return (
        f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{fmt(r)}" '
        f'fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-dasharray="{fmt(dash)} {fmt(p - dash)}" opacity="{opacity}">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-{fmt(p)}" '
        f'dur="{fmt(dur)}s" begin="{fmt(begin)}s" repeatCount="indefinite"/></rect>'
    )


def typing_timeline(n_chars: int, char_w: float, total: float, start: float,
                    type_dur: float, hold: float, erase_dur: float, erase_steps: int = 8):
    """Key times + widths for a discrete type / hold / erase cycle.

    Returns (key_times, widths, end_time).  Suitable for a SMIL <animate
    calcMode="discrete"> driving a clip-rect width (or a cursor x).
    """
    pts = [(0.0, 0.0)]
    dt = type_dur / n_chars
    for k in range(1, n_chars + 1):
        pts.append((start + k * dt, k * char_w))
    erase_start = start + type_dur + hold
    for j in range(1, erase_steps + 1):
        chars = round(n_chars * (1 - j / erase_steps))
        pts.append((erase_start + j * erase_dur / erase_steps, chars * char_w))
    end = erase_start + erase_dur
    # strictly increasing key times
    cleaned = []
    for t, w in pts:
        if cleaned and t <= cleaned[-1][0]:
            t = cleaned[-1][0] + 1e-4
        cleaned.append((min(t, total), w))
    times = ";".join(f"{t / total:.5f}" for t, _ in cleaned)
    widths = ";".join(fmt(w) for _, w in cleaned)
    return times, widths, end
