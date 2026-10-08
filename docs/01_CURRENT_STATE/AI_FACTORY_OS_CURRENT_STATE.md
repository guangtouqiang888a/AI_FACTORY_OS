# AI_FACTORY_OS Current State

Status: LEGACY FROZEN + V2 BASELINE SYNCED（Cursor freeze/sync land；ChatGPT Closure Review pending）
Last verified: 2026-10-08

## Current position
Legacy Entry-driven system is frozen under `99_ARCHIVE_RUNTIME/`. Document history remains under `docs/99_ARCHIVE/`. Active V2 workspace is `app/` `database/` `config/` `tests/` plus root continuity files. Local workspace is intended to stay synchronized with `origin/main` after the freeze/sync land.

## Current objective
Hold the frozen legacy / V2 baseline boundary. No new business capability work until authorized after Closure Review.

## Locked engineering model
Human Owner → Product/Goal → Task → ChatGPT architecture/review → Cursor implementation → Automated validation → Closure review → Release → Real-world evidence → Learning.

## Continuity status
DONE:
- AI-native engineering operating model established
- concise root Agent Map established
- repository remains the durable source of record
- freeze-and-rebuild is no longer the normal evolution strategy
- durable Task / Evidence / Change-Migration-Recovery models established
- TASK-V2-FOUNDATION-002 / 003 ACCEPTED
- TASK-V2-FOUNDATION-004 V2 runtime/database baseline landed
- Archive boundary: `docs/99_ARCHIVE/` ≠ `99_ARCHIVE_RUNTIME/`
- Legacy freeze + local/GitHub sync land（this Task）

IN PROGRESS:
- ChatGPT Closure Review（Cursor evidence ≠ ACCEPTED）

NOT STARTED:
- market-intelligence / product / production deployment

## Active V2 retained

| Role | Path |
|------|------|
| V2 Runtime | `app/` |
| V2 Database | `database/` |
| V2 Config | `config/` |
| V2 Tests | `tests/` |
| Agent map | `AGENTS.md` |
| Requirements file | `requirements.txt`（root retained；V2 baseline uses stdlib） |
| Cursor local boundary | `.cursor/`（V2 rules；legacy rules archived） |

## Archive boundaries（minimal dual system — do not add a third）

| Path | Role |
|------|------|
| `docs/99_ARCHIVE/` | LEGACY DOCUMENTATION history only |
| `99_ARCHIVE_RUNTIME/` | LEGACY runtime code / commercial assets / DB history |

```text
docs/99_ARCHIVE  ≠  99_ARCHIVE_RUNTIME
```

No root `99_ARCHIVE/`. No parallel `archive/` tree.

Active `docs/00`–`07` remain the documentation workspace for V2 navigation and evidence; historical Entry-era material inside them is not Runtime Authority. Deep frozen doc copies remain in `docs/99_ARCHIVE/`.

## Runtime Reality（V2 Active Authority）

```text
python -m app.main
python -m database init|verify|reset
python -m tests.verify_v2
```

Facts:
- V2 does not import `99_ARCHIVE_RUNTIME/legacy_runtime/`.
- V2 does not read archived legacy DBs.
- Retired runtime is frozen historical material only.

## Frozen legacy runtime

```text
99_ARCHIVE_RUNTIME/
  ├── legacy_runtime/     # Entry-driven code + assets + local ops residue
  └── database_history/   # legacy SQLite / manifests
```

## Next permitted work
STOP. No new AI_FACTORY_OS business development until ChatGPT Closure Review and new authorization.
