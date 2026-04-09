# open-accio-skill

E-commerce automation skills — standalone, no vendor lock-in.

**Repository:** https://github.com/simoncai519/open-accio-skill

---

## Why This Exists

The idea of Accio is cool, but why need another agent?

Some tools make you adopt their entire ecosystem to get value from one good idea. Accio had a genuinely useful concept — modular, workflow-oriented AI agent skills for e-commerce operators — but you had to live inside their app to use it. This repo takes the best e-commerce skills, rebuilds them as standalone OpenClaw skills, and publishes them here.

---

## Available Skills

**10 skills currently available** (more being added regularly):

### Data & Analytics
| Skill | What It Does |
|---|---|
| `amz-hot-keywords` | Scrape Amazon search rankings from AMZ123 (ABA data, weekly) |
| `tariff-search` | HS code classification + landed cost calculation |
| `sycm-analysis-skill` | Taobao store weekly report extraction |
| `alibaba-store-analysis` | Alibaba International store weekly report |

### Listing & Content
| Skill | What It Does |
|---|---|
| `amz-product-optimizer` | Amazon listing optimization pipeline (keywords → titles → AI images → CTR monitoring) |
| `product-description-generator` | SEO product descriptions across Amazon, Shopify, eBay, Etsy |
| `etsy-pod-automation` | Etsy + Printify POD full automation (trend → design → list → social) |

### Platform Tools
| Skill | What It Does |
|---|---|
| `cj-dropshipping-api` | CJ Dropshipping V2 integration (products, orders, logistics, Shopify sync) |
| `shopify-dev-mcp` | Shopify Admin/Storefront API, Liquid validation, GraphQL |
| `creating-financial-models` | E-commerce DCF, sensitivity analysis, scenario planning |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/simoncai519/open-accio-skill.git
cd open-accio-skill

# 2. Install a skill into your OpenClaw workspace
clawhub install ./skills/amz-hot-keywords

# 3. Use it — the agent picks it up automatically
# "Check hot keywords for dog bed"
```

Skills also work standalone via their scripts:

```bash
python3 skills/amz-hot-keywords/scripts/amz_scraper.py --keyword "yoga mat"
```

---

## Skill Structure

```
skills/<name>/
├── SKILL.md           # Skill definition + usage guide
├── references/        # Detailed workflow docs (loaded on demand)
└── scripts/          # Executable code (Python/Bash)
```

---

## Philosophy

Skills are rebuilt from the ground up — not forks, not mirrors. Same workflow logic, original expression. MIT licensed — use freely regardless of which agent framework you run.

---

## License

MIT — use freely, modify freely, no attribution required.
