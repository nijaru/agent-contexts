# AI Agent Instructions

## Task Tracking (Beads)

**Use `bd` for task management.** Dependency graphs + multi-session memory. Fallback: ai/TODO.md.

| Phase | Commands |
|-------|----------|
| Start | `bd ready` (unblocked) ・ `bd list --status open` |
| Work | `bd create "desc" -t task -p 2` ・ `bd dep add X blocks Y` ・ `bd update X --status in-progress` |
| End | `bd close X` ・ `bd sync` ・ Provide: "Continue bd-xxxx: [context]" |

**Reference:** `bd show X` (details) ・ `bd tree X` (deps) ・ `bd list` (all)

## ai/ Directory

**Purpose:** AI session context - track state/decisions/research across sessions.

**Core Principle:** Session files (ai/ root) read EVERY session - keep minimal (<500 lines each). Reference files (subdirs) read ON DEMAND - zero token cost unless accessed.

### Files

| File | When | Purpose | Format |
|------|------|---------|--------|
| STATUS.md | ✅ Always | Current state, blockers (read FIRST) | Tables for metrics, bullets for learnings |
| TODO.md | ⚠️ If no beads | Active tasks with dependencies | Checkboxes, deps inline, ready section first |
| DECISIONS.md | ✅ Recommended | Architectural decisions | Context → Decision → Rationale → Tradeoffs (table) |
| RESEARCH.md | ⚠️ If needed | Research index (summaries + pointers) | Topic → Finding → Link to details |
| KNOWLEDGE.md | ⚠️ If quirks | Permanent codebase quirks/gotchas | Table: Area → Knowledge → Impact → Discovered |
| PLAN.md | ⚠️ Optional | Strategic roadmap (ONLY if 3+ phases) | Tables: phases, dependencies, NO time estimates |

### Subdirectories

Create only when needed:

| Directory | When to Create | Contents |
|-----------|----------------|----------|
| research/ | Research becomes detailed OR multiple topics | Detailed research (exec summary if lengthy) |
| design/ | Formal specs needed (API, architecture) | Design specs (delete after implemented) |
| decisions/ | DECISIONS.md hard to navigate OR many superseded | Superseded/topic-split decisions |
| tmp/ | Always (with `echo '*' > ai/tmp/.gitignore`) | Temporary artifacts (never commit) |

### Workflow

**Start:** Read STATUS.md → `bd ready` (or TODO.md) → AGENTS.md
**During:** File issues with `bd create`, document decisions, research in research/ if detailed
**End:** Update STATUS.md → `bd sync` (or update TODO.md) → Prune if needed

### Format Rules

**ALL ai/ files:** Tables/lists/structured, NOT prose. Answer first, evidence second.

❌ "After investigating caching, the team feels Redis would be good..."
✅ `**Decision**: Redis | **Why**: 10x faster, persistence | **Tradeoff**: Service dependency`

### Maintenance

**Prune when accumulating historical/completed content:**

| File | Delete |
|------|--------|
| STATUS.md | Old pivots, completed phases, resolved blockers |
| TODO.md | Completed tasks (no "Done" section) |
| DECISIONS.md | Move superseded → ai/decisions/superseded-YYYY-MM.md |
| RESEARCH.md | Move details → research/, keep index only |
| research/*.md, design/*.md | Delete when no longer relevant |

**Promote learnings:** Permanent rule → AGENTS.md | Permanent quirk → KNOWLEDGE.md | Transient → Delete

### TODO.md Format (fallback when no beads)

- **Sections:** `## Ready` (no blockers) first, `## Blocked` second
- **Dependencies:** `(after: x, y)` or `(blocks: x, y)` inline
- **IDs:** Optional `[a3f8]` prefix for complex projects
- Delete completed tasks immediately

### Scaling

Start minimal, grow as needed:
- **Minimal:** STATUS.md + beads (or TODO.md)
- **Standard:** Add DECISIONS.md + RESEARCH.md
- **Complex:** Add PLAN.md + research/ + design/

### AGENTS.md

**AGENTS.md = primary, CLAUDE.md → AGENTS.md = symlink**

**Belongs:** Build/test/deploy commands, coding standards, architecture, tech stack, verification steps, concrete code examples
**Doesn't belong:** Current issues (STATUS.md), learnings (STATUS.md), tactical roadmap (PLAN.md), detailed research (ai/research/)

Reference: github.com/nijaru/agent-contexts

## Workflow Rules

### Git
- Commit frequently, push regularly (no ask)
- **ASK before:** PRs, publishing packages, force ops, resource deletion
- Never force push to main/master
- Commit messages: Concise, focus on WHY not WHAT

### Files
- Delete directly (no archiving)
- `/tmp`: ephemeral only (delete after use)
- `ai/tmp/`: gitignored temporary artifacts

### Long-running Commands
- Avoid rapid polling on background tasks; scale wait time with expected duration

## Development

**Philosophy:** Do it right the first time. Research → understand → plan → implement.

### Code Quality

1. Research best practices first (state of the art)
2. Fix root cause, no workarounds
3. Production-ready: error handling, logging, validation
4. Follow existing patterns (read code before changing)
5. Update docs: README, docs/, ai/, AGENTS.md
6. Ask before breaking existing code/APIs

**NEVER propose changes to code you haven't read.**

### Testing & TDD

**Workflow:** Plan → Red → Green → Refactor → Validate

| Use TDD | Skip |
|---------|------|
| Systems (DBs, compilers), Performance (SIMD, algorithms), Complex logic | Docs, configs, typos, prototypes, simple scripts |

**Rules:** Declare upfront, commit tests before coding, don't modify during implementation

### Code Style

**Naming:** Concise, context-aware, proportional to scope
- Local: `count` | Package: `userCount`
- Omit redundant context: `Cache` not `LRUCache_V2`
- Booleans: `isEnabled` | Constants: `MAX_RETRIES` | Units: `timeoutMs`

**Comments:** Only WHY, never WHAT. No change tracking, TODOs, or obvious behavior.

## Git & Releases

**Versioning:**
- Use commit hashes for references
- Bump only when instructed
- Sequential: 0.0.1 → 0.0.2 → 0.1.0 → 1.0.0 (not 0.0.1 → 1.0.0)
- Semantics: 0.0.x = unstable | 0.1.0+ = production ready | 1.0.0 = proven in production

**Release:** (wait for CI)
1. Bump version, update docs → commit → push
2. `gh run watch` (wait for pass)
3. `git tag -a vX.Y.Z -m "Description" && git push --tags`
4. `gh release create vX.Y.Z --notes-file release_notes.md`
5. **ASK before publishing** (can't unpublish)

---

**Version:** 2025-11 | **Reference:** github.com/nijaru/agent-contexts | github.com/steveyegge/beads
