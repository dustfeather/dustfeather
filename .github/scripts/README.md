# Badge bot — local dev

The bot's runtime lives in `.github/workflows/refresh-badges.yml` and runs
weekly on the `arc-df-dustfeather` self-hosted runner. The renderer is pure
Python and runs anywhere with `python3` + `jsonschema`.

## What the pieces are

| Path | What it does |
|---|---|
| `.github/workflows/refresh-badges.yml` | Orchestrates: mints App tokens, runs Claude, runs renderer, commits + pushes |
| `.github/prompts/refresh-badges.md` | System prompt Claude reads (its only job is producing `classified.json`) |
| `.github/schemas/classified.schema.json` | JSON Schema for `classified.json`; both Claude and renderer validate against it |
| `.github/scripts/render.py` | Reads `classified.json`, writes `badges-{light,dark}.svg` + splices `README.md` |

## Run the renderer locally

```bash
pip install -r .github/scripts/requirements.txt   # pinned single dep: jsonschema
python .github/scripts/render.py path/to/classified.json
```

`classified.json` shape and constraints: see `.github/schemas/classified.schema.json`. Sample fixture: `sample/classified.json`.

The renderer overwrites `badges-light.svg`, `badges-dark.svg`, and the
`<!-- BADGE-BOT:START -->`…`<!-- BADGE-BOT:END -->` region of `README.md`
in place. If the README lacks those markers it exits non-zero — the one-time
README edit must already have happened.

## Design context

PROF-1 in Jira is the canonical spec. The Jira ticket has a finalized spec
attached. Short version:

- Claude = classification only. Never writes SVG. Never touches README directly.
- Renderer = pure template. No judgment. Pure function of `classified.json`.
- Idempotence is structural: same input → byte-identical output.
- 7 rows, fixed colors per row index (cyan/teal/green/yellow/magenta/purple/orange).
- Pill geometry: `width = max(55, len*7 + 16)`; gap 10px; rightmost must end ≤ x=770.

## Trigger the workflow manually

```bash
gh workflow run refresh-badges.yml
gh run watch
```

Push triggers also fire when `.github/scripts/render.py`,
`.github/prompts/refresh-badges.md`, or
`.github/schemas/classified.schema.json` change on `main` — merging a renderer
tweak immediately re-emits the SVGs without waiting for Monday's cron.
