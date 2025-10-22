# AI Agent Practices

*Essential patterns for organizing AI agent work across all projects*

## Core Principle

**This guide teaches ORGANIZATION, not CODING.** AI agents already know how to code. What they need is a standardized way to organize their work, track progress, and maintain context across sessions.

## Standard Directory Structure

Every project should follow this structure for AI agent working context:

```
YOUR_PROJECT/
├── AGENTS.md                    # AI entry point (or CLAUDE.md)
├── ai/                          # AI working context (visible directory)
│   ├── TODO.md                 # Active tasks
│   ├── STATUS.md               # Current state
│   ├── DECISIONS.md            # Architectural choices
│   ├── RESEARCH.md             # Research index
│   └── research/               # Detailed research by topic
│       └── {topic}.md          # e.g., indexing-algorithms.md
└── [existing project structure]
```

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

## AGENTS.md Structure

Your project's AGENTS.md should include:

```markdown
# Project Name

## Project Structure
- Documentation: docs/
- Internal notes: internal/
- AI working context: ai/

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
        → Scan for docs/, internal/, tests/
        → Propose creating AGENTS.md

    IF ai/ directory missing:
        → Propose creating standard ai/ structure

    IF project has existing docs/:
        → Note in AGENTS.md: "Documentation: docs/"
        → Read from docs/, write working notes to ai/
```

## Anti-Patterns to Avoid

**❌ Don't duplicate project docs in ai/**
- Project specs belong in `docs/`
- AI working notes belong in `ai/`

**❌ Don't put code in ai/ directory**
- Code belongs in src/, not ai/
- ai/ is for meta-work tracking only

**❌ Don't create language/tool pattern docs**
- Research current best practices instead
- Training data covers most syntax/patterns

**❌ Don't bloat AGENTS.md**
- Keep it concise (~100-200 lines max)
- Link to detailed docs, don't inline them

## Token Optimization

- Keep ai/ files concise and current
- Archive old research to ai/research/archive/
- Remove completed tasks from TODO.md promptly
- Update STATUS.md, don't append to it
- Use decision trees over prose
- Link to detailed docs instead of duplicating

---

**Remember**: This structure should feel lightweight. If ai/ becomes a burden to maintain, you're doing too much. The goal is to give AI agents a **standardized working environment**, not comprehensive documentation.