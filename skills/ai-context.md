---
name: ai-context
description: Operate on an established ai/ context, load relevant memory, and enforce its authority and lifecycle rules.
---

# AI Context

Use this skill for routine work inside an established `ai/` directory. Use `setup-ai` for initialization, migration, or a full audit. Use `save` when persisting a handoff or durable outcome.

## Purpose

`ai/` preserves non-derivable context across sessions:

- `brief.md`: current task state
- `journal.md`: historical events and provenance
- `decisions.md`: rationale
- `architecture.md`: current system model
- `research/`: external findings
- `design/`: pending intended behavior

It is a context aid, not a second codebase. Current source, tests, Git, task state, live configuration, and explicit user requests remain authoritative.

## Loading

At session start:

1. Read applicable instruction files.
2. Read `ai/brief.md` when present.
3. Inspect `.tasks/` only when it exists and matters to the task.
4. Follow links or load relevant decisions, architecture, research, and design files.
5. Read `journal.md` only for recovery or deliberate historical investigation.

Do not load all historical context by default.

## File contracts

### Brief

Keep `brief.md` a small, curated hot view:

- objective
- current state
- active constraints
- relevant files
- blockers
- verification
- next action

Rewrite it from verified current state. It is not a transcript or a mechanical cache of the journal.

### Journal

Keep `journal.md` append-only and factual. Record material outcomes, failures, decisions, and handoff facts. Do not record every session. It is cold history and does not override current state.

### Decisions

Keep stable Principles and a bounded recent Log. Record why a durable choice exists and identify what it supersedes when necessary. Current files must reflect current decisions; the log preserves rationale.

### Architecture

Describe what the current system is and where its load-bearing boundaries are. Point to source and configuration for volatile implementation details.

### Research and design

Keep one comprehensive research file per broad topic and consolidate before multiplying. Research uses `Findings`, `Applied`, `Open Questions`, and source links. Design describes pending intent and must be reconciled after implementation. Do not copy code, API signatures, or large outputs into either.

## Lifecycle

```text
capture → validate → promote → deliver → supersede
```

Capture material, non-derivable observations. Validate against current evidence. The parent promotes only future-relevant information into canonical files. Deliver only active, task-relevant context. Supersede obsolete current guidance explicitly when its rationale matters.

Compaction summaries, provider memories, and subagent reports are inputs to validate, not automatic canonical memory.

## Scope

- Session-only information stays ephemeral.
- Task constraints expire with the task.
- Project rules belong in project instructions or project `ai/`.
- User-wide preferences belong in user-wide instructions.

Do not promote a task-specific clarification into global memory.

## Subagents

The parent owns canonical-memory promotion. Researchers and architects return evidence and recommendations. Reviewers and profilers report validation. Workers edit assigned source paths only and do not rewrite `ai/` or `.tasks/` unless the parent assigns an exact path.

## Retrieval

Use descriptive paths, indexes, and ordinary text search first. Consider QMD only as a disposable cold-research projection after real retrieval misses. Do not use a file-count threshold and never make an index authoritative.
