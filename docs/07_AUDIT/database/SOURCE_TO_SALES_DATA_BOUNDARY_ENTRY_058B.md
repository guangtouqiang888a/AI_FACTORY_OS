# SOURCE_TO_SALES_DATA_BOUNDARY_ENTRY_058B.md

ENTRY ID: 058B  
DATE: 2026-08-30  
STATUS: PARTIAL / Architecture PASS with LIVE_COLLECTION = NOT AVAILABLE  
DECISION: DEC-029

## 1. Source Reality

| Source | Status |
|--------|--------|
| Xianyu | Enabled — **EXTERNAL_IMPORT** |
| Taobao / Search / Social | Registered **disabled** placeholders — NOT built |

## 2. Xianyu Collection Reality

| Question | Answer | Tag |
|----------|--------|-----|
| A. Excel-only historically? | Yes (`collect_from_excel` → import drop zone) | REALITY |
| B. Live HTTP/API/browser adapter? | No | MISSING |
| C. Legal real data entry? | User-exported file import | PARTIAL |
| D. Auto live fields? | No live fetch | MISSING |
| E. Fields via import (title/price/url/id…) | Available when present in export | PARTIAL |
| F. Schema-reserved only? | share_count etc. may be null | PARTIAL |
| G. Unavailable without export? | All live engagement fields | UNAVAILABLE |

## 3. Collection Modes

- `LIVE_COLLECTION` — **NOT AVAILABLE**
- `EXTERNAL_IMPORT` — **Implemented**
- `TEST_FIXTURE` — isolated tests only（never Current DB as REAL）

## 4. Raw Data

- Path: `data/raw/xianyu/<date>/import_batches/` + `data/raw/xianyu/imports/` drop zone
- Legacy `*_sample.xlsx` preserved under raw; **rejected** as REAL ingest
- Each run retains raw_reference

## 5. Normalization

- `sources.normalize_row` + `market_source_core` observation insert
- `collector_version` / `normalizer_version` = `058b.1.0`
- Counts: raw / accepted / rejected / duplicate / normalized on Collection Run

## 6. Market Observation

- Table: `market_observations`（platform-agnostic；no `xianyu_products`）
- Historical rows for same `source+source_item_id` kept（no overwrite）
- Dedupe key: `source + source_item_id`（fallback content hash）

## 7. Market Signal

- Existing `market_signals`（054）
- Observation → Signal auto-bridge = **PARTIAL**

## 8. Opportunity

- Keeps `discovery_source` / evidence refs
- Must **not** imply `sales_platform`

## 9–12. Product / Listing / Sales / Feedback

```text
discovery_platform = xianyu
sales_platform     = taobao | xianyu | future   # independent
feedback_source    = independent (Future)
```

Structural helpers + tests PASS. One Product → many Listings.

## 13. Database Boundary

| Layer | Tables / Paths |
|-------|----------------|
| A Source/Collection | market_sources, collection_runs, collection_log |
| B Market Data | market_observations, market_signals |
| C Discovery | selection_results, opportunity JSON |
| D Product | commercial_assets products |
| E Listing | listings, publish_queue, publish_evidence |
| F Results | market_events |
| G Learning | memory（guarded；empty commercial） |
| Legacy | 99_ARCHIVE/...（not_current_sot） |

## 14. Provenance

Required: source, source_item_id, source_url (when known), raw_reference, observed_at, collector_version, data_origin, collection_run.

## 15–17. Future Compatibility

- source_type / platform / product_category extensible
- Future connectors **not built**
- Same observation schema supports xianyu / taobao / future

## 18. Risks

- No live Xianyu fetch without compliance review
- Operator may mis-label export as REAL → verification_mode / REVIEW_REQUIRED
- Observation→Signal still PARTIAL

## 19. Remaining Gaps

1. First REAL import batch（operator file）
2. Observation→Signal bridge
3. Compliant LIVE adapter（only if officially allowed）
4. Evaluation / Commercial Learning after real Market Events

## Final Reality Chain

```text
External Source          PARTIAL (import only)
Collector/Import         REALITY (EXTERNAL_IMPORT)
Raw                      REALITY
Normalizer               REALITY
MarketObservation        REALITY (schema; rows=0 REAL)
MarketSignal             PARTIAL
Opportunity              PARTIAL
Product                  REALITY (commercial_assets)
Listing                  REALITY
Sales Platform           REALITY (independent)
Market Events            REALITY (empty)
Evaluation               MISSING
Commercial Learning      GUARDED (none)
```
