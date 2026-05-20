# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`dustfeather/dustfeather` is a GitHub profile special-repo: `README.md` renders
on the owner's profile page. No application code, build, or tests — just
`README.md` and static SVG/PNG assets.

## Gotchas

- `README.md` references assets by absolute `raw.githubusercontent.com/.../main/...`
  URLs, not relative paths — an asset only renders after it lands on `main`.
- Assets come in light/dark pairs (`name-{light,dark}.svg`,
  `badges-{light,dark}.svg`) swapped via `prefers-color-scheme`. Edit both
  variants of a pair together so the themes stay in sync.
- `.github/workflows/*` are shims delegating to `dustfeather/shared-workflows@v1`;
  the real CI logic lives in that repo, not here.
- `.gitignore` excludes `*.local` / `*.local.*` — put secrets in such files.
