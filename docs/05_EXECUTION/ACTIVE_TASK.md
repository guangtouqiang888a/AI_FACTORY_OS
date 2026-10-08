# ACTIVE_TASK

> Execution pointer — not Reality SoT. Reality: Code / DB / Assets / Runtime.  
> Last updated: 2026-10-08

| Field | Value |
|-------|-------|
| **ACTIVE_TASK** | **TASK-V2-FOUNDATION-004** |
| **STATUS** | **EXECUTED_AWAITING_CHATGPT_REVIEW**（Cursor verification PASS；**not** independently ACCEPTED） |
| **TITLE** | Establish clean V2 runtime/database baseline + land 004B legacy isolation |
| **PRIOR** | TASK-V2-FOUNDATION-004B was **not** previously landed locally（BLOCKED by dirty tree）；isolation executed as Phase 1 of this Task |
| **COMPLETION（Cursor）** | Legacy dirs `git mv` → `99_ARCHIVE/legacy_runtime/`；`app/` + `database/` + `config/` + `tests/` created；`python -m tests.verify_v2` PASS |
| **ACCEPTANCE** | **Pending ChatGPT Closure Review** — Cursor evidence ≠ Formal Acceptance |
| **NEXT** | Stop. No further Task until authorized. |
| **POINTERS** | Current State Runtime Reality；`docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md`（TASK-V2-FOUNDATION-004 entry） |

## Commands（V2）

```text
python -m app.main
python -m database init
python -m database verify
python -m database reset
python -m tests.verify_v2
```

## Out of scope (this Task)

- Xianyu / keywords / product generation / commercial rules
- Legacy file content edits or deletes
- Old DB migration
- Independent approval / ACCEPTED claim
