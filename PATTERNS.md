# AI Agent Patterns

Organization patterns for AI coding agents. **Teaches organization, not coding.**

## Core Concept

**ai/** is the agent's workspace for cross-session context. Not for human docs (that's docs/).

**Token efficiency:** Session files (ai/ root) load every session—keep minimal. Subdirs load on demand.

## Directory Structure

```
project/
├── AGENTS.md              # Project config (AI entry point)
├── CLAUDE.md → AGENTS.md  # Symlink for Claude Code
├── docs/                  # Human documentation
└── ai/                    # AI context
    ├── STATUS.md          # Current state (always)
    ├── DESIGN.md          # Architecture (recommended)
    ├── DECISIONS.md       # Decision log (recommended)
    ├── ROADMAP.md         # Phases (situational)
    ├── research/          # External research
    ├── design/            # Component specs
    ├── review/            # Review findings
    └── tmp/               # Temporary (gitignored)
```

## Task Tracking

Use `tk` for multi-step or cross-session work—persists across compaction.

- `tk add "title"` | `tk ls` | `tk ready` | `tk start <id>` | `tk done <id>`

**Todos/tasks go in tk, not STATUS.md.** STATUS.md is for session state, blockers, notes.

## ai/ Files

| File         | Question              | Create When                     |
| ------------ | --------------------- | ------------------------------- |
| STATUS.md    | Where are we?         | Always                          |
| DESIGN.md    | What are we building? | Non-trivial projects            |
| DECISIONS.md | Why did we choose X?  | Architectural decisions made    |
| ROADMAP.md   | What's the plan?      | 3+ phases or external deadlines |

| Subdir    | Purpose                    | When                 |
| --------- | -------------------------- | -------------------- |
| research/ | External research findings | Substantial research |
| design/   | Component specifications   | Complex components   |
| review/   | Review findings            | Significant reviews  |
| tmp/      | Temporary artifacts        | Always (gitignored)  |

## File Content

**STATUS.md:** Current metrics, what worked/didn't, active work, blockers. Update every session.

**DESIGN.md:** System overview, architecture diagram, components table, data flow. Point to design/ for details.

**DECISIONS.md:** Append-only. Date, context, decision, rationale, tradeoffs.

**ROADMAP.md:** Phases table, dependencies, out-of-scope. No time estimates.

## Single Source of Truth

| Info            | Lives in     | Not in        |
| --------------- | ------------ | ------------- |
| Current state   | STATUS.md    | anywhere else |
| Architecture    | DESIGN.md    | AGENTS.md     |
| Component specs | design/      | DESIGN.md     |
| Decisions       | DECISIONS.md | scattered     |
| Research        | research/    | inline        |
| Tasks           | .tasks/ (tk) | STATUS.md     |

## Session Workflow

| Phase  | Actions                                                      |
| ------ | ------------------------------------------------------------ |
| Start  | Read STATUS.md → `tk ready` → `tk start <id>` → load context |
| During | Research → synthesize → implement → document decisions       |
| End    | `tk done <id>` → update STATUS.md if blockers → prune        |

## Project AGENTS.md

Machine-optimized (tables/lists). Include: project overview, structure, stack, commands, verification steps, standards, examples.

Point to ai/ for current state: "See ai/STATUS.md for current state, ai/DESIGN.md for architecture"

## Scaling

| Size     | Session Files             | Subdirs              |
| -------- | ------------------------- | -------------------- |
| Minimal  | STATUS.md                 | tmp/                 |
| Standard | +DESIGN.md, +DECISIONS.md | +research/, +design/ |
| Complex  | +ROADMAP.md               | +review/             |

Start minimal, add as needed.

## Anti-Patterns

| Don't                         | Do Instead                               |
| ----------------------------- | ---------------------------------------- |
| All research in session files | Use research/ for details                |
| Component specs in DESIGN.md  | DESIGN.md = system, design/ = components |
| Create full structure day 1   | Start minimal, grow as needed            |
| Human docs in ai/             | docs/ for humans, ai/ for AI             |
| Prose in ai/ files            | Tables, lists, structured                |
| Duplicate across files        | Single source of truth                   |

## Maintenance

Trust git history. Prune session files when they accumulate historical content. Reference files: delete when obsolete (don't prune).
