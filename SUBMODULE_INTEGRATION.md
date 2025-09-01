# Submodule Integration for AI Agent Context

*Patterns for integrating agent-contexts repository into projects*

## PATTERN: Add as Submodule
```bash
# In your project repository
git submodule add https://github.com/username/agent-contexts external/agent-contexts
git submodule update --init --recursive
```

## PATTERN: AI Agent Integration
```bash
# Structure in your project:
project/
├── src/
├── docs/
└── external/
    └── agent-contexts/          # This repo as submodule
        ├── AI_AGENT_INDEX.md    # Navigation for AI agents
        ├── ERROR_PATTERNS.md    # Error resolution
        └── standards/           # Universal patterns
```

## USAGE PATTERNS FOR AI AGENTS

### Pattern: Project Setup with Context
```bash
# Initial setup
git clone --recurse-submodules your-project-repo
cd your-project

# AI agent can access context files:
@external/agent-contexts/AI_AGENT_INDEX.md      # Navigation
@external/agent-contexts/ERROR_PATTERNS.md      # Error patterns
@external/agent-contexts/standards/AI_CODE_PATTERNS.md  # Code patterns
```

### Pattern: Context Updates
```bash
# Update agent context in project
git submodule update --remote external/agent-contexts
git add external/agent-contexts
git commit -m "Update AI agent context patterns"
```

### Pattern: Language-Specific Context
```bash
# For Mojo projects, also include:
@external/agent-contexts/languages/mojo/AI_PATTERNS.md
@external/agent-contexts/languages/mojo/advanced/

# For projects using JJ version control:
@external/agent-contexts/standards/JJ_DECISION_TREES.md
```

## PROJECT INTEGRATION EXAMPLES

### Example: CLAUDE.md in Your Project
```markdown
# Your Project Context

@external/agent-contexts/AI_AGENT_INDEX.md     # Start here

## Project-Specific Patterns
- Build commands: `npm run build` or `mojo build`
- Test commands: `pytest tests/` or `mojo test`  
- Lint commands: `eslint src/` or `ruff check`

## Context Loading by Task
IF mojo_development:
    @external/agent-contexts/languages/mojo/AI_PATTERNS.md
IF error_debugging:
    @external/agent-contexts/ERROR_PATTERNS.md
IF version_control:
    @external/agent-contexts/standards/JJ_DECISION_TREES.md
```

### Example: GitHub Actions Integration
```yaml
# .github/workflows/ci.yml
- name: Checkout with submodules
  uses: actions/checkout@v4
  with:
    submodules: recursive

- name: Update agent context  
  run: git submodule update --remote external/agent-contexts
```

## DECISION TREES

### Choose Integration Method
```
IF single_project AND small_team:
    → Copy relevant files directly to docs/
IF multiple_projects AND shared_patterns:
    → Use submodule integration (recommended)
IF evolving_patterns AND need_updates:
    → Use submodule with regular updates
```

### Choose Context Files
```
IF general_development:
    → AI_AGENT_INDEX.md + ERROR_PATTERNS.md + standards/
IF language_specific:
    → Add languages/{language}/ directory
IF specialized_tools:
    → Add tools/{tool}/ directory  
```

## MAINTENANCE PATTERNS

### Pattern: Keep Context Updated
```bash
# Weekly context update
git submodule foreach git pull origin main
git add .
git commit -m "Update AI agent context patterns"
```

### Pattern: Context Versioning
```bash
# Pin to specific version for stability
cd external/agent-contexts
git checkout v1.2.0
cd ../..
git add external/agent-contexts
git commit -m "Pin agent context to v1.2.0"
```