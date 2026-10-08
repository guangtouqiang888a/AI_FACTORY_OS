# AI_FACTORY_OS Evidence and Closure Model

Status: FOUNDATIONAL / V2 BASELINE
Authority: Core engineering governance
Purpose: Define the minimum durable evidence and independent closure contract for AI-assisted engineering work.

## 1. Why this model exists

An implementation agent can report completion without proving that the project should accept the result.

AI_FACTORY_OS therefore separates:

- execution evidence: evidence that the requested work was performed;
- validation evidence: evidence that required checks passed;
- closure judgment: an independent determination that the Task satisfies its contract.

The repository must preserve enough evidence for a future AI or human to reconstruct that judgment without relying on chat history.

## 2. Evidence bundle

Every Task reaching REVIEW must have a traceable evidence bundle containing, as applicable:

1. Task ID and final scope.
2. Changed files/components.
3. Acceptance criteria and result for each criterion.
4. Automated validation commands/checks and outcomes.
5. Relevant manual verification or review findings.
6. Commit SHA and pull request/review reference when used.
7. Migration, compatibility, rollback, or recovery evidence for R2/R3 changes.
8. Known limitations, unresolved uncertainty, or deviations.
9. Real-world observation boundary when the change affects runtime or users.
10. Next permitted action.

Evidence should point to durable repository artifacts rather than copying large logs into core governance files.

## 3. Evidence quality

Evidence is classified as:

- DIRECT: produced by the system, test, runtime, repository, or other reproducible source.
- REVIEWED: interpreted by a human or independent AI review against the Task contract.
- SELF_REPORTED: produced only by the implementing agent or operator.

SELF_REPORTED evidence may support execution history but cannot by itself establish ACCEPTED.

For important claims, prefer DIRECT evidence over inference.

## 4. Acceptance matrix

Closure review must evaluate at least:

| Area | Required question |
|---|---|
| Scope | Was the intended scope implemented? |
| Non-scope | Was unrelated behavior left unchanged? |
| Acceptance | Does every acceptance criterion pass? |
| Validation | Did required automated checks pass? |
| Risk | Were controls appropriate to the Task risk class? |
| Compatibility | Were affected contracts/data handled safely? |
| Evidence | Can the result be independently reconstructed? |
| Uncertainty | Are limitations and unknowns explicit? |
| Release boundary | If applicable, is deployment/observation status clear? |

A single unresolved acceptance failure prevents ACCEPTED unless an authorized decision explicitly changes the Task contract.

## 5. Closure states

The Task state and closure judgment are related but not identical.

- VALIDATING: implementation is ready for required checks.
- REVIEW: required validation has passed and evidence is assembled.
- ACCEPTED: independent closure review confirms the Task contract is satisfied.
- REJECTED: review determines the proposed result is not acceptable.
- BLOCKED: responsible closure cannot proceed because required information/evidence is missing.
- SUPERSEDED: another authorized Task or decision replaces the intended outcome.

A Task must not be marked ACCEPTED merely because tests pass.

## 6. Independent closure review

The closure reviewer must compare the result against:

1. the Task contract;
2. the actual repository change;
3. validation evidence;
4. applicable risk controls.

The reviewer may be ChatGPT or another qualified reviewer; the implementing Cursor/agent must not be treated as the sole acceptance authority.

For R2/R3 changes, closure should explicitly verify migration, compatibility, rollback, security, or external-action controls as applicable.

## 7. Closure record

The durable closure record should contain:

- Task ID
- final state
- acceptance result
- evidence references
- reviewer
- review date
- unresolved findings
- next permitted action

Keep the record concise. Detailed logs belong in their native artifacts.

The active Task file is the primary navigation point for the current closure status; historical execution ledgers are not required to duplicate the closure record.

## 8. Findings

Findings are classified as:

- BLOCKER: acceptance cannot pass.
- MATERIAL: acceptance may pass only with an explicit documented decision or follow-up Task.
- MINOR: does not prevent acceptance but should be recorded.
- OBSERVATION: useful information without an immediate action requirement.

A Task with findings may be ACCEPTED only when no BLOCKER remains and any MATERIAL finding has an explicit disposition.

## 9. Evidence retention

Evidence should remain addressable after the chat session ends.

At minimum, the repository should retain:

Task → change → validation → review → commit → release/observation (when applicable).

Do not rely on model memory, screenshots without repository references, or chat-only conclusions as the sole durable record.

## 10. Recovery rule

If evidence is incomplete:

1. do not infer success;
2. mark the Task BLOCKED or return it to the appropriate earlier state;
3. identify the missing evidence;
4. perform only the smallest required follow-up work;
5. re-run closure review.

Missing evidence is a recoverable control failure, not a reason to reconstruct the project.

## 11. Core-file discipline

This document defines the reusable evidence/closure contract.

Individual Task evidence and closure details remain in the active-work layer or native repository artifacts. Do not create a permanent core file for every Task.

## 12. Non-negotiable principle

AI_FACTORY_OS accepts outcomes, not claims of completion.

The system should make correct work easy to verify, incorrect work easy to detect, and incomplete work easy to recover.
