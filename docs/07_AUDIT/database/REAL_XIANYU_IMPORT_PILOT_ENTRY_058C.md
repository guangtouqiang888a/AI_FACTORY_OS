# REAL_XIANYU_IMPORT_PILOT_ENTRY_058C.md

ENTRY ID: 058C  
DATE: 2026-08-30  
STATUS: **READY_FOR_REAL_IMPORT** / **WAITING_FOR_REAL_SOURCE_FILE**  
(Architecture + importer PASS; first REAL batch not yet possible without source file)

## A. Input File

| Item | Reality |
|------|---------|
| Drop zone | `data/raw/xianyu/imports/` |
| Data files present | **0** (README only) |
| Legacy sample | `data/raw/xianyu/2026-07-04/*_sample.xlsx` — **NOT imported** |
| Fabricated file | **None** |

## B. Source

`src_xianyu_marketplace` · platform=`xianyu` · source_type=`marketplace` · enabled · mode=`EXTERNAL_IMPORT`

## C. Collection Mode

`EXTERNAL_IMPORT` only. `LIVE_COLLECTION` = NOT AVAILABLE.

## D. Raw Data

Importer stages copies under `data/raw/xianyu/<date>/import_batches/<run_id>/` when a file is imported.  
No run created on Current DB this Entry (no candidate file).

## E. Normalization

`sources.normalize_row` + connector. Missing counts → **NULL**. Explicit 0 → **0**. Invalid price → row reject (not coerce to 0).

## F. Provenance

Fields: run_id, raw_reference, collector_version (`058c.1.0`), normalizer_version, source, source_item_id, source_url, observed_at, notes.imported_at.

## G. Data Origin

REAL only when `declared_origin=REAL` **and** no sample markers.  
Otherwise UNKNOWN / SAMPLE rejected. Platform name alone ≠ REAL.

## H. Verification

REAL import → `MANUAL_VERIFIED` (operator attestation).  
UNKNOWN → `UNVERIFIED`.  
Never forged platform-official `VERIFIED`.

## I. Collection Run

Schema ready (`collection_runs`). Current DB runs=**0** (waiting).

## J. Market Observation

Schema ready (`market_observations`). Current DB rows=**0**.  
Does not write `market_events` / Product / our Listing.

## K. Database Rows (Current)

| Table | Count |
|-------|------:|
| market_observations | 0 |
| collection_runs | 0 |
| products | 0 |
| scores | 0 |
| market_signals | 0 |
| selection_results | 0 |
| market_events | 0 |
| publish_queue | 2 (operational metadata preserved) |

## L. Field Availability (via export)

| Field | Status |
|-------|--------|
| title | AVAILABLE (if present) |
| price | AVAILABLE (if present) |
| want_count / view_count / comment_count / share_count | AVAILABLE if present else UNAVAILABLE (NULL) |
| source_url | AVAILABLE if present else UNAVAILABLE |
| source_item_id | PARTIAL (export column or URL derive) |
| published_at | AVAILABLE if present else UNAVAILABLE |

## M. Deduplication

`source + source_item_id` (fallback hash). Same item + different `observed_at` = history retained.

## N. Rejected Rows

Row-level `rejected_rows[{row_reference, reason}]`. Sample path/URL rejected.

## O. Legacy Isolation

Legacy archive not read. Sample file not imported. Current DB clean of sampleish products.

## P. Source / Sales Separation

`sales_platform=None` on import results. DEC-029 unchanged.

## Q. Tests

`test_xianyu_import_pilot_058c` + 050–058B regression = **150 OK**.

## R. Core File Changes

Modified: connector, market_source_core, pilot, tests, Current State, Module Registry, UA, Control Center, Execution Protocol, Execution History, this audit.  
Not modified: Constitution, Decision Log, Authority, Business Strategy, KUP, Evolution Context.

## S. Continuity

Entry 046 satisfied for Reality change (waiting status / importer hardening).

## T. Remaining Issues

1. No real export file yet  
2. Observation→Signal still PARTIAL  
3. LIVE still unavailable (compliance)

## U. Next Step

Place attested real Xianyu export in `data/raw/xianyu/imports/` → run import with `declared_origin=REAL` → first Collection Run birth certificate.
