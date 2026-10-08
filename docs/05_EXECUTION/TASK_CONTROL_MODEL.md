# AI_FACTORY_OS Task Control Model

Status: FOUNDATIONAL / V2 BASELINE
Authority: Core engineering governance
Purpose: Define the smallest durable unit of AI-assisted engineering work.

## 1. Task is the unit of work
A Task is a bounded change with a clear reason, scope, acceptance criteria, validation method, and closure evidence.
A chat session, Cursor session, commit, or Entry is not a Task by itself.

## 2. Required Task fields
Every implementation Task must define:
- Task ID
- Title
- Why / problem
- Goal
- Scope
- Non-scope
- Dependencies
- Risk class
- Acceptance criteria
- Validation requirements
- Expected evidence
- Rollback / recovery expectation when applicable

A Task should be small enough to understand, implement, test, and review without broad context reconstruction.

## 3. State machine
Normal path:
IDEA → BACKLOG → READY → IN_PROGRESS → VALIDATING → REVIEW → ACCEPTED → RELEASED → OBSERVING → LEARNED

Exceptional states:
BLOCKED / REJECTED / SUPERSEDED / RETIRED

BLOCKED means the Task cannot safely proceed with current information or dependencies.
REJECTED means the proposed result does not satisfy acceptance criteria or an authorized decision stops it.
SUPERSEDED means another Task or decision replaces its intended outcome.
RETIRED means the Task's result or direction is no longer active authority.

## 4. State transition rules
IDEA → BACKLOG: a useful problem/opportunity is recorded.
BACKLOG → READY: sufficient context, goal, scope, acceptance criteria, and priority exist.
READY → IN_PROGRESS: implementation is authorized to start.
IN_PROGRESS → VALIDATING: implementation is complete enough for required validation.
VALIDATING → REVIEW: required automated validation passes and evidence is captured.
REVIEW → ACCEPTED: independent closure review confirms scope, acceptance, risk controls, and evidence.
ACCEPTED → RELEASED: accepted change is integrated/released according to delivery requirements.
RELEASED → OBSERVING: change reaches its intended environment and is monitored where meaningful.
OBSERVING → LEARNED: real-world evidence is assessed and resulting knowledge/decision is recorded.

Any active state may become BLOCKED when dependency, uncertainty, safety issue, or missing evidence prevents responsible continuation.

## 5. Definition of Done
A Task is DONE only when:
1. Scope is satisfied.
2. Non-scope has not been unintentionally changed.
3. Acceptance criteria are satisfied.
4. Required automated checks pass.
5. Required migration/compatibility checks pass.
6. Relevant documentation or Current State is updated.
7. Evidence is traceable to the implementation.
8. Independent closure review passes.
9. If real-world behavior changes, release/observation boundary is explicit.

An agent's completion statement is evidence of execution, not proof of acceptance.

## 6. Evidence bundle
Closure evidence should answer:
- What changed and why?
- Which files/components changed?
- Which checks ran and results?
- Which commit contains the change?
- Were migrations performed?
- What remains uncertain?
- What is the next permitted action?

Do not duplicate full logs into core governance files. Store durable evidence at the appropriate repository location and keep navigation concise.

## 7. Risk classes
R0 — documentation/non-functional housekeeping.
R1 — ordinary isolated code/config/test change.
R2 — data/schema, API contract, dependency, or cross-module change.
R3 — architecture, security, credentials, external irreversible action, or production-impacting change.

Higher risk requires stronger validation, review, and explicit authorization.

## 8. Failure and recovery
A failed Task does not justify project reconstruction.

Preferred response:
failure → capture evidence → classify cause → fix same Task if scope remains valid
OR create a corrective Task
OR supersede the Task with an explicit decision.

Rollback should restore a known-good state where technically feasible.

## 9. Task identity and continuity
Task IDs are durable references, not session numbers.
A future AI must recover a Task from repository state without conversation memory.

## 10. Core-file discipline
This model defines the Task contract. Individual Task details belong in the active-work layer, not in this core document.

## 11. Non-negotiable principle
Small, bounded, evidence-backed changes are preferred over large autonomous batches.
Optimize for recoverability and correctness, not maximum code-generation speed.
