# AI Agent Patterns

Organization patterns for AI coding agents. **Teaches organization, not coding.**

## Core Concept

**ai/** is the agent's workspace for cross-session context. Not for human docs (that's docs/).

**Token efficiency:** Root files (ai/ root) load every session — keep minimal. Subdirs load on demand.

## Directory Structure

```
project/
├── AGENTS.md              # Project config (AI entry point)
├── CLAUDE.md → AGENTS.md  # Symlink for Claude Code
├── docs/                  # Human documentation
└── ai/                    # AI context
    ├── brief.md           # Current state, <80 lines (always)
    ├── journal.md         # Append-only session log
    ├── architecture.md    # Architecture (recommended)
    ├── decisions.md       # Decision log — Principles + Log sections (recommended)
    ├── PLAN.md            # Active plan or sprint index (situational)
    ├── research/          # External research findings
    ├── design/            # Component specifications
    ├── review/            # Review findings
    └── tmp/               # Temporary artifacts (gitignored)
```

## Task Tracking

Use `tk` for multi-step or cross-session work — persists across compaction.

- `tk add "title"` | `tk ls` | `tk ready` | `tk start <id>` | `tk done <id>`

**Todos/tasks go in tk, not brief.md.** brief.md is for session state and blockers.

## ai/ Files

| File            | Question                    | Create When                       |
| --------------- | --------------------------- | --------------------------------- |
| brief.md        | Where are we now?           | Always — <80 lines, active state  |
| journal.md      | What happened each session? | Always — append-only log          |
| architecture.md | What are we building?       | Non-trivial projects              |
| decisions.md    | Why did we choose X?        | Architectural decisions made      |
| PLAN.md         | What's the plan?            | Use `/sprint` when spec is ready  |

| Subdir    | Purpose                    | When                 |
| --------- | -------------------------- | -------------------- |
| research/ | External research findings | Substantial research |
| design/   | Component specifications   | Complex components   |
| review/   | Review findings            | Significant reviews  |
| tmp/      | Temporary artifacts        | Always (gitignored)  |

## File Content

**brief.md:** Current state — task, state, files, blockers, next step. Regenerate from journal + decisions. Keep <80 lines, active context only.

**journal.md:** Append-only session log. Format: `- [YYYY-MM-DD] Action/Decision/Learning`. Append every session.

**architecture.md:** System overview, architecture, components table. Point to design/ for details.

**decisions.md:** Two sections:

- **Principles** — distilled stable decisions, load-bearing context
- **Log** — recent ~20 entries verbatim: `[date] Context → Decision → Rationale`

When Log > ~20 entries, distill oldest into Principles and remove from Log.

**PLAN.md:** Active plan. Simple: flat document. Complex: sprint index table with detail files in `ai/sprints/` (managed by `/sprint`). Replace when complete — extract outcomes to decisions.md/architecture.md first.

## Topic File Frontmatter

All files in `research/`, `design/`, `review/` must start with:

```yaml
---
date: YYYY-MM-DD
summary: one-line description
status: active | resolved | stale
---
```

## Single Source of Truth

| Info            | Lives in        | Not in        |
| --------------- | --------------- | ------------- |
| Current state   | brief.md        | anywhere else |
| Session history | journal.md      | anywhere else |
| Architecture    | architecture.md | AGENTS.md     |
| Component specs | design/         | architecture.md |
| Decisions       | decisions.md    | scattered     |
| Research        | research/       | inline        |
| Tasks           | .tasks/ (tk)    | brief.md      |

## Session Workflow

| Phase  | Actions                                                                         |
| ------ | ------------------------------------------------------------------------------- |
| Start  | Read `ai/brief.md` → `tk ready` → `tk start <id>`                               |
| During | Research → synthesize → implement → document decisions                          |
| End    | `tk done <id>` → update brief.md → append journal.md → `/save`                  |

## Project AGENTS.md

Machine-optimized (tables/lists). Include: project overview, structure, stack, commands, verification steps, standards, examples.

Point to ai/ for current state: "See `ai/brief.md` for current state."

## Scaling

| Size     | Session Files                           | Subdirs              |
| -------- | --------------------------------------- | -------------------- |
| Minimal  | brief.md, journal.md                    | tmp/                 |
| Standard | +architecture.md, +decisions.md         | +research/, +design/ |
| Complex  | +PLAN.md (sprint index via `/sprint`)   | +review/             |

Start minimal, add as needed.

## Key Rules

- **Don't persist derivable facts** — if grep-able from code or git history, don't write it to ai/.
- **Merge before multiplying** — one focused file beats three overlapping ones.
- **Delete resolved, don't mark done** — stale context causes hallucinations.
- **ai/ is hints, not truth** — verify against code when it matters.
- **When ai/ is out of sync**, run `/setup-ai` to audit, consolidate, and rebuild the index.

## Anti-Patterns

| Don't                         | Do Instead                                  |
| ----------------------------- | ------------------------------------------- |
| All research in session files | Use research/ for details                   |
| Component specs in architecture.md | architecture.md = system, design/ = components |
| Keep stale topic files        | Delete resolved files, don't archive        |
| Prose in ai/ files            | Tables, lists, structured                   |
| Duplicate across files        | Single source of truth                      |
| Store what's in the codebase  | Don't persist derivable facts               |

## Maintenance

Trust git history. Prune session files when they accumulate historical content. Topic files: delete when resolved. Run `/setup-ai` to audit and consolidate when ai/ feels out of sync.
