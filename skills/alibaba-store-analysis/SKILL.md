---
name: alibaba-store-analysis
description: Generate a concise weekly business report for Alibaba International stores, pulling metrics via browser automation and API calls.
---

# Alibaba International Store Weekly Analysis

## Overview
This skill automates the retrieval and interpretation of the Alibaba International (i.alibaba.com) weekly business report. It logs in via the user’s browser session, fetches summary metrics through the `diagnoseData.json` endpoint, validates the response, and then presents a structured markdown report covering key indicators, diagnostic insights, actionable tasks, and a link to the full weekly report. Optionally it can pull the complete report payload (via `queryWeekReportAllData.json`) for on‑demand deeper analysis.

## Core Workflows
1. **Login Verification** – Open `https://i.alibaba.com/`. If the page redirects to Alibaba’s login portal, prompt the user to complete authentication and wait until the session is valid.
2. **Fetch Summary Data** – Execute a `POST` request to `https://crm.alibaba.com/crmlogin/aisales/dingwukong/diagnoseData.json` from the browser console, requesting credentials‑included cookies.
3. **Silent Validation** – Ensure the response contains non‑empty `encryptedReportId` and `values.receipt`. If critical fields are missing, emit a friendly fallback message and stop.
4. **Render Structured Report** – Using the `values.weekDiagnose` (filtered for the last 7 days) and `values.diagnoseSummary`, assemble four markdown sections:
   - **Store Data Overview** – a table of core metrics (clicks, inquiries, conversion, etc.) with week‑over‑week change and industry‑average comparison.
   - **Diagnostic Summary** – a narrative paragraph taken from `values.diagnoseSummary`.
   - **Merchant Tasks** – a cleaned list of recommended actions extracted from `maTaskList`.
   - **Weekly Report Link** – a URL built with the `encryptedReportId` for the full report.
5. **Optional Full‑Report Retrieval** – If the user requests deeper insight, call `https://crm.alibaba.com/crmlogin/aisales/dingwukong/queryWeekReportAllData.json` with the `receipt` token, validate the payload, store it internally, and reply with a short acknowledgment (“Full data analysis complete…”) before awaiting specific questions.

## Usage
```bash
openclaw skill run alibaba-store-analysis [--profile <browser-profile>]
```
- `--profile` (optional) lets the user specify which browser profile the skill should use; defaults to the globally configured OpenClaw profile.
- The skill runs interactively: it may pause for login, then automatically proceeds once the session is authenticated.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `profile` | string | Name of the browser profile to operate with. | `openclaw` |
| `fullReport` | boolean | If true, after the summary the skill also loads the detailed `queryWeekReportAllData.json` payload for later questions. | `false` |

## Output
The skill emits a single markdown block containing:
```markdown
### Store Data Overview
| Metric | This Week | WoW Change | vs. Industry Avg |
|---|---|---|---|
| Clicks | 123 | +5.2% | -12.3% |
…

### Diagnostic Summary
Your store’s exposure is below the industry average…

### Merchant Tasks
- Publish 5 potential winning products – expected +40 % exposure
- Build 10 premium/trending products – expected +20 % exposure

### Weekly Report Link
https://crm.alibaba.com/crmagent/crm-grow/luyou/report-render.html?id=<<encryptedReportId>>&dateScope=week&isDownload=false
```
If validation fails, the output is a concise apology and a suggestion to provide a screenshot or manual metrics.

## Examples
```
# Basic run (summary only)
openclaw skill run alibaba-store-analysis

# Run with a custom browser profile and fetch the full report for later questions
openclaw skill run alibaba-store-analysis --profile work-profile --fullReport true
```
The first command prints the four‑section summary. The second command also loads the full‑report JSON silently and replies with “Full data analysis complete…” ready for follow‑up queries.

## Troubleshooting
- **Not logged in** – The skill will detect a redirect to `login.alibaba.com`. Open the link, complete the login, then type “done” when you return to the skill.
- **Empty or missing fields** – If `encryptedReportId` or `values.receipt` are absent, the skill reports: “Sorry, no business data is available for the current account…” and stops.
- **API rate‑limit** – Avoid invoking the skill repeatedly within a short window; wait at least a minute between runs.
- **Browser console errors** – Ensure the browser profile has cookies enabled and that you are not using an ad‑blocker that interferes with `crm.alibaba.com` requests.

---