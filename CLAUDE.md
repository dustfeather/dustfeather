# CLAUDE.md

GitHub profile special-repo: `README.md` renders on owner's profile page. No app code, build, tests — just `README.md` + static SVG/PNG assets.

## Gotchas

- `README.md` references assets by absolute `raw.githubusercontent.com/.../main/...` URLs (not relative) — asset only renders after landing on `main`.
- Assets in light/dark pairs (`name-{light,dark}.svg`, `badges-{light,dark}.svg`) swapped via `prefers-color-scheme`. Edit both variants together.
- `.github/workflows/{claude,dependabot-auto-merge,pr-checks}.yml` = shims delegating to `dustfeather/shared-workflows@v1`. `refresh-badges.yml` + `classify-owner.yml` carry full badge-bot logic in-repo.
- `.gitignore` excludes `*.local` / `*.local.*` — put secrets in such files.
- `badges-{light,dark}.svg` + README region between `<!-- BADGE-BOT:START -->` and `<!-- BADGE-BOT:END -->` written by weekly badge-bot — don't hand-edit (spec: Jira PROF-1).
- Badge-bot enrollment is install-driven: install GitHub App `itguys-arc-runners` on new org/user (repo metadata + contents read). `refresh-badges.yml` auto-discovers via `/app/installations`. No workflow edit needed.

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.
