# AI_FACTORY_OS Agent Map

## Purpose
AI_FACTORY_OS is a human-owned, AI-assisted, evidence-driven software system.
Xianyu is the first commercial validation environment, not the final purpose.

## Authority
1. Runtime/data and reproducible evidence
2. Code, tests, configuration, and migrations
3. Versioned requirements and decisions
4. Core governance/current-state documents
5. Conversation memory

Conversation memory is not the project's source of truth.

## Collaboration
- Human Owner: business goals, risk appetite, final authorization.
- ChatGPT: architecture, reasoning, planning, review, closure judgment.
- Cursor: implementation, local execution, tests, technical changes.
- GitHub: durable source of record for code, decisions, evidence, and continuity.

## Main loop
Goal → Product → Task → AI Engineering → Automated Validation → Review → Release → Real World → Evidence → Learning → Product.

## Task rule
Every engineering change must correspond to a bounded Task with purpose, scope, non-scope, acceptance criteria, validation requirements, and evidence/closure requirements.
Prefer small, reviewable batches.

## State rule
A Cursor completion report is not final acceptance.
A task closes only after required validation and independent closure review.

## Change rule
Do not solve architectural problems by defaulting to freeze/rebuild.
Prefer versioned evolution, migration, compatibility, deprecation, rollback, and evidence.

## Knowledge rule
Distinguish FACT / OBSERVATION / HYPOTHESIS / DECISION / VALIDATED_RULE / RETIRED.
Historical material must not silently become runtime authority.

## Context rule
This file is a map, not an encyclopedia.
Read only the deeper sources relevant to the current task.

## Core sources
- docs/00_GOVERNANCE/AI_FACTORY_OS_ENGINEERING_OPERATING_MODEL.md
- docs/01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md
- docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md
- docs/03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md
- docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md
- docs/06_HISTORY/

The existing legacy core documents are historical until the new baseline migration is explicitly completed.
