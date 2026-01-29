# Agent Instructions

## Development

**Philosophy:** Do it right first—workarounds become permanent. Research → understand → plan → implement.

**Problem-solving:** Question assumptions. If something seems off, it probably is—stop and verify. If stuck, reframe the problem.

**Quality:** Research first · Fix root cause · Production-ready (errors, logging, validation) · Read before changing · Update docs · Ask before breaking APIs

**Corrections:** Update AGENTS.md when corrected on non-obvious project patterns—prevents repeat mistakes.

**Style:**

- **Naming:** Proportional to scope. No `_v2`/`_new`—use `_batched`, `_async`.
- **Comments:** Non-obvious context only. Never comment your edits. No TODOs.
- **Files:** Single concern. Tests separate.
- **No breadcrumbs:** When deleting/moving code, just remove it. No `// moved to X`, `// removed`, `// deprecated`.

**Testing:** Unit or e2e only. No mocks—they invent behaviors that hide real bugs.

## Workflow

**Git:** Proactively commit after completing logical units of work—don't wait to be asked. Push regularly. Confirm before PRs/publishing/force ops. No force push main. Messages: concise WHY.

**Releases:** NEVER trigger without explicit approval. Wait for CI.

**Versions:** Bump only when instructed. Sequential only (0.0.1 → 0.0.2).

## ai/ Directory

Persistent memory—survives compaction. Update BEFORE implementing.

| File         | Purpose                                                                                |
| ------------ | -------------------------------------------------------------------------------------- |
| STATUS.md    | Session state: current focus, external blockers, handoff notes. Pointers, not details. |
| DESIGN.md    | Architecture decisions and system design                                               |
| DECISIONS.md | Context → decision → rationale                                                         |

Root files read every session—keep minimal. Subdirs (research/, design/, review/, tmp/) on demand.

**Flow:** research/ → DESIGN.md → design/ → code → review/

**Format:** Tables/lists over prose. Answer first, evidence second.

**Project config:** AGENTS.md primary. Claude Code: `ln -s ../AGENTS.md .claude/CLAUDE.md`

## Task Discipline

Use `tk` for all tasks—persists across compaction. Details in task logs, not STATUS.md.

**Session start:** Read STATUS.md → `tk ready` → `tk start <id>`

**Before investigating:** `tk show <id>` for existing logs, check ai/, git history. Never start fresh without checking.

**During work:** `tk log <id> "finding"` immediately—errors, root cause, file paths.

**Creating tasks:** `tk add "title" -d "context"`. Always include description.

**Completion:** `tk start` when beginning, `tk done` when complete. Stale status causes confusion.

## Subagents

For context isolation, parallelism, fresh perspective. ai/ files are shared memory.

| Agent        | Purpose                          | Persists to  |
| ------------ | -------------------------------- | ------------ |
| `researcher` | External knowledge, synthesis    | ai/research/ |
| `designer`   | Architecture, planning           | ai/design/   |
| `developer`  | Well-scoped implementation       | —            |
| `reviewer`   | Full validation (build/run/test) | ai/review/   |
| `profiler`   | Deep performance analysis        | ai/review/   |

**Context handoff:** Curate relevant context, don't dump history. Put objectives at END (recency bias).

## Context Management

**Prompt user to compact at:** Feature complete · Switching codebase areas · Research synthesized · ~100k tokens

**Before compact:** Update STATUS.md, `tk done` completed tasks, `tk log` any uncommitted findings.

---

**Updated:** 2026-01-29 | github.com/nijaru/agent-contexts
