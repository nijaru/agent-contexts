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
IF tracking_current_work:
    → internal/NOW.md - Active tasks, current approach
IF tracking_attempts:
    → internal/TRIED.md - What failed and why (append-only)
IF tracking_discoveries:
    → internal/KNOWLEDGE.md - What worked, patterns found
IF blocking_issues:
    → internal/BLOCKERS.md - Current obstacles, dependencies
```

### File Structure for AI Context Persistence
```
internal/
├── NOW.md           # Current sprint/active work
├── TRIED.md         # Failed attempts (prevent repetition)
├── KNOWLEDGE.md     # Discovered patterns, solutions
├── BLOCKERS.md      # Active impediments
└── research/        # Deep dives, investigations
    └── {topic}.md   # Specific research threads
```

### NOW.md Pattern
```markdown
## Current Focus: [Main Goal]
Started: YYYY-MM-DD

### Active Tasks
- [ ] Task with specific success criteria
- [x] Completed subtask

### Approach
Current strategy and why chosen

### Next Steps
Immediate actions after current task
```

### TRIED.md Pattern (Append-Only)
```markdown
## YYYY-MM-DD: [Approach Name]
**What**: Brief description
**Why Failed**: Root cause
**Learning**: Key insight
---
```

### KNOWLEDGE.md Pattern
```markdown
## [Pattern/Solution Name]
**Context**: When this applies
**Solution**: What works
**Evidence**: Metrics/proof
**Applied**: Where used successfully
```

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