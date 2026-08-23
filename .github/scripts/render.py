#!/usr/bin/env python3
"""Splice the README badge region from classified.json.

Stack rows render as a GitHub-flavored markdown table of <kbd> chips rather
than a pair of SVGs. GitHub strips <style> and style= from README HTML, so an
SVG used to be the only way to get pill/glow styling — at the cost of the tag
text being pixels: not selectable, not indexed, invisible to screen readers.
<kbd> is styled by GitHub's own stylesheet in both themes and stays real text.
"""
import json
import pathlib
import re
import sys
from html import escape

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SCHEMA_PATH = ROOT / ".github" / "schemas" / "classified.schema.json"
README_PATH = ROOT / "README.md"

CHIP_TABLE_HEADER = "| Domain | Stack |\n| --- | --- |"

def render_chip_row(row: dict) -> str:
    # The schema charset (category ^[A-Z0-9 &/+-]$, pills ^[A-Za-z0-9 ./+#-]$)
    # admits no '|', so no cell can break the table. '&' is still escaped so it
    # survives as a literal ampersand rather than an entity prefix.
    cat = escape(row["category"], quote=False)
    chips = " ".join(f"<kbd>{escape(p, quote=False)}</kbd>" for p in row["pills"])
    return f"| **{cat}** | {chips} |"


def render_chip_table(rows: list[dict]) -> str:
    return "\n".join([CHIP_TABLE_HEADER, *(render_chip_row(r) for r in rows)])


def render_readme_region(data: dict) -> str:
    bullets = []
    for row in data["rows"]:
        title = row["bullet"]["title"].strip()
        body = row["bullet"]["body"].strip()
        bullets.append(f"- **{title}** - {body}")
    exploring = data["currently_exploring"].strip()
    return (
        render_chip_table(data["rows"])
        + "\n\n---\n\n"
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
            "README is missing <!-- BADGE-BOT:START --> / <!-- BADGE-BOT:END --> "
            "markers. One-time setup not done."
        )
    return marker_pat.sub(
        lambda _: f"<!-- BADGE-BOT:START -->\n{region}\n<!-- BADGE-BOT:END -->",
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
    readme = README_PATH.read_text()
    README_PATH.write_text(splice_readme(readme, render_readme_region(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
