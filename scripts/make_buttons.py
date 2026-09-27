#!/usr/bin/env python3
"""assets/btn-github.svg, btn-repos.svg, badge-open.svg — animated call-to-action buttons."""

from theme import C, border_runner, esc, fmt, load_icons, svg_close, svg_open, write_svg

H = 46


def button(file: str, label: str, width: int, color: str, icon: dict | None, title: str, linked: bool = True) -> None:
    css = f"""
.sh{{animation:sh 3.6s ease-in-out infinite}}
@keyframes sh{{0%,55%{{transform:translateX(-80px)}}100%{{transform:translateX({width + 80}px)}}}}
"""
    p = [svg_open(width, H, title, f"{label} button", css)]
    p.append(f"""<defs><clipPath id="b"><rect width="{width}" height="{H}" rx="9"/></clipPath>
<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset=".5" stop-color="{color}" stop-opacity=".28"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>
<rect x=".5" y=".5" width="{width - 1}" height="{H - 1}" rx="9" fill="{C['panel']}" stroke="{color}" stroke-opacity=".55"/>
<g clip-path="url(#b)"><rect class="sh" width="60" height="{H}" fill="url(#shine)" x="0"/></g>
{border_runner(1, 1, width - 2, H - 2, 8, color, dur=4.5, dash=90, width=2)}""")
    x = 22
    if icon:
        p.append(f'<g transform="translate({x} 11) scale(.96)" fill="{color}"><path d="{icon["path"]}"/></g>')
        x += 36
    else:
        p.append(f'<circle class="pulse" cx="{x + 4}" cy="23" r="5" fill="{color}"/>')
        x += 22
    tw = round(len(label) * 13 * 0.6, 1)
    p.append(f'<text x="{x}" y="28.5" font-size="13" font-weight="700" letter-spacing="1" fill="{C["white"]}" '
             f'textLength="{fmt(tw)}" lengthAdjust="spacing">{esc(label)}</text>')
    p.append(svg_close())
    write_svg(file, "\n".join(p))


def main() -> None:
    icons = load_icons()
    button("btn-github.svg", "> GITHUB", 178, C["green"], icons["github"], "Open GitHub profile")
    button("btn-repos.svg", "> REPOSITORIES", 232, C["blue"], icons["github"], "Browse all repositories")
    button("badge-open.svg", "OPEN TO OPPORTUNITIES", 300, C["amber"], None, "Status: open to opportunities")


if __name__ == "__main__":
    main()
