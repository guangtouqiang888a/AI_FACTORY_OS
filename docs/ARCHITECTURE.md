# Architecture

```text
Architecture Version: 0.1
Status: INITIAL CORE
```

This document describes the **current** architecture starting point.  
It is not permanent truth. Stable principles live in [CONSTITUTION.md](CONSTITUTION.md). Role boundaries live in [AGENTS.md](../AGENTS.md).

## 1. Architecture Goal

Enable AI to participate in continuous software evolution under:

- explicit boundaries
- explicit context
- intended automated validation
- traceable facts

## 2. Knowledge Model

Six knowledge layers are defined as a **model only**:

```text
L0 — Project Constitution
L1 — Architecture
L2 — Product Knowledge
L3 — Engineering Knowledge
L4 — Active Work
L5 — Evidence
```

Meaning:

- **L0** — most stable; defines what the system fundamentally is
- **L1** — relatively stable; describes current structure and evolution rules
- **L2 / L3** — change with product and engineering reality
- **L4** — highly dynamic active work
- **L5** — facts, results, and historical evidence

Presence of L0–L5 in this model does **not** authorize creating six matching directory trees or six matching file systems.

Current materialization in the repository:

```text
L0 → docs/CONSTITUTION.md
L1 → docs/ARCHITECTURE.md
L2 → docs/PRODUCT.md
L3 → not established yet
L4 → docs/CURRENT_STATE.md
L5 → not established yet
```

Clarifications:

- `docs/PRODUCT.md` is the current top-level entry for **L2 Product Knowledge**.
- `docs/CURRENT_STATE.md` is the current navigation entry for system state under **L4 Active Work / active-state context**.
- `docs/TASK_MODEL.md` defines the Task mechanism. It is **not** a concrete Task, and its existence does **not** mean a full L4 Task System is established.
- **L5 Evidence System** is not established.
- **L3 Engineering Knowledge** is not established.

## 3. Collaboration Architecture

```text
Human Owner
      ↕
   ChatGPT
      ↕
    Cursor
      ↕
Local Repository
      ↕
     Git
      ↕
   GitHub
```

This is not a one-way pipeline.

- Human provides goals and authorization
- ChatGPT provides analysis, design, and review
- Cursor performs local engineering operations
- GitHub stores durable facts and history

## 4. Evidence Loop

Target loop:

```text
Observation
→ Evidence
→ Analysis
→ Hypothesis
→ Decision
→ Implementation
→ Real Result
→ Validation
```

This phase defines the model only.  
No Evidence system is established here.

## 5. Architecture Evolution

Intended evolution path:

```text
Problem
→ Impact Analysis
→ Decision
→ Migration Plan
→ Compatibility
→ Implementation
→ Validation
→ Retirement
```

Rules:

- architecture may evolve
- uncontrolled breakage is not allowed
- permanent freeze out of fear of change is not allowed
- local problems must not automatically trigger whole-system rebuild

Detailed change-control mechanisms are deferred.

## 6. Core / Dynamic Separation

### Core

Long-lived, cross-task material that defines how the system exists, plus system-level navigation that currently anchors orientation.

Currently:

```text
README.md
AGENTS.md
docs/CONSTITUTION.md
docs/ARCHITECTURE.md
docs/PRODUCT.md
docs/TASK_MODEL.md
docs/CURRENT_STATE.md
```

`docs/CURRENT_STATE.md` is a navigation entry for dynamic content. It currently exists as a system-level core navigation file. It is **not** a Task Registry and **not** an Evidence Registry.

### Dynamic

Active tasks, current evidence, current decisions, current execution state, and similar short-lived material.

Principle:

> Core must not be polluted by a single active task.

Also:

> Core / Dynamic separation depends on the responsibility a file carries, not only on whether its content changes over time.

## 7. Current Architecture Is Not Final

`Architecture 0.1` is only the starting point.

Future architecture changes should carry:

- problem
- rationale
- impact analysis
- decision
- migration
- validation

Those concrete mechanisms belong to later phases.
