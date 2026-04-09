# CLAUDE.md

You are working inside the `open-accio-skill` repository — an open-source e-commerce agent skill hub.

## Repo Context

- **Purpose:** Curated, rewritten e-commerce Agent Skills for cross-border sellers, researchers, and developers.
- **License:** MIT
- **Origin:** Workflows inspired by accio.ai agent skills, but **fully rewritten from scratch** — no copied text, no IP issues.

## Skill Structure

Each skill is a directory under `skills/` with:

```
skills/<skill-name>/
├── SKILL.md          # Required: skill definition, usage, examples
├── scripts/          # Optional: Python/shell helpers
├── references/       # Optional: API docs, reference materials
└── assets/           # Optional: images, data files
```

## SKILL.md Format

```yaml
---
name: <skill-name>
description: <one-liner>
---

# <Skill Name>

## Overview
## Core Workflows
## Usage
## Examples
## Troubleshooting
```

## Rules

1. **Never copy text from accio SKILL.md files**
2. **Extract workflow logic only**, then rewrite entirely in your own words
3. **APIs and endpoints are not copyrightable** — cite them freely
4. **Every skill must have a SKILL.md** — that's the contract with the agent runtime
5. **Test before merging** — if a script is included, verify it runs

## Working in This Repo

- Use `claude` (Claude Code) for any coding tasks
- Python scripts → `scripts/` directory
- Reference docs → `references/` directory
- Keep SKILL.md focused and executable by an agent
