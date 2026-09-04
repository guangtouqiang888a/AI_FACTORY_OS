# REAL_XIANYU_BROWSER_COLLECTION_ENTRY_060.md

ENTRY ID: 060  
DATE: 2026-08-30  
STATUS: **PASS / PARTIAL** — Browser Collector Implemented；live headless run = **BLOCKED_BY_ACCESS_CONTROL**  
FIRST_REAL_XIANYU_MARKET_BATCH: **NO**

## A. Objective

Build Xianyu Browser Collector v1: public page → Raw → Normalize → `market_observations` via Acquisition Engine. No login / captcha / anti-bot bypass. Max 20 records, one query.

## B. Dependencies (Reality)

| Dep | Status |
|-----|--------|
| playwright / selenium pip | **Missing**（install timeout / conflict） |
| System Chrome | **Present** |
| System Edge | **Present** |
| Usable backend | **chrome_headless_dump**（`--dump-dom`） |

## C. Adapter Wiring

- `connectors/xianyu_browser_connector.py` — `XianyuBrowserCollector`
- `collector_abstraction.XianyuBrowserAdapter` + `get_adapter("PUBLIC_WEB_READ")`
- `acquisition_engine` execute path for PUBLIC_WEB_READ → abstraction
- Collectors `col_xianyu_browser` / `col_xianyu_public_web` = **LIMITED**（not ACTIVE）

## D. Live Attempt

| Field | Value |
|-------|-------|
| query | `虚拟资料` |
| method | PUBLIC_WEB_READ / chrome headless dump-dom |
| page result | UI: **非法访问** / 请使用正常浏览器访问闲鱼 |
| classification | **ACCESS_DENIED** → `BLOCKED_BY_ACCESS_CONTROL` |
| items extracted | **0** |
| market_observations delta | **0** |
| collection_runs | 1 FAILED run recorded（audit trail） |
| login_used | False |
| bypass_attempted | False |
| hidden_api_called | False |

Artifacts: `1_DATA/_tests/xianyu_browser_collection_060/`

## E. Relation to 058E

058E: urllib HTML-only → CSR shell → NOT_FEASIBLE.  
060: real browser render attempted → **platform access control blocks headless** → still no listing payload. Not a fake success.

## F. Modes After 060

| Mode | Status |
|------|--------|
| USER_EXPORT / MANUAL_IMPORT | **AVAILABLE** |
| PUBLIC_WEB_READ | **LIMITED**（adapter exists；live headless = ACCESS_DENIED） |
| LIVE_API | **NOT_AVAILABLE_CURRENTLY** |

## G. Separations Held

Source ≠ Sales；Observation ≠ Product/Listing/Event；no Opportunity scoring；no Learning；no CF publish.

## H. Compliance

Stopped on ACCESS_DENIED. No captcha solve, no cookie steal, no mtop reverse, no sample.xlsx, no Archive→Current.

## I. Tests

`test_xianyu_browser_060` + updated `test_acquisition_engine_059` — OK.

## J. Recommended Path

Still **USER_EXPORT / MANUAL_IMPORT** into `data/raw/xianyu/imports/` for first REAL batch. Interactive human browser export is the compliant alternative to headless deny.

## K. Gaps

Interactive (non-headless) read not implemented；selenium/playwright not installed；want_count unavailable until real listings land.
