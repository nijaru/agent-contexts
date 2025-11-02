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
│   ├── PLAN.md                 # Strategic roadmap (optional)
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

| File | Purpose | Update Mode | Scope |
|------|---------|-------------|-------|
| **PLAN.md** | Strategic roadmap | Edit-in-place | Months/quarters - optional |
| **STATUS.md** | Current state + learnings | Edit-in-place | Current session |
| **TODO.md** | Tactical next steps | Edit-in-place | Days/weeks |
| **DECISIONS.md** | Architectural rationale | Append-only | Permanent record |
| **RESEARCH.md** | Knowledge index | Hybrid | As needed |

**PLAN.md is optional** - Only create if project has 3+ phases, critical dependencies, or multi-month roadmap. Skip for simple projects.

## Session Workflow

| Phase | Actions |
|-------|---------|
| **Starting** | Read STATUS.md → Check TODO.md → Review PLAN.md (if exists) → Load CLAUDE.md |
| **During** | Research best practices → Document in research/ → Record decisions → Update PLAN.md if major pivot |
| **Ending** | Update STATUS.md (state + learnings + commits) → Update TODO.md → Compact if needed |
| **Reset (>80%)** | Compact STATUS.md → Update TODO.md → Keep essentials only |

**Reading order:** STATUS (where am I?) → TODO (what's next?) → PLAN (strategic context) → DECISIONS (rationale) → RESEARCH (domain knowledge)

**Update PLAN.md:** Major pivots, phase completions, quarterly reviews. NOT every session.

## File Templates

### PLAN.md

```markdown
## Goal
Production-ready v1.0 by Q2 2025

## Milestones
| Phase | Timeline | Status | Deliverables | Success Criteria |
|-------|----------|--------|--------------|------------------|
| Phase 1 | Q1 2025 | ← CURRENT | Core engine, CLI | 10K req/s, <100ms p95 |
| Phase 2 | Q2 2025 | Planned | REST API, auth | 100 users |

## Critical Dependencies
| Dependency | Blocks | Reason |
|------------|--------|--------|
| Phase 1 complete | Phase 2 | Data model must stabilize |

## Out of Scope
- Mobile apps (deferred to 2026)
- GraphQL (REST sufficient)
```

### TODO.md

```markdown
## High Priority
- [ ] Fix cache invalidation bug
- [ ] Add error handling to parse_query()

## In Progress
- [ ] Implement auth
  - [x] Schema design
  - [ ] Session management

## Backlog
- [ ] Optimize query planner
```

### STATUS.md

```markdown
## Current State
| Metric | Value | Updated |
|--------|-------|---------|
| Performance | 8,420 req/s | 2025-01-15 |
| Test Coverage | 87% | 2025-01-15 |

## What Worked
- Caching (a1b2c3d): 40% boost
- Connection pooling: -120ms latency

## What Didn't Work
- In-memory cache: OOM under load → Switched to Redis (see DECISIONS.md)

## Active Work
Implementing auth (see TODO.md) - schema complete, working on sessions

## Blockers
- AWS credentials needed for S3 (waiting on ops)
```

### DECISIONS.md

```markdown
## 2025-01-15: PostgreSQL over MongoDB

**Context**: Selecting primary database
**Decision**: PostgreSQL with jsonb
**Rationale**:
- Strong consistency required
- Complex joins needed
- Team expertise (5+ years)
- ACID for financial data

**Tradeoffs**:
| Pro | Con |
|-----|-----|
| ACID, reliability | Harder horizontal scaling |
| Rich queries | Slower writes vs Mongo |

**Evidence**: ai/research/db-comparison.md
**Commits**: a1b2c3d

---
```

### RESEARCH.md

```markdown
## Database Indexing (2025-01-15)
**Sources**: PostgreSQL docs, "Database Internals" (Petrov)
**Finding**: B-tree optimal for range queries (80% of our workload)
**Decision**: B-tree indexes on timestamp columns
→ Details: ai/research/indexing.md

## Open Questions
- [ ] Cache eviction strategy
- [ ] WebSocket vs SSE
```

## ai/ File Writing Rules

| File | Format | Rules |
|------|--------|-------|
| **PLAN.md** | Tables for milestones/dependencies | Timeline with phases, NO detailed tasks |
| **STATUS.md** | Tables for metrics, bullets for learnings | NO prose, date measurements |
| **TODO.md** | Checkbox lists | One-line descriptions |
| **DECISIONS.md** | Context → Decision → Rationale → Tradeoffs (table) | Date entries, link evidence |
| **RESEARCH.md** | Index: Topic → Finding → Link | Tables for comparisons |
| **research/ files** | Question → Answer → Evidence (table) | Use exec summary if >500 lines |

**Key principle:** Tables, lists, key-value pairs. NO narrative prose. Answer first, evidence second.

### Example

❌ **Prose:** "After investigating caching, the team feels Redis would be good because it's fast..."

✅ **Structured:**
```markdown
**Decision**: Redis (2025-01-15)
**Why**: 10x faster, persistence, team expertise
**Tradeoff**: Service dependency
```

## Compaction Rules

**Trust git history** - Delete old content when files get large.

| File | Threshold | Action |
|------|-----------|--------|
| **STATUS.md** | 400 lines | Extract current + key learnings → Delete old (git preserves) → Commit: "Compact STATUS.md" |
| **DECISIONS.md** | 1000 lines / 50+ decisions | Create ai/decisions/ dir → Split by category → Keep index in DECISIONS.md |
| **PLAN.md** | 200 lines / 10+ phases | Archive completed phases to DECISIONS.md → Keep current + next 1-2 phases |
| **research/** | No longer relevant | Consolidate findings to RESEARCH.md → Delete file → Reference commit |

## File Hierarchy

| Level | File | Purpose | Update Mode |
|-------|------|---------|-------------|
| **Global** | `~/.claude/CLAUDE.md` | Rules for ALL projects | On workflow changes |
| **Project** | `CLAUDE.md` / `AGENTS.md` | Architecture, commands (~100-200 lines) | On arch changes |
| **Strategic** | `ai/PLAN.md` | Roadmap (optional) | Quarterly/pivots |
| **Session** | `ai/STATUS.md` | Current state | Every session |
| **Session** | `ai/TODO.md` | Active tasks | As tasks change |
| **Append** | `ai/DECISIONS.md` | Decisions | On decisions |
| **Research** | `ai/RESEARCH.md` | Findings | During research |

## Project CLAUDE.md/AGENTS.md

**Belongs:** Build/test/deploy commands, coding standards, architecture, tech stack

**Does NOT belong:** Current issues (→ STATUS.md), learnings (→ STATUS.md), roadmap (→ PLAN.md), detailed breakdowns (→ ai/)

**Format:**
- ✅ `"⚠️ See ai/STATUS.md for routing issues"`
- ❌ `"⚠️ Routing: 1. Problem A... 2. Problem B..."`

## Project Config Template

```markdown
# Project Name
[Brief description]

## Structure
docs/, ai/ (PLAN.md if complex, STATUS.md read first, TODO.md)

## Stack
[Language], [Framework]

## Commands
build: [cmd]
test: [cmd]
deploy: [cmd]

## Standards
[formatting, naming, imports]

## Current Focus
ai/STATUS.md (current state), ai/PLAN.md (roadmap)
```

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|---------------|
| Dated files (SUMMARY_OCT23.md) or archive dirs | Update STATUS.md in-place, trust git history |
| Duplicate docs/ and ai/ | docs/ = permanent, ai/ = working |
| Code in ai/ | Code in src/, ai/ for meta-work only |
| Narrative prose in ai/ | Tables, lists, key-value |
| Detailed tasks or daily updates in PLAN.md | Keep strategic (quarterly), use TODO.md for tasks |
| PLAN.md for simple projects | Only if 3+ phases/dependencies |
| Language/tool pattern docs | Research current best practices |
| Bloat CLAUDE.md (>200 lines) | Brief pointers to ai/ |

## Token Optimization

- Apply compaction rules when thresholds hit
- Update STATUS.md in-place, don't append
- Skip PLAN.md if project doesn't need it
- Use tables/bullets over prose

---

**Remember:** This structure should feel lightweight. If ai/ becomes a burden, you're doing too much. Goal: standardized working environment, not comprehensive documentation.
