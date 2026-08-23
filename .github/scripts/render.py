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

# Chips name capabilities, not the vendor providing them: "Serverless Workers",
# never "CF Workers" or "Lambda Functions". The consolidator prompt says so, but
# a prompt is advisory — an LLM drifts back to whatever the repo READMEs call
# things. These two tables make it structural: known vendor names are rewritten,
# and anything vendor-shaped that is NOT in the alias table hard-fails the run
# rather than shipping quietly. Prose bullets are exempt and stay concrete.
VENDOR_ALIASES = {
    # serverless compute
    "cf workers": "Serverless Workers",
    "cloudflare workers": "Serverless Workers",
    "workers": "Serverless Workers",
    "lambda": "Serverless Functions",
    "aws lambda": "Serverless Functions",
    "lambda functions": "Serverless Functions",
    "azure functions": "Serverless Functions",
    "cloud functions": "Serverless Functions",
    # managed data
    "d1": "Edge SQL",
    "kv": "Edge KV",
    "r2": "Object Storage",
    "s3": "Object Storage",
    "dynamodb": "Managed NoSQL",
    "firestore": "Managed NoSQL",
    "rds": "Managed Postgres",
    "supabase": "Managed Postgres",
    "planetscale": "Managed MySQL",
    # platforms
    "cloudflare": "Edge Platform",
    "vercel": "Edge Platform",
    "netlify": "Edge Platform",
    "fly.io": "Edge Platform",
    "heroku": "Cloud Platform",
    "aws": "Cloud Platform",
    "gcp": "Cloud Platform",
    "azure": "Cloud Platform",
}

# Vendor-shaped tokens. Anything matching after aliasing is an unmapped vendor
# name: fail loudly so the alias table gets extended, rather than shipping it.
VENDOR_TOKENS = re.compile(
    r"\b(cloudflare|cf|aws|amazon|gcp|google\s+cloud|azure|vercel|netlify|heroku"
    r"|fly\.io|render\.com|supabase|planetscale|firebase|dynamodb|lambda|s3|r2|d1)\b",
    flags=re.IGNORECASE,
)


# Categories are single uppercase words by schema pattern, so they alias
# separately: a category wants SERVERLESS SAAS, not the pill-shaped
# "Edge Platform SAAS" that word-substituting VENDOR_ALIASES would produce.
CATEGORY_ALIASES = {
    "cloudflare": "SERVERLESS",
    "vercel": "EDGE",
    "netlify": "EDGE",
    "lambda": "SERVERLESS",
    "aws": "CLOUD",
    "gcp": "CLOUD",
    "azure": "CLOUD",
    "heroku": "CLOUD",
}


def neutralize(label: str, *, kind: str, where: str) -> str:
    """Rewrite a vendor name to its capability equivalent, or refuse."""
    table = CATEGORY_ALIASES if kind == "category" else VENDOR_ALIASES
    out = table.get(label.strip().lower())
    if out is None:
        # Multi-word labels ("CLOUDFLARE SAAS", "Cloudflare Workers") alias word-wise.
        out = " ".join(table.get(w.lower(), w) for w in label.split())
    if kind == "category":
        out = out.upper()
    if VENDOR_TOKENS.search(out):
        raise SystemExit(
            f"vendor name in {where}: {label!r}. Chips name capabilities, not "
            f"vendors — add a mapping to "
            f"{'CATEGORY_ALIASES' if kind == 'category' else 'VENDOR_ALIASES'} "
            f"in render.py (e.g. 'Serverless Workers', 'Edge SQL', "
            f"'Object Storage') and re-run."
        )
    return out


def neutralize_rows(rows: list[dict]) -> list[dict]:
    out = []
    for i, row in enumerate(rows):
        out.append({
            **row,
            "category": neutralize(
                row["category"], kind="category", where=f"rows[{i}].category"
            ),
            "pills": [
                neutralize(p, kind="pill", where=f"rows[{i}].pills[{j}]")
                for j, p in enumerate(row["pills"])
            ],
        })
    return out


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
        render_chip_table(neutralize_rows(data["rows"]))
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
