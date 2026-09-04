# ENTRY_067_ACQUISITION_POLICY_AND_AI_COST_GATE

**ENTRY STATUS:** PASS  
**ENTRY ID:** 067  
**DATE:** 2026-09-03  
**TYPE:** Market Acquisition Policy + Minimal AI Cost Gate

---

## Summary

| Component | Status |
|-----------|--------|
| Market Acquisition Policy | **PARTIAL / Implemented** — goal registry + DB + Filter layer |
| AI Cost Gate | **PARTIAL / Implemented** — estimate / gate / execution log |
| Model Router | **NOT BUILT** — ModelSelector interface only |
| Paid AI calls | **None** |
| Product / Publish / Learning | **Unchanged** |
| 0–6 new Core files | **0** |
| Tests | `test_acquisition_policy_067` — **24 OK** |

---

## A. Acquisition Policy

Extended `1_DATA/acquisition_engine.py` (no parallel `acquisition_policy.py` / `market_policy.py`).

- Singleton `acquisition_policy` (id=1) = **compliance / allowed sources** (pre-existing)
- New table `market_acquisition_policies` = **goal-oriented AcquisitionPolicy**

Fields: `policy_id`, `goal`, `source_preferences`, `query_strategy`, `scope`, `filters`, `budget`

## B. Strategy Registry (closed set)

| Goal | Status |
|------|--------|
| VOLUME_DISCOVERY | Usable |
| HIGH_VALUE_DISCOVERY | Usable |
| MARKET_GAP_DISCOVERY | RESERVED |
| TREND_DISCOVERY | RESERVED |
| TARGETED_RESEARCH | Usable |

## C. AcquisitionTask

Additive columns: `policy_id`, `filters_json`. Task may inherit filters/scope from policy.

## D. Filter Separation

`apply_observation_filters()` — MATCH / BELOW_THRESHOLD / ABOVE_THRESHOLD / UNKNOWN.  
NULL want → UNKNOWN; never coerced to 0; observations retained.

## E–F. Xianyu / Future Sources

`source_preferences` list — policy goal ≠ platform. Same policy may later target taobao/overseas.

## G–L. AI Cost Gate

Module: `1_DATA/ai_cost_gate.py`

| Rule | Behavior |
|------|----------|
| estimated ≤ allowed | PASS |
| estimated > allowed | BLOCKED + REDESIGN_REQUIRED |
| missing either | UNKNOWN (≠ 0) |
| call_count | metadata only |
| revenue without sales | HYPOTHESIS / ESTIMATE_ONLY |

Tables (additive): `ai_cost_estimates`, `ai_execution_records`

## M–O. Skill / Router / Product Creation

- Skills reserved as strings (not Agents)
- `ModelSelector` = manual/configured; router_status=NOT_BUILT
- `ProductCreationCapability` = unified boundary; no Design/Production agent split

## P–Q. Database

Additive CREATE IF NOT EXISTS + ALTER ADD COLUMN. No destructive migration.  
`market_observations` count unchanged by schema ensure.

## R. Extension Compatibility

No change to Extension/Bridge contracts. Filters remain Engine/Filter-layer concern.

## S–V. Documentation

Updated: Current State, Module Registry, UA, Work Principles, Documentation Map, Execution History.  
**0–6 new files = 0**

## W–X. Core File Creation Audit

```
0–6 新增：0
删除：0
重命名：0
Runtime modules added: 1_DATA/ai_cost_gate.py (code, not docs/0–6)
```

## Y. Tests

24 OK in `test_acquisition_policy_067`; regression 059/066 OK.

## Z / AA–AE

Legacy isolation OK. Reality: Policy + Cost Gate partial.  
**Recommended Next:** Entry 068 — wire Filter to Observation candidates after first REAL SEARCH_RESULT import; optional Cost Gate on Product Creation path (still no paid calls until budgeted).

---

## Final Principle

AI_FACTORY_OS does not maximize call count.  
It estimates cost, constrains spend, and uses the cheapest adequate capability for the task.
