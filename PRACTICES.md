# AI Agent Practices

**Organization patterns for AI coding agents**

## Core Principle

**This guide teaches ORGANIZATION, not CODING.** AI agents already know how to code. What they need: standardized way to organize work, track progress, maintain context across sessions.

## Standard Directory Structure

```
YOUR_PROJECT/
├── AGENTS.md                    # AI entry point (primary file)
├── CLAUDE.md → AGENTS.md        # Symlink for Claude Code compatibility
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
- **Respect existing structure** — If project has internal/, wiki/, .github/, note in AGENTS.md and use them

## File Purposes

| File | Purpose | Update Mode | Scope |
|------|---------|-------------|-------|
| **PLAN.md** | Dependencies, architecture, scope | Edit-in-place | Project lifecycle - optional |
| **STATUS.md** | Current state + learnings | Edit-in-place | Current session |
| **TODO.md** | Tactical next steps | Edit-in-place | Active work |
| **DECISIONS.md** | Architectural rationale | Append-only | Permanent record |
| **RESEARCH.md** | Knowledge index | Hybrid | As needed |

**PLAN.md is optional** - Only create if project has 3+ phases, critical dependencies, or external deadlines. Focus: what blocks what, technical approach, scope boundaries. Skip time estimates unless external deadline exists.

## Session Workflow

| Phase | Actions |
|-------|---------|
| **Starting** | Review PLAN.md (if exists) → Read STATUS.md → Check TODO.md → Load AGENTS.md |
| **During** | Research best practices → Document in research/ → Record decisions → Update PLAN.md if major pivot |
| **Ending** | Update STATUS.md (state + learnings + commits) → Update TODO.md → Compact if needed |
| **Reset (>80%)** | Compact STATUS.md → Update TODO.md → Keep essentials only |

**Reading order:** PLAN (strategic vision) → STATUS (current state) → TODO (next actions) → DECISIONS (rationale) → RESEARCH (domain knowledge)

**Update PLAN.md:** Major pivots, phase completions, quarterly reviews. NOT every session.

## File Templates

### PLAN.md

```markdown
## Goal
[What building? Why? External deadline if exists]

## Phases
| Phase | Status | Deliverables | Success Criteria |
|-------|--------|--------------|------------------|
| Phase 1 | ← CURRENT | Core engine, CLI | 10K req/s, <100ms p95 |
| Phase 2 | Planned | REST API, auth | 100 users |

## Dependencies
| Must Complete | Before Starting | Why |
|---------------|-----------------|-----|
| Phase 1 | Phase 2 | Data model must stabilize |
| Auth design | REST API | Security model affects all endpoints |

## Technical Architecture
| Component | Approach | Rationale |
|-----------|----------|-----------|
| Database | PostgreSQL + jsonb | ACID + flexibility |

## Out of Scope
- Mobile apps (v2.0 feature)
- GraphQL (REST sufficient for v1.0)

**Note**: Timeline optional - only add if external deadline exists (customer launch, conference demo)
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
| **PLAN.md** | Tables for phases/dependencies/architecture | Focus: dependencies (A before B), technical approach, scope. Detail okay. NO time estimates (days/weeks/quarters) unless external deadline |
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

## File Maintenance

**Trust git history** - Delete old content when files become unwieldy. Prune when files contain substantial irrelevant or historical content that wastes tokens and obscures current state.

### STATUS.md: Current state only

**What to delete:**
- Old pivots, completed phases, superseded approaches
- Historical metrics from previous architectures
- Resolved blockers

**What to keep:**
- Current metrics and performance data
- Active blockers and ongoing issues
- Recent learnings (last 1-2 sessions)

**Action:** Extract current state + key learnings → Delete rest → Commit: "Compact STATUS.md - removed historical content"

### DECISIONS.md: Active decisions only

**For superseded decisions:**
- Create `ai/decisions/superseded-YYYY-MM.md`
- Move reversed/replaced decisions there
- Keep main file for decisions still affecting codebase

**For topic-based splits (when growing large):**
- Create `ai/decisions/architecture.md`, `ai/decisions/database.md`, etc.
- Keep index/summary in main DECISIONS.md linking to topic files
- Use when file exceeds ~50 decisions or becomes hard to navigate

**Delete entirely:** Decisions that were reversed AND have no historical value

### TODO.md: Active work only

- Delete completed tasks immediately (no "Done" section)
- Git preserves completion history
- Keep only pending/in-progress work

### PLAN.md: Current + next phases

- Archive/delete completed phases
- Keep current phase + dependencies for next 1-2 phases
- Major pivots: update in-place, old content to git history

### research/: Consolidate or delete

- Consolidate key findings to RESEARCH.md
- Delete file when no longer relevant
- Reference commit hash if needed later: "See abc123d for auth research"

**Principle:** Files should efficiently answer "what's current?" without loading substantial irrelevant historical content. Prune when old content dominates token usage or obscures current state.

## File Hierarchy

| Level | File | Purpose | Update Mode |
|-------|------|---------|-------------|
| **Global** | `~/.claude/CLAUDE.md` | Rules for ALL projects | On workflow changes |
| **Project** | `AGENTS.md` (+ symlink `CLAUDE.md`) | Architecture, commands, project overview | On arch changes |
| **Strategic** | `ai/PLAN.md` | Roadmap (optional) | Quarterly/pivots |
| **Session** | `ai/STATUS.md` | Current state | Every session |
| **Session** | `ai/TODO.md` | Active tasks | As tasks change |
| **Append** | `ai/DECISIONS.md` | Decisions | On decisions |
| **Research** | `ai/RESEARCH.md` | Findings | During research |

## Project AGENTS.md

**AGENTS.md = primary file, CLAUDE.md → AGENTS.md = symlink for Claude Code compatibility**

**Optimized for AI consumption:**
- Use tables, lists, code blocks (machine-readable structure)
- Clear sections with ## headers
- Well-structured - logical organization, easy to parse
- Comprehensive - include everything AI needs to understand project
- No length limit - include what's needed, exclude what isn't

**Belongs:** Build/test/deploy commands, coding standards, architecture, tech stack, project overview

**Does NOT belong:** Current issues (→ STATUS.md), learnings (→ STATUS.md), tactical roadmap (→ PLAN.md), detailed breakdowns (→ ai/)

**Quality over brevity:**
- Well-structured 500-line file > poorly organized 100-line file
- Focus: no duplication, effective AI entry point, comprehensive coverage

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
| Artificial time tracking files (WEEK*_DAY*.md) | Update STATUS.md in-place, trust git history. Real dates okay (ANALYSIS_2025-11-05.md) |
| Duplicate docs/ and ai/ | docs/ = permanent, ai/ = working |
| Code in ai/ | Code in src/, ai/ for meta-work only |
| Narrative prose in ai/ | Tables, lists, key-value |
| Time estimates in PLAN.md ("~3-4 days", "Q1 2025") | Dependencies + scope. Add time only if external deadline exists |
| Progress tracking ("Week X Day Y") in PLAN.md | Use git log for timeline, STATUS.md for current state |
| PLAN.md for simple projects | Only if 3+ phases/dependencies/deadlines |
| Language/tool pattern docs | Research current best practices |
| Duplicate ai/ content in AGENTS.md | Brief pointers to ai/, keep AGENTS.md well-structured |

## Token Optimization

- Apply file maintenance when files contain substantial irrelevant content
- Update STATUS.md in-place, don't append
- Skip PLAN.md if project doesn't need it (3+ phases/dependencies)
- Use tables/bullets over prose

---

**Remember:** Keep ai/ minimal and current. Goal: efficient context handoff across agent sessions, not comprehensive documentation.
