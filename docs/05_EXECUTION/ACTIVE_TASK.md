# AI_FACTORY_OS Active Task

Status: V2 BASELINE
Authority: Active-work navigation
Purpose: Keep the current engineering unit recoverable without loading historical execution logs.

## Last closed Task

TASK-V2-FOUNDATION-002

Title: Establish Task control, state, acceptance, evidence, and closure mechanism.

Final state:
ACCEPTED

Closure result:
The Task contract was satisfied. The repository now contains the authoritative Task control model and the Evidence and Closure Model. The implementation change was reviewed after implementation; GitHub's platform rule prevented the PR author from submitting a formal APPROVE review, so no false independent GitHub approval is claimed.

Evidence:
- Task control model: docs/05_EXECUTION/TASK_CONTROL_MODEL.md
- Evidence/closure model: docs/05_EXECUTION/EVIDENCE_CLOSURE_MODEL.md
- Foundation PRs: #2 and #3
- Closure commit for evidence model: 228ca1765f94b6030d47e7358f13da7c54dd6c6b
- No runtime or database files were changed by these foundation Tasks.

Findings:
- GitHub does not allow a PR author to approve their own PR. This is now an explicit platform constraint rather than a hidden assumption.
- Future R2/R3 changes should use a genuinely separate review authority where practical; otherwise the closure record must explicitly disclose the limitation.

## Current Task

TASK-V2-FOUNDATION-003

Title: Establish change, migration, compatibility, and recovery control.

Why:
The project must evolve without returning to freeze-and-rebuild. Runtime, database, APIs, dependencies, and external contracts need a durable way to change safely.

Goal:
Define the minimum change-control mechanism that lets AI_FACTORY_OS introduce structural changes while preserving compatibility, migration traceability, rollback/recovery, and historical evidence.

Scope:
- Change classification and impact assessment
- Schema/data migration rules
- API/contract compatibility rules
- Deprecation and removal rules
- Rollback/recovery expectations
- Relationship between Change and Task
- Required evidence for structural changes

Non-scope:
- Runtime/database implementation
- Market intelligence implementation
- Product implementation
- CI implementation
- Legacy archive migration

Dependencies:
- TASK-V2-FOUNDATION-002
- docs/05_EXECUTION/TASK_CONTROL_MODEL.md
- docs/05_EXECUTION/EVIDENCE_CLOSURE_MODEL.md

Risk class:
R2

Acceptance criteria:
1. Structural changes have an explicit impact classification.
2. Schema/data changes require migration planning and verification.
3. API/contract changes define compatibility and deprecation expectations.
4. Rollback/recovery is addressed before R2/R3 changes are accepted.
5. Change records remain linked to their parent Task.
6. Historical evidence is preserved during evolution.
7. The model explicitly prevents “freeze-and-rebuild” from becoming the default response to change.

Validation:
- Repository review of the resulting change-control model.
- Confirm no runtime or database implementation is changed.
- Confirm the active Task is the sole current work pointer.

Expected evidence:
- Commit(s)
- Pull request/review
- Final closure review
- Updated Current State and Active Task

Current state:
READY
