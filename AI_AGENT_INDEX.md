# AI Agent Pattern Index

*Optimized navigation for AI agent decision making*

## QUICK DECISION TREES

### Primary Task Router
```
IF error_encountered:
    → standards/ERROR_PATTERNS.md           # Error → solution mappings
IF code_organization:
    → standards/AI_CODE_PATTERNS.md         # Naming, structure, AI patterns
IF documentation_setup:
    → standards/DOC_PATTERNS.md             # AGENTS.md setup, file organization
IF language_specific:
    → languages/{language}/*_PATTERNS.md    # Language-specific patterns
IF tool_specific:
    → tools/{tool}/*_PATTERNS.md           # Tool command sequences
```

### Language Selection
```
IF python_development:
    → languages/python/PYTHON_PATTERNS.md   # Modern Python 3.10+ with UV
IF go_development:
    → languages/go/GO_PATTERNS.md           # Concurrency, testing, performance
IF mojo_development:
    → languages/mojo/MOJO_PATTERNS.md       # Memory, performance, type conversions
```

### Tool Selection
```
IF version_control:
    → tools/jj/JJ_PATTERNS.md               # JJ version control workflows
IF github_integration:
    → tools/github/GITHUB_PATTERNS.md      # Projects vs Issues patterns
IF python_packages:
    → tools/python/UV_PATTERNS.md          # UV package management
IF modular_build:
    → tools/modular/BUILD_PATTERNS.md      # Bazel/Pixi build patterns
```

## UNIVERSAL PATTERNS (Always Load)

### Core Standards
- **standards/AI_CODE_PATTERNS.md** - Code organization, naming, AI context engineering
- **standards/ERROR_PATTERNS.md** - Error message → solution mappings
- **standards/DOC_PATTERNS.md** - Documentation organization, AGENTS.md setup

## SPECIALIZED PATTERNS

### Language Patterns
```
languages/
├── go/GO_PATTERNS.md         # Error handling, concurrency, testing
├── mojo/MOJO_PATTERNS.md     # Memory management, FFI, performance
└── python/PYTHON_PATTERNS.md # Async, type hints, UV, modern features
```

### Tool Patterns
```
tools/
├── github/GITHUB_PATTERNS.md  # Projects workflow, TodoWrite sync
├── jj/JJ_PATTERNS.md          # Bookmark management, conflict resolution
├── modular/BUILD_PATTERNS.md  # Bazel wrapper, Pixi tasks
└── python/UV_PATTERNS.md      # Package management, virtual envs
```

## PATTERN CATEGORIES

### Decision Trees
```
IF condition:
    → action/command
ELIF other_condition:
    → alternative_action
```
Used for: Navigation, tool selection, error diagnosis

### Error → Solution Mappings
```
| Error Message | Root Cause | Fix |
|---------------|------------|-----|
```
Used for: Quick error resolution, debugging

### ❌ WRONG vs ✅ CORRECT
```
❌ Anti-pattern example
✅ Correct pattern example
```
Used for: Best practices, common mistakes

### Command Sequences
```bash
# Step 1: Description
command1
# Step 2: Description
command2
```
Used for: Automation, workflows

## LOADING STRATEGY

### For New Tasks
1. Load `AI_AGENT_INDEX.md` (this file)
2. Follow decision tree to specific patterns
3. Load identified pattern files
4. Apply patterns to task

### For Error Resolution
1. Load `standards/ERROR_PATTERNS.md`
2. Search for error message
3. Apply fix pattern
4. If language-specific, load language patterns

### For Code Writing
1. Load `standards/AI_CODE_PATTERNS.md`
2. Load language-specific patterns
3. Apply naming conventions and structure
4. Use ❌ WRONG vs ✅ CORRECT examples

## OPTIMIZATION RULES

- **Load only what's needed** - Don't load all patterns
- **Universal first** - Standards apply everywhere
- **Specific second** - Language/tool patterns override
- **Decision trees guide** - Follow IF/THEN logic
- **Examples matter** - AI performs better with patterns

## QUICK REFERENCE

### Most Used Patterns
1. `standards/ERROR_PATTERNS.md` - Debugging
2. `standards/AI_CODE_PATTERNS.md` - Code quality
3. `languages/python/PYTHON_PATTERNS.md` - Python dev
4. `languages/mojo/MOJO_PATTERNS.md` - Mojo specifics
5. `tools/jj/JJ_PATTERNS.md` - Version control

### Pattern Priority
1. Error resolution (immediate fixes)
2. Code organization (quality patterns)
3. Language specifics (syntax/features)
4. Tool workflows (commands/automation)

---
*Start here → Follow trees → Load patterns → Execute tasks*