# open-accio-skill

E-commerce automation skills — standalone, no vendor lock-in.

**Repository:** https://github.com/simoncai519/open-accio-skill

---

## Why This Exists

Some tools make you adopt their entire ecosystem to get value from one good idea. Accio had a genuinely useful concept — modular, workflow-oriented AI agent skills for e-commerce operators — but you had to live inside their app to use it.

This repo takes the best e-commerce skills, rebuilds them as standalone OpenClaw skills, and publishes them here. The idea is good; the delivery mechanism is optional.

---

## Available Skills

Currently available (4 of ~50 planned):

| Skill | What It Does |
|---|---|
| `amz-hot-keywords` | Scrape Amazon search rankings from AMZ123 (ABA data, weekly) |
| `tariff-search` | HS code classification + landed cost calculation |
| `sycm-analysis-skill` | Taobao store weekly report extraction |
| `alibaba-store-analysis` | Alibaba International store weekly report |

More skills being added regularly.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/simoncai519/open-accio-skill.git
cd open-accio-skill

# 2. Install a skill (into your OpenClaw workspace)
clawhub install ./skills/amz-hot-keywords

# 3. Use it
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

These skills are rebuilt from the ground up — not forks, not mirrors. The goal is to make the workflow logic freely available regardless of which agent framework you use.

---

## License

MIT — use freely, modify freely, no attribution required.
