# DATABASE_PROVENANCE_AUDIT_ENTRY_058A.md

ENTRY STATUS: **PASS**  
ENTRY ID: **058A**  
DATE: **2026-08-30**

## Verdict

| Item | Result |
|------|--------|
| Legacy DB identity | **SAMPLE / TEST_FIXTURE / SIMULATION** (early scoring-practice DB) |
| Current SoT | `data/ai_factory.db` = **CLEAN** (products=0, scores=0) |
| Archive | `99_ARCHIVE/database_history/ai_factory_legacy_simulation_20260830.db` |
| SHA-256 | `79dc56f986893b0e590f904e9e6ff76d90425f72d2c8335e26a33d9efbde62be` |
| Raw xianyu | **Preserved** (`*_sample.xlsx`) |
| Git | **UNAVAILABLE** (no `.git` / git CLI not found) |

## A. Database Identity

Absolute path audited: `D:\AI_FACTORY_OS\data\ai_factory.db`  
Valid SQLite header; size before archive **208896** bytes; mtime **2026-08-30T16:38:33**.

## B–D. Schema / Rows (pre-archive)

| Table | Rows |
|-------|------|
| products | **61** (exact) |
| scores | 519 |
| keywords | 6 |
| collection_log | 29 |
| platforms | 2 |
| market_signals | 30 |
| selection_results | 5 |
| publish_queue | 2 |
| publish_evidence | 0 |
| market_events | 0 |
| trends | 0 |
| audit_log | 1 |

## E. 61-Row Provenance

- Exact count: **61**
- Unique `source_url`: **3 only**
  - `https://goofish.com/item/sample001`
  - `https://goofish.com/item/sample002`
  - `https://goofish.com/item/test`
- Titles include **测试商品0/1/标题** pattern; keyword category includes **test**
- Price distribution artificial: 99.9×9, 29.9×26, 19.9×26
- Repeating cycle of same titles → synthetic/sample pattern
- **Cannot prove REAL platform origin**

## F. Raw Xianyu

Only file: `data/raw/xianyu/2026-07-04/虚拟资料_sample.xlsx`  
- Filename contains **sample**
- Creator: **openpyxl**
- 2 data rows with sample001/sample002 URLs
- **SAMPLE** evidence file — preserved, not deleted

## G–H. Collector / Fixture

- `1_DATA/collector.py` uses Excel→SQLite structure (schema dependency)
- Does **not** require these 61 historical rows to function
- Test suite seeds its own temp DBs (`test_opportunity_discovery` mocks `DB_PATH`)
- No dedicated `*_seed.py` product fixture scripts found beyond tests

## I. Git Evidence

**UNAVAILABLE** — workspace has no `.git`; `git` CLI not on PATH.

## J. 99.9 Provenance

products.price (ids 2,3,7,8,12,13) all **99.9** + `source_url=.../item/test`  
→ price_signal avg → estimated_value → Entry 055/057 hypothesis  
**Origin class: SAMPLE / TEST_FIXTURE** — not REAL market WTP.

## K. Origin Classification

| Asset | Class |
|-------|-------|
| Legacy products/scores/keywords | SAMPLE / TEST_FIXTURE / SIMULATION |
| Raw `*_sample.xlsx` | SAMPLE |
| market_signals / selection_results (pre-archive) | Derived from SAMPLE (not REAL) |
| publish_queue rows | Operational queue metadata (restored; upstream discovery SAMPLE) |
| commercial_assets products (f2f8…) | Real **generated assets**; discovery claim reclassified |

## L. Code Dependency

Code depends on **schema + connection path**, not on legacy SAMPLE rows.  
Clean DB: modules `ensure_*` initialize successfully; tests PASS.

## M–O. Decision / Archive / Clean DB

- Archived whole DB (including mixed 051–057 additive rows)
- Current DB recreated via `database.ensure_schema` + market_event/signal + publish_queue ensures
- Restored **2** publish_queue operational rows only
- products/scores/signals/selection **0** in Current

## P–R. 054 / 055 / 057 Reclassification

| Entry | Reclassification |
|-------|------------------|
| 054 | Discovery pipeline real; **input data ≠ REAL market** → SAMPLE-derived |
| 055 | Product asset `f2f8bab97df8` **physically real**; “Real Market Data” claim **invalidated** → autonomous from legacy/non-real dataset |
| 057 | 99.9 provenance confirmed SAMPLE; recommendation still non-validated |

## S. Commercial Learning

Protected: SAMPLE/simulation cannot enter Real Commercial Learning (Entry 050).  
market_events still 0.

## T–Z. Continuity / Validation / Risks

See Entry 058A Execution History + Continuity sync.  
Risk: future collectors must not treat sample Excel as REAL without provenance gate.
