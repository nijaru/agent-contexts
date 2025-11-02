# AI Agent Practices

**Organization patterns for AI coding agents**

## Core Principle

**This guide teaches ORGANIZATION, not CODING.** AI agents already know how to code. What they need: standardized way to organize work, track progress, maintain context across sessions.

## Standard Directory Structure

```
YOUR_PROJECT/
├── CLAUDE.md or AGENTS.md       # AI entry point
├── docs/                        # Permanent user/team docs
├── ai/                          # AI working context
│   ├── PLAN.md                 # Strategic roadmap
│   ├── TODO.md                 # Active tasks
│   ├── STATUS.md               # Current state
│   ├── DECISIONS.md            # Architectural choices
│   ├── RESEARCH.md             # Research index
│   └── research/               # Detailed research
│       └── {topic}.md
└── [existing project structure]
```

**Core separation:**
- **docs/** — Permanent user/team documentation (guides, API, specs)
- **ai/** — Evolving AI working context (tasks, research, decisions)
- **Respect existing structure** — If project has internal/, wiki/, .github/, note in CLAUDE.md and use them

## File Purposes

**How files work together (plan → history → status → next steps):**

| File | Purpose | Update Mode | Content |
|------|---------|-------------|---------|
| **PLAN.md** | Strategic roadmap and milestones | Edit-in-place | Goals, phases, dependencies, timeline |
| **DECISIONS.md** | Why we made architectural choices | Append-only | Dated decisions with rationale |
| **STATUS.md** | Current state + learnings | Edit-in-place | Metrics, what worked/didn't, blockers |
| **TODO.md** | What's next | Edit-in-place | Active tasks, checkboxes |
| **RESEARCH.md** | External knowledge index | Hybrid | Topics with key findings, links to details |

**Loading context order:**
1. Read STATUS.md first (current state + recent learnings)
2. Check TODO.md (active work)
3. Review PLAN.md (strategic roadmap and milestones)
4. Reference DECISIONS.md (architectural rationale)
5. Consult RESEARCH.md (domain knowledge)

## File Templates

### PLAN.md
```markdown
## Goal
[Overall objective - what are we building/achieving?]

## Milestones
- **Phase 1 (Q1 2025)**: Core engine + CLI ← CURRENT
  - Deliverables: [specific features]
  - Success criteria: [measurable outcomes]
- **Phase 2 (Q2 2025)**: REST API + authentication
  - Deliverables: [specific features]
  - Dependencies: Phase 1 complete (data model must stabilize)
- **Phase 3 (Q3 2025)**: Web UI
  - Deliverables: [specific features]

## Critical Dependencies
- [Dependency 1]: Must complete before [what]
- [Dependency 2]: Blocks [what]

## Out of Scope (for this plan)
- [Feature X] - deferred to future
- [Feature Y] - not aligned with current goal
```

### TODO.md
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

### STATUS.md
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

### DECISIONS.md
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

### RESEARCH.md
```markdown
## Database Indexing (researched 2025-01-15)
**Sources**: [links]
**Key Finding**: LSM trees better for write-heavy workloads
**Relevance**: Our use case is 80% writes
**Decision**: Implement LSM-based index
→ Details: ai/research/indexing-algorithms.md

## Open Questions
- [ ] Optimal cache eviction strategy
- [ ] WebSocket vs SSE comparison needed
```

## Writing for AI: Machine-Optimized

**ai/ is for AI agents (machine-readable), docs/ is for users/team (narrative)**

### Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Structure over prose** | Tables, lists, key-value pairs (NOT narrative paragraphs) |
| **Inverted pyramid** | Answer first, evidence second, rationale third |
| **Token efficiency** | AI processes every token - make scannable |
| **Cross-reference** | Point to detailed files, don't duplicate |
| **Executive summaries** | Docs >500 lines need TL;DR at top with key Q&A |

### Strategic Analysis Pattern

For research/investigations in ai/research/:

```markdown
## Executive Summary
**Question**: [key question]
**Answer**: [decision]
**Impact**: [consequences]

## Evidence
| Option | Pro | Con | Score |
|--------|-----|-----|-------|

## Decision
[action + rationale bullets]
```

### ai/ File Writing Rules

| File | Format | Rules |
|------|--------|-------|
| **PLAN.md** | Milestones (bullets), dependencies (table) | Timeline with phases, NO detailed implementation |
| **STATUS.md** | Tables for metrics, bullets for learnings | NO narrative paragraphs |
| **TODO.md** | Checkbox lists only | One-line descriptions, link to details |
| **DECISIONS.md** | Template: Context → Decision → Rationale (bullets) → Tradeoffs (table) | Date every entry, NO prose |
| **RESEARCH.md** | Index: Topic → Key Finding → Link | Tables for comparisons, NO embedded analysis |
| **research/ files** | Exec summary if >500 lines | Question → Answer → Evidence (table) → Rationale (bullets) |

### Examples

❌ **Narrative:** "After investigating caching, the team feels Redis would be good..."

✅ **Structured:**
```markdown
**Decision**: Redis (2025-01-15)
**Why**: 10x faster, persistence, team expertise
**Tradeoff**: Additional service dependency
```

## File Hierarchy

### Global vs Project vs ai/

| Level | File | Purpose | When to Update |
|-------|------|---------|----------------|
| **Global** | `~/.claude/CLAUDE.md` | Universal rules for ALL projects | On workflow changes |
| **Project** | `CLAUDE.md` or `AGENTS.md` | Architecture, patterns, commands (~100-200 lines) | On architectural changes |
| **Strategic** | `ai/PLAN.md` | Roadmap, milestones, dependencies | On major pivots, quarterly |
| **Session** | `ai/STATUS.md` | Current state, learnings | Every session |
| **Session** | `ai/TODO.md` | Active tasks | As tasks change |
| **Append** | `ai/DECISIONS.md` | Architectural decisions | On decisions |
| **Research** | `ai/RESEARCH.md` | Research findings | During research |

### Project CLAUDE.md/AGENTS.md

**What belongs:**
- Build/test/deploy commands
- Coding standards and naming conventions
- Project architecture and structure
- Technology stack and framework patterns

**What does NOT belong:**
- Current issues, active work (→ ai/STATUS.md)
- Recent learnings (→ ai/STATUS.md)
- Detailed breakdowns (→ ai/)

**Format:**
- ✅ Brief pointers: `"⚠️ Model routing issues. See ai/STATUS.md"`
- ❌ Detailed breakdowns: `"⚠️ Model Routing: 1. Problem A... 2. Problem B..."`

## Project Config Template

See AGENTS.md in this repo for complete example. Minimal version:

```markdown
# Project Name

[Brief description]

## Project Structure
- Documentation: docs/
- AI working context: ai/ (read ai/STATUS.md first)

## Technology Stack
- Language: [e.g., TypeScript]
- Framework: [e.g., Next.js]

## Development Commands
[build/test/deploy commands]

## Code Standards
[specific formatting, naming, import patterns]

## Current Focus
See ai/STATUS.md for current state and active work.
```

## Compaction Rules

**Trust git history** - Delete old content instead of archiving when files get too large.

### STATUS.md Compaction
When ai/STATUS.md exceeds **400 lines**:
1. Extract current state + key learnings to top
2. Delete old detailed sections (git log preserves them)
3. Commit with message: "Compact STATUS.md - see git log for history"

### DECISIONS.md Migration
When ai/DECISIONS.md exceeds **1000 lines** or **50+ decisions**:
1. Create ai/decisions/ directory
2. Split by category: architecture.md, database.md, security.md, etc.
3. Keep index in DECISIONS.md pointing to decisions/*.md files

**Default**: Keep DECISIONS.md as single file until compaction needed.

### Research Cleanup
For ai/research/ files no longer relevant:
1. Consolidate key findings into RESEARCH.md
2. Delete detailed file
3. Commit: "Consolidate [topic] research - see commit [hash] for details"

## Session Workflow

| Phase | Actions |
|-------|---------|
| **Starting** | Read ai/STATUS.md FIRST → Load CLAUDE.md → Check ai/TODO.md |
| **During** | Research current best practices → Document in ai/research/{topic}.md → Record decisions in ai/DECISIONS.md |
| **Ending (CRITICAL)** | Update ai/STATUS.md → Reference commits by hash (e.g., "Fixed in a1b2c3d") → Update ai/TODO.md → Compact if needed (see Compaction Rules) |
| **Context reset (>80% full)** | Update ai/STATUS.md and ai/TODO.md → Start fresh session with essentials only |

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|---------------|
| Create dated summary files (SUMMARY_OCT23.md) | Update ai/STATUS.md |
| Duplicate between docs/ and ai/ | docs/ = permanent, ai/ = working |
| Put code in ai/ directory | Code in src/, ai/ for meta-work only |
| Write narrative prose in ai/ | Tables, lists, key-value pairs |
| Create language/tool pattern docs | Research current best practices |
| Bloat CLAUDE.md/AGENTS.md (>200 lines) | Brief pointers to ai/ |
| Archive/hoard old content | Delete old content (git preserves history) |

## Token Optimization

- Keep ai/ files concise and current
- Apply compaction rules when files exceed thresholds (see Compaction Rules)
- Delete old content (git preserves history - don't archive)
- Remove completed tasks from TODO.md promptly
- Update STATUS.md, don't append to it
- Use decision trees over prose
- Link to detailed docs instead of duplicating

---

**Remember:** This structure should feel lightweight. If ai/ becomes a burden, you're doing too much. Goal: standardized working environment, not comprehensive documentation.
