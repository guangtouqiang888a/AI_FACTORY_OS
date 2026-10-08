# AI_FACTORY_OS Active Task

Status: FOUNDATIONAL / V2 BASELINE
Authority: Active-work navigation
Purpose: Keep the current engineering unit recoverable without loading historical execution logs.

## Current Task

TASK-V2-FOUNDATION-002

Title: Establish Task control, state, acceptance, evidence, and closure mechanism.

Why:
The project needs a durable unit of work that survives ChatGPT context loss, Cursor sessions, and future AI/model changes.

Goal:
Make every future engineering change traceable from intent through validation and independent closure review.

Scope:
- Task identity and required fields
- Task state machine
- Definition of Done
- Evidence bundle
- Risk classes
- Failure/recovery rules
- Active-task recovery entrypoint

Non-scope:
- Runtime/database rebuild
- Market intelligence implementation
- Product implementation
- Legacy archive migration
- CI implementation

Acceptance criteria:
1. Task control model is versioned in GitHub.
2. The model defines normal and exceptional states.
3. Each transition has a clear meaning.
4. Definition of Done separates agent completion from accepted work.
5. Evidence requirements are explicit.
6. Risk classes determine stronger controls.
7. Failure handling explicitly avoids freeze-and-rebuild.
8. A future AI can locate the active Task without conversation memory.

Validation:
- Repository review of the Task control model.
- Confirm no runtime code or database files are changed by this Task.
- Confirm the active Task points to the authoritative control model.

Expected evidence:
- Git commit(s)
- Pull request / review
- Final closure review

Current state:
IN_PROGRESS
