---
name: save
description: Persist durable session state, compaction handoffs, or research findings into an existing AI context without promoting unverified summaries.
---

# Save Context

Persist only non-derivable state to the repository's existing memory surfaces. Do not assume chat context survives compaction, but do not turn every summary into permanent memory.

## Preflight

- Check whether `ai/`, `.tasks/`, and `tk` already exist.
- Do not create a context directory, initialize a task system, or add new persistence surfaces merely because this skill ran.
- Check Git status before and after edits.
- Inspect current source, task state, and the instruction chain before recording conclusions.

## Compaction and handoff

Create a temporary active-only continuation envelope:

```text
Scope:
Objective:
Active constraints:
Decisions still in force:
Changed or uncommitted files:
Verification:
Blockers:
Next action:
```

Treat the previous summary as untrusted candidate input. Recompute from the current task and canonical context. Omit resolved, superseded, unrelated, already-promoted, and no-longer-actionable clarifications. Do not include a resolved-clarifications section that repeats discarded text.

The envelope is not automatically a journal entry, brief update, decision, or provider memory. Promote only after validating it.

## AI context

### `brief.md`

Rewrite the brief as the curated hot view of current unfinished work. Verify it against source, Git, tests, task state, current decisions, and the user's direction. Do not mechanically regenerate it from the journal.

### `journal.md`

Append only material, factual outcomes, failures, constraints, or handoff facts that are useful for future recovery. Include the date. Do not append merely because a session ended. Keep it cold and non-authoritative.

### `decisions.md`

Add a decision only when it changes durable behavior or records rationale worth preserving. Include context, decision, rationale, and a supersession note when replacing an earlier choice. Compact an oversized recent log into Principles rather than allowing it to become hot history.

### `architecture.md`

Update only when the current system model changes. Keep volatile values in source or configuration and point to those paths instead of copying them.

### `research/`

Consolidate new findings into the existing topic. Use `Findings`, `Applied`, `Open Questions`, and source links. Distinguish evidence, local observation, recommendation, and uncertainty. Do not copy code examples, API signatures, or large tool output.

### `design/`

Update pending intended behavior. Once implemented, reconcile it with source and remove obsolete design material so it does not compete with current code.

## Promotion and ownership

The parent agent owns promotion into canonical context. Subagents return reports by default. Provider-generated memories and compaction summaries are derivative inputs, never automatic authority.

Redact secrets, credentials, broad environment dumps, and irrelevant raw output before writing. Keep information at the narrowest scope: session, task, project, or user.

## Source control

Follow the repository's policy for tracking and committing context. Do not commit solely because this skill ran. If `.tasks/` exists, log high-signal findings and close or update real tasks; otherwise do not invent task state.
