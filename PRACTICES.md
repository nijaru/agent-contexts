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

**How files work together (strategy → context → execution):**

| File | Purpose | Update Mode | Scope |
|------|---------|-------------|-------|
| **PLAN.md** | Strategic roadmap and milestones | Edit-in-place | Months/quarters - high-level direction |
| **STATUS.md** | Current state + learnings | Edit-in-place | Current session - what's happening now |
| **TODO.md** | Tactical next steps | Edit-in-place | Days/weeks - immediate actions |
| **DECISIONS.md** | Architectural rationale | Append-only | Permanent record - why we chose X over Y |
| **RESEARCH.md** | External knowledge index | Hybrid | As needed - domain knowledge |

**PLAN.md is optional** - Only create if:
- Project has 3+ phases or milestones
- Critical dependencies exist between phases
- Multi-month roadmap needed

If project is simple enough that TODO.md captures everything, skip PLAN.md.

## Loading Context Order

**Read from strategic to tactical (high-level → details):**

1. **PLAN.md** (if exists) — Understand overall roadmap and current phase
2. **STATUS.md** — Current state, what worked/didn't, blockers
3. **TODO.md** — Immediate next actions
4. **DECISIONS.md** — Why architectural choices were made
5. **RESEARCH.md** — Domain knowledge and findings

## Session Workflow

| Phase | Actions |
|-------|---------|
| **Starting** | Read ai/STATUS.md FIRST → Review ai/PLAN.md (if changed or first session) → Load CLAUDE.md → Check ai/TODO.md |
| **During** | Research current best practices → Document in ai/research/{topic}.md → Record decisions in ai/DECISIONS.md → Update ai/PLAN.md if major pivot |
| **Ending (CRITICAL)** | Update ai/STATUS.md (current state + learnings) → Reference commits by hash (e.g., "Fixed in a1b2c3d") → Update ai/TODO.md → Compact if needed (see Compaction Rules) |
| **Context reset (>80% full)** | Compact ai/STATUS.md → Update ai/TODO.md → Keep only essentials → Start fresh session |

**When to update PLAN.md:**
- Major architectural pivots
- Phase completion (mark complete, focus next phase)
- Quarterly/milestone reviews
- NOT every session (strategic, not tactical)

## File Templates

### PLAN.md

```markdown
## Goal
Production-ready v1.0 by Q2 2025 with core features and API

## Milestones

| Phase | Timeline | Status | Deliverables | Success Criteria |
|-------|----------|--------|--------------|------------------|
| **Phase 1** | Q1 2025 | ← CURRENT | Core engine, CLI | 10K req/s, <100ms p95 |
| **Phase 2** | Q2 2025 | Planned | REST API, auth | 100 concurrent users |
| **Phase 3** | Q3 2025 | Planned | Web UI, monitoring | Production-ready |

## Critical Dependencies

| Dependency | Blocks | Reason |
|------------|--------|--------|
| Phase 1 complete | Phase 2 start | Data model must stabilize before API |
| Auth system | Payment integration | PCI compliance requires auth first |

## Out of Scope
- Mobile apps (deferred to 2026)
- GraphQL API (REST sufficient for v1.0)
- Real-time collaboration (future feature)
```

### TODO.md

```markdown
## High Priority
- [ ] Fix cache invalidation bug causing stale reads
- [ ] Add error handling to parse_query() - currently panics

## In Progress
- [ ] Implement user authentication
  - [x] Design auth schema
  - [x] Add bcrypt hashing
  - [ ] Write session management
  - [ ] Add tests

## Backlog
- [ ] Optimize query planner
- [ ] Add connection pooling
```

### STATUS.md

```markdown
## Current State

| Metric | Value | Updated |
|--------|-------|---------|
| Performance | 8,420 req/s | 2025-01-15 |
| Test Coverage | 87% | 2025-01-15 |
| Build | Passing | 2025-01-15 |

## What Worked
- **Caching strategy** (commit a1b2c3d): 40% performance boost
- **Connection pooling**: Reduced latency by 120ms
- **Error handling refactor**: Caught 3 edge cases in testing

## What Didn't Work
- **In-memory cache**: Too much memory pressure under load
  - Switched to Redis (see DECISIONS.md 2025-01-14)
- **Async writes**: Race condition on shutdown
  - Reverted in commit b4e5f6g, using sync writes

## Active Work
Implementing user authentication (see TODO.md)
- Schema complete, working on session management

## Blockers
- **AWS credentials** needed for S3 integration (waiting on ops team)
- **API rate limit** on external service (requested increase)
```

### DECISIONS.md

```markdown
## 2025-01-15: PostgreSQL over MongoDB

**Context**: Selecting primary database for production
**Decision**: PostgreSQL with jsonb for semi-structured data
**Rationale**:
- Strong consistency guarantees required
- Complex joins needed for reporting
- Team has 5+ years PostgreSQL experience
- ACID compliance for financial data

**Tradeoffs**:

| Pro | Con |
|-----|-----|
| ACID, proven reliability | Horizontal scaling more complex |
| Rich query capabilities | Slightly slower writes vs MongoDB |
| Strong typing | Less flexible schema changes |

**Evidence**: ai/research/database-comparison.md
**Commits**: Initial implementation in a1b2c3d

---

## 2025-01-14: Redis for caching

**Context**: In-memory cache causing OOM errors under load
**Decision**: External Redis cache with 1-hour TTL
**Rationale**:
- Decouples cache memory from app memory
- Persistence across restarts
- 10x faster than previous solution

**Tradeoffs**: Additional service dependency, network latency
**Commits**: Implemented in b4e5f6g

---
```

### RESEARCH.md

```markdown
## Database Indexing (2025-01-15)

**Sources**:
- [PostgreSQL Docs](https://www.postgresql.org/docs/current/indexes.html)
- "Database Internals" by Alex Petrov

**Key Finding**: B-tree indexes optimal for range queries, Hash for exact matches
**Relevance**: 80% of our queries are range scans (timestamps)
**Decision**: Use B-tree indexes on timestamp columns
→ Details: ai/research/indexing-strategies.md

## Authentication Patterns (2025-01-10)

**Sources**: OWASP guidelines, Auth0 docs
**Key Finding**: JWT + refresh tokens for stateless auth
**Relevance**: Need to support mobile clients (future)
**Decision**: Implement JWT with 15min access, 7d refresh
→ Details: ai/research/auth-comparison.md

## Open Questions
- [ ] Optimal cache eviction strategy for our workload
- [ ] WebSocket vs SSE for real-time updates
- [ ] Sharding strategy for 100M+ rows
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
**Question**: Which database for production?
**Answer**: PostgreSQL with jsonb for semi-structured data
**Impact**: Enables ACID compliance, complex queries, team expertise

## Evidence

| Option | Pro | Con | Score |
|--------|-----|-----|-------|
| PostgreSQL | ACID, joins, team expertise | Harder to scale horizontally | 8/10 |
| MongoDB | Easy scaling, flexible schema | No joins, eventual consistency | 6/10 |
| DynamoDB | Managed, scales automatically | Vendor lock-in, learning curve | 5/10 |

## Decision
Use PostgreSQL with these considerations:
- jsonb columns for semi-structured data
- Read replicas for scale-out
- Regular vacuum and index maintenance
```

### ai/ File Writing Rules

| File | Format | Rules |
|------|--------|-------|
| **PLAN.md** | Milestones table, dependencies table | Timeline with phases, NO detailed tasks (use TODO.md) |
| **STATUS.md** | Tables for metrics, bullets for learnings | NO narrative paragraphs, date all measurements |
| **TODO.md** | Checkbox lists only | One-line descriptions, link to details if complex |
| **DECISIONS.md** | Template: Context → Decision → Rationale (bullets) → Tradeoffs (table) | Date every entry, NO prose, link to evidence |
| **RESEARCH.md** | Index: Topic → Key Finding → Link | Tables for comparisons, NO embedded analysis |
| **research/ files** | Exec summary if >500 lines | Question → Answer → Evidence (table) → Rationale (bullets) |

### Examples

❌ **Narrative:** "After investigating caching options, the team feels Redis would be a good choice because it's fast and the team has some experience with it..."

✅ **Structured:**
```markdown
**Decision**: Redis (2025-01-15)
**Why**: 10x faster, persistence, team expertise
**Tradeoff**: Additional service dependency
```

## Compaction Rules

**Trust git history** - Delete old content instead of archiving when files get too large.

### STATUS.md Compaction
When ai/STATUS.md exceeds **400 lines**:
1. Extract current state + key recent learnings to top
2. Delete old detailed sections (git log preserves them)
3. Commit: "Compact STATUS.md - see git log for history"

### DECISIONS.md Migration
When ai/DECISIONS.md exceeds **1000 lines** or **50+ decisions**:
1. Create ai/decisions/ directory
2. Split by category: architecture.md, database.md, security.md, etc.
3. Keep index in DECISIONS.md pointing to decisions/*.md files

**Default**: Keep DECISIONS.md as single file until compaction needed.

### PLAN.md Compaction
When ai/PLAN.md exceeds **200 lines** or has 10+ completed phases:
1. Archive completed phases to DECISIONS.md with commit references
2. Keep current phase + next 1-2 upcoming phases
3. Document major pivots as decisions in DECISIONS.md
4. Commit: "Archive completed phases from PLAN.md - see [commits]"

**If PLAN.md stays small:** No compaction needed - strategic docs should be concise.

### Research Cleanup
For ai/research/ files no longer relevant:
1. Consolidate key findings into RESEARCH.md
2. Delete detailed file (git preserves it)
3. Commit: "Consolidate [topic] research - see commit [hash] for details"

## File Hierarchy

### Global vs Project vs ai/

| Level | File | Purpose | When to Update |
|-------|------|---------|----------------|
| **Global** | `~/.claude/CLAUDE.md` | Universal rules for ALL projects | On workflow changes |
| **Project** | `CLAUDE.md` or `AGENTS.md` | Architecture, patterns, commands (~100-200 lines) | On architectural changes |
| **Strategic** | `ai/PLAN.md` | Roadmap, milestones, dependencies (optional) | On major pivots, quarterly |
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
- Strategic roadmap (→ ai/PLAN.md)

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
- AI working context: ai/
  - Strategic roadmap: ai/PLAN.md
  - Current state: ai/STATUS.md (read first)
  - Next steps: ai/TODO.md

## Technology Stack
- Language: [e.g., TypeScript]
- Framework: [e.g., Next.js]

## Development Commands
[build/test/deploy commands]

## Code Standards
[specific formatting, naming, import patterns]

## Current Focus
See ai/STATUS.md for current state and active work.
For roadmap and milestones, see ai/PLAN.md.
```

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|---------------|
| Create dated summary files (SUMMARY_OCT23.md) | Update ai/STATUS.md in-place |
| Duplicate between docs/ and ai/ | docs/ = permanent, ai/ = working |
| Put code in ai/ directory | Code in src/, ai/ for meta-work only |
| Write narrative prose in ai/ | Tables, lists, key-value pairs |
| Put detailed tasks in PLAN.md | Keep strategic, use TODO.md for details |
| Create PLAN.md for simple projects | Only use when 3+ phases or dependencies exist |
| Update PLAN.md every session | Quarterly/milestone updates only |
| Create language/tool pattern docs | Research current best practices |
| Bloat CLAUDE.md/AGENTS.md (>200 lines) | Brief pointers to ai/ |
| Archive/hoard old content | Delete old content (git preserves history) |

## Token Optimization

- Keep ai/ files concise and current
- Apply compaction rules when files exceed thresholds (see Compaction Rules)
- Delete old content (git preserves history - don't archive)
- Remove completed tasks from TODO.md promptly
- Update STATUS.md in-place, don't append
- Use tables and bullets over prose
- Link to detailed docs instead of duplicating
- Skip PLAN.md if project doesn't need it

---

**Remember:** This structure should feel lightweight. If ai/ becomes a burden, you're doing too much. Goal: standardized working environment, not comprehensive documentation.
