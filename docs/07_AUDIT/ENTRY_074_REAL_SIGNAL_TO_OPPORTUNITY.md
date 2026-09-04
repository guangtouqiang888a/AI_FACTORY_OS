# ENTRY_074_REAL_SIGNAL_TO_OPPORTUNITY

**ENTRY STATUS:** **BLOCKED** (`BLOCKED_AT_SIGNAL_TO_OPPORTUNITY`)  
**ENTRY ID:** 074  
**DATE:** 2026-09-03  
**TYPE:** Read-Only Runtime Reality Preflight + Minimal-Bridge Gate (no bridge authorized by Reality)  
**Code Modification:** **NONE**  
**Schema Modification:** **NONE**  
**DB Modification:** **NONE**  
**External Action:** **NONE**  
**AI provider calls:** **0**  
**AI cost:** **0**  
**Opportunity discovery (Observation lineage):** **NOT_EXECUTED**  
**Product / Publish / Commercial Learning:** **NOT_EXECUTED**

---

## INPUT SIGNALS (ENTRY 073)

| Field | Reality |
|-------|---------|
| Evidence | `1_DATA/_tests/xianyu_entry_073/candidate_to_signal_result.json` |
| market_signals count | **6** |
| source | `market_observation` |
| keyword | `Excel模板` |
| lineage | `market_observation` |

### SIGNAL IDS

```text
sig_f1173cc0edca  demand_signal
sig_9a3983efb2a4  engagement_signal
sig_10fa1228c3f2  competition_signal
sig_82a523bc2bc1  price_signal
sig_90277d017e37  trend_signal
sig_90064dc020a6  growth_signal
```

### OBSERVATION LINEAGE

Locked 7 Observation IDs (REAL / MANUAL_VERIFIED / MATCH):

```text
mobs_48d5a1daa0ee, mobs_4eeed83520dc, mobs_77abed5da432,
mobs_558206dd2057, mobs_2198f9db4742, mobs_217cd4886838, mobs_a28b1bc7faca
```

Session `sess_1788419997563` · Collection `crun_378745ca45e0` · Extension `run_1788419997563`

---

## PRE-EXECUTION REALITY

| Table | Count |
|-------|------:|
| market_observations | 20 |
| market_signals | 6 |
| selection_results | 0 |
| products | **0** |

---

## OPPORTUNITY RUNTIME REALITY

### Actual call chain (code)

```text
discover_opportunities()
  → market_signal_core.load_products_grouped_by_keyword()   # READ products TABLE
  → for each keyword group:
        derive_signals_from_product_group(keyword, products)  # RE-DERIVE; ignores DB market_signals
        score_opportunity_from_signals(signals, products)       # score_product(p) per listing
        assess_opportunity_risk(keyword, products)              # assess_risk(p) per listing
        build_opportunity_candidate(keyword, products, signals, …)
  → select_discovered_candidates
  → optional persist: signals + selection_results + JSON file
```

**No AI:** Opportunity Runtime does not call ExecutionRuntime / ModelBridge / OpenAI / DeepSeek.

### What Opportunity actually accepts

| Input | Accepted by `discover_opportunities`? |
|-------|----------------------------------------|
| Product rows / Product keyword groups from `products` | **YES — required** |
| Persisted `market_signals` (any lineage) | **NO** — never loaded for discovery |
| Observation-lineage Signal | **NO** |
| MarketObservation / Candidate | **NO** |

### Formal `Signal → Opportunity` entry?

**NOT_FOUND** for Observation lineage.  
In-memory signals only exist as a side-product of product-group derivation inside discovery.

### Hard Product dependency?

**YES.**

- Entry loads only `products`.
- With `products = 0`, dry-run (`persist=False`) returns:

```text
status = INSUFFICIENT_DATA
reason = no_keyword_groups_meeting_min_listings
```

- `score_opportunity_from_signals` / `assess_opportunity_risk` / `build_opportunity_candidate` require listing dicts shaped for product scorers (`score_product` uses `want_count or 0`).

### Does Opportunity use `evidence_refs` Observation fields?

`build_opportunity_candidate` stores `signal_id` / `signal_type` / `observation_timestamp` and **product_id / source_url / collect_date**.  
It does **not** read or propagate `lineage=market_observation`, `observation_ids`, `collection_run_ids`, `session_ids`, `extension_run_ids` from Signal `evidence_refs`.

### Opportunity output (when product path works)

- In-memory / JSON `discovered_candidate` (`candidate_id` like `aoc_*`)
- `opportunity_id = None` (not auto-promoted)
- Optional `selection_results` table rows
- **Not** Product; **not** Publish; flags: `auto_production_forbidden=True`

### Dry-run on Current DB (074)

```text
discover_opportunities(min_listings=1, persist=False)
→ INSUFFICIENT_DATA (products=0)
→ candidates=0, selection=0
→ no DB writes
```

---

## SIGNAL → OPPORTUNITY MAPPING

**NOT_EXECUTED** — Observation-lineage path cannot enter existing Runtime without Product substitution.

---

## MINIMAL BRIDGE GATE (Section 9)

| Condition | Met? |
|-----------|------|
| Runtime designed to consume MarketSignal as primary input | **NO** — primary input is `products`; signals re-derived |
| Gap only evidence/lineage read compatibility | **NO** — Product-hard pipeline |
| No Product manufacture required | Would require Product table **or** Observation→Product-shaped substitution |
| No algorithm / schema / AI / Product-path contract change | N/A — bridge not authorized |

**Decision:** Do **not** implement adapter. Do **not** INSERT products. Do **not** disguise Observations as Products.

**Status:** `BLOCKED_AT_SIGNAL_TO_OPPORTUNITY`

---

## PROVENANCE

073 Signal provenance in DB is intact.  
Opportunity did not consume Signals → **no Opportunity provenance produced**.

If a future Entry authorizes Observation-native Opportunity: must wire Signal `evidence_refs` through candidate `evidence_refs` (current builder lacks Observation lineage fields) → **PROVENANCE_GAP** on Opportunity side relative to Observation lineage.

---

## AI PROVIDER CALLS / AI COST

```text
AI provider calls = 0
AI cost = 0
```

---

## TABLE DELTAS

| Table | Before | After | Delta |
|-------|-------:|------:|------:|
| market_observations | 20 | 20 | **0** |
| products | 0 | 0 | **0** |
| market_signals | 6 | 6 | **0** (073 Signals untouched) |
| selection_results | 0 | 0 | **0** |

Opportunity persistence: **NONE** (discovery not executed for Observation lineage).

---

## EXTERNAL ACTION

**NONE**

---

## 073 IDEMPOTENCY_GAP

```text
073 IDEMPOTENCY_GAP acknowledged
NOT_MODIFIED
OUT_OF_SCOPE
```

`persist_signals()` not touched.

---

## TEST RESULTS

```text
tests_run: 20
  - 3_DECISION.test_opportunity_discovery
  - 1_DATA.test_candidate_to_signal_073
passed: 20
failed: 0
skipped: 0
```

Product → Signal → Opportunity regression: **PASS** (temp-DB seeded products path).  
No new Observation→Opportunity tests added (capability not implemented).

---

## CODE / SCHEMA / DB MODIFICATION

```text
CODE MODIFICATION = NONE
SCHEMA MODIFICATION = NONE
DB MODIFICATION = NONE
```

---

## CAPABILITY GAPS / FINDINGS

1. **BLOCKED_AT_SIGNAL_TO_OPPORTUNITY** — `discover_opportunities` requires `products` keyword groups; ignores Observation-lineage `market_signals`.
2. **No load-from-`market_signals` discovery entry** for any lineage.
3. **Opportunity evidence builder** does not propagate Observation provenance fields from Signal `evidence_refs`.
4. **073 IDEMPOTENCY_GAP** — acknowledged, unmodified.
5. Scoring helper `score_product` uses `want_count or 0` — Observation NULL semantics incompatible without a dedicated Observation-native score path (future Entry).

---

## NEXT AUTHORIZATION

Separate Entry required to design/implement **Observation-native Signal → Opportunity** that:

- Consumes 073 `market_signals` (or Observation listings) **without** `products` INSERT
- Reuses scoring/selection logic without Product substitution
- Preserves Observation provenance end-to-end
- Stops before Product / Publish / Commercial Learning
- Remains AI = 0 unless separately authorized

**STOP — do not auto-implement.**

---

## DOCUMENTATION SYNC

| File | Action |
|------|--------|
| This Audit | Created |
| `docs/01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md` | Modified — 074 BLOCKED |
| `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` | Modified — Signal→Opportunity Observation = BLOCKED |
| `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` | Modified — ledger |
| UA / Execution Protocol / Constitution / DEC / Authority / Control Center / KUP / Business Strategy / WORK_PRINCIPLES | Reviewed — Not Modified |

Note: Entry text referenced `docs/04_STATE/*`; Reality uses `docs/01_CURRENT_STATE/*`.

---

## STOP CONDITION

Reached Opportunity Reality Preflight boundary.  
No Opportunity discovery executed for Observation lineage.  
No Product / Publish / Commercial Learning / External Action / AI.
