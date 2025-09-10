# Documentation Patterns

*Decision trees for AI agent documentation organization*

## AI Context File Naming

```
IF using_multiple_ai_tools → AGENTS.md (universal standard)
IF claude_code_only → CLAUDE.md (legacy)
IF supporting_both → AGENTS.md (primary) + CLAUDE.md (symlink)
```

### File Transition Decision Trees

#### Current State Detection
```
IF [ -L CLAUDE.md ] && [ -f AGENTS.md ] → Already configured correctly
IF [ -L AGENTS.md ] && [ -f CLAUDE.md ] → Reverse symlink setup
IF [ -f CLAUDE.md ] && [ -f AGENTS.md ] → Both exist as files
IF [ -f CLAUDE.md ] && [ ! -f AGENTS.md ] → Only CLAUDE exists
IF [ ! -f CLAUDE.md ] && [ -f AGENTS.md ] → Only AGENTS exists  
IF [ ! -f CLAUDE.md ] && [ ! -f AGENTS.md ] → Neither exists
```

#### Actions by State
```
IF already_configured_correctly → No action needed
IF reverse_symlink_setup → rm AGENTS.md && ln -s CLAUDE.md AGENTS.md
IF both_exist_as_files → diff CLAUDE.md AGENTS.md, merge if needed
IF only_CLAUDE_exists → mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md
IF only_AGENTS_exists → ln -s AGENTS.md CLAUDE.md
IF neither_exists → Create AGENTS.md first, then ln -s AGENTS.md CLAUDE.md
```

#### Content Conflict Resolution
```
IF files_identical → rm CLAUDE.md && ln -s AGENTS.md CLAUDE.md
IF CLAUDE_newer → mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md  
IF AGENTS_newer → rm CLAUDE.md && ln -s AGENTS.md CLAUDE.md
IF files_different → Manual merge required - review both files
```

## Hierarchical Documentation Pattern

```
AGENTS.md (entry point - always read first)
    ↓
Key Files (always check/update):
- internal/NOW.md - Current tasks & sprint
- internal/DECISIONS.md - Major decisions (append-only) 
- internal/KNOWLEDGE.md - Patterns & learnings
    ↓
Detail Files (load when needed):
- internal/WORKAROUNDS.md - Known issues & fixes
- internal/IMPLEMENTATION.md - Feature guides
    ↓
Research Files (reference for decisions):
- internal/research/ - Background & analysis
```

## File Placement Decision Trees

### Greenfield Projects
```
IF ai_context → AGENTS.md
IF strategic_planning → ROADMAP.md, STRATEGY.md
IF current_work → internal/NOW.md
IF decision_tracking → internal/DECISIONS.md
```

### Existing Projects
```
IF has_docs_directory → docs/internal/
IF has_planning_docs → Add internal/ subdirectory
IF scattered_md_files → Consolidate by type:
    - Strategy docs → Root level
    - Work tracking → internal/
    - Component docs → component/README.md
```

## Naming Decision Trees

```
IF strategic_document → ALL_CAPS.md (ROADMAP.md, STRATEGY.md)
IF ai_context_file → AGENTS.md or CLAUDE.md  
IF internal_tracking → internal/ALL_CAPS.md (internal/NOW.md, internal/DECISIONS.md)
IF technical_documentation → kebab-case.md (api-reference.md)
IF component_documentation → README.md
```

## AI Context Loading Patterns

```
IF creating_agents_file → Include navigation hierarchy
IF loading_context → Use @filepath references
IF organizing_content → Separate current from archived  
IF writing_index_files → Keep under 50 lines
IF documenting_patterns → Use decision trees over explanations
```