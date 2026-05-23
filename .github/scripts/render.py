#!/usr/bin/env python3
"""Render badges-{light,dark}.svg + splice README region from classified.json."""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html import escape
from typing import Iterable

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = ROOT / ".github" / "schemas" / "classified.schema.json"
README_PATH = ROOT / "README.md"
SVG_PATHS = {"light": ROOT / "badges-light.svg", "dark": ROOT / "badges-dark.svg"}

GLOW_IDS = ["cyan", "teal", "green", "yellow", "magenta", "purple", "orange"]
TEXT_Y = [42, 98, 154, 210, 266, 322, 378]
RECT_Y = [25, 81, 137, 193, 249, 305, 361]
SEP_Y = [62, 118, 174, 230, 286, 342]

COLORS = {
    "dark":  ["#00f0ff", "#00ffa0", "#39ff14", "#ffee00", "#ff00aa", "#bd00ff", "#ff6a00"],
    "light": ["#006080", "#007744", "#1a7a00", "#8a7000", "#aa0066", "#7700aa", "#cc5500"],
}
STROKES = {
    "dark":  COLORS["dark"],
    "light": ["#0088aa", "#009966", "#2a9a10", "#aa8800", "#cc0088", "#9900cc", "#dd6600"],
}

THEMES = {
    "dark": {
        "bg": "#0a0a0f",
        "grid_stroke": "rgba(0,240,255,0.04)",
        "pill_stroke_width": "1",
        "pill_opacity": "0.7",
        "sep_stroke_width": "0.3",
        "std_dev": "3",
    },
    "light": {
        "bg": "#f0f2f5",
        "grid_stroke": "rgba(0,100,140,0.06)",
        "pill_stroke_width": "1.2",
        "pill_opacity": "0.8",
        "sep_stroke_width": "0.4",
        "std_dev": "2",
    },
}

PILL_START_X = 200
PILL_MAX_X = 770
PILL_GAP = 10
PILL_HEIGHT = 24
PILL_RX = 12
CAT_TEXT_X = 30
ROW_X_LEFT = 30
ROW_X_RIGHT = 770


def pill_width(label: str) -> int:
    # 7 px/char assumes the schema's ASCII character class rendered in Courier New
    # (monospace). If the schema ever permits wider unicode, revisit this formula
    # before the renderer silently overflows past PILL_MAX_X.
    return max(55, len(label) * 7 + 16)


def lay_out_pills(pills: Iterable[str]):
    layouts = []
    x = PILL_START_X
    for label in pills:
        w = pill_width(label)
        layouts.append((x, w))
        x += w + PILL_GAP
    last_x, last_w = layouts[-1]
    if last_x + last_w > PILL_MAX_X:
        raise ValueError(
            f"pill layout overflow: rightmost pill ends at {last_x + last_w} "
            f"(max {PILL_MAX_X}). pills={list(pills)}"
        )
    return layouts


def render_defs(std_dev: str) -> str:
    parts = []
    for gid in GLOW_IDS:
        parts.append(
            f'    <filter id="glow-{gid}" x="-20%" y="-20%" width="140%" height="140%">\n'
            f'      <feGaussianBlur stdDeviation="{std_dev}" result="blur" />\n'
            f'      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>\n'
            f'    </filter>'
        )
    return "  <defs>\n" + "\n".join(parts) + "\n  </defs>"


def render_row(idx: int, row: dict, theme: str) -> str:
    th = THEMES[theme]
    text_fill = COLORS[theme][idx]
    stroke = STROKES[theme][idx]
    glow = GLOW_IDS[idx]
    text_y = TEXT_Y[idx]
    rect_y = RECT_Y[idx]
    cat = escape(row["category"], quote=True)
    lines = [
        f'  <text x="{CAT_TEXT_X}" y="{text_y}" font-family="Courier New, monospace" '
        f'font-size="13" font-weight="bold" fill="{text_fill}" '
        f'filter="url(#glow-{glow})" letter-spacing="1">{cat}</text>'
    ]
    for (px, pw), label in zip(lay_out_pills(row["pills"]), row["pills"]):
        esc = escape(label, quote=True)
        text_x = px + pw // 2
        text_y_pill = rect_y + 16
        lines.append(
            f'  <rect x="{px}" y="{rect_y}" width="{pw}" height="{PILL_HEIGHT}" '
            f'rx="{PILL_RX}" fill="none" stroke="{stroke}" '
            f'stroke-width="{th["pill_stroke_width"]}" opacity="{th["pill_opacity"]}" />'
        )
        lines.append(
            f'  <text x="{text_x}" y="{text_y_pill}" font-family="Courier New, monospace" '
            f'font-size="11" fill="{text_fill}" text-anchor="middle">{esc}</text>'
        )
    if idx < len(SEP_Y):
        sep_y = SEP_Y[idx]
        lines.append(
            f'  <line x1="{ROW_X_LEFT}" y1="{sep_y}" x2="{ROW_X_RIGHT}" y2="{sep_y}" '
            f'stroke="{stroke}" stroke-width="{th["sep_stroke_width"]}" opacity="0.3" />'
        )
    return "\n".join(lines)


def render_svg(data: dict, theme: str) -> str:
    th = THEMES[theme]
    defs = render_defs(th["std_dev"])
    rows = "\n\n".join(render_row(i, row, theme) for i, row in enumerate(data["rows"]))
    return (
        f'<svg viewBox="0 0 800 420" width="800" height="420" xmlns="http://www.w3.org/2000/svg">\n'
        f'{defs}\n\n'
        f'  <rect width="800" height="420" rx="8" fill="{th["bg"]}" />\n\n'
        f'  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">\n'
        f'    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{th["grid_stroke"]}" stroke-width="0.5" />\n'
        f'  </pattern>\n'
        f'  <rect width="800" height="420" fill="url(#grid)" />\n\n'
        f'{rows}\n'
        f'</svg>\n'
    )


def render_readme_region(data: dict) -> str:
    bullets = []
    for row in data["rows"]:
        title = row["bullet"]["title"].strip()
        body = row["bullet"]["body"].strip()
        bullets.append(f"- **{title}** - {body}")
    exploring = data["currently_exploring"].strip()
    return (
        "---\n\n"
        + "\n".join(bullets)
        + "\n\n---\n\n"
        + f"`📡 Currently exploring {exploring}`"
    )


def splice_readme(text: str, region: str) -> str:
    marker_pat = re.compile(
        r"<!-- BADGE-BOT:START -->.*?<!-- BADGE-BOT:END -->",
        flags=re.DOTALL,
    )
    if not marker_pat.search(text):
        raise SystemExit(
            "README is missing <!-- BADGE-BOT:START --> / <!-- BADGE-BOT:END --> markers. "
            "One-time setup not done."
        )
    return marker_pat.sub(
        f"<!-- BADGE-BOT:START -->\n{region}\n<!-- BADGE-BOT:END -->",
        text,
        count=1,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <classified.json>", file=sys.stderr)
        return 2
    data = json.loads(pathlib.Path(argv[1]).read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(data, schema)
    try:
        for theme, path in SVG_PATHS.items():
            svg = render_svg(data, theme)
            ET.fromstring(svg)   # well-formedness smoke check (not SVG schema)
            path.write_text(svg)
    except ValueError as e:
        print(f"render error: {e}", file=sys.stderr)
        return 1
    readme = README_PATH.read_text()
    README_PATH.write_text(splice_readme(readme, render_readme_region(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
