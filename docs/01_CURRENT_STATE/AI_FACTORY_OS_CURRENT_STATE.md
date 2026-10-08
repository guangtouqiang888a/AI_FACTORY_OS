# AI_FACTORY_OS Current State

Status: V2 BASELINE INITIALIZATION
Last verified: 2026-10-08

## Current position
The previous Entry-driven implementation and its supporting runtime/data are retired from active development and preserved as historical material. A new engineering baseline is being established in the same repository.

## Current objective
Establish a durable AI-native engineering system first, then rebuild product/runtime capabilities incrementally from that baseline.

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
- TASK-V2-FOUNDATION-002 closed as ACCEPTED

IN PROGRESS:
- establish change/migration/compatibility/recovery control
- archive old active baseline without deleting historical evidence
- establish clean runtime/database baseline

NOT STARTED:
- new runtime/database implementation
- new market-intelligence implementation
- new product implementation

## Authority boundary
Runtime/data and reproducible evidence outrank documents. Legacy documents/data/code are historical until the new baseline explicitly promotes a reusable fact or component. Historical material must not silently become runtime authority.

## Foundation control boundary
The V2 foundation now has three explicit layers:
1. Engineering operating model
2. Task control
3. Evidence and closure

The next required layer is change/migration/compatibility/recovery control. Runtime implementation must not start until this foundation gap is closed.

## Recovery entrypoint
For a new AI/session with limited context, read in this order:
1. AGENTS.md
2. this file
3. docs/00_GOVERNANCE/AI_FACTORY_OS_ENGINEERING_OPERATING_MODEL.md
4. docs/05_EXECUTION/ACTIVE_TASK.md
5. the authoritative model(s) named by the active Task
6. only the deeper architecture/business/evidence sources required by that Task

## Next permitted work
TASK-V2-FOUNDATION-003 is the sole current work pointer:
Establish change, migration, compatibility, and recovery control before rebuilding runtime code or database structures.
