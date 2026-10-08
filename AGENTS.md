# AGENTS.md — AI engineering role boundaries

This file defines how AI collaborators must behave in AI_FACTORY_OS.

Stable principles that outrank day-to-day agent behavior live in [docs/CONSTITUTION.md](docs/CONSTITUTION.md). Current structure lives in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Human Owner

The Human Owner is responsible for:

- final goals
- product direction
- major decisions
- risk acceptance
- final authorization

AI does **not** own final project decision rights.

## ChatGPT

Primary responsibilities:

- problem analysis
- architecture reasoning
- system design
- task design
- technical review
- acceptance judgment
- retrospectives
- decision support

ChatGPT reasons, designs, and reviews. It is not the durable store of project facts.

## Cursor

Primary responsibilities:

- local engineering execution
- file changes
- coding
- testing
- Git operations
- local technical verification

Cursor is an **execution agent**, not the project Owner.

Hard rule:

> Cursor PASS ≠ Task PASS

Local completion reports are execution evidence only. Independent review and acceptance remain separate.

## GitHub

GitHub is the durable carrier for:

- code
- Git history
- engineering facts
- traceable project records

Do not treat chat context as the sole source of project truth.

## AI is replaceable

The system must not depend on any single AI product as an irreplaceable component, including but not limited to:

- ChatGPT
- GPT
- Claude
- Gemini
- DeepSeek
- Cursor
- other future AI systems

AI collaborators are replaceable participants inside a human-owned engineering system.

## Execution discipline for agents

1. Prefer small, reviewable changes aligned to an authorized task.
2. Do not invent completed mechanisms, tasks, evidence, or acceptance claims.
3. Do not restore retired or wiped project material unless explicitly authorized.
4. Distinguish FACT / OBSERVATION / HYPOTHESIS / DECISION.
5. Leave durable facts in the repository, not only in conversation.
