<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dustfeather/dustfeather/main/name-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dustfeather/dustfeather/main/name-light.svg" />
  <img src="https://raw.githubusercontent.com/dustfeather/dustfeather/main/name-dark.svg" alt="Catalin Teodorescu" />
</picture>

*[Full-stack engineer](https://www.linkedin.com/in/dustfeather/) turned [company builder](https://itguys.ro).*

*Most of my work lives in private repos, but here's the gist:*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dustfeather/dustfeather/main/badges-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dustfeather/dustfeather/main/badges-light.svg" />
  <img src="https://raw.githubusercontent.com/dustfeather/dustfeather/main/badges-dark.svg" alt="Tech Stack" />
</picture>

<!-- BADGE-BOT:START -->
---

- **Browser automation utilities** - Four TypeScript extensions across Chrome and Firefox — discord-purge for bulk-deleting Discord DMs, uninsta for Instagram DMs, series-auto-skip for automatically skipping intros and credits on Plex and Netflix, and filelist-ext for torrent release notifications on filelist.io.
- **Self-managed k3s cluster and CI/CD backbone** - The private k3s platform is driven by helmfile (cert-manager, monitoring, ARC runner pools) with raw manifests for Cloudflare tunnels and nginx proxies; dustfeather/shared-workflows provides the CI/CD backbone with reusable GitHub Actions workflows for Node/Python testing, Claude Code review, and Chrome/Firefox extension publishing.
- **Self-hosted services on k3s** - Three services run on the private k3s cluster: the ITGuys-RO/nextcloud deployment (MariaDB, Valkey, cert-manager TLS, nightly SSH backups), a WSL2 GPU-backed Ollama inference server running Qwen 35B with an OpenAI-compatible /v1 endpoint, and age-encrypted nightly Vaultwarden backups with GitHub Actions freshness monitoring.
- **Flotila — fleet management SaaS** - Full-stack fleet management SaaS for the Romanian market — multi-tenant with RBAC (owner/manager/driver), vehicle and driver registries, deadline tracking, GPS and fuel/mileage logging, and Stripe billing, built on Next.js 16, Cloudflare Workers with D1, Drizzle ORM, and MapLibre.
- **Cloudflare-hosted web applications** - Two private Next.js 16 apps on Cloudflare Workers with D1 backends: a multilingual IT services corporate website with automated blog generation via Claude API on a daily Cloudflare cron, and a personal investment tracker with time-weighted return calculations, 10-year forecasts, and automated eToro/Alpaca broker sync.
- **Personal automation bots and collectors** - device-activity-telegram-bot sends Telegram alerts on device login and unlock events and accepts remote shutdown commands; social-update collects daily GitHub and Obsidian activity via an Express/SQLite API and uses Claude to draft LinkedIn posts; a private Obsidian vault is maintained by a headless Claude Code pipeline that sorts inbox notes and generates digests.

---

`📡 Currently exploring Claude API for personal automation — activity collection, content drafts, and vault maintenance`
<!-- BADGE-BOT:END -->

[contact@itguys.ro](mailto:contact@itguys.ro)
