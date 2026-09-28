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
| **KUBERNETES INFRASTRUCTURE** | <kbd>Kubernetes</kbd> <kbd>k3s</kbd> <kbd>Helm</kbd> <kbd>GitOps</kbd> <kbd>Self-Hosted</kbd> |
| **SERVERLESS WEB APPS** | <kbd>Next.js</kbd> <kbd>TypeScript</kbd> <kbd>Serverless Workers</kbd> <kbd>Edge SQL</kbd> <kbd>Drizzle ORM</kbd> <kbd>Tailwind</kbd> |
| **BROWSER EXTENSIONS** | <kbd>TypeScript</kbd> <kbd>Chrome MV3</kbd> <kbd>Firefox</kbd> <kbd>Vite</kbd> <kbd>esbuild</kbd> |
| **AI &amp; LOCAL INFERENCE** | <kbd>Python</kbd> <kbd>FastAPI</kbd> <kbd>RAG</kbd> <kbd>MCP</kbd> <kbd>Local Models</kbd> |
| **CI/CD &amp; DEVOPS** | <kbd>GitHub Actions</kbd> <kbd>CI/CD</kbd> <kbd>Docker</kbd> <kbd>Kubernetes</kbd> <kbd>Node.js</kbd> <kbd>Python</kbd> |
| **DEVELOPER TOOLS** | <kbd>TypeScript</kbd> <kbd>Node.js</kbd> <kbd>React</kbd> <kbd>Markdown</kbd> <kbd>Claude API</kbd> |
| **SECURITY &amp; MONITORING** | <kbd>Python</kbd> <kbd>Rust</kbd> <kbd>OSV</kbd> <kbd>Telegram</kbd> <kbd>Monitoring</kbd> |

---

- **Self-hosted k3s cluster running production and homelab workloads** - Maintains a k3s cluster with GitHub Actions Runner Controller for self-hosted CI, Helm-managed Nextcloud with Cert-Manager and object storage backend, and nightly Vaultwarden backups encrypted with age and versioned in git.
- **Edge-hosted web products on Next.js and serverless workers** - Five Next.js applications deployed on serverless workers with edge SQL and Drizzle ORM — spanning a SaaS fleet management platform with Stripe payments, a two-sided marketplace for Romanian business registration, a corporate site with Claude-powered blog automation, an investment tracker, and gw2roi, a public Guild Wars 2 crafting ROI calculator with hourly data refreshes.
- **Privacy and productivity extensions across Chrome and Firefox** - Five MV3 extensions — chrome-group-discard pauses tab groups by discarding tabs and restores media position on expand; discord-purge and uninsta bulk-delete DMs and Instagram messages; series-auto-skip auto-skips intros and credits on Plex and Netflix; filelist-ext monitors a torrent tracker for new releases.
- **Self-hosted AI workspace and LLM inference tooling** - odysseus is a full-featured self-hosted AI workspace with RAG, MCP, and local model support via Ollama; social-update is a daily Claude agent that summarizes dev sessions into a SQLite log and generates LinkedIn drafts via a k3s-hosted web UI; and benchmarking work compares MoE inference (Qwen 35B) across FreeToken, llama.cpp, and Ollama on an RTX 3070.
- **Shared CI/CD library and deployment automation** - shared-workflows is a central reusable GitHub Actions library covering Node.js and Python testing, Kubernetes and serverless deployments, browser extension publishing, and automated Claude PR review; private deployment configs cover a Workers-based PDF toolkit and an internal tool directory.
- **Developer-facing utilities and personal knowledge tooling** - deckrun is a local-first Markdown presentation tool with 14+ themes, KaTeX equations, Mermaid diagrams, and PDF export; personal config tooling covers a Claude Code setup with custom skills, hooks, and memory, alongside an Obsidian vault following the PARA method and maintained by an automated Claude pipeline.
- **Vulnerability tracking and device security monitoring** - advisory-db is a security advisory database for Rust crates with OSV-format export integrating with cargo-audit, cargo-deny, and Dependabot; device-activity-telegram-bot monitors login and unlock events and dispatches Telegram alerts with a remote shutdown command.

---

`📡 Currently exploring integrating Claude Code agents into daily development and CI workflows`
<!-- BADGE-BOT:END -->

[contact@itguys.ro](mailto:contact@itguys.ro)
