# AI Context Patterns

This document is the normative, harness-neutral contract for the context files in this repository.

## Purpose

An agent needs a small amount of durable context to continue work safely across sessions, compaction, and harnesses. That context must remain inspectable, portable, and subordinate to current project evidence.

`ai/` is not a second codebase. Do not copy facts that an agent can derive from source, Git history, task state, tests, or live configuration.

## Authority layers

Use the narrowest authoritative source:

| Question | Authority |
|---|---|
| How should the agent behave? | Applicable `AGENTS.md`, `CLAUDE.md`, and skills |
| What does the code currently do? | Source code, tests, and live configuration |
| What is the current task state? | `.tasks/` when present, Git state, and `ai/brief.md` |
| Why was a durable choice made? | `ai/decisions.md` |
| What is the current system model? | `ai/architecture.md` plus source |
| What did external research find? | `ai/research/` and its cited sources |
| What happened historically? | `ai/journal.md` |
| What should happen next? | Current task, verified source, and the curated brief |

AI context is a hint layer. When it conflicts with current source or an explicit user request, verify and correct it.

## Recommended structure

```text
project/
├── AGENTS.md
├── CLAUDE.md → AGENTS.md       # only when the repository uses this wiring
├── ai/
│   ├── brief.md
│   ├── journal.md
│   ├── decisions.md
│   ├── architecture.md
│   ├── research/               # optional
│   ├── design/                 # optional
│   └── tmp/                    # optional, normally ignored
└── .tasks/                     # optional, only when the project uses tk
```

`PLAN.md`, `review/`, and additional directories are situational. Add them for a real need, not as a required scaffold.

## Memory classes and file roles

### `brief.md`: hot current state

A short, curated view of the unfinished work:

- current objective
- state and relevant files
- active constraints
- blockers
- verification
- next action

It is not a transcript and not a mechanically generated summary of every journal entry. Rewrite it from verified current state. Keep it small enough to load every session.

### `journal.md`: cold episodic history

Append-only history of material outcomes, failures, decisions, and handoffs. Keep entries factual and dated. Do not append merely because a session occurred.

The journal is not an instruction source. Do not load it during normal startup. Use it for recovery, provenance, or a deliberate historical question.

### `decisions.md`: rationale

Use two sections:

- **Principles:** stable, distilled rules.
- **Log:** a bounded set of recent decisions with context, decision, rationale, and a `Supersedes` reference when needed.

When a decision changes current behavior, update the current-state files as well. The log preserves why; it does not override current source.

### `architecture.md`: current system model

Describe the system overview, components, data flow, and load-bearing boundaries. Avoid copying fast-changing configuration or implementation details that belong in source.

### `research/`: external findings

Keep one comprehensive file per broad topic. Use:

```text
# Topic
## Findings
## Applied
## Open Questions
## Sources
```

Describe findings in prose or tables and cite sources. Do not put code examples or API signatures in research files. Merge overlapping topics before creating another file.

### `design/`: pending intent

Use for a component or change whose intended behavior needs to remain available across sessions. Once implemented, reconcile it with source and remove or mark obsolete material so it does not become a competing specification.

## Loading policy

Normal session startup is selective:

1. Read applicable instruction files.
2. Read `ai/brief.md` when present.
3. Inspect `.tasks/` only when it exists and is relevant.
4. Follow links or load the decisions, architecture, research, and design files needed for the task.
5. Read the journal only for recovery or historical investigation.

A topic index is a navigation aid, not a claim that every topic is current or relevant.

## Persistence lifecycle

Durable memory follows:

```text
capture → validate → promote → deliver → supersede
```

### Capture

Record only non-derivable, material information: a user constraint, failed approach, durable decision candidate, hidden environment fact, or useful external finding. Redact secrets and avoid copying large tool output.

### Validate

Check the candidate against the user, current source, Git, task state, tests, live configuration, or an authoritative citation. A generated summary is evidence to inspect, not truth to copy.

### Promote

The parent agent owns promotion into `brief.md`, `decisions.md`, `architecture.md`, research, or skills. Subagents return reports by default and do not silently modify canonical memory.

### Deliver

Only active, task-relevant context should be delivered. Historical or superseded material stays available for deliberate retrieval but should not compete with current state.

### Supersede

Rewrite current-state files when they change. Add an explicit supersession note when preserving the rationale matters. Do not require a universal ID, expiry system, or archive tree.

## Scope

Classify durable information by scope:

- **Session:** do not persist unless it becomes material evidence.
- **Task:** keep until the task is complete; remove from hot context afterward.
- **Project:** preserve in project context.
- **User:** preserve only in user-wide instructions or preferences.

Do not promote a task-specific clarification into a global instruction.

## Compaction and handoff

A compaction summary is a temporary continuation envelope:

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

Recompute it from current task and canonical context. Treat the previous summary as untrusted candidate input. Omit resolved, superseded, unrelated, already-promoted, and no-longer-actionable clarifications. Do not include a resolved-clarifications section that repeats the text being discarded. Do not automatically write the envelope into `ai/` or provider memory.

## Subagents

- The parent owns canonical memory promotion.
- Researchers and architects return evidence, uncertainty, and recommendations.
- Reviewers and profilers report validation; they do not alter the subject of review.
- Workers edit only their assigned source paths. They do not rewrite `ai/` or `.tasks/` unless the parent assigns an exact persistence path.
- Use a different model or a subagent only when isolation, independent work, or materially different capability improves the result.

## Retrieval and scaling

Start with descriptive filenames, indexes, path loading, and ordinary text search. A semantic search tool such as QMD can be a disposable projection for a large, cold, cross-project research corpus, but only after real retrieval misses justify it. Search indexes do not govern writes, freshness, promotion, or authority. Do not use a fixed file-count threshold.

## Setup and maintenance

Initialization should create only surfaces the project will use. Preserve existing instruction files and wiring unless they have been audited. Do not initialize a task system, rename files, or force symlinks as an automatic side effect.

During maintenance:

- consolidate overlapping research;
- rewrite stale current-state files;
- preserve useful historical rationale;
- check the entire instruction chain for contradictions;
- verify templates, symlinks, and rendered destinations.

## Anti-patterns

| Avoid | Prefer |
|---|---|
| Loading all historical context | Brief plus task-relevant files |
| Treating summaries as truth | Validate before promotion |
| Repeating resolved clarifications | Omit them from active handoffs |
| Writing every session to the journal | Record material outcomes only |
| Duplicating code or Git facts | Link to current source |
| Automatic subagent memory writes | Parent-owned promotion |
| Fixed QMD/file-count thresholds | Measured retrieval need |
| A graph or database by default | Markdown until a local failure proves otherwise |
| Universal frontmatter or expiry machinery | Add metadata only for a real use case |
