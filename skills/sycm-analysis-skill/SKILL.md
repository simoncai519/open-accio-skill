---
name: sycm-analysis-skill
description: Retrieve Taobao Sycm weekly business insights via a browser‑driven API flow.
---

# Sycm Weekly Business Insight Skill

## Overview
This skill taps the internal Taobao Sycm (Business Advisor) service to fetch a store’s weekly performance summary. It orchestrates a short browser session, validates that the user is logged in, fires a request to the Sycm endpoint, and then polls the result until a markdown report materialises.

## Core Workflow
1. **Launch a browser page** pointing at `https://sycm.taobao.com`. The skill expects the `openclaw` browser profile to be used.
2. **Detect login state** – if the page redirects to `https://login.taobao.com` we know the user is not authenticated. In that case the skill prompts the user to complete QR‑code login and re‑checks every few seconds.
3. **Ask Sycm for the weekly report** by sending a GET request to:
   ```
   https://sycm.taobao.com/ucc/next/message/send.json?text=%E6%9F%A5%E7%9C%8B%E5%91%A8%E6%8A%A5
   ```
   The JSON reply contains `conversationCode` and `sendTime` which identify the request.
4. **Poll for the result** – every 5 seconds the skill calls:
   ```
   https://sycm.taobao.com/ucc/next/message/getReportResult.json?conversationCode={conversationCode}&sendTime={sendTime}
   ```
   The loop stops as soon as `data.content` is non‑empty (or after a 5‑minute timeout). The content is already formatted in markdown.
5. **Return the markdown** straight to the user, preserving any embedded links or tables.

## Usage
```text
/accio run sycm-analysis-skill
```
The command launches the flow described above. The user only needs to be logged into Sycm; the skill handles all networking and waiting.

## Edge Cases & Guidance
| Situation | How the skill reacts |
|-----------|----------------------|
| Page redirects to login.taobao.com | Prompts the user to complete QR login, then retries the login check every 5 s.
| API returns an error or no `conversationCode` | Informs the user that the request failed and suggests retrying later.
| Polling exceeds 5 minutes without data | Stops the loop and notifies the user that the report generation timed out.
| The service replies with a “too many visitors” message | Suggests waiting a few minutes before trying again.

## Remarks
* The skill never alters store configuration – it only reads publicly available report data.
* All markdown is handed back unchanged, so charts, tables, and Qianniu links remain clickable.
* Rate‑limit awareness: the skill limits itself to one request per minute per user to stay friendly with Sycm's API.

## Troubleshooting
- **Login never succeeds** – ensure the `openclaw` profile is linked to a logged‑in Chrome or Safari session.
- **Empty response** – confirm that the store actually has a weekly report for the requested period.
- **Network errors** – check your internet connection or any corporate firewall that might block `sycm.taobao.com`.
