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
    ├── README.md          # Index: pointers to all topic files (~150 chars/entry, no content)
    ├── STATUS.md          # Phase, focus, blockers (always)
    ├── DESIGN.md          # Architecture (recommended)
    ├── DECISIONS.md       # Decision log — Principles + Log sections (recommended)
    ├── PLAN.md            # Active plan or sprint index (situational)
    ├── research/          # External research findings
    ├── design/            # Component specifications
    ├── review/            # Review findings
    ├── sprints/           # Sprint detail files (NN-name.md) — created by /sprint
    └── tmp/               # Temporary artifacts (gitignored)
```

## Task Tracking

Use `tk` for multi-step or cross-session work — persists across compaction.

- `tk add "title"` | `tk ls` | `tk ready` | `tk start <id>` | `tk done <id>`

**Todos/tasks go in tk, not STATUS.md.** STATUS.md is for session state and blockers.

## ai/ Files

| File         | Question              | Create When                       |
| ------------ | --------------------- | --------------------------------- |
| README.md    | Where is everything?  | Always — index of all topic files |
| STATUS.md    | Where are we now?     | Always                            |
| DESIGN.md    | What are we building? | Non-trivial projects              |
| DECISIONS.md | Why did we choose X?  | Architectural decisions made      |
| PLAN.md      | What's the plan?      | Use `/sprint` when spec is ready  |

| Subdir    | Purpose                    | When                 |
| --------- | -------------------------- | -------------------- |
| research/ | External research findings | Substantial research |
| design/   | Component specifications   | Complex components   |
| review/   | Review findings            | Significant reviews  |
| sprints/  | Sprint detail files        | When using /sprint   |
| tmp/      | Temporary artifacts        | Always (gitignored)  |

## File Content

**README.md:** Index only — pointers, ~150 chars/entry. Format: `- [Title](path) — one-line hook`. No content. Write to file → update README.md immediately.

**STATUS.md:** Phase, active focus, blockers. Update every session. Keep minimal.

**DESIGN.md:** System overview, architecture, components table. Point to design/ for details.

**DECISIONS.md:** Two sections:

- **Principles** — distilled stable decisions, load-bearing context
- **Log** — recent ~20 entries verbatim: `[date] Context → Decision → Rationale`

When Log > ~20 entries, distill oldest into Principles and remove from Log.

**PLAN.md:** Active plan. Simple: flat document. Complex: sprint index table with detail files in `ai/sprints/` (managed by `/sprint`). Replace when complete — extract outcomes to DECISIONS.md/DESIGN.md first.

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

| Info            | Lives in     | Not in        |
| --------------- | ------------ | ------------- |
| Navigation      | README.md    | anywhere else |
| Current state   | STATUS.md    | anywhere else |
| Architecture    | DESIGN.md    | AGENTS.md     |
| Component specs | design/      | DESIGN.md     |
| Decisions       | DECISIONS.md | scattered     |
| Research        | research/    | inline        |
| Tasks           | .tasks/ (tk) | STATUS.md     |

## Session Workflow

| Phase  | Actions                                                                         |
| ------ | ------------------------------------------------------------------------------- |
| Start  | Read `ai/README.md` → `ai/STATUS.md` → `tk ready` → `tk start <id>`             |
| During | Research → synthesize → implement → document decisions → update README.md index |
| End    | `tk done <id>` → update STATUS.md → update README.md if files changed → `/save` |

## Project AGENTS.md

Machine-optimized (tables/lists). Include: project overview, structure, stack, commands, verification steps, standards, examples.

Point to ai/ for current state: "See `ai/README.md` for index, `ai/STATUS.md` for current state."

## Scaling

| Size     | Session Files                         | Subdirs              |
| -------- | ------------------------------------- | -------------------- |
| Minimal  | README.md, STATUS.md                  | tmp/                 |
| Standard | +DESIGN.md, +DECISIONS.md             | +research/, +design/ |
| Complex  | +PLAN.md (sprint index via `/sprint`) | +review/, +sprints/  |

Start minimal, add as needed.

## Key Rules

- **Don't persist derivable facts** — if grep-able from code or git history, don't write it to ai/.
- **Merge before multiplying** — one focused file beats three overlapping ones.
- **Delete resolved, don't mark done** — stale context causes hallucinations.
- **ai/ is hints, not truth** — verify against code when it matters.
- **When ai/ is out of sync**, run `/setup-ai` to audit, consolidate, and rebuild the index.

## Anti-Patterns

| Don't                         | Do Instead                               |
| ----------------------------- | ---------------------------------------- |
| All research in session files | Use research/ for details                |
| Component specs in DESIGN.md  | DESIGN.md = system, design/ = components |
| Content in README.md          | README.md = pointers only                |
| Keep stale topic files        | Delete resolved files, don't archive     |
| Prose in ai/ files            | Tables, lists, structured                |
| Duplicate across files        | Single source of truth                   |
| Store what's in the codebase  | Don't persist derivable facts            |

## Maintenance

Trust git history. Prune session files when they accumulate historical content. Topic files: delete when resolved. Run `/setup-ai` to audit and consolidate when ai/ feels out of sync.
