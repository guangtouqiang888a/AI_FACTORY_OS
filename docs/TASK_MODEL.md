# Task Model

Defines what a Task is, and how a Task may lawfully move the system.

Stable principles: [CONSTITUTION.md](CONSTITUTION.md).  
Roles: [AGENTS.md](../AGENTS.md).  
Product intent: [PRODUCT.md](PRODUCT.md).

This phase defines the **model only**.  
It does **not** create Task templates, Task registries, or concrete Task files.

## Task definition

A Task is:

> an engineering work unit with a clear objective, clear boundary, clear completion conditions, clear responsibility, and independent verifiability.

A Task is **not**:

- an idea
- a chat message
- a Cursor instruction line
- a Git commit
- “I think it is done”

## Task lifecycle

Normal path:

```text
IDEA
↓
BACKLOG
↓
READY
↓
IN_PROGRESS
↓
VALIDATING
↓
REVIEW
↓
ACCEPTED
↓
RELEASED
↓
OBSERVING
↓
CLOSED
```

Exception states:

```text
BLOCKED
REJECTED
SUPERSEDED
RETIRED
```

## State meanings

### IDEA

Only an idea or problem.  
Not executable.

### BACKLOG

Worth keeping, but not yet ready to execute.

### READY

Executable conditions are present. At minimum all of the following are explicit:

- Objective
- Scope
- Non-goals
- Acceptance Criteria
- Risk
- Dependencies
- Required Validation

### IN_PROGRESS

Execution is authorized and underway.

### VALIDATING

Implementation is complete and validation is underway.

Hard rule:

> Cursor finishing implementation does not mean the Task is complete.

### REVIEW

Independent technical / system review is underway.

### ACCEPTED

Acceptance Criteria are met and required review is complete.  
Only here may a Task be treated as complete in the engineering sense.

### RELEASED

The change is in a formally usable state.

### OBSERVING

The change is in a real environment and outcomes are being observed.

### CLOSED

The Task lifecycle is formally finished.

## Exception states

### BLOCKED

A blocking condition prevents safe continuation.

### REJECTED

The Task or its approach is rejected.

### SUPERSEDED

Replaced by a newer Task, approach, or direction.

### RETIRED

Related mechanism or objective is formally retired.

## Legal transitions

Allowed normal transitions:

```text
IDEA → BACKLOG
BACKLOG → READY
READY → IN_PROGRESS
IN_PROGRESS → VALIDATING
VALIDATING → REVIEW
REVIEW → ACCEPTED
ACCEPTED → RELEASED
RELEASED → OBSERVING
OBSERVING → CLOSED
```

Allowed exception transitions:

```text
any in-flight state → BLOCKED
REVIEW → REJECTED
READY / IN_PROGRESS / REVIEW → SUPERSEDED
work that is no longer needed → RETIRED
```

States must **not** be jumped arbitrarily.

Forbidden examples (unless a future exception mechanism is formally defined):

```text
IDEA → ACCEPTED
IN_PROGRESS → CLOSED
READY → RELEASED
```

No exception mechanism is defined in this phase.

## Propose / Verify / Authorize

These three actions are distinct and must not collapse into one automatic AI action.

### Propose

Propose a Task or a state change.

### Verify

Check whether facts satisfy stated conditions.

### Authorize

A party with authority approves continuation or completion.

AI may perform technical checks required for Verify.  
AI must **not** self-grant final Acceptance merely because its own execution succeeded.

## Acceptance

Acceptance requires:

```text
Acceptance Criteria
+
Validation
+
Review
+
Authorization
```

Not:

```text
Cursor says PASS
```

> Cursor PASS is only part of Implementation / Local Validation evidence.  
> Cursor PASS ≠ Task PASS

See also [CONSTITUTION.md](CONSTITUTION.md) and [AGENTS.md](../AGENTS.md).

## Minimal Task structure

A future Task should at least contain:

```text
Task ID
Title
Objective
Scope
Non-goals
Dependencies
Risk
Acceptance Criteria
Validation Plan
Authorization
State
History
```

This phase defines the structure only.  
**No Task template is created.**  
**No concrete Task is created.**

## Risk

```text
R0 — trivial / low impact
R1 — ordinary engineering
R2 — significant system impact
R3 — high-risk / external / irreversible
```

Higher risk implies stricter future requirements for:

- Impact Analysis
- Review
- Authorization
- Validation

**No Risk Engine is established in this phase.**

## Change Type

A Task must be able to distinguish change types such as:

```text
Bug Fix
Feature
Refactor
Database Change
API Change
Architecture Change
Product Change
Security Change
External Action
```

Different Change Types may later trigger different controls, for example:

```text
Database Change → Migration / Compatibility concerns
API Change → Compatibility concerns
Architecture Change → Architecture Decision / Migration
Product Change → Product Decision
```

These are concepts only.  
**No Change / Migration / Decision mechanism files are created in this phase.**

## Task and Evidence

A Task should eventually point to validation facts:

```text
Task
↓
Validation
↓
Evidence
```

**Evidence System is not established yet.**  
Do not invent Evidence IDs in this phase.
