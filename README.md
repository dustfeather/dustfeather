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
| **SERVERLESS SAAS** | <kbd>TypeScript</kbd> <kbd>Next.js</kbd> <kbd>Tailwind</kbd> <kbd>Edge SQL</kbd> <kbd>Drizzle ORM</kbd> <kbd>Hono</kbd> |
| **KUBERNETES INFRA** | <kbd>k3s</kbd> <kbd>Helm</kbd> <kbd>GitOps</kbd> <kbd>Docker</kbd> <kbd>Self-hosted LLM</kbd> |
| **BROWSER EXTENSIONS** | <kbd>TypeScript</kbd> <kbd>Chrome MV3</kbd> <kbd>Firefox</kbd> <kbd>esbuild</kbd> <kbd>WebExtension</kbd> |
| **DEVOPS &amp; CI/CD** | <kbd>GitHub Actions</kbd> <kbd>Docker</kbd> <kbd>Node.js</kbd> <kbd>Python</kbd> <kbd>Shell</kbd> |
| **DATA PIPELINES** | <kbd>TypeScript</kbd> <kbd>Bun</kbd> <kbd>PostgreSQL</kbd> <kbd>Grafana</kbd> <kbd>Kubernetes</kbd> |
| **SECURITY &amp; BACKUP** | <kbd>Security</kbd> <kbd>Rust</kbd> <kbd>Encryption</kbd> <kbd>Shell</kbd> <kbd>TOML</kbd> |
| **PERSONAL AUTOMATION** | <kbd>Python</kbd> <kbd>TypeScript</kbd> <kbd>Telegram API</kbd> <kbd>Claude API</kbd> <kbd>SQLite</kbd> |

---

- **Multi-tenant SaaS products on the serverless edge** - Three TypeScript SaaS products deployed on serverless workers — fleet management for Romanian companies, a multilingual corporate site with automated Claude API blog generation, and a business-registration onboarding wizard — all sharing Next.js App Router, Drizzle ORM, and edge-resident SQL.
- **Self-hosted k3s cluster running production workloads** - GitOps-managed k3s cluster running Nextcloud with Helm, MariaDB, and cert-manager TLS; an internal app directory on WARP-only networking; and an Ollama LLM inference node with NVIDIA RTX 3070 GPU passthrough serving a 35B-parameter model at the homelab edge.
- **MV3 extensions for privacy and media automation** - Four TypeScript extensions for Chrome and Firefox: discord-purge and uninsta bulk-unsend messages from Discord and Instagram (with rate-limit handling and reverse-engineered APIs), filelist-seed-purge auto-purges completed torrents from qBittorrent by ratio or seeding-time threshold, and series-auto-skip clicks intro and credit skip buttons on Netflix and Plex.
- **Centralised reusable GitHub Actions library** - shared-workflows is a reusable GitHub Actions hub covering Claude Code review, Dependabot auto-merge, Node.js and Python CI, Cloudflare Workers deployments, and browser extension publishing — consumed as callable workflow references across all org and personal repos.
- **Scheduled data pipelines with Grafana observability** - gw2roi is an hourly k3s CronJob built with Bun that fetches Guild Wars 2 item prices from the GW2 API and datawars2, ranks craftable items by profit margin, and streams results into a PostgreSQL StatefulSet visualised in Grafana dashboards.
- **Security advisories and encrypted backup tooling** - Contributes to the RustSec advisory-db for the Rust crates.io ecosystem — consumed by cargo-audit, cargo-deny, and Dependabot for CVE scanning — alongside age-encrypted nightly backup automation for a self-hosted Vaultwarden password manager.
- **Personal automation bots and knowledge tooling** - A Python Telegram bot (device-activity-telegram-bot) alerts on device logins and enables remote shutdown; social-update collects daily activity into SQLite and drafts LinkedIn posts via Claude; and a private Obsidian vault maintained by a Claude Code pipeline that sorts the inbox and generates daily digests.

---

`📡 Currently exploring Serverless edge SaaS for Romanian business registration — Next.js App Router + Hono API on Cloudflare Workers with EU-resident D1/KV/R2 storage`
<!-- BADGE-BOT:END -->

[contact@itguys.ro](mailto:contact@itguys.ro)
