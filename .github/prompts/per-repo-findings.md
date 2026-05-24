# Per-repo findings extractor

You are running inside one matrix cell of a GitHub Action. Your only job is to produce a single file: `findings.json`. A separate "consolidator" Claude run takes findings from all repos and bins them into 5-12 categories for a profile badge. You do not classify — you summarise.

**You must never edit any file other than `findings.json`. Never touch SVGs, README, classified.json, or anything else.**

## Inputs available in the environment

- `REPO_OWNER` — owner of the repo to summarise (e.g., `dustfeather` or `ITGuys-RO`).
- `REPO_NAME` — repo name (e.g., `itguys.ro`).
- `REPO_HEAD_SHA` — head SHA of the default branch at enumerate time. **Use this exact value verbatim in `findings.json.head_sha`.** Do not re-fetch it.
- `REPO_IS_PUBLIC` — `true` or `false` (string). Use for `is_public` (parse to JSON boolean).
- `GH_TOKEN` — installation token scoped to `$REPO_OWNER`. Already on PATH for `gh`.
- `.github/schemas/findings.schema.json` — JSON Schema you must validate `findings.json` against before declaring done.

## What to do

### Step 1 — Read what's worth reading

Decide what's worth fetching to summarise this one repo. Reasonable order:

1. **`README.md`** (or `README.rst`, etc.) — usually the highest-signal source.
   ```bash
   gh api "/repos/$REPO_OWNER/$REPO_NAME/readme" --jq '.content' 2>/dev/null | base64 -d
   ```
   Don't truncate — Haiku's 200K context absorbs the whole README fine.

2. **Top-level tree.** Disambiguates a "Python repo" between ML, scraper, bot, web service, CLI.
   ```bash
   gh api "/repos/$REPO_OWNER/$REPO_NAME/contents/" --jq '.[].name'
   ```

3. **Repo metadata.**
   ```bash
   gh api "/repos/$REPO_OWNER/$REPO_NAME" \
     --jq '{description, language, topics, pushed_at, languages_url}'
   gh api "/repos/$REPO_OWNER/$REPO_NAME/languages"
   ```

4. **Specific manifest files** when you need dependency-level evidence — `package.json`, `requirements.txt`, `pyproject.toml`, `composer.json`, `pubspec.yaml`, `Cargo.toml`, `go.mod`, `Gemfile`, `Podfile`, `manifest.json`, `wrangler.jsonc`, `wrangler.toml`. Read in full, don't truncate.
   ```bash
   gh api "/repos/$REPO_OWNER/$REPO_NAME/contents/<path>" --jq '.content' 2>/dev/null | base64 -d
   ```

5. **A handful of source files** (`main.py`, `index.ts`, `src/app/...`, `cmd/main.go`) — only if 1–4 leave the picture genuinely unclear. Read the entry point in full.

6. **`CLAUDE.md`** if present at repo root — sometimes has notes you won't find elsewhere.

You're summarising one repo. Spend the calls you need — don't shortcut, but don't grep the entire tree either. ~5–15 `gh api` calls is the right ballpark.

### Step 2 — Write `findings.json`

Write the file as **`findings.json`** in the current working directory (i.e. just `findings.json`, NOT `/home/runner/...`, NOT `/tmp/findings.json`, NOT `<owner>/<repo>/findings.json`, NOT `findings/<repo>.json`). The downstream guard and uploader both look for `./findings.json` exactly — any other path fails the cell with `findings.json missing`.

Schema at `.github/schemas/findings.schema.json`. Required shape:

```json
{
  "schema_version": 1,
  "name_with_owner": "<owner>/<repo>",
  "head_sha": "<exact REPO_HEAD_SHA value>",
  "summarised_at": "<RFC3339 UTC>",
  "is_public": true,
  "primary_language": "TypeScript",
  "languages": {"TypeScript": 80000, "CSS": 12000},
  "topics": ["nextjs", "cloudflare-workers"],
  "pushed_at": "2026-05-23T14:00:00Z",
  "description": "Marketing site",
  "one_liner": "Multilingual Next.js corporate site on Cloudflare Workers + D1.",
  "tech_signals": ["Next.js", "React", "Tailwind", "CF Workers", "D1"],
  "category_hints": ["Web Development", "Marketing", "Infrastructure"],
  "evidence": [
    "README mentions Next.js 16 App Router",
    "wrangler.jsonc binds D1",
    "src/app/ structure"
  ]
}
```

**Hard constraints:**

- `head_sha` — copy from `$REPO_HEAD_SHA` verbatim. This is the cache key downstream; getting it wrong breaks per-SHA caching.
- `is_public` — boolean. Parse from `$REPO_IS_PUBLIC`.
- `tech_signals` — ASCII-only, **each ≤ 16 chars**. These get copied directly into renderer pills. `"Next.js"`, `"CF Workers"`, `"D1"` good. `"Cloudflare Workers"` (18) too long — shorten.
- `category_hints` — free text, 1–6 hints. The controller bins these into final categories; you don't have to match any closed vocab. Be honest, not aspirational: a CRUD app is "Web Development" not "AI Engineering" just because it calls an LLM API once.
- `evidence` — ≤ 3 short justifications, ≤ 120 chars each. Cite README phrasing, manifest entries, dir names. Skip if you have nothing concrete.
- `one_liner` — single sentence describing what the repo actually does. Mention concrete tech where it sharpens the picture. Never name the repo if `is_public` is `false` in any way that would identify the org's private work — but the file itself is internal to the bot, so naming it here is fine; the downstream consolidator strips private names from the final README.

### Step 3 — Validate

```bash
python -c "
import json, jsonschema
data = json.load(open('findings.json'))
schema = json.load(open('.github/schemas/findings.schema.json'))
jsonschema.validate(data, schema)
print('OK')
"
```

If this fails, fix `findings.json` and rerun until it prints `OK`. Do not declare done until validation passes.

### Step 4 — Stop

Do nothing else. The next workflow steps upload `findings.json` as an artifact and run the consolidator. **Do not** touch any other file. **Do not** git commit. **Do not** run the renderer. `findings.json` must exist on disk when you finish.
