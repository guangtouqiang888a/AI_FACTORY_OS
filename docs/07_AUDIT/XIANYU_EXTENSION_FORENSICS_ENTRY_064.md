# XIANYU_EXTENSION_FORENSICS_ENTRY_064

---

**ENTRY STATUS:** PASS  
**ENTRY ID:** 064  
**DATE:** 2026-08-30  
**TYPE:** Forensics / Architecture Blueprint（无生产采集）

**ZIP Source:** `D:\闲鱼全自动采集插件1.zip`  
**Extracted:** `1_DATA/_tests/xianyu_extension_forensics_064/`  
**Reference Copy:** `1_DATA/_tests/xianyu_extension_forensics_064/reference_plugin/my-xianyu-scraper/`

---

## A. Plugin Identity

| Field | Value |
|-------|-------|
| Display name | 闲鱼全自动高热度采集器 |
| Popup title | 闲鱼自动采集助手 |
| Internal folder | `my-xianyu-scraper` |
| Manifest version | **3** |
| Extension version | **1.3** |
| Background / Service Worker | **None** |
| Options page | **None** |
| External libraries | **None** |

## B. ZIP Integrity

- File exists at `D:\闲鱼全自动采集插件1.zip`
- `zipfile.testzip()` → **None** (no corruption)
- Extracted to `plugin_zip_extract/` and clean reference copy in `reference_plugin/`

## C. Manifest

```json
{
  "manifest_version": 3,
  "name": "闲鱼全自动高热度采集器",
  "version": "1.3",
  "permissions": ["activeTab", "scripting", "storage"],
  "action": { "default_popup": "popup.html" },
  "content_scripts": [{
    "matches": ["*://*.goofish.com/*", "*://*.2yuanbao.com/*"],
    "js": ["content.js"]
  }]
}
```

## D. Permissions

| Permission | Used? | AIFO necessity |
|------------|-------|----------------|
| `activeTab` | Yes (popup → active tab) | **Required** |
| `scripting` | Declared; content_scripts auto-inject | **Required** (MV3) |
| `storage` | Declared; **not used in popup/content** | Optional (session prefs) |
| Host: `goofish.com` | Yes | **Required** for Xianyu |
| Host: `2yuanbao.com` | Declared | **Remove** unless needed |
| `cookies` / `webRequest` | Not declared | **Do not add** |

**Principle:** Minimal permissions — no cookie, no broad `<all_urls>`.

## E. Files

| File | Size (approx) | Role |
|------|---------------|------|
| `manifest.json` | 365 B | MV3 config |
| `content.js` | 3522 B | Scroll, paginate, scrape, message listener |
| `popup.html` | 2037 B | Config UI (minWant, maxPages) |
| `popup.js` | 2665 B | Start scrape, preview, CSV export |
| `1 部署插件.png` | guide | Install instructions |
| `2 使用插件.png` | guide | Usage instructions |

**Absent:** `background.js`, `service_worker`, `options.js`, `utils/`, npm libs, historical CSV/XLSX in ZIP.

## F. Content Script — Forensics

**Who calls:** Chrome auto-injects on `goofish.com` / `2yuanbao.com` page load.  
**When:** On matched page; also responds to popup message `start_auto_scrape`.  
**Input:** `{ action, minWant, maxPages }` via `chrome.runtime.onMessage`.  
**Output:** `{ data: [{ wantCount, title, price, link, imgUrl }] }`.  
**State:** `seenTitles` Set — page-local only; not persisted.  
**DOM dependency:** **Yes** — `querySelectorAll`, `innerText`, class substring selectors.  
**URL dependency:** **Indirect** — assumes user already on search results; no URL parsing.  
**CSS selectors:** `[class*="item"]`, `[class*="card"]`, `[class*="title"]`, `[class*="price"]`, `[class*="search-pagination-page-box"]`.  
**Platform text:** Regex `/(\d+)\s*人想要/` on card `innerText`.  
**API dependency:** **None** — no `fetch`, no `mtop`, no XHR.

## G. Popup

**Who calls:** User clicks extension icon.  
**When:** Before/after scrape.  
**Input:** User sets `minWant` (default **50**), `maxPages` (default **3**).  
**Output:** Status text, preview table (first 5 rows), CSV download.  
**Communication:** `chrome.tabs.query` → `chrome.tabs.sendMessage(tab.id, { action: "start_auto_scrape", minWant, maxPages })`.  
**State:** `currentData` array in popup memory only.

## H. Background

**N/A** — no background/service worker. All logic in content script + popup.

## I. Original Workflow (源码证据)

```text
User manually opens Xianyu search results in normal Chrome
    ↓
User clicks extension popup
    ↓
User sets minWant (≥50) and maxPages (3)
    ↓
popup.js → chrome.tabs.sendMessage({ action: "start_auto_scrape", minWant, maxPages })
    ↓
content.js: for i in 0..maxPages-1:
    autoScrollToBottom()
    scrapeCurrentPage(minWant)   ← filter INSIDE collector
    goToNextPage() + sleep(5000)
    ↓
sendResponse({ data: finalResults })
    ↓
popup: preview table + CSV Blob download
```

## J. Search Control

**Plugin does NOT:**
- Type keywords
- Navigate to search URL
- Validate SEARCH_RESULT vs RECOMMENDED

**Plugin assumes:** User has already performed search and is on a results page.

**AIFO:** Search Controller (063) must be separate from Collector; classify `result_origin`.

## K. Scroll Logic

| Parameter | Value |
|-----------|-------|
| Step | 400px |
| Interval | 300ms |
| Stop condition | `totalHeight < scrollHeight - 1000` |
| Bottom wait | 2000ms after `scrollTo(bottom)` |
| Assumption | Lazy-load listings/images on scroll |

**Verdict:** Pattern **reusable**; constants should become bounded-wait config in Xianyu Adapter.

## L. Pagination Logic

| Aspect | Implementation |
|--------|----------------|
| Selector | `[class*="search-pagination-page-box"]` |
| Current page | `className.includes('active')` |
| Next page | Click next box if text is numeric, `>`, or contains `下一页` |
| Max pages | `request.maxPages` from popup |
| Pre-click | `scrollIntoView` + 600ms |
| Post-click wait | **sleep(5000)** hardcoded |
| Retry | None |

**Verdict:** Click pattern **reusable**; fixed 5s sleep **must rewrite** to page readiness.

## M. Title Extraction

- Selector: `[class*="title"]` → `innerText.trim()`
- Fallback: `"未知标题"`
- **Class:** REALITY (heuristic selector)

## N. Price Extraction

- Selector: `[class*="price"]` → `innerText.trim()`
- Fallback: `"面议"`
- **Class:** REALITY

## O. Want Count Extraction

- Source: `card.innerText`
- Regex: `/(\d+)\s*人想要/`
- Parse: `parseInt(match[1])`
- **Class:** REALITY when matched

## P. Want Count Missing Behavior

```javascript
const match = text.match(/(\d+)\s*人想要/);
if (match) { /* only then consider card */ }
// cards without match → silently skipped
```

| Scenario | Plugin behavior |
|----------|-----------------|
| Visible "61人想要" | Extracted; filtered by minWant |
| No want text on card | **Discarded entirely** |
| want_count = 0 with text | Would pass if ≥ minWant |
| Threshold | `minWant` inside `scrapeCurrentPage` |
| Threshold source | Popup input, default **50** |

**AIFO:** `want_count=NULL`, `want_count_status=MISSING_ON_CARD`; Filter decides; **never NULL→0**.

## Q. URL Extraction

- `card.querySelector('a')` or `card.closest('a')` → `href`
- Fallback: `window.location.href`
- **Class:** REALITY
- **No** `/item?id=` parsing for item ID

## R. Item ID

- **Class:** **MISSING** — not extracted from URL
- **AIFO:** Parse from `source_url` in Xianyu Adapter (`/item?id=`)

## S. Deduplication

- Key: **`title` only** (`seenTitles` Set)
- Scope: Per-page only (Set recreated each `scrapeCurrentPage` call)
- Cross-page dedupe: **No** (concat without global dedupe)

**Problems:**
- Different items with same title collapse
- Same item on multiple pages may duplicate
- href/item_id ignored

**AIFO:** `source + source_item_id` primary; content hash fallback; **not title-only**.

## T. Filtering

- Location: **Inside `scrapeCurrentPage`** (Collector)
- Rule: `wantCount >= minWant`
- Cards without want text never reach filter

**AIFO:** Filter is **separate layer** after full MarketRecord capture.

## U. Export

- Format: CSV UTF-8 with BOM (`\ufeff`)
- Method: `Blob` → `URL.createObjectURL` → anchor `download`
- Columns: 想要人数, 商品标题, 价格, 图片链接, 商品链接
- Filename: `闲鱼采集数据_{timestamp}.csv`

**AIFO:** CSV = **debug/export layer only**; core = MarketRecord → Raw → MarketObservation.

## V. Original Strengths

1. Runs in user's **normal visible Chrome** — not headless automation
2. **DOM-only** — no hidden API / mtop abuse
3. Proven **scroll + pagination + extract** loop
4. Simple **popup ↔ content** message bridge
5. Works when user reaches real search page with rendered cards

## W. Original Weaknesses

1. No search control / result_origin classification
2. Collector-side want filter → selection bias
3. Drops cards without want_count entirely
4. Title-only dedupe
5. No `source_item_id`
6. Broad fragile selectors (`[class*="item"]`)
7. Hardcoded `sleep(5000)` after pagination
8. CSV as only output — no structured pipeline
9. Per-page dedupe only; cross-page duplicates possible

## X. KEEP

| Item | Reason |
|------|--------|
| Content script on visible goofish page | Core Browser-Native Acquisition Pattern |
| DOM visible-text extraction | Matches 061–063 direction |
| Scroll-for-lazy-load pattern | Reusable in Xianyu Adapter |
| Pagination UI click pattern | Adapter-specific, proven |
| popup ↔ content messaging | Extension internal bridge |
| Want regex `人想要` | Move to Xianyu Adapter (versioned) |

## Y. REWRITE

| Item | Target |
|------|--------|
| minWant in scrape loop | `AcquisitionTask.filters.min_want_count` → Filter layer |
| Skip cards without want | NULL + `want_count_status` |
| Title dedupe | `source_item_id` + dedupe_key |
| Broad selectors | Versioned `feeds-item-wrap` selectors (062/063) |
| sleep(5000) | Bounded page readiness wait |
| CSV as core output | MarketRecord batch + Local Bridge |
| User-on-search assumption | SearchSession + Search Controller reporting |
| No result_origin | SEARCH_RESULT / RECOMMENDED / UNKNOWN (DEC-032) |

## Z. REMOVE

| Item | Reason |
|------|--------|
| Collector-side discard of NULL want | Selection bias |
| CSV/Excel as system of record | AIFO uses Raw + Observation |
| 2yuanbao.com match | Unnecessary scope |
| "高热度" framing in production extension | Collector ≠ hotness judgment |
| Excel export as core feature | Debug only |

---

## AA. Acquisition Engine Integration

**Reuse existing modules:**

| Module | Path |
|--------|------|
| Acquisition Engine | `1_DATA/acquisition_engine.py` |
| Collector abstraction | `1_DATA/collector_abstraction.py` |
| Market source core | `1_DATA/market_source_core.py` |
| Search session | `1_DATA/connectors/xianyu_search_session_063.py` |
| Targeted search / want audit | `1_DATA/connectors/xianyu_targeted_search_062.py` |

**AcquisitionTask (minimal):**

```python
{
  "source_id": "src_xianyu_marketplace",
  "query": "Excel模板",
  "scope": {"max_records": 20, "max_pages": 3},
  "schedule": "MANUAL",
  "filters": {
    "min_want_count": null,
    "min_price": null,
    "max_price": null
  }
}
```

## AB. Browser Extension Integration (Entry 065 — not built)

Own MV3 extension with:
- Minimal permissions (`activeTab`, `scripting`, optional `storage`)
- Xianyu-only content script matches
- Emits versioned MarketRecord batches
- Does **not** apply business filters during scrape

## AC. Search Controller

**Original plugin:** User manual only.  
**AIFO:** Search Controller decides navigation to SEARCH_RESULT page; Collector reads whatever is visible; must not conflate EMPTY_SEARCH + 猜你喜欢 with SEARCH_RESULT (DEC-032, 061/062/063 lessons).

## AD. Collector

**Collector responsibility:** "I see product A on this page" — record facts.  
**Not:** Opportunity, score, profit, min_want filtering, business model.

## AE. Filter Layer

```text
MarketObservation
    ↓
Filter (optional min_want_count, price range)
    ↓
Candidate Set
```

| want_count | min_want_count=50 | Result |
|------------|-------------------|--------|
| 61 | | MATCH |
| 20 | | BELOW_THRESHOLD |
| NULL | | **UNKNOWN** (not 0) |

## AF. Data Contract — MarketRecord

Contract version: **064.1.0**  
Artifact: `1_DATA/_tests/xianyu_extension_forensics_064/market_record_contract_064.json`

Minimum fields: `source`, `platform`, `source_item_id`, `source_url`, `title`, `price`, `currency`, `want_count`, `want_count_status`, `result_origin`, `observed_at`, `query`, `session_id`, `collector_version`

## AG. Message Contract

```json
{
  "contract_version": "064.1.0",
  "message_type": "MARKET_RECORD_BATCH",
  "run_id": "...",
  "session_id": "...",
  "source": "xianyu",
  "query": "...",
  "result_origin": "SEARCH_RESULT",
  "records": [...]
}
```

Error statuses: `SUCCESS` | `PARTIAL` | `NO_RESULTS` | `ACCESS_BLOCKED` | `PAGE_STRUCTURE_CHANGED` | `UNKNOWN`

## AH. Raw / Normalize / Observation

```text
Extension → MarketRecord batch
    ↓
Local Bridge (validate contract)
    ↓
Raw { acquisition_run_id, raw_record_id, source, raw_payload, ... }
    ↓
Normalizer (market_source_core)
    ↓
MarketObservation { observation_id, verification_status, ... }
```

Extension **must not** write SQLite directly.

## AI. Source / Sales Separation (DEC-029)

Extension sets `source_platform=xianyu`. Does **not** set `sales_platform`. Discovery source ≠ future sales channel.

## AJ. Product Separation (DEC-030)

External listings → MarketObservation. Not AI_FACTORY_OS Product. No downloading competitor product files.

## AK. Business Model Separation

Extension does **not** evaluate VOLUME_LOW_PRICE, LEAD_GENERATION, PREMIUM_SCARCE, DIRECT_SALE. That belongs to Business Intelligence after Signal/Opportunity layers.

## AL. Future Source Compatibility

Same Engine + MarketRecord schema for Taobao, Search, Social, Overseas — new Source Adapter + extension content script per platform.

## AM. Future Product Compatibility

MarketObservation not locked to Excel; `product_type` reserved for digital_template, document, video, etc.

## AN. Future Sales Platform Compatibility

Supports `source=xianyu`, `sales_platform=taobao` for own products on multiple listing channels.

## AO. Security (Local Bridge)

- Localhost-only binding
- Origin validation
- Versioned JSON schema
- Request/response IDs + timeout
- No credential passthrough

## AP. Compliance Boundary

- No login automation
- No CAPTCHA bypass
- No anti-bot bypass
- No hidden API abuse
- No cookie/token extraction
- On block → `ACCESS_BLOCKED`

## AQ. Current DB Impact

**delta = 0**  
`market_observations = 0`, `products = 0` (verified)

## AR. Tests

`python -m unittest test_xianyu_extension_forensics_064` → **12 OK**

| # | Test |
|---|------|
| 1 | ZIP integrity |
| 2 | Manifest parse |
| 3 | DOM not API |
| 4 | Want count regex |
| 5 | Filter in collector (document anti-pattern) |
| 6 | Title dedupe |
| 7 | Pagination selector + sleep |
| 8 | Popup message bridge |
| 9 | CSV Blob export |
| 10 | No credential extraction |
| 11 | Inventory file |
| 12 | AIFO duplicate modules present |

## AS. Modified Core Files

- `docs/07_AUDIT/XIANYU_EXTENSION_FORENSICS_ENTRY_064.md`
- `docs/02_ARCHITECTURE/XIANYU_BROWSER_EXTENSION_BLUEPRINT_064.md`
- `docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md`
- `docs/01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md`
- `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md`
- `docs/00_GOVERNANCE/AI_FACTORY_OS_EXECUTION_PROTOCOL.md`
- `docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md`
- `docs/00_GOVERNANCE/AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md`
- `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md`
- `1_DATA/test_xianyu_extension_forensics_064.py` (path fix)

## AT. Reviewed but Not Modified

- Constitution (DEC-029/030/031/032 sufficient)
- Decision Log (no new DEC)
- Authority Model
- Business Strategy
- Evolution Context

## AU. Reality Changes

- Reference plugin forensically analyzed — **first concrete Extension prototype evidence**
- Browser Extension + Local Bridge path **formally designed** (not implemented)
- Confirms 061–063 direction: DOM in visible browser works; headless/automation blocked

## AV. Documentation Continuity Check

All required sync items updated per Entry 046.

## AW. Validation Results

All PASS criteria met (see Section 94 of Entry spec).

## AX. Remaining Issues

1. Own Extension not built (→ 065)
2. Local Bridge not built (→ 065)
3. Anonymous automation still cannot reach SEARCH_RESULT (063)
4. Reference plugin selectors differ from 062 `feeds-item-wrap` — adapter must use project selectors

## AY. Recommended Next Entry

**Entry 065 — AI_FACTORY_OS Xianyu Browser Extension v1**

Scope:
- Own MV3 extension (minimal permissions)
- Localhost HTTP bridge receiver in Python
- Wire Acquisition Engine to accept extension batches
- Test-dir first; no Current DB until human-verified import Entry

---

## Required Architecture Diagrams

### 图1 — Original Plugin

```text
User (manual search page)
    ↓
Popup (minWant, maxPages)
    ↓
Content Script
    ↓
DOM (scroll → extract → paginate)
    ↓
Filter (wantCount >= minWant)  ← coupled in collector
    ↓
CSV Export (Blob download)
```

### 图2 — AI_FACTORY_OS Target

```text
User Policy
    ↓
Acquisition Engine
    ↓
AcquisitionTask + Query Strategy
    ↓
Search Controller
    ↓
Browser Extension (065)
    ↓
Xianyu DOM
    ↓
MarketRecord
    ↓
Local Bridge (HTTP POST)
    ↓
Raw
    ↓
Normalize
    ↓
MarketObservation
    ↓
Filter
    ↓
Signal
    ↓
Opportunity
    ↓
Product
```

---

## Required Comparison Table

| Feature | Original Plugin | AI_FACTORY_OS | Action |
|---------|-----------------|---------------|--------|
| Search | User manual | Search Controller + user/065 | **Rewrite** |
| Scroll | 400px/300ms | Xianyu Adapter bounded wait | **Keep pattern** |
| Pagination | UI click + 5s sleep | Adapter + readiness | **Rewrite wait** |
| Title | `[class*=title]` | Versioned adapter selector | **Rewrite** |
| Price | `[class*=price]` | Versioned adapter selector | **Rewrite** |
| Want Count | regex 人想要 | Same regex + status enum | **Keep + extend** |
| URL | a.href | source_url + item_id parse | **Rewrite** |
| Item ID | Missing | Parse from URL | **Add** |
| Dedup | title | source_item_id | **Rewrite** |
| Filter | In collector | Filter layer | **Rewrite** |
| Export | CSV core | Debug only | **Remove from core** |
| DB | None | Raw → Observation | **Add** |
| Provenance | None | run_id, session_id, origin | **Add** |
| Historical Observation | None | MarketObservation timeline | **Add** |
| Source separation | Implicit xianyu | source_platform explicit | **Add** |
| Sales separation | N/A | DEC-029 enforced | **Add** |
| Product separation | N/A | DEC-030 enforced | **Add** |
| Business Model | "高热度" implicit | BI layer only | **Remove from ext** |
| Scheduling | Manual only | Manual now; future AI | **Design** |
| AI Query | None | QueryStrategyProvider reserved | **Design** |
| UI | Popup tool | Future Market Acquisition dashboard | **Design** |

---

## Bridge Options Evaluation

| Option | Security | Stability | Dev complexity | Cross-platform | Python | Verdict |
|--------|----------|-----------|----------------|----------------|--------|---------|
| **A. Local HTTP** | Good (localhost bind) | Good | Low | Yes | Excellent | **Recommended v1** |
| B. WebSocket | Good | Good | Medium | Yes | Good (061已有) | Alternative |
| C. Native Messaging | Good | Medium | High | OS-specific | Medium | Defer |
| D. File queue | Medium | Low (races) | Low | Yes | Good | Defer |
| E. Extension-only storage | N/A | N/A | Low | Yes | None | Rejected |

---

## Key Answers (1–15)

1. **原插件为什么能工作？** 用户在正常 Chrome 中手动打开搜索结果页；content script 读取已渲染 DOM；非 headless/Python 自动化。
2. **与 058E/060 差异？** 058E/060 用 urllib/headless CDP → ACCESS_DENIED；插件继承用户浏览器会话与可见页面。
3. **DOM 还是 API？** **纯 DOM** — 源码无 fetch/mtop/XHR。
4. **能否作为 Xianyu Browser Adapter 参考？** **是** — 提取 scroll/pagination/message 模式；selector 须对齐 062 `feeds-item-wrap`。
5. **可复用思想？** 可见浏览器采集、懒加载滚动、翻页点击、popup↔content 桥、想要数正则。
6. **必须重写？** Collector 内过滤、title 去重、无 item_id、无 result_origin、CSV 为核心、固定 sleep。
7. **想要数缺失？** 原插件丢弃；AIFO 保留 `want_count=NULL` + status。
8. **为何不能作 Collector 硬门槛？** 产生 Selection Bias；系统会误以为所有商品都有 want_count（DEC-032）。
9. **搜索与采集为何分离？** 搜索决定"进哪页"；采集决定"页上有什么"；063 已证明 URL≠SEARCH_RESULT。
10. **扩展与 Engine 如何通信？** Localhost HTTP POST `/acquisition/v1/market-record-batch` v1。
11. **Excel/CSV 在哪层？** Debug/export 层，非 SoT。
12. **以后淘宝？** 新 Source Adapter + extension matches；同一 MarketRecord schema。
13. **以后海外？** 同上；`market_region` 已预留。
14. **source ≠ sales_platform？** Contract + DEC-029；Extension 只写 source。
15. **外部商品 ≠ Product？** DEC-030；Observation 入库；Product 仅自主生产。

---

## Original Plugin Feature Table (Section 55)

| Original Plugin Feature | Keep | Rewrite | Remove | Reason |
|-------------------------|------|---------|--------|--------|
| popup config UI | ✓ | | | Task params pattern |
| content script | ✓ | | | Core acquisition |
| DOM extraction | ✓ | | | Browser-native pattern |
| want regex | ✓ | | | Proven on visible cards |
| pagination | ✓ | | | UI click works |
| scrolling | ✓ | | | Lazy-load trigger |
| dedupe (title) | | ✓ | | Use item_id |
| filtering (minWant) | | ✓ | | Filter layer |
| export (CSV) | | | ✓ | Debug only in AIFO |
| UI "高热度" | | | ✓ | Not collector semantics |
| 2yuanbao match | | | ✓ | Scope reduction |
| no background | ✓ | | | Simpler MV3 |
