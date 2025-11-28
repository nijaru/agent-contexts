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
│   ├── PLAN.md                 # Strategic roadmap (optional)
│   ├── TODO.md                 # Active tasks (if not using beads)
│   ├── STATUS.md               # Current state
│   ├── DECISIONS.md            # Architectural choices
│   ├── RESEARCH.md             # Research index
│   ├── KNOWLEDGE.md            # Permanent codebase quirks (optional)
│   ├── research/               # Detailed research (inputs)
│   │   └── {topic}.md
│   ├── design/                 # Design documents (outputs)
│   │   └── {component}.md
│   ├── decisions/              # Archived/split decisions
│   │   └── {topic}.md
│   └── tmp/                    # Temporary artifacts (gitignored: echo '*' > ai/tmp/.gitignore)
└── [existing project structure]
```

**Core separation:**
- **docs/** — Permanent user/team documentation (guides, API, specs)
- **ai/** — AI session context management (agent's workspace for tracking state across sessions)
- **Respect existing structure** — If project has internal/, wiki/, .github/, note in AGENTS.md and use them

**Token efficiency:** Session files in ai/ root are read every session. Reference files in subdirectories (research/, design/, decisions/) are loaded only when needed, preventing token waste on unused context.

## ai/ Directory Organization

**Purpose:** AI agent session context management - track state, decisions, and research across sessions

**Design principle:** Minimize tokens loaded per session while maintaining comprehensive context

### File Tiers

| Tier | Location | Read Frequency | Size Guideline | Purpose |
|------|----------|----------------|----------------|---------|
| **Session** | ai/*.md | Every session | <500 lines each | Current state, active work |
| **Reference** | ai/research/ | On demand | Any size | Detailed research findings |
| **Reference** | ai/design/ | On demand | Any size | Design specifications |
| **Reference** | ai/decisions/ | On demand | Archive only | Superseded/split decisions |
| **Scratch** | ai/tmp/ | On demand | Any size | Temporary artifacts, logs, diffs |

### Session Files (ai/ root)

**These are read EVERY session** - keep minimal, current, focused:

| File | Required? | When to Create | Purpose |
|------|-----------|----------------|---------|
| STATUS.md | ✅ Always | Project start | Current state, metrics, blockers |
| TODO.md | ⚠️ If no beads | If not using beads | Active tasks with dependencies |
| DECISIONS.md | ✅ Recommended | First decision | Architectural decisions |
| RESEARCH.md | ⚠️ If researching | When needed | Research index |
| KNOWLEDGE.md | ⚠️ If quirks exist | When discovering non-obvious behavior | Permanent codebase quirks |
| PLAN.md | ⚠️ Optional | 3+ phases/dependencies | Strategic roadmap |

**Principle:** Keep session files focused on current/active work. If accumulating historical/completed content, prune it. If accumulating detailed content still relevant, move to subdirectories.

### Reference Subdirectories

**Only loaded when AI needs them** - no token cost unless accessed:

#### research/ - Detailed Research Findings

**Create when:**
- Research becomes detailed/lengthy
- OR multiple research topics
- OR RESEARCH.md becoming cluttered with details

**Contents:**
- Deep dives: `ai/research/database-comparison.md`
- Benchmarks: `ai/research/performance-analysis.md`
- Technology evaluations: `ai/research/framework-evaluation.md`

**Maintenance:**
- Keep while relevant to active work
- Delete when insights consolidated to RESEARCH.md
- Reference in git if needed later: "See commit abc123d for details"

#### design/ - Design Specifications

**Create when:**
- Formal design review needed
- OR design becomes detailed/lengthy
- OR complex component requiring detailed spec

**Contents:**
- API specifications: `ai/design/rest-api-v1.md`
- System architecture: `ai/design/architecture.md`
- Protocol specs: `ai/design/websocket-protocol.md`

**Workflow:** research/ (inputs) → design/ (specifications) → code (implementation)

**Maintenance:**
- Delete after implementation stabilizes (code becomes source of truth)
- Design docs are pre-implementation artifacts

#### decisions/ - Decision Organization

**Create when:**
- DECISIONS.md becomes difficult to navigate (split by topic)
- OR many superseded decisions (archive old ones)

**Patterns:**
- `ai/decisions/superseded-YYYY-MM.md` - Archived reversed decisions
- `ai/decisions/{topic}.md` - Topic-based splits (architecture, database, etc.)

### KNOWLEDGE.md - Permanent Codebase Quirks

**Purpose:** Store non-obvious behaviors, gotchas, and permanent quirks that affect every session. Unlike STATUS.md (current state) or DECISIONS.md (why we chose X), KNOWLEDGE.md captures **how things actually behave**.

**Create when:**
- Discovering non-obvious codebase behavior
- Finding gotchas that will affect future work
- Documenting implicit requirements not in code

**Contents:**
- Race conditions, timing issues
- Implicit dependencies between components
- Non-obvious configuration requirements
- External service quirks (API rate limits, caching behaviors)
- "Magic" values or undocumented conventions

**Template:**
```markdown
# Codebase Knowledge

**Purpose:** Permanent quirks, gotchas, non-obvious behavior

| Area | Knowledge | Impact | Discovered |
|------|-----------|--------|------------|
| Auth | Session cache is 30s | Logout delay possible | 2025-01 |
| DB | Migrations must run in order | FK dependencies | 2025-01 |
| API | Rate limit resets at UTC midnight | Batch jobs should avoid 00:00 | 2025-02 |

## Details

### Auth: Session Cache (30s)
- Sessions cached in Redis for performance
- Logout doesn't invalidate immediately
- Workaround: Force cache clear on sensitive operations
```

**Maintenance:**
- Add entries when discovering quirks
- Remove when quirk is fixed in code
- Keep concise - detailed investigation goes in research/

### Scaling Complexity

**Minimal (small projects, <1 month):**
```
.beads/              # Task tracking (or ai/TODO.md if no beads)
ai/
└── STATUS.md
```

**Standard (typical projects, 1-6 months):**
```
.beads/              # Task tracking
ai/
├── STATUS.md
├── DECISIONS.md
└── RESEARCH.md
```

**Complex (multi-phase, 6+ months):**
```
.beads/              # Task tracking
ai/
├── PLAN.md
├── STATUS.md
├── DECISIONS.md
├── RESEARCH.md
├── research/
│   ├── db-comparison.md
│   └── auth-eval.md
└── design/
    └── api-v2.md
```

**Very Complex (major projects, 1+ year):**
```
.beads/              # Task tracking
ai/
├── PLAN.md
├── STATUS.md
├── DECISIONS.md
├── RESEARCH.md
├── research/
│   ├── db-comparison.md
│   ├── auth-eval.md
│   └── performance-2025-Q1.md
├── design/
│   ├── api-v1.md
│   ├── api-v2.md
│   └── data-model.md
└── decisions/
    ├── superseded-2024-12.md
    ├── architecture.md
    └── database.md
```

**Principle:** Start minimal, grow as needed. Don't create structure you don't use.

## File Purposes

| File | Purpose | Update Mode | Scope |
|------|---------|-------------|-------|
| **PLAN.md** | Dependencies, architecture, scope | Edit-in-place | Project lifecycle - optional |
| **STATUS.md** | Current state + learnings | Edit-in-place | Current session |
| **.beads/** | Task tracking (recommended) | `bd` commands | Multi-session |
| **TODO.md** | Task tracking (fallback) | Edit-in-place | Active work - if no beads |
| **DECISIONS.md** | Architectural rationale | Append-only | Permanent record |
| **RESEARCH.md** | Knowledge index | Hybrid | As needed |
| **KNOWLEDGE.md** | Codebase quirks/gotchas | Edit-in-place | Permanent (until fixed) |

**PLAN.md is optional** - Only create if project has 3+ phases, critical dependencies, or external deadlines. Focus: what blocks what, technical approach, scope boundaries. Skip time estimates unless external deadline exists.

## Session Workflow

| Phase | Actions |
|-------|---------|
| **Starting** | Review PLAN.md (if exists) → Read STATUS.md → `bd ready` or check TODO.md → Load AGENTS.md |
| **During** | Research best practices → Document in research/ → Record decisions → `bd create` for new work |
| **Ending** | Update STATUS.md → `bd close`/`bd sync` or update TODO.md → Compact if needed |
| **Reset (>80%)** | Compact STATUS.md → Keep essentials only |

**Reading order:** PLAN (strategic vision) → STATUS (current state) → `bd ready`/TODO (next actions) → DECISIONS (rationale) → RESEARCH (domain knowledge)

**Update PLAN.md:** Major pivots, phase completions, quarterly reviews. NOT every session.

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
├── TODO.md (active tasks)
└── RESEARCH.md (all research inline: 5 detailed topics)
Total: All research loaded every session (even if not needed)
```

**With subdirectories:**
```
ai/
├── STATUS.md (current state)
├── TODO.md (active tasks)
├── RESEARCH.md (index with summaries only)
└── research/
    ├── database-comparison.md (detailed analysis)
    ├── auth-eval.md (detailed analysis)
    └── performance.md (detailed analysis)
Session: Only index loaded
Reference: Detailed research loaded only when AI needs it
```

**Result:** Significant token savings by loading detailed content only when relevant to current work

**Best practices:**
- Keep session files focused on current/active work only
- Move detailed content to subdirectories (loaded on demand)
- Use indexes (RESEARCH.md, DECISIONS.md) to point to subdirectories
- Reference format: "→ Details: ai/research/topic.md"

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

### TODO.md (if not using beads)

**Note:** If using beads (`bd`), skip TODO.md. Beads provides better dependency tracking and multi-session memory.

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
```

**Dependency notation:**
- `(after: x, y)` — requires other tasks first
- `(blocks: x, y)` — this task blocks others
- Optional `[a3f8]` prefix for complex projects with many cross-references

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

**All ai/ files are for AI consumption** - optimize for machine readability, not human narrative.

| File/Directory | Format | Rules |
|----------------|--------|-------|
| **PLAN.md** | Tables for phases/dependencies/architecture | Focus: dependencies (A before B), technical approach, scope. NO time estimates unless external deadline |
| **STATUS.md** | Tables for metrics, bullets for learnings | NO prose, date measurements, current state only |
| **TODO.md** | Checkbox lists | Ready/Blocked sections, deps inline `(after: x)`, file links |
| **DECISIONS.md** | Context → Decision → Rationale → Tradeoffs (table) | Date entries, link evidence, active decisions |
| **RESEARCH.md** | Index: Topic → Finding → Link to details | Summary + pointers to research/ |
| **KNOWLEDGE.md** | Table: Area → Knowledge → Impact → Discovered | Permanent quirks only, remove when fixed |
| **research/** | Question → Answer → Evidence (tables) | Exec summary if lengthy (helps AI decide if needs full details) |
| **design/** | Spec format: API/system/protocol | Tables for parameters/endpoints, clear sections, exec summary if lengthy |
| **decisions/** | Same as DECISIONS.md | Organized by topic or superseded status |

**Key principles:**
- **Tables, lists, key-value pairs** - NO narrative prose
- **Answer first, evidence second** - conclusions up front
- **Exec summary for lengthy files** - helps AI decide if it needs full details
- **Clear ## sections** - easy navigation
- **All ai/ files follow same rules** - session files AND reference files

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
| STATUS.md | Old pivots/completed phases/resolved blockers | Current metrics, active blockers, recent learnings |
| TODO.md | Any completed tasks | Only pending/in-progress work |
| DECISIONS.md | Difficult to navigate OR many superseded | Active decisions affecting codebase |
| RESEARCH.md | Accumulating detailed research | Index with summaries, pointers to research/ |
| PLAN.md | Completed phases | Current phase + next 1-2 phases |

**Guidance:** Prune when files contain substantial **irrelevant or historical content**, not based on size. Growing files usually indicate accumulated past content that should be pruned or moved to subdirectories.

### Promoting Learnings

**Before pruning "Recent Learnings" from STATUS.md:**
1. **Permanent project rule?** → Move to `AGENTS.md` (Standards section)
2. **Permanent codebase quirk?** → Move to `ai/KNOWLEDGE.md` or `docs/internal/`
3. **Transient/Fixed?** → Delete

### Session Files vs Reference Files

**Session files (ai/ root):**
- Prune historical/completed content (edit-in-place, delete old)
- Read every session - keep current/active work only
- If accumulating relevant details, move to subdirectory

**Reference files (subdirs):**
- Deleted entirely when no longer relevant
- Not pruned - either useful or deleted
- No token cost unless loaded

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

**For topic-based splits (when becomes difficult to navigate):**
- Create `ai/decisions/architecture.md`, `ai/decisions/database.md`, etc.
- Keep index/summary in main DECISIONS.md linking to topic files
- Use when file becomes hard to navigate

**Delete entirely:** Decisions that were reversed AND have no historical value

### TODO.md: Active work only (if not using beads)

- Delete completed tasks immediately (no "Done" section)
- Git preserves completion history
- Keep only pending/in-progress work
- **Better alternative:** Use beads (`bd`) for dependency tracking and multi-session memory

### PLAN.md: Current + next phases

- Archive/delete completed phases
- Keep current phase + dependencies for next 1-2 phases
- Major pivots: update in-place, old content to git history

### research/: Consolidate or delete

- Consolidate key findings to RESEARCH.md
- Delete file when no longer relevant
- Reference commit hash if needed later: "See abc123d for auth research"

### design/: Optional design documents

**Purpose:** Design documents and specifications (API designs, system designs, protocol specs). These are outputs from research that document concrete design decisions before implementation.

**Workflow:** research/ (inputs/findings) → design/ (specifications) → implementation

**When to use:**
- Documenting API designs before implementation
- System architecture specifications
- Protocol or data format specifications
- Complex component designs requiring review

**Example:** `ai/research/python_api_research.md` (compared 6 different API approaches) → `ai/design/python_api.md` (concrete specification for our API design)

**Maintenance:** Delete or archive to git history when implemented and stabilized. Design docs are pre-implementation artifacts; once code exists, it becomes the source of truth.

**Principle:** Files should efficiently answer "what's current?" without loading substantial irrelevant historical content. Prune when old content dominates token usage or obscures current state.

## File Hierarchy

| Level | File | Purpose | Update Mode |
|-------|------|---------|-------------|
| **Global** | `~/.claude/CLAUDE.md` | Rules for ALL projects | On workflow changes |
| **Project** | `AGENTS.md` (+ symlink `CLAUDE.md`) | Architecture, commands, project overview | On arch changes |
| **Strategic** | `ai/PLAN.md` | Roadmap (optional) | Quarterly/pivots |
| **Session** | `ai/STATUS.md` | Current state | Every session |
| **Tasks** | `.beads/` | Task tracking (recommended) | `bd` commands |
| **Tasks** | `ai/TODO.md` | Task tracking (fallback) | As tasks change |
| **Append** | `ai/DECISIONS.md` | Decisions | On decisions |
| **Research** | `ai/RESEARCH.md` | Findings | During research |

## Project AGENTS.md

**AGENTS.md = primary file, CLAUDE.md → AGENTS.md = symlink for Claude Code compatibility**

**Optimized for AI consumption:**
- Use tables, lists, code blocks (machine-readable structure)
- **Concrete examples > abstract descriptions** - show actual code patterns
- Clear sections with ## headers
- Well-structured - logical organization, easy to parse
- Comprehensive - include everything AI needs to understand project
- No length limit - include what's needed, exclude what isn't

**Belongs:** Build/test/deploy commands, coding standards, architecture, tech stack, project overview, verification steps

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

## Verification Steps
Commands to verify correctness (must pass):
- Build: `npm run build` (zero errors)
- Tests: `npm test` (all pass)
- Lint: `npm run lint` (zero warnings)

## Standards
[formatting, naming, imports]

## Examples
[Concrete code patterns specific to this project]

## Deprecated Patterns
| ❌ Don't Use | ✅ Use Instead | Why |
|-------------|---------------|-----|
| [old pattern] | [new pattern] | [reason] |

## Current Focus
ai/STATUS.md (current state), ai/PLAN.md (roadmap)
```

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|---------------|
| Detailed research in RESEARCH.md (wastes tokens every session) | Use research/ for detailed research, RESEARCH.md as index |
| All decisions in DECISIONS.md when hard to navigate | Split to decisions/{topic}.md or archive superseded |
| Detailed content in session files | Move to subdirectories (loaded on demand) |
| Create full structure on day 1 | Start minimal, add subdirs as needed |
| Human documentation in ai/ | User docs → docs/, AI context → ai/ |
| Narrative prose in ai/ files | Tables, lists, structured content (all ai/ files) |
| Artificial time tracking files (WEEK*_DAY*.md) | Update STATUS.md in-place, trust git history. Real dates okay (ANALYSIS_2025-11-05.md) |
| Duplicate docs/ and ai/ | docs/ = permanent, ai/ = session context |
| Code in ai/ | Code in src/, ai/ for meta-work only |
| Time estimates in PLAN.md ("~3-4 days", "Q1 2025") | Dependencies + scope. Add time only if external deadline exists |
| Progress tracking ("Week X Day Y") in PLAN.md | Use git log for timeline, STATUS.md for current state |
| PLAN.md for simple projects | Only if 3+ phases/dependencies/deadlines |
| Language/tool pattern docs | Research current best practices |
| Duplicate ai/ content in AGENTS.md | Brief pointers to ai/, keep AGENTS.md well-structured |

## Token Optimization

**Session files (read every time):**
- Keep current/active content only (prune completed/historical)
- Update in-place, don't append (edit STATUS.md, don't add to bottom)
- Delete completed/historical content (trust git history)
- Use tables/bullets over prose

**Reference files (read on demand):**
- Move detailed research to ai/research/ (keep RESEARCH.md as index)
- Move design specs to ai/design/ when detailed/formal
- Archive superseded decisions to ai/decisions/superseded-YYYY-MM.md
- Split DECISIONS.md by topic when becomes difficult to navigate

**Structure decisions:**
- Skip PLAN.md if project doesn't need it (3+ phases/dependencies)
- Start with minimal structure (STATUS + TODO), grow as needed
- Create subdirectories when helpful for organizing detailed/reference content

---

**Remember:** ai/ is AI session context management, not comprehensive documentation. Goal: efficient context handoff - load only what's needed per session.
