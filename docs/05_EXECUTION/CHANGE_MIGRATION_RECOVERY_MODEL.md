# AI_FACTORY_OS Change, Migration, Compatibility and Recovery Model

Status: FOUNDATIONAL / V2 BASELINE
Authority: Core engineering governance
Purpose: Define how AI_FACTORY_OS evolves structural behavior without defaulting to freeze-and-rebuild.

## 1. Change is normal

AI_FACTORY_OS is expected to evolve.

A structural problem must not automatically trigger project reconstruction. The default strategy is:

assess → isolate → change → migrate/compatibilize → validate → release → observe → retire old path.

Reconstruction is an exceptional decision requiring explicit evidence that controlled evolution is no longer viable.

## 2. Change classes

Every change is classified before implementation:

| Class | Typical examples | Minimum control |
|---|---|---|
| C0 | wording, comments, nonfunctional docs | Task + normal review |
| C1 | isolated code/config/test behavior | Task + automated validation |
| C2 | schema, data, API, dependency, cross-module, shared contract | Task + impact assessment + compatibility/migration/recovery plan |
| C3 | architecture, security, credentials, irreversible external action, production-critical change | Task + explicit authorization + stronger validation + recovery plan + independent review |

Task risk class and change class are related but not identical. A Task may contain multiple changes; the highest applicable control governs.

## 3. Impact assessment

For C2/C3 changes, record:

- affected components;
- affected data/schema;
- affected APIs/contracts;
- affected dependencies;
- compatibility window;
- migration requirements;
- rollback/recovery path;
- operational/user impact;
- evidence required after release.

Do not begin structural implementation while a material impact is still unknown unless the Task explicitly defines a bounded discovery step.

## 4. Task and Change relationship

Task is the durable unit of authorized work.

A Change is a concrete structural modification performed under a Task.

Relationship:

Task → one or more Changes → validation/evidence → closure.

A Change must not exist as an untracked architectural mutation outside a Task.

For a small C0/C1 Task, a separate Change record is unnecessary.

For C2/C3 work, the Task must retain enough information to identify each material Change and its validation/migration evidence.

## 5. Schema and data migration

Schema/data changes require an explicit migration plan before acceptance.

The plan should define, as applicable:

1. current schema/data state;
2. target state;
3. forward migration;
4. data transformation/backfill;
5. validation of migrated data;
6. compatibility during transition;
7. rollback or recovery strategy;
8. cleanup/removal of obsolete structures.

Prefer additive or expand/contract migrations when live compatibility matters:

expand → migrate/backfill → switch consumers → verify → contract.

Do not destroy old data or schema solely to simplify implementation when a controlled migration is practical.

## 6. API and contract compatibility

For shared APIs/contracts, classify the change as:

- compatible: existing valid consumers continue to work;
- conditionally compatible: existing consumers work only under a documented transition condition;
- breaking: existing valid consumers require change.

Breaking changes require an explicit migration/deprecation path unless the contract is provably non-live or an authorized decision accepts the break.

Prefer:

introduce new behavior → migrate consumers → observe → deprecate old behavior → remove old behavior.

Do not silently change the meaning of an existing field, endpoint, event, or persisted value.

## 7. Deprecation and removal

A deprecated path should identify:

- what is deprecated;
- replacement path;
- reason;
- migration guidance;
- expected coexistence period or removal condition;
- evidence that active consumers have migrated.

Removal is a separate controlled change when the old path may still be used.

“Unused” must be established by evidence, not assumption, when practical.

## 8. Dependencies

Dependency changes are at least C2 when they can affect runtime behavior, interfaces, security, or reproducibility.

Before acceptance, verify:

- version/source;
- compatibility;
- tests;
- configuration changes;
- known security or behavior impact where relevant;
- rollback or pinning path.

Do not upgrade dependencies merely because a newer version exists.

## 9. Rollback and recovery

Every C2/C3 change must define the recovery strategy before acceptance.

Possible strategies include:

- revert commit/release;
- disable feature;
- switch consumer back to old contract;
- restore compatible schema/data state;
- restore from backup/snapshot;
- run compensating migration;
- isolate affected component.

Rollback is not assumed to be trivial. For destructive or irreversible operations, define recovery before execution.

If true rollback is impossible, the Task must explicitly state the irreversibility and required safeguards.

## 10. Historical evidence preservation

Evolution must preserve the ability to understand what happened.

Do not rewrite history to conceal failed approaches or delete evidence merely because an implementation was replaced.

When replacing a component:

old version → migration/change evidence → new version.

Historical material may be retired from runtime authority while remaining available as evidence.

## 11. Versioning

Use explicit versioning when a contract or persisted structure needs compatibility management.

Version only what needs a stable compatibility boundary; do not create versions for every internal implementation detail.

Possible version boundaries include:

- database schema version;
- API/contract version;
- data format version;
- externally visible behavior version.

Version identifiers must be traceable to the migration/change that introduced them.

## 12. Recovery-first failure handling

If a structural change fails:

1. stop further expansion of the failed change;
2. preserve failure evidence;
3. determine whether the known-good state remains intact;
4. rollback/recover where appropriate;
5. classify the failure;
6. continue the same Task only if its scope and safety remain valid;
7. otherwise create a corrective Task or supersede the original decision.

Do not respond to a failed migration, API change, or architecture change by deleting the project and rebuilding from scratch.

## 13. Acceptance requirements for C2/C3

Before ACCEPTED, closure review must confirm:

- impact assessment exists;
- migration/compatibility plan exists where applicable;
- validation covers old and new behavior where compatibility matters;
- recovery path is documented and credible;
- irreversible actions were explicitly authorized;
- evidence links the change to its parent Task;
- obsolete paths are not removed prematurely;
- Current State and relevant architecture/contract documentation are updated.

## 14. Minimal change record

A C2/C3 change record may be embedded in the Task or native migration/API artifact. A new permanent core file is not required for every change.

Minimum durable fields:

- Change ID
- Parent Task ID
- change class
- affected surface
- before/after state
- migration/compatibility strategy
- validation
- recovery strategy
- evidence references
- disposition

## 15. Core-file discipline

This document defines the reusable change-control contract.

Individual migrations, API versions, deprecations, and change details belong in native repository artifacts or the active Task. Do not grow the core with one document per change.

## 16. Non-negotiable principle

AI_FACTORY_OS must be able to change without forgetting what existed before the change, and recover without reconstructing the whole project.

Evolution is the default. Reconstruction is an exceptional, evidence-backed decision.
