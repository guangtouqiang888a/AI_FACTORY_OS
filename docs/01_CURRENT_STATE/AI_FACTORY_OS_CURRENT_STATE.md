# AI_FACTORY_OS Current State

Status: V2 BASELINE ESTABLISHED — archive boundary finalized (Cursor-executed; ChatGPT Closure Review pending)
Last verified: 2026-10-08

## Current position
V2 Active Workspace is isolated from retired Entry-driven runtime and from documentation history archives. Dual archive names are disambiguated: `docs/99_ARCHIVE/` ≠ `99_ARCHIVE_RUNTIME/`.

## Current objective
Operate from the V2 runtime/database baseline and evolve product/runtime capabilities only through authorized Tasks and V2 engineering controls.

## Locked engineering model
Human Owner → Product/Goal → Task → ChatGPT architecture/review → Cursor implementation → Automated validation → Closure review → Release → Real-world evidence → Learning.

## Continuity status
DONE:
- AI-native engineering operating model established
- concise root Agent Map established
- repository remains the durable source of record
- freeze-and-rebuild is no longer the normal evolution strategy
- durable Task control model established
- durable Evidence and Closure model established
- durable Change/Migration/Compatibility/Recovery model established
- TASK-V2-FOUNDATION-002 closed as ACCEPTED
- TASK-V2-FOUNDATION-003 closed as ACCEPTED
- TASK-V2-FOUNDATION-004 Cursor execution: V2 `app/` + `database/` + `config/` + `tests/` baseline verified
- Archive boundary finalized: root `99_ARCHIVE/` renamed to `99_ARCHIVE_RUNTIME/`; `docs/99_ARCHIVE/` retained for document history

IN PROGRESS:
- ChatGPT Closure Review for TASK-V2-FOUNDATION-004 / archive-boundary land（Cursor evidence ≠ ACCEPTED）

NOT STARTED:
- market-intelligence implementation
- product implementation
- production deployment

## Active V2 boundaries

| Role | Path |
|------|------|
| V2 Runtime | `app/` |
| V2 Database | `database/` |
| V2 Config | `config/` |
| V2 Tests | `tests/` |
| Document history archive | `docs/99_ARCHIVE/` |
| Code / runtime assets / DB history archive | `99_ARCHIVE_RUNTIME/` |

```text
docs/99_ARCHIVE  ≠  99_ARCHIVE_RUNTIME
```

- `docs/99_ARCHIVE/` — frozen **documentation** history only（blueprint / old governance / execution history docs）. Never place code or DB files here.
- `99_ARCHIVE_RUNTIME/` — retired **runtime code**, commercial assets, and **database history**. Never place documentation SoT here.

## Runtime Reality（V2 Active Authority）

```text
V2 Runtime entrypoint:  python -m app.main
V2 Database entrypoint: python -m database init|verify|reset
Verification:           python -m tests.verify_v2
Reset:                  python -m database reset

schema_identity=ai_factory_os_v2
schema_version=1
storage=database/runtime/ai_factory_v2.db (local SQLite; gitignored)
config=config/settings.py (secrets via env / gitignored .env only)
```

Facts:
- V2 does not import retired Entry-driven packages under `99_ARCHIVE_RUNTIME/legacy_runtime/`.
- V2 does not read archived legacy DBs under `99_ARCHIVE_RUNTIME/database_history/` or `99_ARCHIVE_RUNTIME/legacy_runtime/data/`.
- Root `99_ARCHIVE/` no longer exists as a current directory name.
- Retired runtime is not current Runtime Authority.

## Retired Entry-driven Runtime（historical only）

```text
99_ARCHIVE_RUNTIME/
  ├── legacy_runtime/
  │     0_START/ 1_DATA/ 2_COGNITION/ 3_DECISION/ 4_PRODUCT/ 5_CONTENT/
  │     6_EXECUTION/ 7_MEMORY/ 8_CONFIG/ 9_PRODUCT/ 10_DEPLOY/
  │     11_CONTENT_FACTORY/ commercial_assets/
  │     data/ logs/ output/   # local gitignored operational residue (moved off root)
  └── database_history/       # archived legacy SQLite / manifests (≠ V2 DB)
```

## Authority boundary
Runtime/data and reproducible evidence outrank documents. Legacy documents/data/code are historical until the new baseline explicitly promotes a reusable fact or component. Historical material must not silently become runtime authority.

## Foundation control boundary
The V2 engineering foundation now has four explicit layers:
1. Engineering operating model
2. Task control
3. Evidence and closure
4. Change, migration, compatibility, and recovery

## Recovery entrypoint
For a new AI/session with limited context, read in this order:
1. AGENTS.md
2. this file
3. docs/00_GOVERNANCE/AI_FACTORY_OS_ENGINEERING_OPERATING_MODEL.md
4. docs/05_EXECUTION/ACTIVE_TASK.md
5. the authoritative model(s) named by the active Task
6. only the deeper architecture/business/evidence sources required by that Task

## Next permitted work
STOP after archive-boundary land/push. No further Task until ChatGPT Closure Review and new authorization.
