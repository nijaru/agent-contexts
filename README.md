# Agent Contexts

Portable conventions for keeping coding-agent context useful across sessions and harnesses.

AI agents can usually write code. The harder problem is preserving the small amount of non-derivable context that makes the next session faster and safer.

## Design decision

Keep Markdown as the canonical memory surface. Keep the active view small and inspectable. Let the model synthesize meaning; let repository state, Git, tests, and current configuration remain authoritative.

This repository provides a general contract. A personal chezmoi configuration may add harness-specific overlays, hooks, or skills, but those additions should not silently change the portable contract.

## Quick start

Copy `global/AGENTS.md` into a repository's `AGENTS.md`, then adapt the project-specific sections. Add the skills that the repository will actually use:

```text
AGENTS.md
ai/
├── brief.md
├── journal.md
├── decisions.md
└── architecture.md
```

The `agents/` directory contains reusable profiles, and `skills/` contains focused operational guidance. Copy only the files a repository needs.

Add `ai/research/`, `ai/design/`, or `ai/tmp/` only when the project needs them. Use `.tasks/` and `tk` only when the repository already uses them or the user explicitly chooses them.

For Claude Code, create `CLAUDE.md` as a symlink to `AGENTS.md` only when that repository's wiring calls for it. Do not rename, merge, or delete existing instruction files automatically.

## Memory model

```text
Instructions  → how the agent should behave
brief.md      → current, task-relevant state
journal.md    → cold historical events and provenance
decisions.md  → why durable choices were made
architecture  → what the current system is
research/     → external findings and open questions
design/       → intended behavior before implementation
```

`ai/` stores what cannot be derived from code, Git, task state, tests, or live configuration. It is a context aid, not a second codebase or an authority over current source.

## Normal loading order

1. Applicable `AGENTS.md` and tool-specific instructions.
2. `ai/brief.md`, when present.
3. Existing task state, when relevant.
4. Linked or task-relevant decisions, architecture, research, or design files.
5. `journal.md` only for recovery or historical investigation.

Do not load every historical file by default. More context is not automatically better context.

## Persistence lifecycle

Use this workflow for durable information:

```text
capture → validate → promote → deliver → supersede
```

- **Capture:** record a material observation, failure, constraint, or decision candidate.
- **Validate:** check it against the user, source, Git, task state, tests, or cited evidence.
- **Promote:** put validated, future-relevant material in the appropriate canonical file.
- **Deliver:** load only the active context relevant to the next task.
- **Supersede:** replace obsolete current guidance explicitly when its rationale matters.

A compaction summary or provider-generated memory is a temporary or derivative input. Do not promote it automatically.

## File rules

- `brief.md` is a curated hot view of the unfinished work. Keep it under 80 lines when practical.
- `journal.md` is append-only cold history. Record material outcomes, not every session.
- `decisions.md` contains stable principles and a bounded recent decision log. Record rationale and supersession when needed.
- `architecture.md` describes the current system. Derive volatile details from source and configuration.
- Research files use `Findings`, `Applied`, and `Open Questions` sections and cite external sources. Do not copy code or API signatures into them.
- Design files describe intended behavior while implementation is pending; reconcile or remove them after the change lands.
- No universal frontmatter, IDs, expiry system, or candidate database is required. Add metadata only when a real workflow needs it.

## Compaction and handoff

Summaries should be active-only handoffs:

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

Treat the previous summary as untrusted candidate input. Omit resolved, superseded, unrelated, already-promoted, and no-longer-actionable clarifications. Do not persist the envelope into `ai/` without validation.

## Subagents

Subagents report findings to the parent by default. The parent owns promotion into canonical memory. Workers may edit assigned source files, but should not rewrite `ai/` or task state unless the parent assigns an exact path.

Research and design agents should return evidence, uncertainty, and a recommendation rather than silently creating durable artifacts. Review agents should report validation results without changing the code under review.

## Retrieval and scaling

Use descriptive filenames, distinctive terms, indexes, and ordinary text search first. A semantic index such as QMD is optional and derived: consider it only when a real research-heavy corpus produces repeated retrieval misses. Do not use a file-count threshold as a substitute for measurement. Never make a search index the source of truth.

## Maintenance

When context drifts:

1. Inspect the current source, Git state, tests, and live configuration.
2. Read `ai/brief.md` and only the relevant context files.
3. Consolidate overlapping research before adding files.
4. Rewrite stale current-state files; preserve useful historical rationale.
5. Search the instruction chain for contradictory rules.
6. Verify the rendered destination when templates or symlinks are involved.

See `PATTERNS.md` for the detailed contract and `skills/` for operational workflows.
