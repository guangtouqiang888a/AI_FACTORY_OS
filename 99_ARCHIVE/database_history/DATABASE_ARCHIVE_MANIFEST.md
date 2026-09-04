# DATABASE ARCHIVE MANIFEST
# Entry 058A

| Field | Value |
|-------|-------|
| original_path | `D:\AI_FACTORY_OS\data\ai_factory.db` |
| archive_path | `D:\AI_FACTORY_OS\99_ARCHIVE\database_history\ai_factory_legacy_simulation_20260830.db` |
| sha256 | `79dc56f986893b0e590f904e9e6ff76d90425f72d2c8335e26a33d9efbde62be` |
| size_bytes | 208896 |
| archived_at | 2026-08-30T18:09:50+08:00 |
| not_current_sot | **true** |
| origin_classification | **SAMPLE / TEST_FIXTURE / SIMULATION (scoring-practice legacy)** |
| reason | Early scoring-practice / sample-fixture database; source_url uses sample/test; raw file named `*_sample.xlsx`; product titles/keywords marked 测试/test. Mixed later Entry 051–057 schema rows archived together. |

## Table Row Counts (at archive)

| Table | Rows |
|-------|------|
| `audit_log` | 1 |
| `collection_log` | 29 |
| `keywords` | 6 |
| `market_events` | 0 |
| `market_signals` | 30 |
| `platforms` | 2 |
| `products` | 61 |
| `publish_evidence` | 0 |
| `publish_queue` | 2 |
| `scores` | 519 |
| `selection_results` | 5 |
| `trends` | 0 |

## Rules

- LEGACY / Archive only — **not** Current Operational SoT
- Do not feed archived SAMPLE rows into Real Commercial Learning
- Raw xianyu files preserved separately under `data/raw/xianyu/`
