# Badge bot — local dev

The bot's runtime lives in `.github/workflows/refresh-badges.yml` and runs
weekly on the `arc-df-dustfeather` self-hosted runner. The renderer is pure
Python and runs anywhere with `python3` + `jsonschema`.

## Architecture (map/reduce)

```
enumerate-repos        →  JSON array of {owner, repo, head_sha, is_public}
download-prior-findings →  prior/findings/<owner>__<repo>.json from last week's bundle
classify-repo (matrix)  →  N parallel Haiku jobs, one per repo
                            ├─ cache_gate.sh: prior head_sha == current → copy forward, skip Claude
                            └─ else Haiku reads README + tree + manifests → findings.json
consolidate             →  Sonnet bins all findings/ into classified.json (5-12 rows)
render-and-commit       →  python render.py classified.json → SVGs + README region → commit
```

Steady state on a quiet week: most matrix cells hit cache, only the consolidator
makes a Claude call. Cold start / many repos changed: full matrix runs.

## What the pieces are

| Path | What it does |
|---|---|
| `.github/workflows/refresh-badges.yml` | 5-job pipeline (enumerate → prior → matrix → consolidate → render+commit) |
| `.github/prompts/per-repo-findings.md` | Haiku prompt — one repo → `findings.json` |
| `.github/prompts/consolidate-classification.md` | Sonnet prompt — all findings → `classified.json` |
| `.github/schemas/findings.schema.json` | Per-repo output contract (one file per matrix cell) |
| `.github/schemas/classified.schema.json` | Final classification contract (5-12 rows; renderer input) |
| `.github/scripts/cache_gate.sh` | Per-matrix-cell cache check (prior head_sha vs current) |
| `.github/scripts/render.py` | Pure-Python renderer: classified.json → SVGs + README splice |
| `.github/scripts/requirements.txt` | Single pinned dep: `jsonschema` (baked into runner image too) |

## Run the renderer locally

```bash
pip install -r .github/scripts/requirements.txt   # baked into runner image
python .github/scripts/render.py path/to/classified.json
```

Fixtures: `sample/classified.json` (7-row example) and `sample/findings/<owner>__<repo>.json`
(per-repo finding example). Schemas in `.github/schemas/` are authoritative for both.

The renderer overwrites `badges-light.svg`, `badges-dark.svg`, and the
`<!-- BADGE-BOT:START -->`…`<!-- BADGE-BOT:END -->` region of `README.md`
in place. If the README lacks those markers it exits non-zero — the one-time
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

- **Claude = classification only.** Never writes SVG. Never touches README directly.
- **Renderer = pure template.** No judgment. Pure function of `classified.json`.
- **Idempotence is structural:** same input → byte-identical output.
- **Row count is variable (5-12):** the consolidator picks the right N from the
  data. Renderer cycles the 7-color palette via `i % 7` for rows ≥ 7.
- **Pill geometry:** `width = max(55, len*7 + 16)`; gap 10px; rightmost must
  end ≤ x=770. Renderer raises `ValueError` if a row overflows.

## Trigger the workflow manually

```bash
gh workflow run refresh-badges.yml
gh run watch
```

Push triggers also fire when anything under `.github/{scripts,prompts,schemas}/` or
the workflow file itself changes on `main` — merging a renderer tweak immediately
re-emits the SVGs without waiting for Monday's cron.

## Failure isolation

- `strategy.fail-fast: false` + `continue-on-error: true` on the matrix job → a
  single broken repo can't take down the run.
- Consolidator runs with `if: always()` and computes `missing_repos`. If more
  than 5 repos are missing, it hard-fails — that's a systemic issue, not transient.
- No retry inside one run. The next cron picks up only the still-failed repos
  (every other repo is cache-hit, so it's nearly free).
