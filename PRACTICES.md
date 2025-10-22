# AI Agent Practices

*Essential patterns for organizing AI agent work across all projects*

## Core Principle

**This guide teaches ORGANIZATION, not CODING.** AI agents already know how to code. What they need is a standardized way to organize their work, track progress, and maintain context across sessions.

## Standard Directory Structure

Every project should follow this structure:

```
YOUR_PROJECT/
├── AGENTS.md                    # AI entry point (or CLAUDE.md)
├── docs/                        # Permanent documentation (human-facing)
│   ├── adr/                    # Architecture Decision Records (optional)
│   ├── api/                    # API reference
│   ├── guides/                 # Tutorials, how-tos
│   └── architecture/           # System design, technical specs
├── ai/                          # AI working context (evolving)
│   ├── TODO.md                 # Active tasks
│   ├── STATUS.md               # Current state
│   ├── DECISIONS.md            # Working decision log
│   ├── RESEARCH.md             # Research index
│   └── research/               # AI's research findings
│       ├── {topic}.md          # e.g., indexing-algorithms.md
│       └── archive/            # Old research
└── .github/                     # Platform-specific (optional)
    └── workflows/
```

**Key Principles:**
- **docs/** — Permanent, human-facing documentation (committed, versioned)
- **ai/** — Evolving, AI-optimized working context (committed, but changes frequently)
- **Start minimal** — New projects just need `docs/` + `ai/`. Add subdirs as needed.
- **Respect existing** — If project has `internal/`, `wiki/`, etc., note in AGENTS.md and use them.

## File Purposes and Update Modes

### TODO.md (Edit in place)
**Purpose**: Track active tasks and priorities
**Update**: Edit in place - remove completed, add new
```markdown
## High Priority
- [ ] Task with specific success criteria
- [ ] Blocking issue

## In Progress
- [ ] Feature being developed
  - [x] Subtask completed

## Backlog
- [ ] Future improvements
```

### STATUS.md (Edit in place)
**Purpose**: Current project state and what worked/didn't
**Update**: Edit in place - represents current truth
```markdown
## Current State
- Performance: 1,234 req/s (measured 2025-01-15)
- Test Coverage: 87%
- Build: Passing

## What Worked
- Approach X improved performance by 40%
- Pattern Y solved concurrency issue

## What Didn't Work
- Tried Z but failed because [reason]

## Active Work
Currently implementing [feature]

## Blockers
- [Issue] blocking [what]
```

### DECISIONS.md (Append-only)
**Purpose**: Record architectural decisions with rationale
**Update**: Append only - never delete past decisions
```markdown
## 2025-01-15: Choose PostgreSQL over MongoDB
**Context**: Selecting primary database
**Decision**: PostgreSQL
**Rationale**:
- Strong consistency requirements
- Complex relational queries needed
- Team expertise with SQL
**Tradeoffs**: Horizontal scaling more complex
---
```

### RESEARCH.md (Hybrid)
**Purpose**: Index external research findings
**Update**: Update summaries, append new research
```markdown
## Database Indexing (researched 2025-01-15)
**Sources**: [links to papers/articles]
**Key Finding**: LSM trees better for write-heavy workloads
**Relevance**: Our use case is 80% writes
**Decision**: Implement LSM-based index
→ Details: ai/research/indexing-algorithms.md

## Open Questions
- [ ] Optimal cache eviction strategy
- [ ] WebSocket vs SSE comparison needed
```

## Directory Organization

### docs/ — Permanent Documentation
**What belongs here:**
- User guides, API documentation, tutorials
- Architecture documentation (`docs/architecture/`)
- Architecture Decision Records (`docs/adr/`) — optional, for formal projects
- Requirements, specifications
- Team processes, onboarding guides

**Update pattern:** Versioned, permanent. Changes are deliberate.

**Examples:**
- `docs/api/authentication.md` — API reference
- `docs/guides/quickstart.md` — Getting started guide
- `docs/adr/0001-use-postgresql.md` — Formal architectural decision
- `docs/architecture/system-overview.md` — System design

### ai/ — AI Working Context
**What belongs here:**
- TODO.md — Current tasks, sprint planning
- STATUS.md — Project health, what worked/didn't
- DECISIONS.md — Working decision log during development
- RESEARCH.md — Index of AI's web research
- research/{topic}.md — Technical deep-dives from research

**Update pattern:** Evolving, frequent changes. Optimized for AI context.

**Examples:**
- `ai/research/indexing-algorithms.md` — AI researched LSM vs B-tree
- `ai/research/caching-strategies.md` — Redis vs Memcached comparison
- `ai/DECISIONS.md` — "Tried approach X, didn't work because Y"

### Decision Flow (Knowledge Graduation)
```
Active work → ai/TODO.md
           ↓ (completed)
         ai/STATUS.md (what worked/didn't)
           ↓ (if important decision)
         ai/DECISIONS.md (working log)
           ↓ (if architectural/formal)
         docs/adr/NNNN-title.md (formal ADR)

Research → ai/research/{topic}.md
        ↓ (if valuable/permanent)
      docs/architecture/ or code comments
        ↓ (if outdated)
      ai/research/archive/
```

### Optional Directories
**docs/adr/** — Use if project has formal ADR process. Small projects can skip this.
**internal/** — Only if separating public vs private docs (rare, mostly corporate).
**.github/** — Only if using GitHub (workflows, issue templates).

## AGENTS.md Structure

Your project's AGENTS.md should document the discovered structure:

```markdown
# Project Name

## Project Structure
- Documentation: docs/ (guides, API, architecture)
- Architecture decisions: docs/adr/ (if exists)
- AI working context: ai/
- GitHub workflows: .github/ (if using GitHub)

## Development Setup
[How to get started]

## Code Conventions
[Project-specific patterns]

## Current Focus
[What we're working on now]

## Known Issues
[Important gotchas]
```

## When to Research vs Use Training Data

```
IF language_syntax OR standard_library:
    → Use training data, you already know this

IF new_library_version OR evolved_best_practices:
    → Research current documentation and SOTA

IF project_architecture OR business_logic:
    → Check AGENTS.md and existing docs

IF algorithm_comparison OR system_design:
    → Research and document in ai/research/
```

## Context Management

### Loading Context
```
ON session_start:
    → Load @AGENTS.md or @CLAUDE.md
    → Check ai/TODO.md for active work
    → Check ai/STATUS.md for current state
    → Load relevant ai/research/ files as needed

IF multi-file_task:
    → Load only files relevant to current task
    → Reference ai/DECISIONS.md for architectural context
```

### Context Reset Strategy
```
IF context > 80% full:
    → Update ai/STATUS.md with progress
    → Update ai/TODO.md with remaining work
    → Start fresh session
    → Load only essential context

IF switching_tasks:
    → Mark current task state in ai/TODO.md
    → Update ai/STATUS.md
    → Load new task context
```

## Multi-Session Handoff

**Before ending session:**
1. Update `ai/TODO.md` with progress
2. Update `ai/STATUS.md` with current state
3. Document any discoveries in `ai/RESEARCH.md`
4. Record decisions in `ai/DECISIONS.md`

**Starting new session:**
1. Load `AGENTS.md` for project context
2. Check `ai/TODO.md` for active work
3. Check `ai/STATUS.md` for current state
4. Continue from documented state

## Project Discovery Pattern

```
ON first_encounter_with_project:
    IF AGENTS.md exists:
        → Load it, note documented structure
    ELSE:
        → Scan for docs/, internal/, wiki/, .github/, tests/
        → Note discovered directories
        → Propose creating AGENTS.md with discovered structure

    IF ai/ directory missing:
        → Propose creating standard ai/ structure
        → Explain: "For AI working context (TODO, STATUS, research)"

    Document discovered structure in AGENTS.md:
        → docs/ → "Documentation: docs/"
        → docs/adr/ → "Architecture decisions: docs/adr/"
        → internal/ → "Internal team docs: internal/"
        → .github/ → "GitHub workflows: .github/"

    Working pattern:
        → Read from docs/ (permanent knowledge)
        → Write working notes to ai/ (evolving context)
        → Don't restructure existing directories
```

## Anti-Patterns to Avoid

**❌ Don't duplicate between docs/ and ai/**
- Project specs, API docs → `docs/`
- AI working notes, research → `ai/`
- Don't copy the same content to both

**❌ Don't put code in ai/ directory**
- Code belongs in src/, not ai/
- ai/ is for meta-work tracking only

**❌ Don't create internal/ by default**
- Most projects don't need it
- Only for public vs private doc separation (corporate/enterprise)
- Open-source projects: just use `docs/`

**❌ Don't create docs/adr/ unless you need it**
- Formal ADRs are optional
- Small projects: `ai/DECISIONS.md` is sufficient
- Large projects with formal process: use `docs/adr/`

**❌ Don't create language/tool pattern docs**
- Research current best practices instead
- Training data covers most syntax/patterns

**❌ Don't bloat AGENTS.md**
- Keep it concise (~100-200 lines max)
- Link to detailed docs, don't inline them

**❌ Don't hoard old research**
- Archive to `ai/research/archive/` or delete
- Keep `ai/` focused on current work

## Token Optimization

- Keep ai/ files concise and current
- Archive old research to ai/research/archive/
- Remove completed tasks from TODO.md promptly
- Update STATUS.md, don't append to it
- Use decision trees over prose
- Link to detailed docs instead of duplicating

---

**Remember**: This structure should feel lightweight. If ai/ becomes a burden to maintain, you're doing too much. The goal is to give AI agents a **standardized working environment**, not comprehensive documentation.