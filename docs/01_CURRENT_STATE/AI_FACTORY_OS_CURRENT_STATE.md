# AI_FACTORY_OS Current State

Status: V2 BASELINE ESTABLISHED (Cursor-executed; ChatGPT Closure Review pending)
Last verified: 2026-10-08

## Current position
Retired Entry-driven runtime is physically isolated under `99_ARCHIVE/legacy_runtime/` and is historical preserve only — not current Runtime Authority. A minimal V2 Runtime and Database baseline now exists in the Active Workspace.

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
- TASK-V2-FOUNDATION-004B isolation landed (with TASK-004): Entry-driven dirs moved to `99_ARCHIVE/legacy_runtime/`
- TASK-V2-FOUNDATION-004 Cursor execution: V2 `app/` + `database/` + `config/` + `tests/` baseline verified

IN PROGRESS:
- ChatGPT Closure Review for TASK-V2-FOUNDATION-004（Cursor evidence ≠ ACCEPTED）

NOT STARTED:
- market-intelligence implementation
- product implementation
- production deployment

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
- V2 does not import retired Entry-driven packages (`0_START` … `11_CONTENT_FACTORY`).
- V2 does not read legacy `data/ai_factory.db` and does not migrate old data.
- `99_ARCHIVE/legacy_runtime/` is the retired runtime historical preserve zone.
- Retired runtime is no longer current Runtime Authority.

## Retired Entry-driven Runtime（historical only）

```text
99_ARCHIVE/legacy_runtime/
  0_START/ 1_DATA/ 3_DECISION/ 6_EXECUTION/ 7_MEMORY/
  8_CONFIG/ 9_PRODUCT/ 10_DEPLOY/ 11_CONTENT_FACTORY/
  commercial_assets/
```

BOUNDARY_REVIEW_REQUIRED (not moved):
`2_COGNITION/`, `4_PRODUCT/`, `5_CONTENT/`, `data/`, `logs/`, `output/`

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
STOP after TASK-V2-FOUNDATION-004 land/push. No further Task until ChatGPT Closure Review and new authorization.
