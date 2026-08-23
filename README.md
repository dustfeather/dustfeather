<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dustfeather/dustfeather/main/name-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dustfeather/dustfeather/main/name-light.svg" />
  <img src="https://raw.githubusercontent.com/dustfeather/dustfeather/main/name-dark.svg" alt="Catalin Teodorescu" />
</picture>

*[Full-stack engineer](https://www.linkedin.com/in/dustfeather/) turned [company builder](https://itguys.ro).*

*Most of my work lives in private repos, but here's the gist:*

<!-- BADGE-BOT:START -->
| Domain | Stack |
| --- | --- |
| **SELF-HOSTED INFRA** | <kbd>Kubernetes</kbd> <kbd>k3s</kbd> <kbd>Helmfile</kbd> <kbd>Prometheus</kbd> <kbd>GPU Inference</kbd> |
| **CI/CD &amp; TOOLING** | <kbd>GitHub Actions</kbd> <kbd>Docker</kbd> <kbd>Shell</kbd> <kbd>Python</kbd> <kbd>Automation</kbd> |
| **SERVERLESS SAAS** | <kbd>TypeScript</kbd> <kbd>Next.js</kbd> <kbd>Hono</kbd> <kbd>Serverless</kbd> <kbd>Edge SQL</kbd> |
| **BROWSER EXTENSIONS** | <kbd>TypeScript</kbd> <kbd>Chrome MV3</kbd> <kbd>Firefox</kbd> <kbd>esbuild</kbd> <kbd>SCSS</kbd> |
| **BOTS &amp; AUTOMATION** | <kbd>Python</kbd> <kbd>TypeScript</kbd> <kbd>Bun</kbd> <kbd>Telegram</kbd> <kbd>PostgreSQL</kbd> |
| **AI-ASSISTED TOOLS** | <kbd>TypeScript</kbd> <kbd>Claude API</kbd> <kbd>SQLite</kbd> <kbd>Obsidian</kbd> <kbd>Node.js</kbd> |

---

- **Homelab k3s platform with GPU inference** - Versioned Helmfile cluster managing cert-manager, Prometheus/Grafana/Loki observability, ARC runner sets, Nextcloud, and a GPU-backed Ollama inference server running qwen3:35b on an NVIDIA RTX 3070; encrypted Vaultwarden nightly backups round out the self-hosted stack.
- **Reusable CI/CD and profile automation** - Centralised reusable GitHub Actions workflows (shared-workflows) covering Node.js/Python CI, Claude Code review, browser-extension publishing to the Chrome Web Store and Mozilla Add-ons, and serverless worker deployment, backed by a containerised ARC runner fleet.
- **Production SaaS on serverless edge workers** - Two production SaaS products on serverless workers with edge SQL — a Romanian PFA/SRL business-registration compliance platform (Next.js App Router + Hono, D1, R2) and a personal investment portfolio tracker with time-weighted return calculations and a k3s-hosted trading bot.
- **Cross-browser Manifest V3 extension suite** - Four privacy and productivity extensions for Chrome MV3 and Firefox built from unified TypeScript + esbuild pipelines: discord-purge (bulk-delete DMs with rate-limit backoff), uninsta (bulk-unsend Instagram messages), series-auto-skip (auto-click Skip Intro/Credits on Netflix and Plex), and filelist-ext (torrent tracker notifications).
- **Standalone bots and data-pipeline automation** - A strictly-typed Python Telegram bot (device-activity-telegram-bot) that detects Windows login/unlock events and triggers remote shutdown, plus a Bun-based k3s CronJob (gw2roi) that ranks Guild Wars 2 crafting-ROI items hourly and writes results to Postgres for Grafana dashboards.
- **AI-augmented personal knowledge pipeline** - social-update ingests GitHub, Obsidian, Claude Code, and claude.ai activity into SQLite, uses Claude API to generate weekly LinkedIn drafts, and pairs with an Obsidian PARA vault managed by an automated vault-keeper pipeline for long-term knowledge storage.

---

`📡 Currently exploring serverless edge SaaS for Romanian business registration and PFA/SRL compliance`
<!-- BADGE-BOT:END -->

[contact@itguys.ro](mailto:contact@itguys.ro)
