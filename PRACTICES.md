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

**docs/** — Permanent documentation for humans
- API references, user guides, tutorials
- Architecture documentation for team/users
- Requirements, specifications
- Optional: docs/adr/ for formal Architecture Decision Records
- Purpose: Normal project docs (readable by humans)

**ai/** — AI agent working context (session tracking & research)
- TODO.md — Current tasks
- STATUS.md — Project state, what worked/didn't
- DECISIONS.md — Development decisions and rationale
- RESEARCH.md — Index of research findings
- research/{topic}.md — Detailed research (e.g., indexing-algorithms.md)
- Purpose: Purely for AI agents to track project and maintain context across sessions

**Simple rule:**
- Does it change frequently during development? → ai/
- Is it permanent reference material for humans? → docs/
- When in doubt, start in ai/, move to docs/ when stable

## Writing for AI: Machine-Optimized Content

**ai/ is for AI agents (machine-readable), docs/ is for humans (narrative)**

### Core Principles

1. **Structure over prose**: Use tables, lists, key-value pairs instead of narrative paragraphs
2. **Inverted pyramid**: Answer/conclusion first, evidence second, rationale third
3. **Token efficiency**: AI agents process every token - make content scannable
4. **Cross-reference**: Point to detailed files, don't duplicate content inline
5. **Executive summaries**: Docs >500 lines need TL;DR at top with key Q&A

### Strategic Analysis Pattern

For research/investigations in ai/research/:

```markdown
## Executive Summary
**Question**: [key question]
**Answer**: [decision]
**Impact**: [consequences]

### Evidence
| Option | Pro | Con | Score |
|--------|-----|-----|-------|

### Decision
[action + rationale bullets]
```

### ai/ File Writing Rules

**STATUS.md**:
- Use tables for metrics: `| Metric | Value | Last Updated |`
- Bullet points for learnings: `- Pattern X improved Y by Z%`
- NO narrative paragraphs explaining context

**TODO.md**:
- Checkbox lists only: `- [ ] Task with success criteria`
- NO descriptions beyond one line
- Link to detailed docs: `See ai/research/feature-analysis.md`

**DECISIONS.md**:
- Use template: Context → Decision → Rationale (bullets) → Tradeoffs (table)
- Date every entry
- NO prose justifications

**RESEARCH.md**:
- Index format: Topic → Key Finding (one line) → Link to details
- Use tables to compare options
- NO embedded analysis (put in research/ files)

**research/ files**:
- Executive summary mandatory if >500 lines
- Question → Answer → Evidence (table) → Rationale (bullets)
- Use headings for scannability

### Examples

❌ Narrative: "After investigating caching, the team feels Redis would be good..."
✅ Structured:
```markdown
**Decision**: Redis (2025-01-15)
**Why**: 10x faster, persistence, team expertise
**Tradeoff**: Additional service dependency
```

## Global vs Project Files

**Global ~/.claude/CLAUDE.md** (or equivalent):
- Universal rules for ALL projects (commit formats, naming, testing)
- Loaded in EVERY conversation across projects
- Maximum token efficiency required

**Project AGENTS.md** (repo-level, team-shared):
- **Recommendation**: Use `AGENTS.md` as the universal standard (works with Cursor, Cline, Claude Code, Copilot, Windsurf, etc.)
- For Claude Code compatibility: `ln -s AGENTS.md CLAUDE.md` or vice versa
- **What belongs here**: Architecture, patterns, commands, code style (~100-200 lines)
  - Build/test/deploy commands
  - Coding standards and naming conventions
  - Project architecture and structure
  - Technology stack and framework patterns
- **When to update**: On architectural changes, new patterns adopted, tooling changes
- **What does NOT belong**: Current issues, active work, recent learnings
- ✅ Brief pointers: `"⚠️ Model routing issues. See ai/STATUS.md"`
- ❌ Detailed breakdowns: `"⚠️ Model Routing: 1. Problem A... 2. Problem B..."`

**ai/ files** (session-level, evolving context):
- **ai/STATUS.md**: Current state, active work, implementation learnings
- **ai/DECISIONS.md**: Architectural decisions with dates and rationale
- **ai/RESEARCH.md**: External research findings and open questions
- **When to update**: Every session (STATUS.md), on decisions (DECISIONS.md), during research (RESEARCH.md)

## AGENTS.md Template

```markdown
# Project Name

Brief description of what this project does.

## Project Structure
- Documentation: docs/
- AI working context: ai/ (read ai/STATUS.md first)
- [Other key directories]

## Technology Stack
- Language: [e.g., TypeScript, Python]
- Framework: [e.g., Next.js, FastAPI]
- [Key libraries and tools]

## Development Commands
```bash
# Install dependencies
[command]

# Run dev server
[command]

# Run tests
[command]

# Build
[command]
```

## Code Standards
- [Specific formatting rules]
- [Naming conventions]
- [Import patterns]
- [Testing requirements]

## Architecture Patterns
- [Key architectural decisions]
- [Folder structure conventions]
- [Data flow patterns]

## Current Focus
See ai/STATUS.md for current state and active work.
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

**❌ Don't write narrative prose in ai/ files**
- Use tables, lists, key-value pairs for machine readability
- Front-load answers, use inverted pyramid structure
- ai/ is for agents (structured), docs/ is for humans (narrative)

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