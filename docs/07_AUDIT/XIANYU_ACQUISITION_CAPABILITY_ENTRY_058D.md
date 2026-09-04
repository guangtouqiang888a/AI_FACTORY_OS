# XIANYU_ACQUISITION_CAPABILITY_ENTRY_058D.md

ENTRY ID: 058D  
DATE: 2026-08-30  
STATUS: PASS（capability understood；LIVE not eligible；IMPORT valid path）

## 1. Official options

| Item | Reality |
|------|---------|
| Open platform | **Exists** — https://open.goofish.com/ |
| Public self-serve apply | **No** — 定向邀请服务商 only（quick-start 明文） |
| Taobao Open Platform | Enterprise 入驻 / AppKey / OAuth |
| Published partner APIs | ISV **order / user**（alibaba.idle.isv.* 等） |
| Public competitor listing search API | **Not evidenced** for this use case |

Sources consulted (public): open.goofish.com quick-start & server docs; open.taobao.com 应用软件开发商指南.

## 2. Current eligibility

| Requirement | Project has? |
|-------------|--------------|
| 闲鱼运营邀请 | No |
| 企业淘宝开放平台身份 | No |
| AppKey / AccessToken | No |
| 聚石塔部署 | No |

**Classification for market observation LIVE:** `NOT_AVAILABLE_CURRENTLY`  
Partner ISV order APIs at platform level: `AVAILABLE_WITH_REQUIREMENTS` ≠ project can use today.

## 3. User Export

**VALID PATH** — operator legally obtains export/download; place under `data/raw/xianyu/imports/`.

## 4. Manual Import

**IMPLEMENTED** — `XianyuImportAdapter` / `EXTERNAL_IMPORT` / modes `USER_EXPORT` + `MANUAL_IMPORT`.

## 5. Live API

**NOT_AVAILABLE_CURRENTLY** for AI_FACTORY_OS market observation.  
Adapter `XianyuLiveApiAdapter` fails honestly with ACCESS_REQUIREMENTS.  
No captcha/login/anti-bot bypass.

## 6. Data fields

| Field | Class |
|-------|--------|
| title, price, counts, seller, url, item_id, published_at | AVAILABLE_VIA_EXPORT (if in file; else NULL) |
| observed_at | CURRENTLY_AVAILABLE (set at import) |
| LIVE API listing fields | UNAVAILABLE |
| Official competitor search | UNAVAILABLE |

## 7. Risks

- Misreading “官方有 API” as “我们能抓市场 listing”
- Using sample as REAL
- Scrape bypass temptation
- Mixing Observation with Events / Products

## 8. Recommended current mode

**USER_EXPORT / MANUAL_IMPORT** → Raw → MarketObservation → (later Signal → Opportunity)

## 9. Future path

Only after invitation + enterprise AppKey + confirmed API scope covering needed fields: add LIVE_API adapter implementation. Until then keep LIVE = NOT_AVAILABLE.

## Architecture

```text
XianyuSource
  → XianyuImportAdapter (ACTIVE)
  → Raw (+ sha256 + provenance.json)
  → Normalizer
  → market_observations

XianyuLiveApiAdapter = NOT_AVAILABLE_CURRENTLY
```

Collector kind evidence: `XianyuCollector.collector_kind = EXTERNAL_IMPORT`；`live_collect` fails.

## Collector Registry

| collector_id | mode | status |
|--------------|------|--------|
| col_xianyu_import | MANUAL_IMPORT | ACTIVE |
| col_xianyu_live_api | LIVE_API | NOT_AVAILABLE_CURRENTLY |
