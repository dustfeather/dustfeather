# dustfeather

GitHub profile special-repo (`dustfeather/dustfeather`) whose `README.md` renders on the profile page, plus a weekly "badge-bot" automation that regenerates the tech-stack badges and the project summary from a live scan of every repo I own.

## Goal

Keep the profile README current without hand-editing. A scheduled GitHub Actions pipeline ("badge-bot") enumerates every repo across all accounts/orgs where the `itguys-arc-runners` GitHub App is installed, classifies them with Claude, and deterministically rewrites:

- `badges-light.svg` / `badges-dark.svg` — the neon tech-stack badge graphics (light/dark pairs swapped via `prefers-color-scheme`).
- The README region between `<!-- BADGE-BOT:START -->` and `<!-- BADGE-BOT:END -->` — the themed project summary bullets and the "currently exploring" line.

Those badges and the README region are machine-written — never hand-edit them.

## Stack

- **Python** — `.github/scripts/render.py` does the deterministic SVG + README render and `jsonschema` validation (`requirements.txt`: `jsonschema==4.23.0`).
- **GitHub Actions** — multi-job pipeline in `refresh-badges.yml` calling reusable `classify-owner.yml`, running on self-hosted ARC runners (`arc-df-dustfeather`).
- **Claude Code CLI** — `claude --print` for classification: Haiku (`claude-haiku-4-5`) per-repo findings, Sonnet (`claude-sonnet-4-6`) consolidation.
- **APIs hit** — GitHub App auth via minted JWT (`/app/installations`, per-install access tokens), repo enumeration over the GitHub GraphQL API. Claude via `CLAUDE_CODE_OAUTH_TOKEN`.

## Repo

`dustfeather/dustfeather` (confirmed remote: `git@github.com:dustfeather/dustfeather.git`). GitHub profile special-repo — no app code, build, or tests.

Layout:

- `README.md` — profile page (references assets by absolute `raw.githubusercontent.com/.../main/...` URLs).
- `name-{light,dark}.svg`, `badges-{light,dark}.svg`, `itguys_logo.png` — static profile assets.
- `.github/workflows/` — `refresh-badges.yml` + `classify-owner.yml` (full badge-bot logic in-repo); `claude.yml`, `dependabot-auto-merge.yml`, `pr-checks.yml` are shims delegating to `dustfeather/shared-workflows`.
- `.github/scripts/` — `render.py`, `cache_gate.sh`, `requirements.txt`.
- `.github/prompts/` — `per-repo-findings.md`, `consolidate-classification.md` (Claude prompts).
- `.github/schemas/` — `findings.schema.json`, `classified.schema.json`.
- `sample/` — tracked local-dev fixtures (`classified.json` + a findings example).

## Deploy

No server. Runs entirely as scheduled GitHub Actions (cron `0 6 * * 1`, Monday 06:00 UTC), plus `workflow_dispatch` and `push` to `main` on script/prompt/schema/workflow changes. Jobs execute on self-hosted ARC runners but the automation itself is not an in-cluster deployment — it produces commits to `main`, nothing is hosted.

## Status

Active. Last automated badge refresh commit `2026-05-25`; most recent commit migrates shared-workflows callers to `@v2` and pins the `arc-df-dustfeather` runner.

## Tasks

Open GitHub issues:

- [ ] [dustfeather#15](https://github.com/dustfeather/dustfeather/issues/15) — rebrand profile to the ITGuys design system (badges + name SVGs)

Repo idea (no issue): extend the 7-slot color palette so badge rows beyond 7 stop cycling (renderer-only change in `render.py`).

## Notes

The badge-bot is a 5-stage pipeline in `refresh-badges.yml`:

1. **enumerate-repos** — mint per-install GitHub App tokens, enumerate repos via GraphQL across every install; skips archived/empty/profile repos.
2. **download-prior-findings** — pull last successful run's `findings-bundle` artifact so unchanged repos (matched on `head_sha` via `cache_gate.sh`) can be fast-pathed and skip a Claude call.
3. **classify-owner** (reusable) — per-owner waves (`max-parallel: 1`), inner matrix runs that owner's repos and calls Claude Haiku to produce per-repo findings.
4. **consolidate** — Claude Sonnet merges all findings into `classified.json` (schema-validated); guard steps forbid touching tracked files outside the allowlist.
5. **render-and-commit** — pure Python `render.py` regenerates the badge SVGs + splices the README region, then commits/pushes only if changed.

Schedule: weekly cron (Monday 06:00 UTC), on-demand dispatch, and on relevant pushes. Enrollment is install-driven — installing the `itguys-arc-runners` App on a new org/user auto-adds it to the scan with no workflow edit.

**CI runners:** the badge-bot jobs and the `claude`/`dependabot`/`pr-checks` shims run on the self-hosted k3s ARC runner `arc-df-dustfeather`, built from [shared-workflows](https://github.com/dustfeather/shared-workflows/blob/main/docs/OVERVIEW.md) and hosted in [Homelab](https://github.com/ITGuys-RO/k3s-cluster/blob/main/docs/homelab.md).

Area: Software Engineering

## Log

- **2026-05-31** — Note created from repo scan.
- **2026-05-31** — Moved task tracking from Jira (PROF-2) back to GitHub issue #15; dropped the stale PROF-N palette item to a non-issue idea.
