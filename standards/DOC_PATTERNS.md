# Documentation Patterns

*Universal decision trees for AI agent documentation organization*

## AI Context File Standards (2025)

### Primary Context Files
```
IF new_project_2025+ → AGENTS.md (industry standard)
IF multiple_ai_tools → AGENTS.md (universal)
IF claude_code_only → CLAUDE.md or AGENTS.md
IF cursor_ai → .cursorrules or .cursor/rules/*.mdc
IF github_copilot → .github/prompts/*.prompt.md
IF supporting_all → AGENTS.md + tool-specific symlinks
```

### Context File Hierarchy
```
Root Level:
├── AGENTS.md              # Universal AI context (primary)
├── CLAUDE.md             # Symlink to AGENTS.md (compatibility)
├── .cursorrules          # Legacy Cursor (migrating to .cursor/)
├── .cursor/
│   └── rules/*.mdc       # Modern Cursor rules
├── .claude/
│   ├── commands/*.md     # Claude custom commands
│   └── rules.md          # Claude-specific rules
└── .github/
    └── prompts/*.prompt.md  # Copilot prompt files
```

## Universal Content Structure

### AGENTS.md Essential Sections
```
IF setup_instructions → ## Development Setup
IF coding_standards → ## Code Conventions
IF testing_requirements → ## Testing
IF build_instructions → ## Build & Deploy
IF commit_guidelines → ## Git Workflow
IF project_specific → ## Project Context
IF examples_available → ## Examples
```

### Context Engineering Patterns
```
IF providing_context:
    IF task_specific → Include only relevant files
    IF complex_task → Break into subtasks with focused context
    IF pattern_based → Include examples/ directory
    IF error_fixing → Include error logs and stack traces
    IF refactoring → Include current + desired patterns
```

### Content Optimization
```
IF context_too_large → Remove verbose comments, focus on patterns
IF context_too_small → Add examples, include related files
IF ambiguous_requirements → Add success criteria, test cases
IF multiple_frameworks → Specify versions and constraints
```

## Tool-Specific Patterns

### Claude Code (.claude/)
```
IF custom_commands → .claude/commands/{name}.md
IF project_rules → CLAUDE.md or AGENTS.md
IF team_sharing → Commit .claude/ to version control
IF personal_prefs → ~/.claude/commands/ (global)
```

### Cursor AI (.cursor/)
```
IF project_rules → .cursor/rules/*.mdc
IF file_scoping → Use glob patterns in .mdc files
IF team_consistency → Share .cursor/ in repository
IF legacy_project → Migrate .cursorrules to .cursor/
```

### GitHub Copilot (.github/)
```
IF prompt_templates → .github/prompts/*.prompt.md
IF workspace_context → Use @workspace in chat
IF knowledge_base → Configure documentation collections
IF enterprise → Use Copilot Spaces for shared context
```

## AI Work Tracking Patterns

### Progress Documentation
```
IF tracking_current_tasks:
    → internal/TODO.md - Active tasks for AI agent
IF tracking_project_status:
    → internal/STATUS.md - Current state, what's been done, what worked/didn't
IF researching_external_topics:
    → internal/RESEARCH.md - Algorithm research, system design, best practices
IF tracking_releases:
    → CHANGELOG.md - Public release history (root level)
```

### File Structure for AI Context Persistence
```
Root Level (Public):
├── README.md        # Project overview
├── CHANGELOG.md     # Release history (follows keepachangelog.com)
├── LICENSE          # Legal

internal/ (AI Agent Working Context):
├── TODO.md          # Active tasks and priorities (edit in place)
├── STATUS.md        # Current state, progress, what worked/didn't (edit in place)
├── RESEARCH.md      # External research: algorithms, architectures, best practices (append findings)
├── DECISIONS.md     # Architectural decisions (append-only, never delete)
└── research/        # Deep topic investigations
    └── {topic}.md   # Specific research threads (e.g., indexing-algorithms.md)
```

### TODO.md Pattern (internal/)
```markdown
## Active Development Tasks
_Updated: YYYY-MM-DD_

### High Priority
- [ ] Task with specific success criteria
- [ ] Blocking issue that needs resolution

### In Progress
- [ ] Feature being developed
  - [x] Subtask completed
  - [ ] Subtask pending

### Backlog
- [ ] Future improvements

### Completed This Session
- [x] What was finished (move to STATUS.md periodically)
```

### STATUS.md Pattern (internal/)
```markdown
## Project Status
_Last Updated: YYYY-MM-DD_
_Update Mode: Edit in place - represents current truth_

### Current State
- Performance: X req/s (measured on date)
- Test Coverage: X%
- Build: Passing/Failing

### Recent Progress
- Completed: [what was done this week]
- Implemented: [feature that now works]

### What Worked
- Approach X improved performance by Y%
- Pattern Z solved the concurrency issue

### What Didn't Work
- Attempted [approach] but [why it failed]
- Tried [solution] but [limitation discovered]

### Active Work
Currently implementing [feature]

### Blockers
- Issue description and impact
```

### RESEARCH.md Pattern (internal/)
```markdown
## External Research & Best Practices
_Update Mode: Append new findings, update summaries_

### Database Indexing Algorithms
#### B-Tree vs LSM Tree (researched YYYY-MM-DD)
- **Source**: [paper/article/link]
- **Key Finding**: LSM better for write-heavy workloads
- **Relevance**: Our use case is 80% writes
- **Decision**: Implement LSM-based index

### Web App Architecture Patterns
#### Microservices vs Monolith (researched YYYY-MM-DD)
- **Sources**: [links to articles, papers]
- **Key Findings**: Microservices add complexity for <10 devs
- **Our Context**: 3-person team
- **Recommendation**: Start monolith, prepare for extraction

### Open Research Questions
- [ ] Optimal cache eviction strategy for our access patterns
- [ ] Comparison of WebSocket vs SSE for our real-time needs
```

### DECISIONS.md Pattern (internal/)
```markdown
## Architectural Decision Log
_Append-only - never delete past decisions_

### YYYY-MM-DD: Choose PostgreSQL over MongoDB
**Context**: Need to select primary database
**Decision**: PostgreSQL
**Rationale**:
- Strong consistency requirements
- Complex relational queries needed
- Team expertise with SQL
**Consequences**: Need to handle JSON data carefully
---

### YYYY-MM-DD: Adopt Event Sourcing for Audit Trail
**Context**: Regulatory requirement for complete audit history
**Decision**: Implement event sourcing pattern
**Rationale**:
- Immutable event log satisfies compliance
- Enables temporal queries
**Tradeoffs**: Increased storage, complexity
```

### CHANGELOG.md Pattern (root level)
```markdown
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - YYYY-MM-DD
### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes
```
**Note**: CHANGELOG.md is for public releases, not daily notes

## Documentation Organization

### File Placement Decision Trees
```
IF ai_agent_context → Root level (AGENTS.md)
IF internal_tracking → internal/ subdirectory
IF strategic_docs → Root level (ROADMAP.md, STRATEGY.md)
IF component_docs → {component}/README.md
IF research_notes → internal/research/
IF workflow_templates → patterns/ or templates/
```

### Naming Conventions
```
IF ai_context → AGENTS.md (standard) or CLAUDE.md (legacy)
IF strategic_document → ALL_CAPS.md
IF internal_tracking → internal/ALL_CAPS.md
IF technical_docs → kebab-case.md
IF component_docs → README.md
IF prompt_files → *.prompt.md
IF rule_files → *.mdc or *.rules
```

## File Transition Patterns

### Migrating to AGENTS.md
```
IF has_CLAUDE_md_only:
    → mv CLAUDE.md AGENTS.md
    → ln -s AGENTS.md CLAUDE.md
IF has_cursorrules_only:
    → Create AGENTS.md with content
    → Keep .cursorrules for compatibility
IF has_multiple_configs:
    → Consolidate to AGENTS.md
    → Create tool-specific symlinks/references
```

### Content Consolidation
```
IF scattered_instructions:
    → Merge into AGENTS.md sections
IF duplicate_rules:
    → Single source in AGENTS.md
    → Reference from tool configs
IF outdated_patterns:
    → Archive to internal/archive/
```

## Best Practices

### Context Quality
```
IF adding_context:
    → Include "why" not just "what"
    → Add examples of good patterns
    → Specify anti-patterns to avoid
    → Keep descriptions concise
    → Use decision trees over prose
```

### Team Collaboration
```
IF team_project:
    → Commit AGENTS.md to repository
    → Document in onboarding guides
    → Review in code reviews
    → Update with major changes
    → Version control all AI configs
```

### Performance Optimization
```
IF slow_ai_responses:
    → Reduce irrelevant context
    → Split large files into sections
    → Use file references vs inline
    → Archive old documentation
    → Index frequently used patterns
```

## Examples Directory Pattern

```
examples/
├── api-calls/       # Request/response patterns
├── components/      # UI component examples
├── tests/          # Test structure patterns
└── workflows/      # Common task sequences
```

**Critical**: AI agents perform significantly better with examples to follow. Include representative patterns even if minimal.

## Document Maintenance Patterns

### Document Metadata
```markdown
# Document Title

**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD
**Status**: Active | Historical | Superseded
**Superseded By**: [filename] (if applicable)

---
```

**Why this matters for AI**:
- Agents can quickly assess document relevance
- Clear status prevents outdated info usage
- Dates enable time-based filtering
- Supersession tracking prevents confusion

### Single Source of Truth Principle

```
❌ ANTI-PATTERN: Multiple competing documents
internal/STATUS_OLD.md
internal/STATUS_NEW.md
internal/STATUS_LATEST.md
internal/CURRENT_STATUS.md

✅ CORRECT: Versioned with clear successor
internal/STATUS_REPORT_OCT_2025.md     # Current
internal/STATUS_REPORT_SEP_2025.md     # Historical (marked as superseded)
internal/archive/STATUS_AUG_2025.md    # Archived
```

### Version Strategy for Status Docs
```
IF monthly_updates:
    → STATUS_REPORT_MMM_YYYY.md format
    → Mark old ones as "Superseded by: ..."
    → Archive >3 months old

IF continuous_updates:
    → Single STATUS.md (edit in place)
    → Git history tracks changes
    → No versioned files

IF major_milestones:
    → Milestone-based naming (STATUS_V2_COMPLETE.md)
```

### Session Documentation Pattern
```markdown
# Session Summary - [Topic]

**Date**: YYYY-MM-DD
**Duration**: X hours
**Focus**: Brief description

## What We Built
- Feature 1: Description + impact
- Feature 2: Description + impact

## Key Decisions
1. Decision: Rationale and alternatives considered
2. Decision: Why this approach over others

## Results
- Benchmark: X% improvement
- Tests: Added N tests, all passing
- Performance: Changed from X to Y

## Learnings
- What worked well
- What didn't work
- What to avoid next time

## Next Steps
- [ ] Follow-up task 1
- [ ] Follow-up task 2
```

**When to create**: After sessions >2 hours or major milestones

### Document Update Triggers

```
UPDATE documentation WHEN:
- Major milestone achieved
- Architecture changes significantly
- Performance characteristics change >20%
- API contracts modified
- New competitive advantages validated

DO NOT update for:
- Minor code refactoring (implementation details)
- Internal variable renames
- Small bug fixes
- Cosmetic changes
```

### Archival Policy

```
ARCHIVE documents when:
1. **Superseded**: New version exists
2. **Completed**: Milestone docs after completion
3. **Obsolete**: Plans that were changed/abandoned
4. **Historical**: >3 months old and not referenced

HOW to archive:
1. Add "Superseded by: [new_file]" to header
2. git mv old_doc.md internal/archive/category/
3. Update references to point to new doc
4. Keep in git - DON'T delete (git history isn't enough)
```

### Cross-Reference Patterns

```markdown
## Related Documentation
- Technical details: [Architecture](../technical/ARCHITECTURE.md)
- Performance data: [Benchmarks](../research/BENCHMARKS.md)
- Next steps: [Roadmap](../business/ROADMAP.md)
```

**Use relative links** - Git moves preserve them

### Documentation Hierarchy

```
IF project_overview → README.md (root)
IF AI_context → AGENTS.md (root)
IF user_documentation → docs/ (external docs)
IF developer_docs → ARCHITECTURE.md, CONTRIBUTING.md (root)
IF internal_strategy → internal/ (not for external users)
IF research_notes → internal/research/ (findings, analysis)
IF business_strategy → internal/business/ (funding, market)
IF technical_decisions → internal/technical/ (architecture)
```

## AI-Friendly Writing Patterns

### Decision Trees Over Prose
```
❌ LESS EFFECTIVE (prose):
"When you encounter a performance issue, you should first try profiling
the application to identify bottlenecks. After that, consider whether
the issue is CPU-bound or I/O-bound..."

✅ MORE EFFECTIVE (decision tree):
IF performance_issue:
    THEN profile_application
    IF cpu_bound:
        → Check algorithm complexity
        → Add caching
    ELIF io_bound:
        → Batch operations
        → Add connection pooling
```

### Explicit "Why" Over Implicit "What"
```
❌ LESS HELPFUL:
"Use Arc<RwLock<T>> for shared mutable state"

✅ MORE HELPFUL:
"Use Arc<RwLock<T>> for shared mutable state
WHY: Arc enables multi-threaded sharing, RwLock allows concurrent reads
ALTERNATIVE: If single-threaded, use Rc<RefCell<T>> (cheaper)"
```

### Examples Required for Complex Patterns
```
Every pattern should include:
1. Description of pattern
2. When to use it
3. When NOT to use it
4. Example (code or structure)
5. Common mistakes to avoid
```

## Documentation Quality Checklist

```
BEFORE committing documentation:
[ ] Dates are current
[ ] Status is accurate (Active/Historical/Superseded)
[ ] Cross-references work
[ ] Examples are representative
[ ] Decision trees use consistent format
[ ] No project-specific secrets or credentials
[ ] Markdown formatting is valid
[ ] Links are relative (not absolute)
```