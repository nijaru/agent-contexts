# AI Agent Practices

**Organization patterns for AI coding agents**

## Core Principle

**This guide teaches ORGANIZATION, not CODING.** AI agents already know how to code. What they need: standardized way to organize work, track progress, maintain context across sessions.

**ai/ is your AI agent's workspace** - This is where AI agents manage project state, maintain context between sessions, and track progress. Not for human documentation (that's docs/). Think of ai/ as the agent's working memory and scratch space for maintaining continuity across sessions.

**Token efficiency through structure:**
- **Session files** (ai/ root): Read every session - keep minimal, current only (<500 lines each)
- **Reference files** (subdirectories): Read only when needed - detailed research, design specs
- Subdirectories prevent paying token cost for unused context each session

## Task Tracking Options

**Recommended: Beads (`bd`)** — Graph-based issue tracker with dependency tracking, multi-session memory, and git-backed sync. Survives context compaction. See: github.com/steveyegge/beads

**Alternative: TODO.md** — Markdown-based task tracking. Simpler, no dependencies, but lacks dependency graphs and doesn't survive compaction as well.

| Aspect | Beads (`bd`) | TODO.md |
|--------|--------------|---------|
| Dependencies | Native graph (`bd dep add X blocks Y`) | Inline notation `(after: x)` |
| Ready work | `bd ready` auto-filters | Manual ## Ready section |
| Multi-session | Survives compaction | Lost on /compact |
| Multi-agent | Hash IDs prevent collisions | Manual coordination |
| Setup | `bd init` | Create file |

**Workflow with beads:**
- Start: `bd ready` → pick unblocked work
- During: `bd create`, `bd update`, `bd dep add`
- End: `bd close`, `bd sync`, provide follow-up prompt

**If using TODO.md:** See TODO.md Format section below.

## Standard Directory Structure

```
YOUR_PROJECT/
├── AGENTS.md                    # AI entry point (primary file)
├── CLAUDE.md → AGENTS.md        # Symlink for Claude Code compatibility
├── .beads/                      # Beads task tracking (if using beads)
├── docs/                        # Permanent user/team docs
├── ai/                          # AI working context
│   ├── STATUS.md               # Current state (always)
│   ├── DESIGN.md               # System architecture (recommended)
│   ├── DECISIONS.md            # Architectural choices (recommended)
│   ├── ROADMAP.md              # Phases, milestones (situational)
│   ├── research/               # External research (inputs)
│   │   └── {topic}.md
│   ├── design/                 # Component specs (outputs)
│   │   └── {component}.md
│   └── tmp/                    # Temporary artifacts (gitignored)
└── [existing project structure]
```

**Core separation:**
- **docs/** — Permanent user/team documentation (guides, API, specs)
- **ai/** — AI session context management (agent's workspace for tracking state across sessions)
- **Respect existing structure** — If project has internal/, wiki/, .github/, note in AGENTS.md and use them

**Token efficiency:** Session files in ai/ root are read every session. Reference files in subdirectories (research/, design/) are loaded only when needed, preventing token waste on unused context.

## ai/ Directory Organization

**Purpose:** AI agent session context management - track state, decisions, and research across sessions

**Design principle:** Minimize tokens loaded per session while maintaining comprehensive context

### File Tiers

| Tier | Location | Read Frequency | Size Guideline | Purpose |
|------|----------|----------------|----------------|---------|
| **Session** | ai/*.md | Every session | <500 lines each | Current state, active work |
| **Reference** | ai/research/ | On demand | Any size | Detailed research findings |
| **Reference** | ai/design/ | On demand | Any size | Component specifications |
| **Scratch** | ai/tmp/ | On demand | Any size | Temporary artifacts, logs, diffs |

### Session Files (ai/ root)

**These are read EVERY session** - keep minimal, current, focused:

| File | When | Purpose |
|------|------|---------|
| STATUS.md | **Always** | Current state, metrics, blockers |
| DESIGN.md | **Recommended** | System architecture, components, data flow |
| DECISIONS.md | **Recommended** | Architectural decisions and rationale |
| ROADMAP.md | Situational | Phases, milestones, scope (multi-phase projects only) |
| TODO.md | Situational | Tasks (only if not using beads) |

**Scaling guidance:**

| Project Size | Files |
|--------------|-------|
| Minimal (scripts, small tools) | STATUS.md only |
| Standard (typical projects) | STATUS.md, DESIGN.md, DECISIONS.md |
| Complex (multi-phase) | + ROADMAP.md |

### Reference Subdirectories

**Only loaded when AI needs them** - no token cost unless accessed:

#### research/ - External Research Findings

**Purpose:** Store outputs from web searches, documentation research, exploration of external resources. These are *inputs* that inform design decisions.

**Create when:**
- Doing web research on libraries, APIs, best practices
- Exploring external documentation
- Comparing technologies

**Contents:**
- Technology comparisons: `ai/research/database-comparison.md`
- Best practices research: `ai/research/auth-patterns.md`
- External API documentation: `ai/research/stripe-api.md`

**Workflow:** research/ (inputs) → DESIGN.md (synthesis) → design/ (component specs) → code

**Maintenance:**
- Keep while relevant to active work
- Delete when insights consolidated to DESIGN.md or DECISIONS.md
- Reference in git if needed later: "See commit abc123d for details"

#### design/ - Component Specifications

**Purpose:** Detailed pre-implementation specifications for individual components. These are *outputs* from synthesizing research into concrete designs.

**Create when:**
- Designing complex component before implementation
- Formal design review needed
- API specification required

**Contents:**
- API specifications: `ai/design/rest-api-v1.md`
- Component designs: `ai/design/auth-module.md`
- Protocol specs: `ai/design/websocket-protocol.md`

**Workflow:** research/ (inputs) → DESIGN.md (system overview) → design/ (component details) → implementation

**Maintenance:**
- Delete after implementation stabilizes (code becomes source of truth)
- Design docs are pre-implementation artifacts

**Hierarchy:** DESIGN.md (system level) → design/ (component level)

### Scaling Complexity

**Minimal (small projects, <1 month):**
```
ai/
└── STATUS.md
```

**Standard (typical projects, 1-6 months):**
```
ai/
├── STATUS.md
├── DESIGN.md
└── DECISIONS.md
```

**Complex (multi-phase, 6+ months):**
```
ai/
├── STATUS.md
├── DESIGN.md
├── DECISIONS.md
├── ROADMAP.md
├── research/
│   ├── db-comparison.md
│   └── auth-eval.md
└── design/
    └── api-v2.md
```

**Principle:** Start minimal, grow as needed. Don't create structure you don't use.

## File Purposes

| File | Question it Answers | Update Mode | When to Create |
|------|---------------------|-------------|----------------|
| **STATUS.md** | Where are we now? | Edit-in-place | Always |
| **DESIGN.md** | What are we building? | Edit-in-place | Recommended (non-trivial projects) |
| **DECISIONS.md** | Why did we choose X? | Append-only | Recommended |
| **ROADMAP.md** | What's the plan? | Edit-in-place | Situational (multi-phase) |
| **TODO.md** | What's next? | Edit-in-place | Situational (if no beads) |

**Single source of truth:**

| Information | Lives in | Not in |
|-------------|----------|--------|
| Current state, blockers | STATUS.md | anywhere else |
| System architecture | DESIGN.md | ROADMAP.md, AGENTS.md |
| Component specs | design/ | DESIGN.md |
| Decision rationale | DECISIONS.md | DESIGN.md |
| Raw research | research/ | DECISIONS.md |
| Phases, milestones | ROADMAP.md | STATUS.md |
| Tasks | beads / TODO.md | STATUS.md |

## Session Workflow

| Phase | Actions |
|-------|---------|
| **Starting** | Read STATUS.md → `bd ready` or check TODO.md → Load AGENTS.md → DESIGN.md if needed |
| **During** | Research → research/ → Synthesize to DESIGN.md → Component specs to design/ → Document decisions |
| **Ending** | Update STATUS.md → `bd sync` or update TODO.md → Prune if needed |
| **Reset (>80%)** | Compact STATUS.md → Keep essentials only |

**Reading order:** STATUS (current state) → DESIGN (architecture) → ROADMAP (if exists) → DECISIONS (rationale)

## Token Efficiency Strategy

**Goal:** Load only relevant context per session while maintaining comprehensive project knowledge

**How subdirectories help:**
1. Session files (ai/ root): Always loaded - keep current/active work only
2. Reference files (subdirs): Loaded only when needed - zero token cost unless accessed
3. AI reads STATUS.md → sees "See ai/research/db-comparison.md for details" → loads only if relevant

**Example:**

**Without subdirectories:**
```
ai/
├── STATUS.md (current state)
└── all research inline (5 detailed topics loaded every session)
Total: All research loaded every session (even if not needed)
```

**With subdirectories:**
```
ai/
├── STATUS.md (current state)
├── DESIGN.md (system overview with pointers)
└── research/
    ├── database-comparison.md (detailed analysis)
    ├── auth-eval.md (detailed analysis)
    └── performance.md (detailed analysis)
Session: Only STATUS.md and DESIGN.md loaded
Reference: Detailed research loaded only when AI needs it
```

**Best practices:**
- Keep session files focused on current/active work only
- Move detailed content to subdirectories (loaded on demand)
- Use pointers in session files: "→ Details: ai/research/topic.md"

## File Templates

### STATUS.md (Always)

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
Implementing auth (see TODO or beads) - schema complete, working on sessions

## Blockers
- AWS credentials needed for S3 (waiting on ops)

**Note:** Update EVERY session. Prune historical content (trust git).
```

### DESIGN.md (Recommended)

```markdown
## System Overview
[Brief description of what we're building]

## Architecture
```
[ASCII diagram or description of component relationships]
```

## Components

| Component | Purpose | Status |
|-----------|---------|--------|
| Auth | User authentication, sessions | Implemented |
| API | REST endpoints | In progress |
| DB | PostgreSQL with jsonb | Implemented |

## Data Flow
1. Request → API Gateway → Auth middleware
2. Auth validates session → forwards to handler
3. Handler queries DB → returns response

## Key Design Decisions
- PostgreSQL for ACID guarantees (→ DECISIONS.md for rationale)
- Redis for session cache (→ DECISIONS.md)

## Component Details
→ See ai/design/{component}.md for detailed specs

**Note:** This is system-level overview. Component specs go in design/.
```

### DECISIONS.md (Recommended)

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

## 2025-01-14: Redis for Session Cache

**Context**: Session storage approach
**Decision**: Redis over in-memory
**Rationale**: OOM issues with in-memory (see STATUS.md "What Didn't Work")

---
```

### ROADMAP.md (Situational - multi-phase only)

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

## Out of Scope
- Mobile apps (v2.0 feature)
- GraphQL (REST sufficient for v1.0)

**Note**: Only create if 3+ phases, external deadlines, or critical dependencies.
```

### TODO.md (Situational - if no beads)

```markdown
## Ready
- [ ] Fix cache invalidation bug [src/lib/cache.ts]
- [ ] Add error handling to parse_query() [src/parser/query.rs]

## In Progress
- [ ] Implement auth
  - [x] Schema design [src/db/schema.sql]
  - [ ] Session management [src/auth/session.ts]

## Blocked
- [ ] Deploy to prod (after: cache-fix, auth)
- [ ] API v2 endpoints (after: auth)

**Note:** Delete completed immediately (no "Done" section). Trust git.
```

**Dependency notation:**
- `(after: x, y)` — requires other tasks first
- `(blocks: x, y)` — this task blocks others

## ai/ File Writing Rules

**All ai/ files are for AI consumption** - optimize for machine readability, not human narrative.

| File | Format | Rules |
|------|--------|-------|
| **STATUS.md** | Tables for metrics, bullets for learnings | Current state only, date measurements |
| **DESIGN.md** | ASCII diagrams, tables for components | System-level overview, point to design/ for details |
| **DECISIONS.md** | Context → Decision → Rationale → Tradeoffs | Date entries, link evidence, append-only |
| **ROADMAP.md** | Tables for phases/dependencies | Focus: what blocks what, scope. NO time estimates |
| **TODO.md** | Checkbox lists | Ready/Blocked sections, deps inline `(after: x)` |
| **research/** | Question → Answer → Evidence | Exec summary if lengthy |
| **design/** | Spec format: API/system/protocol | Tables for parameters/endpoints |

**Key principles:**
- **Tables, lists, key-value pairs** - NO narrative prose
- **Answer first, evidence second** - conclusions up front
- **Exec summary for lengthy files** - helps AI decide if it needs full details
- **Clear ## sections** - easy navigation

### Example

❌ **Prose:** "After investigating caching, the team feels Redis would be good because it's fast..."

✅ **Structured:**
```markdown
**Decision**: Redis (2025-01-15)
**Why**: 10x faster, persistence, team expertise
**Tradeoff**: Service dependency
```

## File Maintenance

**Trust git history** - Delete old content when files grow large. Prune when files contain substantial irrelevant or historical content that wastes tokens and obscures current state.

**Remember:** ai/ is for AI session context, not permanent documentation. Permanent docs go in docs/. Historical context lives in git history.

### When to Prune

| File | Prune When | Keep |
|------|-----------|------|
| STATUS.md | Old blockers, completed work | Current metrics, active blockers, recent learnings |
| DESIGN.md | Superseded architecture | Current system design |
| DECISIONS.md | Difficult to navigate | Active decisions affecting codebase |
| ROADMAP.md | Completed phases | Current phase + next 1-2 phases |
| TODO.md | Any completed tasks | Only pending/in-progress work |

### Session Files vs Reference Files

**Session files (ai/ root):**
- Prune historical/completed content (edit-in-place, delete old)
- Read every session - keep current/active work only
- If accumulating relevant details, move to subdirectory

**Reference files (subdirs):**
- Deleted entirely when no longer relevant
- Not pruned - either useful or deleted
- No token cost unless loaded

### Promoting Learnings

**Before pruning "Recent Learnings" from STATUS.md:**
1. **Permanent project rule?** → Move to `AGENTS.md` (Standards section)
2. **Permanent codebase quirk?** → Move to `AGENTS.md` or `docs/internal/`
3. **Transient/Fixed?** → Delete

## File Hierarchy

| Level | File | Purpose | Update Mode |
|-------|------|---------|-------------|
| **Global** | `~/.claude/CLAUDE.md` | Rules for ALL projects | On workflow changes |
| **Project** | `AGENTS.md` (+ symlink `CLAUDE.md`) | Architecture, commands, project overview | On arch changes |
| **Session** | `ai/STATUS.md` | Current state | Every session |
| **Session** | `ai/DESIGN.md` | System architecture | On design changes |
| **Session** | `ai/DECISIONS.md` | Decision rationale | On decisions |
| **Session** | `ai/ROADMAP.md` | Roadmap (optional) | On phase changes |
| **Tasks** | `.beads/` or `ai/TODO.md` | Task tracking | As tasks change |
| **Reference** | `ai/research/` | External research | During research |
| **Reference** | `ai/design/` | Component specs | Pre-implementation |

## Project AGENTS.md

**AGENTS.md = primary file, CLAUDE.md → AGENTS.md = symlink for Claude Code compatibility**

**Optimized for AI consumption:**
- Use tables, lists, code blocks (machine-readable structure)
- **Concrete examples > abstract descriptions** - show actual code patterns
- Clear sections with ## headers
- Well-structured - logical organization, easy to parse
- Comprehensive - include everything AI needs to understand project
- No length limit - include what's needed, exclude what isn't

**Belongs:** Build/test/deploy commands, coding standards, architecture overview, tech stack, project overview, verification steps

**Does NOT belong:** Current issues (→ STATUS.md), system design details (→ DESIGN.md), tactical roadmap (→ ROADMAP.md), detailed research (→ ai/research/)

**Format:**
- ✅ `"See ai/DESIGN.md for system architecture"`
- ❌ `"Architecture: 1. Component A... 2. Component B..."`

## Project Config Template

```markdown
# Project Name
[Brief description]

## Structure
docs/, ai/ (STATUS.md read first, DESIGN.md for architecture)

## Stack
[Language], [Framework]

## Commands
build: [cmd]
test: [cmd]
deploy: [cmd]

## Verification Steps
Commands to verify correctness (must pass):
- Build: `npm run build` (zero errors)
- Tests: `npm test` (all pass)
- Lint: `npm run lint` (zero warnings)

## Standards
[formatting, naming, imports]

## Examples
[Concrete code patterns specific to this project]

## Current Focus
ai/STATUS.md (current state), ai/DESIGN.md (architecture)
```

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|---------------|
| All research in session files | Use research/ for details, STATUS.md for summaries |
| System design in ROADMAP.md | ROADMAP.md = phases/milestones, DESIGN.md = architecture |
| Component specs in DESIGN.md | DESIGN.md = system overview, design/ = component details |
| Create full structure on day 1 | Start with STATUS.md, add files as needed |
| Human documentation in ai/ | User docs → docs/, AI context → ai/ |
| Narrative prose in ai/ files | Tables, lists, structured content |
| Duplicate info across files | Single source of truth for each type of info |
| Code in ai/ | Code in src/, ai/ for meta-work only |
| Time estimates in ROADMAP.md | Dependencies + scope only. Add time only if external deadline |

---

**Remember:** ai/ is AI session context management, not comprehensive documentation. Goal: efficient context handoff - load only what's needed per session.
