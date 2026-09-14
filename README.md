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
| **BROWSER EXTENSIONS** | <kbd>TypeScript</kbd> <kbd>Manifest V3</kbd> <kbd>Chrome MV3</kbd> <kbd>Firefox</kbd> <kbd>Vite</kbd> <kbd>esbuild</kbd> |
| **SERVERLESS SAAS** | <kbd>TypeScript</kbd> <kbd>Next.js</kbd> <kbd>Drizzle ORM</kbd> <kbd>Edge SQL</kbd> <kbd>Serverless Workers</kbd> <kbd>Stripe</kbd> |
| **CORPORATE WEB &amp; TOOLS** | <kbd>Next.js</kbd> <kbd>TypeScript</kbd> <kbd>Claude API</kbd> <kbd>Edge Workers</kbd> <kbd>Multilingual</kbd> <kbd>Static Site</kbd> |
| **SELF-HOSTED INFRA** | <kbd>k3s</kbd> <kbd>Helm</kbd> <kbd>Kubernetes</kbd> <kbd>Docker</kbd> <kbd>Shell</kbd> <kbd>Backup</kbd> |
| **CI/CD &amp; DEPLOYMENT** | <kbd>GitHub Actions</kbd> <kbd>Docker</kbd> <kbd>Python</kbd> <kbd>Reusable Workflows</kbd> <kbd>Wrangler</kbd> <kbd>WASM</kbd> |
| **AI WORKSPACE &amp; LLM** | <kbd>Python</kbd> <kbd>FastAPI</kbd> <kbd>RAG</kbd> <kbd>MCP</kbd> <kbd>Docker</kbd> <kbd>LLM Benchmarks</kbd> |
| **AUTOMATION &amp; BOTS** | <kbd>Python</kbd> <kbd>TypeScript</kbd> <kbd>Telegram Bot</kbd> <kbd>SQLite</kbd> <kbd>Kubernetes</kbd> <kbd>Obsidian</kbd> |
| **DEVELOPER TOOLS** | <kbd>TypeScript</kbd> <kbd>Node.js</kbd> <kbd>Markdown</kbd> <kbd>Rust</kbd> <kbd>CLI</kbd> <kbd>Security</kbd> |

---

- **Six cross-browser MV3 extensions for privacy, productivity, and media** - Extensions for Chrome and Firefox handling tab-group snooze in chrome-group-discard, bulk unsend on Discord and Instagram via discord-purge and uninsta, torrent tracking and qBittorrent automation through filelist-ext and filelist-seed-purge, and intro/credit auto-skip on Netflix and Plex — all built with TypeScript and Vite or esbuild targeting Manifest V3.
- **Edge-deployed SaaS products with payments, GPS, and market analysis** - Flotila (fleet management with GPS tracking, driver deadlines, and Stripe payments), dosar-rapid.ro (two-sided marketplace for Romanian business-registration documents), a personal investment tracker with eToro and Alpaca sync and TWR/Monte Carlo analysis, and gw2roi (Guild Wars 2 crafting ROI bot) — all deployed to serverless workers backed by edge SQL and object storage.
- **Corporate website with AI-generated content and access-gated portal** - itguys.ro is a multilingual (6-locale) Next.js 16 corporate site deployed to serverless workers with automated blog generation via Claude API, JWT admin panel, and Turnstile CAPTCHA; apps-page is an access-gated static portal listing all IT Guys tools and infrastructure, gated via Google Workspace IdP.
- **Self-hosted k3s cluster running Nextcloud, Vaultwarden, and CI runners** - Production 3-node k3s cluster running Nextcloud with Valkey cache, Vaultwarden with age-encrypted nightly backups, Prometheus/Grafana/Loki observability, cert-manager TLS, and 20 GitHub Actions runner pools — all declared in helmfile and raw Kubernetes manifests with automated drift-check validation.
- **Reusable CI/CD workflows and edge deployment pipelines** - shared-workflows provides 10+ reusable GitHub Actions workflows for Node.js, Python, Kubernetes, Helm, and serverless deployments — including Claude Code automated PR review and Dependabot auto-merge; bentopdf is a dedicated deploy pipeline for BentoPDF that routes oversized WASM assets through object storage to stay within edge platform size limits.
- **Self-hosted AI workspace and local LLM inference benchmarking** - Odysseus is a full-stack self-hosted AI workspace with chat, agents, RAG, email, calendar, and MCP integration, backed by FastAPI and ChromaDB with Docker Compose GPU support for NVIDIA/AMD; paired with empirical LLM inference benchmarking comparing Ollama, llama.cpp, and FreeToken throughput on an RTX 3070 with VRAM and PCIe analysis.
- **Telegram bots and schedulers for device monitoring and content drafts** - device-activity-telegram-bot sends real-time login/unlock alerts and remote-shutdown commands across Windows and Linux; social-update collects Claude session summaries to SQLite and drafts LinkedIn posts, running on k3s with systemd timers; obsidian-sync maintains a PARA knowledge vault with automated inbox sorting, weekly digests, and Syncthing sync.
- **CLI presentation tool and Rust security advisory database** - deckrun is a local-first Markdown presentation CLI for writing, presenting, and exporting slides with 14 themes, KaTeX equations, Mermaid diagrams, and Puppeteer PDF export; advisory-db mirrors the RustSec security advisory database in TOML/Markdown format with OSV export for cargo-audit, trivy, and GitHub Advisory Database integration.

---

`📡 Currently exploring Self-hosted AI workspace with MCP agents and RAG, alongside local LLM inference optimization on consumer GPU`
<!-- BADGE-BOT:END -->

[contact@itguys.ro](mailto:contact@itguys.ro)
