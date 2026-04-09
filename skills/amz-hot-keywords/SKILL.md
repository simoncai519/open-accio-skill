---
name: amz-hot-keywords
description: Retrieve Amazon hot‑search keywords and their rank trends from AMZ123 (Amazon Brand Analytics)
---

# Amazon Hot Keywords

## Overview
This skill pulls the weekly Amazon Brand Analytics (ABA) hot‑keyword list from the public AMZ123 portal. It returns a CSV where each row contains the search term, the current week’s rank, the previous week’s rank, and a simple trend indicator (up, down, flat, new).

## Core Workflows
1. **Navigate** – Build a URL to AMZ123’s US top‑keywords page with the user‑provided query.
2. **Scrape** – Launch a head‑less Chrome instance via Selenium, wait for the keyword table to load, and harvest up to 200 entries using a set of fallback CSS selectors.
3. **Calculate Trend** – Compare the current rank with the last‑week rank to label the movement.
4. **Persist** – Write the results to a timestamped CSV file under the chosen output directory.
5. **Report** – Emit a short JSON summary (keyword, total rows, CSV path, sample rows) for downstream agents.

## Usage
```bash
python3 $(pwd)/scripts/amz_scraper.py --keyword "<your term>" [options]
```

### Parameters
| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--keyword` | Yes | The seed term to query on AMZ123. | `--keyword "dog bed"` |
| `--max-results` | No | Upper limit of records to retrieve (default 200). | `--max-results 100` |
| `--output-dir` | No | Destination folder for the CSV (default current directory). | `--output-dir ./data` |
| `--headless` | No | Run Chrome headless (`true`/`false`, default `true`). | `--headless false` |

## Output
The script creates a file named:
```
amz123_hotwords_<keyword>_<YYYYMMDD>_<HHMMSS>.csv
```
with columns:
- **search_term** – The keyword being tracked.
- **current_rank** – Rank for the current week.
- **last_rank** – Rank for the previous week (0 if not present).
- **trend** – One of `up`, `down`, `flat`, or `new`.

## Examples
```bash
# Basic request
python3 scripts/amz_scraper.py --keyword "yoga mat"

# Limited to 50 results, store in ./results, run with a visible browser
python3 scripts/amz_scraper.py \
  --keyword "pet supplies" \
  --max-results 50 \
  --output-dir ./results \
  --headless false
```
Both commands will output a CSV and print a JSON block like:
```json
{
  "keyword": "yoga mat",
  "total": 123,
  "csv": "./amz123_hotwords_yoga_mat_20240409_191200.csv",
  "sample": [
    {"search_term":"yoga mat","current_rank":5,"last_rank":7,"trend":"up"},
    ...
  ]
}
```

## Troubleshooting
- **Empty CSV** – The site may have changed; inspect `debug_page.html` (saved alongside the script) for missing elements.
- **Selector errors** – Update the selector lists in `scripts/amz_scraper.py` under the `SELECTORS` constant.
- **Chrome launch failures** – Verify Chrome is installed; Selenium 4.6+ bundles the driver automatically.
- **Rate‑limit or CAPTCHA** – Reduce request frequency or run with `--headless false` to manually solve challenges.

For persistent issues, consider filing a bug upstream with a snapshot of the HTML and the script version.
