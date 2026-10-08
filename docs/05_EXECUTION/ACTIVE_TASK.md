# AI_FACTORY_OS Active Task

Status: V2 BASELINE
Authority: Active-work navigation
Purpose: Keep the current engineering unit recoverable without loading historical execution logs.

## Last closed Task

TASK-V2-FOUNDATION-003

Title: Establish change, migration, compatibility, and recovery control.

Final state:
ACCEPTED

Closure result:
The Task contract was satisfied. AI_FACTORY_OS now has an explicit control model for structural change classification, impact assessment, schema/data migration, API compatibility, deprecation, dependency changes, rollback/recovery, historical evidence preservation, and C2/C3 acceptance.

Evidence:
- Change/migration/recovery model: docs/05_EXECUTION/CHANGE_MIGRATION_RECOVERY_MODEL.md
- Foundation PR: #5
- Closure commit: f98d06c7df8504362b5e4f8d717fab7b5ca0d413
- No runtime or database implementation files were changed by this Task.

Findings:
- C2/C3 work requires stronger evidence and recovery controls than ordinary isolated changes.
- The next runtime/database work must be treated as structural work and must therefore use these controls.

## Current Task

TASK-V2-FOUNDATION-004

Title: Establish the clean runtime/database baseline and verification boundary.

Why:
The engineering control foundation is now in place. The project needs a new runtime/data baseline that is isolated from the retired Entry-driven implementation and can evolve through the V2 controls.

Goal:
Create the smallest executable baseline for AI_FACTORY_OS, with a clear runtime boundary, database boundary, configuration boundary, automated verification boundary, and recovery path.

Scope:
- Define the new runtime/application boundary
- Define the initial database boundary
- Establish minimal project configuration
- Establish deterministic automated verification entrypoint
- Establish clean separation from retired implementation
- Record initial schema/version identity where applicable
- Establish local recovery/reset procedure for the new baseline

Non-scope:
- Xianyu market intelligence
- Keyword collection
- Product generation
- Business rules beyond baseline health checks
- Production deployment
- Legacy migration into the new runtime

Dependencies:
- TASK-V2-FOUNDATION-003
- docs/05_EXECUTION/TASK_CONTROL_MODEL.md
- docs/05_EXECUTION/EVIDENCE_CLOSURE_MODEL.md
- docs/05_EXECUTION/CHANGE_MIGRATION_RECOVERY_MODEL.md

Risk class:
R2

Acceptance criteria:
1. New runtime boundary is explicit and does not depend on retired runtime code.
2. New database boundary is explicit and version-identifiable.
3. Configuration/secrets are separated from source-controlled code.
4. A deterministic automated verification command exists and passes.
5. The baseline can be initialized/recovered without manual reconstruction of project history.
6. No market-intelligence or product behavior is smuggled into the baseline.
7. Current State and evidence point to the new baseline unambiguously.

Validation:
- Repository inspection of runtime/database/configuration boundaries.
- Execute the deterministic verification command.
- Confirm retired runtime remains historical only.
- Confirm no business behavior beyond health/baseline checks is introduced.

Expected evidence:
- Commit(s)
- Pull request/review
- Test/verification output
- Final closure review
- Updated Current State and Active Task

Current state:
READY
