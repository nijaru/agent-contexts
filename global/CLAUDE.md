## Task Tracking (Beads)

**Use `bd` for task management.** Dependency graphs + multi-session memory. Fallback: ai/TODO.md.

| Phase | Commands |
|-------|----------|
| Start | `bd ready` (unblocked) ・ `bd list --status open` |
| Work | `bd create "title" -t task -p 2` ・ `bd update X --status in-progress` |
| Depend | `bd dep add <task> <blocker>` (task depends on blocker) |
| End | `bd close X` ・ `bd sync` ・ Provide: "Continue bd-xxxx: [context]" |

**Reference:** `bd show X` (details) ・ `bd dep tree X` (deps) ・ `bd list` (all)

## ai/ Directory

Cross-session project context. Root files read every session—keep minimal. Subdirs read on demand.

| File | When | Purpose |
|------|------|---------|
| STATUS.md | **Always** | Current state, blockers (read FIRST) |
| DESIGN.md | **Recommended** | System architecture, components |
| DECISIONS.md | **Recommended** | Decisions: Context → Decision → Rationale |
| ROADMAP.md | Situational | Phases, milestones (multi-phase only) |
| TODO.md | Situational | Tasks (if no beads) |

**Subdirs:** Create when needed—research/, design/, tmp/ (gitignored)

**Workflow:** research/ (inputs) → DESIGN.md (synthesis) → design/ (component specs) → code

**Format:** Tables/lists, not prose. Answer first, evidence second.
- ❌ "After investigating, the team feels Redis would be good..."
- ✅ `**Decision**: Redis | **Why**: 10x faster | **Tradeoff**: dependency`

**Maintenance:** Prune completed/resolved content. Promote: permanent rules → AGENTS.md.

**Project config:** AGENTS.md as primary. For Claude Code: `ln -s AGENTS.md CLAUDE.md`

---

**Reference:** github.com/nijaru/agent-contexts | github.com/steveyegge/beads
