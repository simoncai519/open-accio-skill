---
name: tariff-search
description: Retrieve HS codes and calculate import tariffs via TurtleClassify API
---

# Tariff Search Tool

## Overview
The Tariff Search skill connects to the TurtleClassify REST API to identify the correct HS (Harmonized System) code for a product and compute the applicable import duty. It is useful for cross‑border merchants who need to estimate landed costs, classify items for customs, or batch‑process product catalogs.

## Core Workflows
1. **Provide product data** – each entry must contain an origin country, a destination country, and a product name. Optional fields include the desired HS‑code digit length and additional metadata.
2. **Invoke `search_tariff`** – the client sends the list to TurtleClassify, which returns HS code, description, tariff rate, formula and other details.
3. **Consume results** – the skill can output a flat list for easy insertion into a pandas DataFrame/CSV, or a detailed object that includes processing metadata.

## Usage
```python
import os, sys
# Ensure the skill directory is on the Python path
skill_dir = os.path.abspath(os.path.dirname(__file__))
if skill_dir not in sys.path:
    sys.path.insert(0, skill_dir)

from scripts.script import TariffSearch

search = TariffSearch()

products = [
    {
        "originCountryCode": "CN",
        "destinationCountryCode": "US",
        "productName": "Wireless Headphones",
        "digit": 10,
    }
]

# Get a simple list suitable for CSV/DataFrame
results = search.search_tariff(products)
print(results)

# Or request the full response with metadata
full = search.search_tariff(products, return_type="detail")
print(full)
```

## Parameters
| Parameter | Required? | Description |
|-----------|-----------|-------------|
| `originCountryCode` | ✅ | Two‑letter ISO‑3166‑1 code of the exporting country (e.g., `CN`). |
| `destinationCountryCode` | ✅ | Two‑letter ISO‑3166‑1 code of the importing country (e.g., `US`). |
| `productName` | ✅ | Human‑readable product title.
| `digit` | optional | Desired HS‑code length: `8` or `10`. |
| other optional fields | optional | `productId`, `productSource`, `productCategoryId`, `productCategoryName`, `productProperties`, `productKeywords`, `channel` – passed through to the API unchanged. |

## Output
- **List mode** (`return_type='list'`):
  ```json
  [{
    "hsCode": "85171200",
    "hsCodeDescription": "...",
    "tariffRate": 0.0,
    "tariffFormula": "Base Rate: 0%",
    "tariffCalculateType": "AD_VALOREM",
    "originCountryCode": "CN",
    "destinationCountryCode": "US",
    "productName": "Wireless Headphones",
    "calculationDetails": { ... raw API payload ... }
  }]
  ```
- **Detail mode** (`return_type='detail'`): returns a dictionary containing `success`, `results`, `processing_time`, and the raw API payload.

## Examples
### Single product lookup
```python
product = [{"originCountryCode":"CN","destinationCountryCode":"US","productName":"Silk Scarf"}]
print(search.search_tariff(product))
```
### Batch processing from CSV
```python
import pandas as pd

df = pd.read_csv("catalog.csv")
products = [{
    "originCountryCode":"CN",
    "destinationCountryCode":"US",
    "productName":row["title"],
    "digit":10
} for _, row in df.iterrows()]

results = search.search_tariff(products)
# Attach results to the DataFrame using the title‑case column names expected by downstream tools
df["HS Code"] = [r.get("hsCode", "N/A") for r in results]
df["Tariff Rate (%)"] = [r.get("tariffRate", 0) for r in results]
df["HS Description"] = [r.get("hsCodeDescription", "") for r in results]
df["Tariff Formula"] = [r.get("tariffFormula", "") for r in results]

df.to_csv("catalog_with_tariffs.csv", index=False)
```

## Troubleshooting
- **Empty results** – Verify that required fields (`originCountryCode`, `destinationCountryCode`, `productName`) are present and non‑empty.
- **API error codes** – `20001` indicates parameter validation failure; check field formats. `-1` signals a server‑side issue; retry later.
- **Rate limits** – The client enforces a maximum of 10 requests per second and batches no more than 50 items per concurrent worker. Reduce batch size or add delays if you encounter throttling.
- **Missing tariff formula** – The TurtleClassify service may not return a detailed formula; the client fabricates a simple placeholder (`Base Rate: X%`).

---
