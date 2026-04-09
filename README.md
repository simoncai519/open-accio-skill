# open-accio-skill

> Curated e-commerce Agent Skills, rewritten from scratch.  
> Each skill is a self-contained workflow for cross-border e-commerce operators, researchers, and developers.

---

## 🎯 What Is This?

A community-driven, open-source collection of AI agent skills purpose-built for e-commerce.

All skills are **rewritten from the ground up** — extracting core workflow logic without copying any existing IP. The goal: one repo where e-commerce professionals can find production-ready agent skills for every stage of the business.

---

## 📦 Available Skills

### 🔴 High Priority

| Skill | Description |
|---|---|
| `amz-hot-keywords` | Scrape Amazon ABA (AMZ123) weekly search term rankings |
| `amz-product-optimizer` | End-to-end Amazon listing optimization (keywords → titles → AI images → CTR monitoring) |
| `tariff-search` | HS code classification + landed cost calculation via TurtleClassify API |
| `sycm-analysis-skill` | Taobao Sycm (生意参谋) weekly report extraction + structured analysis |
| `alibaba-store-analysis` | Alibaba International weekly business report parser + diagnostic summary |
| `etsy-pod-automation` | Etsy + Printify POD full automation (trend → design → list → social → monitor) |
| `cj-dropshipping-api` | CJ Dropshipping V2 API deep dive (products, orders, logistics, Shopify integration) |

### 🟠 Medium Priority

| Skill | Description |
|---|---|
| `shopify-dev-mcp` | Shopify Dev MCP — Admin/Storefront API, Liquid, Polaris, Theme Check |
| `shopify-developer` | Shopify GraphQL + App development assistant |
| `alibaba-publish-skill` | Alibaba International product publishing workflow |
| `product-description-generator` | Multi-platform SEO product descriptions (Amazon / Shopify / eBay / Etsy) |
| `product-selection` | Data-driven product selection workflow |
| `product-supplier-sourcing` | Supplier sourcing and verification |
| `cross-border-selection` | Cross-border e-commerce product selection |
| `market-insight-product-selection` | Market insight-driven product selection with charting |
| `product-marketing-context` | Product marketing context generation |
| `ecommerce-marketing` | E-commerce marketing strategy toolkit |
| `launch-strategy` | New product launch playbook |
| `review-analyst-agent` | Competitor review analysis |
| `review-summarizer` | Review summarization + insight extraction |
| `sales-negotiator` | B2B sales negotiation strategies |

### 🟡 Operations & Tools

| Skill | Description |
|---|---|
| `social-content` | Social media content creation |
| `social-media-publisher` | Social media scheduling + publishing |
| `social-network-mapper` | Social network mapping |
| `lark-tools` | Feishu/Lark integration toolkit |
| `docx` | Word document generation |
| `pdf` | PDF generation + processing |
| `pptx` | PowerPoint generation |
| `xlsx` | Excel data processing |

---

## 🚀 Quick Start

### Prerequisites

- OpenClaw agent runtime (or any compatible agent framework)
- Python 3.9+ (for skills with scripts)
- Browser access (for scraping skills)
- Platform API credentials as required per skill

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/open-accio-skill.git
cd open-accio-skill

# Explore skills
ls skills/
```

### Usage

Each skill lives in its own directory under `skills/`. Read the `SKILL.md` inside each skill for specific usage instructions.

---

## ⚖️ Legal & Contribution

- **License:** MIT (see `LICENSE`)
- **Contribution:** All skills must be original rewrites — no copy-paste from proprietary sources
- **Quality bar:** Every skill must be executable and tested before merging

---

## 📂 Repo Structure

```
open-accio-skill/
├── README.md
├── LICENSE
├── CLAUDE.md
└── skills/
    ├── amz-hot-keywords/
    ├── amz-product-optimizer/
    ├── tariff-search/
    ├── sycm-analysis-skill/
    └── ...
```
