# AI_FACTORY_OS Engineering Operating Model

Status: FOUNDATIONAL / V2 BASELINE
Authority: Core governance
Purpose: Define the durable engineering model for human + AI development.

## 1. System definition
AI_FACTORY_OS is developed as a human-owned, AI-assisted, evidence-driven software system.
The system must be able to evolve without requiring routine freeze-and-rebuild cycles.

## 2. Stable collaboration model
Human Owner → owns goals, business judgment, risk appetite, and final authorization.
ChatGPT → owns architecture reasoning, planning, challenge, review, and closure judgment.
Cursor → owns implementation, local execution, technical validation, and repository changes.
GitHub → is the durable engineering record: code, tests, decisions, evidence, and continuity.
AI providers are replaceable implementation dependencies, not project authorities.

## 3. Engineering control loop
GOAL → PRODUCT → TASK → AI ENGINEERING → AUTOMATED VALIDATION → REVIEW → RELEASE → REAL WORLD → EVIDENCE → LEARNING → PRODUCT.
A development session is not the primary unit of continuity. The Task and repository state are.

## 4. Context architecture
L0 Governance: stable rules and boundaries.
L1 Architecture: system structure and contracts.
L2 Product/Business: goals, requirements, hypotheses, validation.
L3 Engineering: implementation, tests, data, deployment.
L4 Active Work: current task, plan, acceptance criteria, blockers.
L5 Evidence: tests, commits, runtime observations, commercial results.
Agents receive a map and retrieve only relevant layers. No single document should become an encyclopedia.

## 5. Task lifecycle
IDEA → BACKLOG → READY → IN_PROGRESS → VALIDATING → REVIEW → ACCEPTED → RELEASED → OBSERVING → LEARNED.
Exceptional states: BLOCKED / REJECTED / SUPERSEDED / RETIRED.
A state transition must have an explicit reason and, where applicable, evidence.

## 6. Definition of Done
A Task is not complete because an agent says it is complete.
Completion requires, as applicable: implementation matches scope; non-scope was not unintentionally changed; acceptance criteria pass; automated validation passes; migration/compatibility requirements pass; relevant documentation/current-state updates are made; commit/evidence is identifiable; independent closure review passes.

## 7. Risk-based change control
Ordinary change: Task → implement → test → review.
Data/schema change: impact analysis → migration → compatibility check → tests → review.
Architecture change: problem → alternatives → decision → migration plan → implementation → validation → review.
Security/credentials/external irreversible action: plan → risk assessment → explicit human authorization → action → evidence.

## 8. Evolution rule
Architecture is expected to evolve. When a design becomes inadequate: identify the concrete problem; record the decision; assess impact; define migration/compatibility needs; implement incrementally; validate old/new boundaries; deprecate old behavior; remove it only after safe migration.
Freeze-and-rebuild is an exceptional recovery measure, not a normal development lifecycle.

## 9. Knowledge states
FACT — directly supported reality.
OBSERVATION — recorded observation not yet generalized.
HYPOTHESIS — proposed explanation or opportunity.
DECISION — chosen direction.
VALIDATED_RULE — repeatedly supported rule suitable for system use.
RETIRED — no longer authoritative.
Historical knowledge must retain provenance and must not silently enter runtime authority.

## 10. Core-file discipline
Core files are few, stable, and cross-task.
A new core file is justified only when: the responsibility is durable; existing core files cannot reasonably own it; the file reduces rather than increases context burden; its role can be mechanically navigated.
Task logs, reports, experiments, and temporary notes are not core by default.

## 11. Continuity
The repository must always expose: what the system is; where it is now; what task is active; what was last verified; what is blocked; what the next permitted action is.
Conversation memory may accelerate recovery but cannot be required for recovery.

## 12. Non-negotiable principle
Build for evolution, verification, and recovery — not for the illusion that the first architecture will be permanently correct.
