# Badge bot — local dev

The bot's runtime lives in `.github/workflows/refresh-badges.yml` and runs
weekly on the `arc-df-dustfeather` self-hosted runner. The renderer is pure
Python and runs anywhere with `python3` + `jsonschema`.

## Architecture (map/reduce)

```
enumerate-repos        →  GET /app/installations → per-install token → repo list
                          Emits {owner, repo, head_sha, is_public} + unique owners[]
download-prior-findings →  prior/findings/<owner>__<repo>.json from last week's bundle
classify-owner (waves)  →  Outer matrix max-parallel:1 over owners — sequential per-owner bursts
  └─ classify-owner.yml →  Inner matrix max-parallel:30 over that owner's repos
                            ├─ cache_gate.sh: prior head_sha == current → copy forward, skip Claude
                            └─ else Haiku reads README + tree + manifests → findings.json
consolidate             →  Sonnet bins all findings/ into classified.json (5-12 rows)
render-and-commit       →  python render.py classified.json → README region → commit
```

Enrollment is install-driven: install the GitHub App on a new org or user
account and it appears in the next `enumerate-repos` run with no workflow
edit. The skiplist (`owner==repo`, `*-profile`, `.github`) is the only
hardcoded filter.

Steady state on a quiet week: most matrix cells hit cache, only the consolidator
makes a Claude call. Cold start / many repos changed: full matrix runs.

## What the pieces are

| Path | What it does |
|---|---|
| `.github/workflows/refresh-badges.yml` | 5-job pipeline (enumerate → prior → per-owner waves → consolidate → render+commit) |
| `.github/workflows/classify-owner.yml` | Reusable workflow called once per owner wave; runs that owner's per-repo Haiku matrix |
| `.github/prompts/per-repo-findings.md` | Haiku prompt — one repo → `findings.json` |
| `.github/prompts/consolidate-classification.md` | Sonnet prompt — all findings → `classified.json` |
| `.github/schemas/findings.schema.json` | Per-repo output contract (one file per matrix cell) |
| `.github/schemas/classified.schema.json` | Final classification contract (5-12 rows; renderer input) |
| `.github/scripts/cache_gate.sh` | Per-matrix-cell cache check (prior head_sha vs current) |
| `.github/scripts/render.py` | Pure-Python renderer: classified.json → README splice |
| `.github/scripts/requirements.txt` | Single pinned dep: `jsonschema` (baked into runner image too) |

## Run the renderer locally

```bash
pip install -r .github/scripts/requirements.txt   # baked into runner image
python .github/scripts/render.py path/to/classified.json
```

Fixtures: `sample/classified.json` (7-row example) and `sample/findings/<owner>__<repo>.json`
(per-repo finding example). Schemas in `.github/schemas/` are authoritative for both.

The renderer overwrites the `<!-- BADGE-BOT:START -->`…`<!-- BADGE-BOT:END -->`
region of `README.md` in place. Stack rows render as a markdown table of
`<kbd>` chips — real selectable, indexable text. GitHub strips `<style>` and
`style=` from README HTML, so custom CSS is not an option; `<kbd>` is pilled
by GitHub's own stylesheet in both themes. If the README lacks those markers it exits non-zero — the one-time
README edit must already have happened. To test without mutating the real
README, copy the project to a temp dir first.

## Caching contract

- **Key:** the repo's `defaultBranchRef.target.oid` (head SHA of default branch) at
  enumerate time.
- **Hit:** `cache_gate.sh` finds `prior/findings/<owner>__<repo>.json`, compares
  `head_sha`, copies forward. No Claude call.
- **Miss:** no prior file, or `head_sha` differs, or `schema_version` differs.
  Haiku runs and writes a fresh `findings.json`.
- **Force-miss for everything:** bump `findings.schema.json`'s `schema_version`
  const. Cache invalidates across the board on the next run.

## Design context

PROF-5 in Jira is the canonical spec. Short version:

- **Claude = classification only.** Never writes markup. Never touches README directly.
- **Renderer = pure template.** No judgment. Pure function of `classified.json`.
- **Idempotence is structural:** same input → byte-identical output.
- **Row count is variable (5-12):** the consolidator picks the right N from the
  data. Each row is one markdown table row, so N only changes table height.
- **No geometry:** chips are `<kbd>` spans in a table cell, laid out by the
  browser. Pill widths, the 7-color palette and the x≤770 overflow check went
  away with the SVGs. The schema's `≤ 20 chars` / `3-6 pills` caps are now
  about readability, not fitting a fixed canvas.
- **Chips are vendor-neutral by construction:** `render.py` rewrites known
  vendor names to capability names (`CF Workers` → `Serverless Workers`,
  `D1` → `Edge SQL`) and hard-fails on vendor-shaped tokens missing from its
  alias table. The prompts ask for this too, but the renderer is what makes
  it hold when the model drifts. Bullet prose is exempt and stays concrete.
- **No CSS is possible:** GitHub strips `<style>` and `style=` from README HTML.
  `<kbd>`, tables and `> [!NOTE]` alerts are the entire styling budget — and
  unlike an SVG they leave the tag text selectable and indexable.

## Trigger the workflow manually

```bash
gh workflow run refresh-badges.yml
gh run watch
```

Push triggers also fire when anything under `.github/{scripts,prompts,schemas}/` or
the workflow file itself changes on `main` — merging a renderer tweak immediately
re-splices the README without waiting for Monday's cron.

## Failure isolation

- `strategy.fail-fast: false` + `continue-on-error: true` on the matrix job → a
  single broken repo can't take down the run.
- Consolidator runs with `if: always()` and computes `missing_repos`. If more
  than 5 repos are missing, it hard-fails — that's a systemic issue, not transient.
- No retry inside one run. The next cron picks up only the still-failed repos
  (every other repo is cache-hit, so it's nearly free).
