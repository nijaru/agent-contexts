# AI Agent Practices

*Essential patterns for organizing AI agent work across all projects*

## Core Principle

**This guide teaches ORGANIZATION, not CODING.** AI agents already know how to code. What they need is a standardized way to organize their work, track progress, and maintain context across sessions.

## Standard Directory Structure

Every project should follow this structure:

```
YOUR_PROJECT/
├── AGENTS.md                    # AI entry point (or CLAUDE.md)
├── docs/                        # Permanent documentation (optional)
├── ai/                          # AI working context
│   ├── TODO.md                 # Active tasks
│   ├── STATUS.md               # Current state
│   ├── DECISIONS.md            # Working decision log
│   ├── RESEARCH.md             # Research index
│   └── research/               # Detailed research by topic
│       └── {topic}.md
└── [existing project structure]
```

**Core separation:**
- **docs/** — Permanent, human-facing documentation (guides, API, specs)
- **ai/** — Evolving AI working context (tasks, research, decisions)
- **Respect existing structure** — If project has internal/, wiki/, .github/, note in AGENTS.md and use them

## File Purposes and Update Modes

**How files work together (history → status → next steps)**:
- **DECISIONS.md**: Why we made architectural choices (append-only history)
- **STATUS.md**: Where we are now + implementation learnings (edit-in-place, "What Worked/Didn't" = working history)
- **TODO.md**: What's next (edit-in-place)
- **RESEARCH.md**: External knowledge gathered (hybrid, index with details in research/)

**Loading context**: Read STATUS.md first (current state + recent learnings), check TODO.md (active work), reference DECISIONS.md (architectural rationale), consult RESEARCH.md (domain knowledge).

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

## What Goes Where

**docs/** — Permanent documentation
- API references, user guides, tutorials
- Architecture documentation
- Requirements, specifications
- Optional: docs/adr/ for formal Architecture Decision Records

**ai/** — AI working context (focus of this guide)
- TODO.md — Current tasks
- STATUS.md — Project state, what worked/didn't
- DECISIONS.md — Development decisions and rationale
- RESEARCH.md — Index of research findings
- research/{topic}.md — Detailed research (e.g., indexing-algorithms.md)

**Simple rule:**
- Does it change frequently during development? → ai/
- Is it permanent reference material? → docs/
- When in doubt, start in ai/, move to docs/ when stable

## Global vs Project Files

**Global ~/.claude/CLAUDE.md** (or equivalent):
- Universal rules for ALL projects (commit formats, naming, testing)
- Loaded in EVERY conversation across projects
- Maximum token efficiency required

**Project CLAUDE.md/AGENTS.md**:
- Brief project overview (~100-200 lines max)
- Setup instructions, current focus, pointers
- ✅ Use brief notices: `"⚠️ Model routing issues. See ai/STATUS.md"`
- ❌ NOT detailed breakdowns: `"⚠️ Model Routing: 1. Problem A (5 lines)... 2. Problem B..."`
- Detailed issues → ai/STATUS.md
- Architectural decisions → ai/DECISIONS.md
- Research findings → ai/RESEARCH.md

## AGENTS.md Structure

Document the project structure you discover:

```markdown
# Project Name

## Project Structure
- Documentation: docs/ (or wherever it exists)
- AI working context: ai/
- [Other discovered directories: .github/, internal/, etc.]

## Development Setup
[How to get started]

## Current Focus
[What we're working on now]
```

## Session Workflow

**Starting work:**
- **Read ai/STATUS.md FIRST** - current state, what works/doesn't
- Load AGENTS.md for project context
- Check ai/TODO.md for active work

**During work:**
- Research current best practices (don't rely on stale patterns)
- Document findings in ai/research/{topic}.md
- Record decisions in ai/DECISIONS.md

**Ending session (CRITICAL):**
- **Update ai/STATUS.md** - keep it current for next session
- **Reference commits by short hash** - When documenting changes, include short hash (e.g., "Fixed in a1b2c3d") for traceability
- Update ai/TODO.md with progress
- Archive old research if needed

**Context reset (>80% full):**
- Update ai/STATUS.md and ai/TODO.md
- Start fresh session with only essential context

## Anti-Patterns to Avoid

**❌ Don't create dated summary files**
- NO SUMMARY_OCT23.md, IMPLEMENTATION_DAY1.md, etc.
- Update ai/STATUS.md instead - it's designed for this

**❌ Don't duplicate between docs/ and ai/**
- Permanent docs → docs/, working notes → ai/

**❌ Don't put code in ai/ directory**
- Code belongs in src/, ai/ is for meta-work only

**❌ Don't create language/tool pattern docs**
- Research current best practices instead

**❌ Don't bloat AGENTS.md/CLAUDE.md**
- Keep concise (~100-200 lines max) - loaded in EVERY conversation
- Use pointers, not details: `"⚠️ Issue. See ai/STATUS.md"` (NOT multi-line breakdowns)
- Link to ai/ and docs/, don't inline them

**❌ Don't hoard old research**
- Archive or delete, keep ai/ focused on current work

## Token Optimization

- Keep ai/ files concise and current
- Archive old research to ai/research/archive/
- Remove completed tasks from TODO.md promptly
- Update STATUS.md, don't append to it
- Use decision trees over prose
- Link to detailed docs instead of duplicating

---

**Remember**: This structure should feel lightweight. If ai/ becomes a burden to maintain, you're doing too much. The goal is to give AI agents a **standardized working environment**, not comprehensive documentation.