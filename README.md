# open-accio-skill

E-commerce automation skills — standalone, no vendor lock-in.

---

## Why This Exists

Some tools make you adopt their entire ecosystem to get value from one good idea. Accio had a genuinely useful concept — modular, workflow-oriented AI agent skills for e-commerce operators — but you had to live inside their app to use it.

This repo takes the best e-commerce skills, rebuilds them to work as standalone OpenClaw skills, and publishes them here. Use them with OpenClaw, or adapt them for any agent framework. The idea is good; the delivery mechanism is optional.

---

## What You Get

Cross-border e-commerce workflows for: Amazon keyword research, tariff & HS code lookup, Taobao and Alibaba store analytics, product description generation, Shopify development, and more.

Each skill is self-contained and runs against real platform APIs and data sources — no synthetic data, no toy examples.

---

## Skills

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
| `product-description-generator` | SEO product descriptions across Amazon, Shopify, eBay, Etsy |
| `alibaba-publish-skill` | Alibaba International product publishing workflow |

### Platform Tools

| Skill | What It Does |
|---|---|
| `shopify-dev-mcp` | Shopify Admin/Storefront API, Liquid validation |
| `shopify-developer` | Shopify GraphQL and app development |
| `cj-dropshipping-api` | CJ Dropshipping V2 integration (products, orders, logistics) |

---

## Quick Start

**Prerequisites:** OpenClaw agent runtime

```bash
# Install a skill
clawhub install ./skills/amz-hot-keywords

# Use it — the agent picks it up automatically
# "Check hot keywords for dog bed"
```

Skills can also be used standalone via their scripts:

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

## License

MIT — use freely, modify freely.
