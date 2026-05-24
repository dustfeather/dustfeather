# CLAUDE.md

GitHub profile special-repo: `README.md` renders on owner's profile page. No app code, build, tests — just `README.md` + static SVG/PNG assets.

## Gotchas

- `README.md` references assets by absolute `raw.githubusercontent.com/.../main/...` URLs (not relative) — asset only renders after landing on `main`.
- Assets in light/dark pairs (`name-{light,dark}.svg`, `badges-{light,dark}.svg`) swapped via `prefers-color-scheme`. Edit both variants together.
- `.github/workflows/{claude,dependabot-auto-merge,pr-checks}.yml` = shims delegating to `dustfeather/shared-workflows@v1`. `refresh-badges.yml` + `classify-owner.yml` carry full badge-bot logic in-repo.
- `.gitignore` excludes `*.local` / `*.local.*` — put secrets in such files.
- `badges-{light,dark}.svg` + README region between `<!-- BADGE-BOT:START -->` and `<!-- BADGE-BOT:END -->` written by weekly badge-bot — don't hand-edit (spec: Jira PROF-1).
- Badge-bot enrollment is install-driven: install GitHub App `itguys-arc-runners` on new org/user (repo metadata + contents read). `refresh-badges.yml` auto-discovers via `/app/installations`. No workflow edit needed.
