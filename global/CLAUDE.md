# Agent Instructions

## Development

**Philosophy:** Do it right first—workarounds become permanent. Research → understand → plan → implement.

**Performance:** Idiomatic > clever. Profile before optimizing.

**Problem-solving:** Question assumptions. If something seems off, it probably is—stop and verify. If stuck, reframe the problem.

**Quality:**

- Research before implementing
- Fix root cause, not symptoms
- Read code before changing it
- Update docs (README, ai/, AGENTS.md)
- Ask before breaking APIs

**Errors:** Let errors propagate. Catch only to recover.

**Refactoring:** Clean breaks, not gradual migrations. When changing interfaces, signatures, or patterns:

- Replace completely in one commit—old code and all callers
- No version suffixes (V2, V3), no "old"/"legacy"/"new" markers
- No shims, adapters, or re-exports "for compatibility"
- No deprecation unless explicitly instructed
- If callers exist outside the repo, ask before breaking

**Corrections:** Update AGENTS.md when corrected—prevents repeat mistakes.

**Style:**

- **Naming:** Proportional to scope. Descriptive suffixes (`_batched`, `_async`) over version markers.
- **Comments:** Non-obvious context only. Never comment your edits. No TODOs.
- **Files:** Single concern. Tests separate.
- **No breadcrumbs:** When deleting/moving code, just remove it. No `// moved to X`, `// removed`, `// deprecated`.
- **Maintenance:** Fix what you touch. Technical debt compounds.

**Testing:** Unit or e2e only. No mocks—they invent behaviors. Flaky tests are bugs. Verify tests actually ran.

**Benchmarks:** Compare equivalent configs. Report config, dataset, environment, methodology.

## Workflow

**Stopping Points:** Proactively advise the user when to compact context or start a new session (e.g., after feature completion, major milestones, or significant context shifts).

**Git:** Commit after each fix, feature, or milestone. Push regularly. Confirm before PRs/publishing/force ops. No force push main. Messages: concise WHY.

**Releases:** NEVER trigger without explicit approval. Wait for CI.

**Versions:** Bump only when instructed. Sequential only (0.0.1 → 0.0.2).

## ai/ Directory

Persistent memory—survives compaction. Update BEFORE implementing.

| File         | Purpose                                                                                |
| ------------ | -------------------------------------------------------------------------------------- |
| STATUS.md    | Session state: current focus, external blockers, handoff notes. Pointers, not details. |
| DESIGN.md    | Architecture decisions and system design                                               |
| DECISIONS.md | Context → decision → rationale                                                         |
| ROADMAP.md   | Phases, milestones (situational—3+ phases or external deadlines)                       |

Root files read every session—keep minimal. Subdirs (research/, design/, review/, tmp/) on demand.

**Flow:** research/ → DESIGN.md → design/ → code → review/

**Format:** Tables/lists over prose. Answer first, evidence second.

**Project config:** AGENTS.md primary. Claude Code: `ln -s AGENTS.md CLAUDE.md`

## Task Tracking

Use `tk` for multi-step or cross-session work—persists across compaction.

- `tk add "title"` | `tk ls` | `tk ready` | `tk start <id>` | `tk done <id>`
- `tk show <id>` | `tk log <id> "msg"` | `tk block <id> <blocker>`

**Session start:** Read STATUS.md → `tk ready` → `tk start <id>`

**Before investigating:** `tk show <id>` for existing logs, check ai/, git history. Never start fresh without checking.

**During work:** `tk log <id> "finding"` immediately—errors, root cause, file paths. Update STATUS.md when focus shifts, blockers emerge, or significant progress is made.

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

**When to spawn:** Batch searches, large research → `researcher`. Significant changes → `reviewer`.

**Context handoff:** Curate relevant context, don't dump history. Objectives at END (recency bias).

## Context Management

**Prompt user to compact at:** Feature complete · Switching codebase areas · Research synthesized · ~100k tokens

**Before compact:** Update STATUS.md, mark completed tasks, log any uncommitted findings.

---

**Updated:** 2026-01-30 | github.com/nijaru/agent-contexts
