# Agent Instructions

## Development

**Philosophy:** Do it right first—workarounds become permanent. Fix what you touch. Research → understand → plan → implement.

**Design:** Clear > clever. Hard to explain = wrong abstraction. Small interfaces. A little copying over a little dependency.

**Functional core, imperative shell:** Pure logic at the center; push side effects (IO, state, randomness) to the edges.

**Performance:** Profile before optimizing.

**Problem-solving:** Reproduce before fixing. Question assumptions. If something seems off, it probably is—stop and verify. If stuck, reframe the problem.

**Quality:**

- Fix root cause, not symptoms
- Read code before changing it
- Update docs—record corrections in AGENTS.md to prevent repeats
- Ask before breaking APIs

**Errors:** Let errors propagate. Catch only to recover.

**Refactoring:** Clean breaks, not gradual migrations. When changing interfaces, signatures, or patterns:

- Replace completely in one commit—old code and all callers
- No version suffixes (V2, V3), no "old"/"legacy"/"new" markers
- No shims, adapters, or re-exports "for compatibility"
- No breadcrumbs: no `// moved to X`, `// removed`, `// deprecated` comments. Just delete.
- No deprecation unless explicitly instructed. If callers exist outside the repo, ask first.

**Review:** `/review` before major commits.

**Style:**

- **Naming:** Proportional to scope. Descriptive suffixes (`_batched`, `_async`) over version markers.
- **Comments:** Why, not what—only when non-obvious from code. Never narrate changes. No TODOs. No commented-out code.
- **Files:** Single concern. Tests separate.

**Testing:** Unit or e2e only. No mocks—they invent behaviors. Test failure paths, not just happy paths. Flaky tests are bugs. Verify tests actually ran.

**Benchmarks:** Compare equivalent configs. Report config, dataset, environment, methodology.

## Workflow

**Git:** Just commit—don't ask permission. Commit often. One logical change = one commit (function + callers, feature + tests). Don't split cohesive changes across commits or bundle unrelated ones. Push regularly. Only confirm before: PRs, publishing, force push, destructive ops. No force push main. Messages: concise WHY.

**Releases:** NEVER trigger without explicit approval. Wait for CI.

**Versions:** Bump only when instructed. Sequential only (0.0.1 → 0.0.2).

## ai/ Directory

Persistent memory — survives compaction. Update before implementing. Stale files mislead — update or delete.

### Structure

```
ai/
├── README.md        # Index: pointers to all topic files (~150 chars/entry, no content)
├── STATUS.md        # Phase, focus, blockers — updated every session
├── DESIGN.md        # Current architecture — answers "what is it?"
├── DECISIONS.md     # Why decisions were made — Principles + Log sections
├── PLAN.md          # Active plan. Simple: flat doc. Complex: sprint index (managed by /sprint)
├── research/        # Investigation docs
├── design/          # Detailed design docs
├── review/          # Review outputs
├── sprints/         # Sprint detail files (NN-name.md) — created by /sprint
└── tmp/             # Scratch (gitignored)
```

### Session Start

Read `ai/README.md` → `ai/STATUS.md` → load relevant topic files for current task. Only load what the task requires.

### File Roles

| File         | Purpose                                                                                                                                         | Update Rule                                                                                                 |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| README.md    | Index only — pointers, ~150 chars/entry. No content.                                                                                            | Update when topic files are added/changed. Verify links are live. Remove dead links.                        |
| STATUS.md    | Phase, active focus, blockers.                                                                                                                  | Every session.                                                                                              |
| DESIGN.md    | Current architecture — answers "what is it?"                                                                                                    | When architecture changes.                                                                                  |
| DECISIONS.md | Why it is that way. Two sections: **Principles** (distilled, stable) + **Log** (recent ~20 entries verbatim, `Context → Decision → Rationale`). | Append to Log. When Log > ~20 entries, run `/setup-ai` to compact into Principles.                          |
| PLAN.md      | Active plan. Simple: flat document. Complex: sprint index table with detail files in `ai/sprints/` (managed by `/sprint`).                      | Update as sprints progress. When plan is complete, extract outcomes to DECISIONS.md/DESIGN.md then replace. |

### Index Discipline

README.md is pointers only. Format: `- [Title](path) — one-line hook`

- Write to file → update README.md immediately. Index must stay synchronized.
- Don't persist derivable facts — if it's grep-able from code or git history, don't write it to ai/.
- ai/ is hints, not truth — verify against code when it matters.

### Topic File Frontmatter

All files in `research/`, `design/`, `review/` must start with:

```yaml
---
date: YYYY-MM-DD
summary: one-line description
status: active | resolved | stale
---
```

### Consolidation Rules

- Merge before multiplying — one focused file beats three overlapping ones.
- Delete resolved files — don't mark done, delete.
- When ai/ is out of sync or bloated, run `/setup-ai` to audit, consolidate, and rebuild the index.

**Flow:** `research/` → `DESIGN.md` → `/sprint` → `PLAN.md` → code → `review/`

**Format:** Tables/lists over prose. Answer first, evidence second.

**Project config:** AGENTS.md primary. Claude Code: `ln -s ../AGENTS.md .claude/CLAUDE.md`

## Task Discipline

Use `tk` for all tasks—persists across compaction. Details in task logs, not STATUS.md.

**Session start:** Read `ai/README.md` → `ai/STATUS.md` → `tk ready` → `tk start <id>`

**Before investigating:** `tk show <id>` for existing logs, check ai/, git history. Never start fresh without checking.

**During work:** `tk log <id> "finding"` immediately—errors, root cause, file paths. Update `ai/STATUS.md` when focus shifts, blockers emerge, or significant progress is made.

**Creating tasks:** `tk add "title" -d "context"`. Always include description.

**Completion:** `tk start` when beginning, `tk done` when complete. Stale status causes confusion.

## Subagents

For context isolation, parallelism, fresh perspective. ai/ files are shared memory.

| Agent        | Purpose                          | Persists to  |
| ------------ | -------------------------------- | ------------ |
| `researcher` | External knowledge, synthesis    | ai/research/ |
| `designer`   | Architecture, planning           | ai/design/   |
| `reviewer`   | Full validation (build/run/test) | ai/review/   |
| `profiler`   | Deep performance analysis        | ai/review/   |

**When to spawn:** Batch searches, large research → `researcher`. Significant changes → `reviewer`.

**Teams vs subagents:** Teams for coordinated parallel work with shared task lists. Subagents for isolated one-off tasks.

**Before spawning:** Run build/test/lint once in the parent, include output in agent context.

**Avoid parallel agents when:**

- Results depend on each other (sequential by nature)
- One agent covers the scope—don't split reviewers across the same files
- The approach is unvalidated—confirm it works before parallelizing

**Context handoff:** Curate relevant context, don't dump history. Objectives at END (recency bias).

## Context Management

**Compact/new session at:** Feature complete · Switching codebase areas · Research synthesized · ~150k tokens. Proactively advise the user.

**Before compact:** Update `ai/STATUS.md` and `ai/README.md` (index), `tk done` completed tasks, `tk log` any uncommitted findings.

---

**Updated:** 2026-04-04 | github.com/nijaru/agent-contexts
