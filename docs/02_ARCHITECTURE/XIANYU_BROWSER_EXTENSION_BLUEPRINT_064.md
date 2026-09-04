# Xianyu Browser Extension Integration Blueprint (Entry 064)

> Status: **Blueprint only** — no Extension or Bridge implemented in Entry 064.

## Reuse existing modules

| Module | Path | Role |
|--------|------|------|
| Acquisition Engine | `1_DATA/acquisition_engine.py` | Task orchestration |
| Collector abstraction | `1_DATA/collector_abstraction.py` | Adapter boundary |
| Market source core | `1_DATA/market_source_core.py` | Raw / Observation |
| Search session | `1_DATA/connectors/xianyu_search_session_063.py` | Session + state classification |
| Targeted search / want audit | `1_DATA/connectors/xianyu_targeted_search_062.py` | result_origin, want_status |
| Reference plugin | `1_DATA/_tests/xianyu_extension_forensics_064/reference_plugin/` | Forensics only |

## Layer responsibilities

| Layer | Responsibility |
|-------|------------------|
| **Search Controller** | Navigate to SEARCH_RESULT page (user, extension, or future automation) |
| **Browser Extension** | Read visible DOM → MarketRecord |
| **Local Bridge** | Receive batches; validate contract |
| **Acquisition Engine** | Task policy; run_id; delegate adapter |
| **Xianyu Adapter** | Selectors, regex, pagination, scroll — **only here** |
| **Filter** | min_want_count, price range — **not in extension scrape loop** |
| **Signal / Opportunity** | Future — not in Extension |

## AcquisitionTask (minimal)

```python
{
  "source_id": "src_xianyu_marketplace",
  "query": "Excel模板",
  "scope": {"max_records": 20, "max_pages": 3},
  "schedule": "MANUAL",
  "filters": {
    "min_want_count": null,  # Filter layer; null = no filter
    "min_price": null,
    "max_price": null
  }
}
```

## Filter semantics (min_want_count)

| want_count | Result |
|------------|--------|
| 61 | MATCH |
| 20 | BELOW_THRESHOLD |
| NULL | UNKNOWN (never coerced to 0) |

## Error contract

`SUCCESS` | `PARTIAL` | `NO_RESULTS` | `ACCESS_BLOCKED` | `PAGE_STRUCTURE_CHANGED` | `UNKNOWN`

Zero records with EMPTY_SEARCH_RESULT = **NO_RESULTS**, not SUCCESS.

## Entry 065 scope (implemented)

1. Own MV3 extension — **done**
2. Localhost bridge — **done**
3. Test sink ingest — **done**
4. Current DB import — **Entry 066**
