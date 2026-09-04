# ENTRY_075_REAL_OBSERVATION_NATIVE_OPPORTUNITY

**ENTRY STATUS:** **PASS_WITH_FINDINGS**  
**ENTRY ID:** 075  
**DATE:** 2026-09-04  
**TYPE:** Authorized Runtime Implementation — Observation-native Signal → Opportunity  
**Code Modification:** **YES** — scoped  
**Schema Modification:** **NONE**  
**DB Modification:** **YES** — `selection_results` +1 (existing Opportunity contract); JSON persistence  
**External Action:** **NONE**  
**AI provider calls:** **0**  
**AI cost:** **0**  
**Product:** **NOT_CREATED**  
**Publish / Commercial Learning:** **NOT_EXECUTED**

---

## INPUT SIGNALS / SIGNAL IDS

From ENTRY 073 persisted `market_signals` (6):

```text
sig_f1173cc0edca  demand_signal
sig_9a3983efb2a4  engagement_signal
sig_10fa1228c3f2  competition_signal
sig_82a523bc2bc1  price_signal
sig_90277d017e37  trend_signal
sig_90064dc020a6  growth_signal
```

source=`market_observation` · keyword=`Excel模板` · lineage=`market_observation`

---

## OBSERVATION LINEAGE

7 REAL / MANUAL_VERIFIED Observations (070 MATCH):

```text
mobs_48d5a1daa0ee … mobs_a28b1bc7faca
```

Session `sess_1788419997563` · Collection `crun_378745ca45e0` · Extension `run_1788419997563`

---

## PRE-EXECUTION REALITY

| Table | Count |
|-------|------:|
| market_observations | 20 |
| market_signals | 6 |
| selection_results | 0 |
| products | 0 |

---

## OLD OPPORTUNITY RUNTIME REALITY (074)

`discover_opportunities()` → `products` only → re-derive signals.  
Observation-lineage `market_signals` **not consumed**.

---

## NEW OBSERVATION-NATIVE RUNTIME

**Entry:** `discover_opportunities_from_observation_signals(signal_ids, persist=True)`

```text
market_signals (load_signals_by_ids — 073 persisted)
  → validate lineage REAL / MANUAL_VERIFIED
  → group by keyword
  → load_observations_by_ids (from evidence_refs)
  → score_opportunity_from_signals(signals, observations, score_observation_listing)
  → assess_opportunity_risk(keyword, observations)
  → build_observation_opportunity_candidate
  → select_discovered_candidates
  → JSON + selection_results (NO persist_signals)
```

**Shared scoring:** `score_listing_metrics(null_as_zero=True|False)`  
- Product: `score_product` → null_as_zero=True (054 unchanged)  
- Observation: `score_observation_listing` → NULL want → None (NULL ≠ 0)

---

## SCORING LOGIC / NULL SEMANTICS

- Reuses `score_opportunity_from_signals`, `assess_opportunity_risk`, `select_discovered_candidates`
- Observation listings scored via `score_observation_listing` — **NULL want_count not coerced to 0**
- Product path regression unchanged (`score_product` → null_as_zero=True)

---

## SIGNAL → OPPORTUNITY MAPPING

| grouping_key | keyword | signals | observations | candidate_id |
|--------------|---------|---------|--------------|--------------|
| keyword | Excel模板 | 6 | 7 | `aoc_19399677b7ba` |

`opportunity_id` = **null** (discovered candidate only — not promoted)

Selection: `sel_53e7c414624f` · rank=1 · score=68.92 · selected=true

Evidence: `1_DATA/_tests/xianyu_entry_075/observation_opportunity_result.json`

---

## PROVENANCE

**SUFFICIENT** — candidate `provenance` + `evidence_refs` include:

signal_ids · observation_ids · source_item_ids · collection_run_ids · session_ids · extension_run_ids · data_origins · verification_statuses

Per-observation refs: observation_id, source_item_id, source_url, observed_at, REAL/MANUAL_VERIFIED

---

## REAL / MANUAL_VERIFIED VALIDATION

Signal `evidence_refs` and loaded Observations validated REAL + MANUAL_VERIFIED before scoring.

---

## AI PROVIDER CALLS / AI COST

```text
0 / 0
```

No ExecutionRuntime / ModelBridge / OpenAI / DeepSeek on this path.

---

## DATABASE BEFORE / AFTER / DELTA

| Table | Before | After | Delta |
|-------|-------:|------:|------:|
| market_observations | 20 | 20 | **0** |
| market_signals | 6 | 6 | **0** |
| products | 0 | 0 | **0** |
| selection_results | 0 | 1 | **+1** |

Opportunity JSON: `commercial_assets/opportunity_candidates/observation_discovery_v1.json`

---

## TEST RESULTS

```text
tests_run: 26
  - test_opportunity_discovery (13) — Product path regression
  - test_observation_opportunity_075 (6)
  - test_candidate_to_signal_073 (7)
passed: 26
failed: 0
```

---

## CODE MODIFICATION

| File | Change |
|------|--------|
| `3_DECISION/scorer.py` | `score_listing_metrics`, `score_observation_listing`; refactor `score_product` |
| `1_DATA/market_signal_core.py` | `load_signals_by_ids` |
| `3_DECISION/opportunity_discovery.py` | Observation-native discovery entry + provenance builder |
| `3_DECISION/test_observation_opportunity_075.py` | New tests |

**Schema:** NONE  
**073 Signals:** NOT modified / NOT re-persisted

---

## FINDINGS

1. **073 IDEMPOTENCY_GAP** — ACKNOWLEDGED · NOT_MODIFIED · OUT_OF_SCOPE  
2. **selection_reason** string in `select_discovered_candidates` still embeds `discovery_method=market_signal` even when candidate uses `observation_market_signal` (cosmetic; selection row `discovery_method` field is correct)

---

## CAPABILITY GAPS

- Product lineage `discover_opportunities()` unchanged — still requires `products`  
- `opportunity_id` not auto-assigned (by design)  
- Signal → Opportunity re-run may add duplicate selection rows (selection_id UUID — separate from 073 idempotency)

---

## NEXT AUTHORIZATION

**STOP** at Opportunity Candidate.

Separate Entry required for:

```text
Opportunity → Product
Publish
Commercial Learning
External Action
```

---

## DOCUMENTATION SYNC

| File | Action |
|------|--------|
| This Audit | Created |
| CURRENT_STATE | Modified |
| MODULE_REGISTRY | Modified |
| CURSOR_EXECUTION_HISTORY | Modified |
| UA / Execution Protocol / Constitution / DEC / Authority / Control Center / KUP / Business Strategy / WORK_PRINCIPLES | Reviewed — Not Modified |

---

## STOP CONDITION

Opportunity discovery completed. No Product / Publish / Commercial Learning / External Action / AI.
