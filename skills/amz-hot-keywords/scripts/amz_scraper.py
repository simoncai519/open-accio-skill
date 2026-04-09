#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reimplemented scraper for AMZ123 US Top Keywords.
It fetches Amazon Brand Analytics weekly rankings via the public AMZ123 interface.
Outputs a CSV containing the search term, this week's rank, prior week's rank, and a trend indicator.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = "https://www.amz123.com/usatopkeywords"

# CSS selectors used to locate elements. Multiple fallbacks increase resilience to site redesigns.
SELECTORS = {
    "container": [
        ".table-body-item",
        ".hotword-item",
        ".keyword-item",
        "[class*='table-body'] > div",
    ],
    "term": [
        ".table-body-item-words-word",
        ".table-body-item-word",
        "[class*='word']",
    ],
    "rank": [
        ".table-body-item-rank",
        "[class*='rank']",
    ],
}


def evaluate_trend(this_week: int, last_week: int) -> str:
    """Derive a simple trend label.

    lower numeric rank = higher popularity.
    "new" indicates the term was absent last week.
    "up" means the rank improved (numerically lower), "down" the opposite, and "flat" unchanged.
    """
    if last_week == 0:
        return "new"
    if this_week < last_week:
        return "up"
    if this_week > last_week:
        return "down"
    return "flat"


def launch_browser(headless: bool = True) -> webdriver.Chrome | None:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
    try:
        return webdriver.Chrome(options=opts)
    except Exception as exc:
        print(f"[ERROR] Chrome launch failed: {exc}", file=sys.stderr)
        print("[HINT] Ensure Chrome is installed; Selenium 4.6+ bundles the driver.", file=sys.stderr)
        return None


def try_select(driver, selectors):
    """Return the first non‑empty result set for a list of CSS selectors."""
    for sel in selectors:
        try:
            elems = driver.find_elements(By.CSS_SELECTOR, sel)
            if elems:
                return elems, sel
        except Exception:
            continue
    return [], None


def harvest_keywords(driver, limit: int = 200) -> list[dict]:
    """Extract raw keyword data from the page.
    Attempts a JavaScript based bulk fetch first; falls back to element‑by‑element parsing.
    """
    # JS bulk extraction using the first term and container selectors
    for term_sel in SELECTORS["term"]:
        for cont_sel in SELECTORS["container"]:
            script = f"""
            const items = Array.from(document.querySelectorAll('{cont_sel}'));
            return items.slice(0, {limit}).map(item => {{
              const termElem = item.querySelector('{term_sel}');
              const term = termElem ? termElem.textContent.trim() : '';
              const rankBox = item.querySelector('{SELECTORS['rank'][0]}');
              let cur = 0, prev = 0;
              if (rankBox) {{
                const spans = rankBox.querySelectorAll('span');
                if (spans.length >= 2) {{
                  const c = spans[0].textContent.trim();
                  const p = spans[1].textContent.trim();
                  cur = /^\\d+$/.test(c) ? parseInt(c) : 0;
                  prev = /^\\d+$/.test(p) ? parseInt(p) : 0;
                }}
              }}
              return {{ term, cur, prev }};
            }});
            """
            try:
                data = driver.execute_script(script)
                filtered = [d for d in data if d.get('term')]
                if filtered:
                    print(f"[INFO] Collected {len(filtered)} entries via JS (container={cont_sel}, term={term_sel})")
                    return filtered
            except Exception:
                continue
    # Fallback using alternate rank selectors
    for rank_sel in SELECTORS["rank"][1:]:
        for cont_sel in SELECTORS["container"]:
            script = f"""
            const items = Array.from(document.querySelectorAll('{cont_sel}'));
            return items.slice(0, {limit}).map(item => {{
              const termElem = item.querySelector('{SELECTORS['term'][0]}');
              const term = termElem ? termElem.textContent.trim() : '';
              const rankBox = item.querySelector('{rank_sel}');
              let cur = 0, prev = 0;
              if (rankBox) {{
                const spans = rankBox.querySelectorAll('span');
                if (spans.length >= 2) {{
                  const c = spans[0].textContent.trim();
                  const p = spans[1].textContent.trim();
                  cur = /^\\d+$/.test(c) ? parseInt(c) : 0;
                  prev = /^\\d+$/.test(p) ? parseInt(p) : 0;
                }}
              }}
              return {{ term, cur, prev }};
            }});
            """
            try:
                data = driver.execute_script(script)
                filtered = [d for d in data if d.get('term')]
                if filtered:
                    print(f"[INFO] Collected {len(filtered)} entries via fallback rank selector (container={cont_sel}, rank={rank_sel})")
                    return filtered
            except Exception:
                continue
    return []


def run_scrape(keyword: str, max_items: int = 200, headless: bool = True) -> list[dict]:
    """Core routine that returns a list of dictionaries ready for CSV export."""
    browser = launch_browser(headless)
    if not browser:
        return []
    try:
        target = f"{BASE_URL}?k={keyword}"
        print(f"[INFO] Opening {target}")
        browser.get(target)
        try:
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS["term"][0]))
            )
        except TimeoutException:
            print("[WARN] Primary selector not found within timeout; proceeding anyway.")
            time.sleep(5)
        # Store a copy of the page for debugging
        debug_path = os.path.join(os.path.dirname(__file__), "debug_page.html")
        with open(debug_path, "w", encoding="utf-8") as dbg:
            dbg.write(browser.page_source)
        raw = harvest_keywords(browser, max_items)
        if not raw:
            print("[WARN] No data on first pass – scrolling then retrying.")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            raw = harvest_keywords(browser, max_items)
        results = []
        for entry in raw:
            cur = entry["cur"]
            prev = entry["prev"]
            results.append({
                "search_term": entry["term"],
                "current_rank": cur,
                "last_rank": prev,
                "trend": evaluate_trend(cur, prev),
            })
        print(f"[OK] Gathered {len(results)} keyword rows for '{keyword}'.")
        return results
    except Exception as exc:
        print(f"[ERROR] Scrape failed: {exc}", file=sys.stderr)
        return []
    finally:
        browser.quit()


def dump_csv(rows: list[dict], keyword: str, out_dir: str) -> str | None:
    if not rows:
        print("[ERROR] No rows to write.")
        return None
    os.makedirs(out_dir, exist_ok=True)
    safe_key = keyword.replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(out_dir, f"amz123_hotwords_{safe_key}_{timestamp}.csv")
    pd.DataFrame(rows).to_csv(file_path, index=False, encoding="utf-8")
    print(f"[OK] CSV saved to {file_path}")
    return file_path


def cli():
    parser = argparse.ArgumentParser(description="Fetch Amazon Brand Analytics hot‑keywords via AMZ123.")
    parser.add_argument("--keyword", required=True, help="Primary search term, e.g. 'dog bed'")
    parser.add_argument("--max-results", type=int, default=200, help="Maximum records to retrieve (default 200)")
    parser.add_argument("--output-dir", default=".", help="Folder for the CSV output (default cwd)")
    parser.add_argument("--headless", type=str, default="true", help="Run Chrome headless (true/false)")
    args = parser.parse_args()
    headless = args.headless.lower() == "true"
    data = run_scrape(args.keyword, args.max_results, headless)
    if not data:
        sys.exit(1)
    csv_file = dump_csv(data, args.keyword, args.output_dir)
    # Provide a concise JSON payload for downstream agents
    summary = {
        "keyword": args.keyword,
        "total": len(data),
        "csv": csv_file,
        "sample": data[:5],
    }
    print("\n--- RESULT_JSON ---")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    cli()
