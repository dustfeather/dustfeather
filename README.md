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
| **BROWSER EXTENSIONS** | <kbd>TypeScript</kbd> <kbd>Chrome MV3</kbd> <kbd>Firefox</kbd> <kbd>esbuild</kbd> <kbd>Vite</kbd> |
| **SERVERLESS SAAS** | <kbd>TypeScript</kbd> <kbd>Next.js</kbd> <kbd>Serverless Workers</kbd> <kbd>Edge SQL</kbd> <kbd>Drizzle ORM</kbd> |
| **SELF-HOSTED PLATFORM** | <kbd>Kubernetes</kbd> <kbd>k3s</kbd> <kbd>Helm</kbd> <kbd>Shell</kbd> <kbd>GitHub Actions</kbd> |
| **CI/CD &amp; DEVOPS** | <kbd>GitHub Actions</kbd> <kbd>Docker</kbd> <kbd>YAML</kbd> <kbd>Node.js</kbd> <kbd>Python</kbd> |
| **BOTS &amp; AUTOMATION** | <kbd>TypeScript</kbd> <kbd>Python</kbd> <kbd>Bun</kbd> <kbd>Telegram Bot API</kbd> <kbd>SQLite</kbd> |
| **FINANCE &amp; INVESTMENT** | <kbd>TypeScript</kbd> <kbd>Serverless Workers</kbd> <kbd>Edge SQL</kbd> <kbd>Chartist</kbd> <kbd>Docker</kbd> |
| **SECURITY** | <kbd>Rust</kbd> <kbd>OSV Format</kbd> <kbd>Security</kbd> <kbd>Cargo</kbd> <kbd>Vulnerability</kbd> |

---

- **Cross-browser MV3 extensions shipped to Chrome Web Store and Mozilla Add-ons** - Five TypeScript Manifest V3 extensions built from a shared esbuild/Vite pipeline: discord-purge and uninsta for bulk-unsending DMs on Discord and Instagram with rate-limit handling, filelist-ext for polling the filelist.io API and surfacing torrent notifications, filelist-seed-purge for automatically purging completed qBittorrent seeds by time/ratio thresholds, and series-auto-skip for auto-clicking Skip Intro on Netflix and Plex.
- **Production SaaS platforms on Next.js deployed to Cloudflare Workers** - Three TypeScript SaaS products shipped via opennextjs-cloudflare with Drizzle ORM over D1 edge databases: a vehicle fleet management system with deadline tracking and org-scoped auth, a multilingual corporate website with Claude API-powered blog automation, and a business-registration onboarding platform with a Hono API worker and document generation engine.
- **Self-managed k3s cluster hosting internal services and LLM inference** - A multi-node k3s cluster managed via Helmfile with declarative Helm charts and raw manifests for Nextcloud file sync, self-hosted Ollama LLM inference with NVIDIA RTX 3070 GPU passthrough on WSL2, age-encrypted Vaultwarden backup automation, a WARP-only internal app directory, and GitHub Actions ARC runner pools bootstrapped from a GitOps cluster IaC repo.
- **Centralized reusable GitHub Actions workflow library** - shared-workflows is a hub of 14+ reusable workflows consumed across the portfolio: Node.js and Python test runners, Claude Code AI code review, browser extension publishing pipelines for Chrome Web Store and Mozilla Add-ons, Cloudflare Workers deployment with startup verification and budget gates, and Dependabot auto-merge automation.
- **Scheduled bots for device monitoring, game analytics, and content generation** - A strictly-typed Python Telegram bot (device-activity-telegram-bot) alerting on Windows login and unlock events with remote shutdown commands, an hourly Bun/TypeScript Kubernetes CronJob (gw2roi) ranking profitable Guild Wars 2 crafts from live trade post data and writing results to Postgres for Grafana visualization, and a Node.js social journal (social-update) collecting GitHub, Obsidian, and Claude session activity to generate weekly LinkedIn drafts via in-cluster Claude AI.
- **Personal investment portfolio tracker with multi-broker sync and forecasting** - A monorepo investment dashboard deployed on Cloudflare Workers with D1 storage, syncing positions from eToro and Alpaca via automated API integrations, computing time-weighted returns, generating 10-year Monte Carlo forecasts with Chartist visualizations, and running a Kubernetes-hosted algorithmic trading bot alongside offline backtesting tooling.
- **Contributor to the RustSec open-source vulnerability advisory database** - Active contributions to the official RustSec Advisory Database (advisory-db), which publishes CVE-style advisories for Rust crates in OSV format and powers cargo-audit, cargo-deny, trivy, and GitHub Dependabot security checks for the broader Rust ecosystem on crates.io.

---

`📡 Currently exploring legaltech SaaS for document-driven business registration and compliance workflows`
<!-- BADGE-BOT:END -->

[contact@itguys.ro](mailto:contact@itguys.ro)
