# Profile badge classifier

You are running inside a weekly GitHub Action on `dustfeather/dustfeather`. Your only job is to produce two files: `raw-inventory.json` and `classified.json`. A deterministic Python renderer takes `classified.json` and produces the SVG badges + README region. **You must never edit SVGs, README, or any file other than the two JSON files named above.**

## Inputs available

- `GH_TOKEN_DUSTFEATHER` — installation token for the `dustfeather` user account (read access to all `dustfeather/*` repos).
- `GH_TOKEN_ITGUYS` — installation token for the `ITGuys-RO` org (read access to all `ITGuys-RO/*` repos including private).
- `prior/classified.json` — last week's `classified.json` (may not exist on first run or if the prior artifact expired). Use this for stability: prefer prior category labels and bullet phrasings unless the underlying repo data has shifted meaningfully.
- `.github/schemas/classified.schema.json` — JSON Schema you must validate `classified.json` against before declaring done.

## Step 1 — Build `raw-inventory.json`

For each org enumeration, list non-archived, non-fork, non-empty repos. Skip these always: `dustfeather/dustfeather`, `dustfeather/.github`, `ITGuys-RO/.github`, and anything whose name ends in `-profile`.

Use `gh` with the matching token:

```bash
GH_TOKEN="$GH_TOKEN_DUSTFEATHER" gh repo list dustfeather \
  --json nameWithOwner,description,primaryLanguage,languages,repositoryTopics,pushedAt,isArchived,isFork,isEmpty \
  --limit 500 \
  > /tmp/df.json

GH_TOKEN="$GH_TOKEN_ITGUYS" gh repo list ITGuys-RO \
  --json nameWithOwner,description,primaryLanguage,languages,repositoryTopics,pushedAt,isArchived,isFork,isEmpty \
  --limit 500 \
  > /tmp/itg.json
```

For each kept repo, fetch any of these manifest files that exist (Contents API; silently skip 404s; truncate each to 4 KB):

```
package.json
requirements.txt
pyproject.toml
composer.json
pubspec.yaml
Cargo.toml
go.mod
Gemfile
Podfile
manifest.json
wrangler.jsonc
wrangler.toml
```

Use the matching token per repo's owner. Example:

```bash
GH_TOKEN="$GH_TOKEN_ITGUYS" gh api \
  "/repos/ITGuys-RO/<repo>/contents/package.json" \
  --jq '.content' 2>/dev/null | base64 -d | head -c 4096
```

Emit one JSON object per repo with: `name_with_owner`, `description`, `primary_language`, `languages` (map of language → bytes), `topics`, `pushed_at`, and `manifests` (map of filename → first 4 KB of content). Write the combined array to `raw-inventory.json`.

## Step 2 — Classify into `classified.json`

Schema is at `.github/schemas/classified.schema.json`. Required shape:

```json
{
  "schema_version": 1,
  "generated_at": "<RFC3339 UTC timestamp>",
  "rows": [
    {
      "category": "<UPPERCASE, max 32 chars, ASCII + & / + - >",
      "pills": ["<3 to 6 short labels, max 16 chars each>", ...],
      "bullet": {
        "title": "<sentence-case, single phrase>",
        "body": "<single sentence describing what this category covers, naming concrete tech and projects where public-friendly>"
      }
    }
    // exactly 7 rows
  ],
  "currently_exploring": "<short phrase, no leading emoji, max 200 chars>"
}
```

**Hard rules:**

- Exactly 7 rows. Color/glow/y-coord assignment is positional by index — the renderer hard-codes which row is cyan, which is orange, etc. You decide the categories; the renderer decides the visual treatment.
- Each row gets 3–6 pills. Each pill is 1–16 chars, ASCII-only, no slashes-with-spaces (use `Doc Mgmt`, not `Document Management`).
- Pill labels longer than ~14 chars risk row overflow at render time. The renderer asserts `rightmost pill x + width ≤ 770`; if your row violates, you must shorten pills or drop one.
- `bullet.body` is a single sentence describing what the category covers. Mention concrete tech and a couple of project names where public-friendly. **Never name a private repo by name** — only aggregated themes.
- `currently_exploring` is a short phrase. No leading emoji (the renderer adds the `📡` glyph). Update only if the inventory shows a clear new direction.

**Stability rule:** if `prior/classified.json` exists, do not rewrite category labels or bullet wording cosmetically. Change only when the underlying data has shifted enough that the prior label is misleading. Idempotent runs are the goal — cosmetic week-to-week churn is a bug.

## Step 3 — Validate

```bash
python -c "
import json, sys, jsonschema
data = json.load(open('classified.json'))
schema = json.load(open('.github/schemas/classified.schema.json'))
jsonschema.validate(data, schema)
print('OK')
"
```

If this fails, fix `classified.json` and rerun until it prints `OK`. Do not declare done until validation passes.

## Step 4 — Stop

Do nothing else. The next workflow step runs the renderer. **Do not** run the renderer. **Do not** touch `badges-*.svg` or `README.md`. **Do not** git commit anything.
