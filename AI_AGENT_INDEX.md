# AI Agent Pattern Index

*Optimized lookup for AI agent decision making*

## QUICK DECISION TREES

### Choose Documentation by Task Type
```
IF error_encountered:
    → ERROR_PATTERNS.md                    # Universal error → solution mapping
IF code_organization_task:
    → standards/AI_CODE_PATTERNS.md        # Universal naming/structure patterns
IF version_control_needed:
    → standards/JJ_DECISION_TREES.md       # VCS workflow decisions
IF github_project_management:
    → GITHUB_PROJECTS.md                   # AI agent GitHub integration
IF language_specific_task:
    → languages/{language}/                # Language-specific patterns
IF tool_specific_task:  
    → tools/{tool}/                        # Tool-specific command sequences
IF build_system_task:
    → tools/modular/BUILD_PATTERNS.md      # Bazel/Pixi patterns
```

### Choose Documentation by Language
```
IF working_with_mojo:
    → languages/mojo/MOJO_PATTERNS.md      # Consolidated Mojo patterns
    → languages/mojo/CODING_ASSISTANT_INTEGRATION.md  # AI setup
IF working_with_python:
    → languages/python/python-3-13.md      # Python 3.13 patterns
    → tools/python/uv/uv.md                # UV package manager
IF working_with_go:
    → languages/go/go-1-23.md              # Go 1.23 patterns
```

### Choose by Context Type
```
IF setting_up_workflow:
    → standards/JJ_DECISION_TREES.md       # VCS workflow
    → standards/AI_CODE_PATTERNS.md        # Code standards
    → GITHUB_PROJECTS.md                   # Project tracking
IF debugging_issue:
    → ERROR_PATTERNS.md                    # Error diagnosis
    → languages/mojo/MOJO_PATTERNS.md      # Mojo-specific fixes
IF optimizing_performance:
    → languages/mojo/MOJO_PATTERNS.md      # Performance patterns
IF integrating_ai_assistant:
    → languages/mojo/CODING_ASSISTANT_INTEGRATION.md  # Setup guides
    → tools/modular/BUILD_PATTERNS.md      # Build commands
```

## PATTERN TYPES BY FILE

### `ERROR_PATTERNS.md` - Error Recognition
- Compilation error → fix mappings
- Runtime error → diagnostic commands  
- Performance issue → optimization patterns
- Recovery procedures for common mistakes

### `GITHUB_PROJECTS.md` - AI GitHub Integration
- TodoWrite ↔ GitHub issue sync
- AI session management patterns
- Automated project board updates
- Decision trees for issue creation

### `standards/JJ_DECISION_TREES.md` - Version Control Logic
- AI agent workflow decisions
- Command sequences for common scenarios
- State recognition patterns
- Emergency recovery procedures

### `standards/AI_CODE_PATTERNS.md` - Code Organization  
- Naming decision trees
- Anti-pattern recognition  
- Code smell → fix mappings
- File organization logic
- Comment patterns and dev notes

### `languages/mojo/AI_PATTERNS.md` - Mojo-Specific
- Type conversion patterns
- Memory management decisions
- Function type selection logic
- Performance optimization triggers

### `languages/mojo/CODING_ASSISTANT_INTEGRATION.md` - AI Setup
- llms.txt documentation selection
- Cursor/Claude Code configuration
- Error resolution strategies
- Context loading patterns

### `tools/modular/BUILD_PATTERNS.md` - Build Systems
- Bazel command patterns
- Pixi task discovery
- Environment setup decisions
- Git commit formats

## CORE AI AGENT DECISION TREES

### DECISION: Task Complexity Assessment
```
IF single_file_change AND < 50_lines:
    → Work directly, use TodoWrite for tracking
ELIF multiple_files OR > 100_lines:
    → Create GitHub issue for tracking
    → Use TodoWrite for subtasks
ELIF collaborative_work OR needs_review:
    → Create GitHub issue + PR workflow
ELSE:
    → Use TodoWrite only
```

### DECISION: Documentation Loading Strategy
```
IF starting_fresh:
    → Load AI_AGENT_INDEX.md first
    → Follow specific paths based on task
ELIF fixing_error:
    → Load ERROR_PATTERNS.md + language-specific
ELIF optimizing_code:
    → Load performance patterns + benchmarks
ELIF setting_up_project:
    → Load integration guides + build patterns
```

### DECISION: Session Management
```
IF new_session:
    → Check for existing GitHub issues
    → Load relevant context files
    → Initialize TodoWrite from issues
ELIF resuming_session:
    → Sync TodoWrite with GitHub
    → Check for upstream changes
    → Continue from last state
ELIF ending_session:
    → Sync completed todos to GitHub
    → Update issue statuses
    → Document blockers
```

## USAGE PATTERNS FOR AI AGENTS

### Pattern: Starting New Task
```
SEQUENCE:
1. Check AI_AGENT_INDEX.md for relevant docs
2. Load specific pattern files based on task type  
3. Apply decision trees to current context
4. Execute command sequences as needed
5. Refer to error patterns if issues arise
```

### Pattern: Error Resolution
```
SEQUENCE:
1. Identify error message/symptoms
2. Check ERROR_PATTERNS.md for mapping
3. Apply suggested fix pattern
4. If Mojo-related, check languages/mojo/AI_PATTERNS.md
5. If VCS-related, check standards/JJ_DECISION_TREES.md
```

### Pattern: Code Quality Check
```
SEQUENCE:  
1. Apply patterns from standards/AI_CODE_PATTERNS.md
2. Run diagnostic commands from ERROR_PATTERNS.md
3. Check for anti-patterns using pattern recognition
4. Apply fixes using decision tree logic
```

### Pattern: Build System Integration
```
SEQUENCE:
1. Check for build system (Bazel/Pixi/Magic)
2. Load tools/modular/BUILD_PATTERNS.md
3. Execute appropriate build commands
4. Handle errors with pattern matching
```

### Pattern: AI Assistant Setup
```
SEQUENCE:
1. Determine assistant type (Cursor/Claude/Copilot)
2. Load CODING_ASSISTANT_INTEGRATION.md
3. Configure with appropriate llms.txt
4. Set up project-specific rules
```

## FILE PRIORITY FOR AI AGENTS

### High Priority (Load First)
1. `AI_AGENT_INDEX.md` - This file (navigation)
2. `ERROR_PATTERNS.md` - Error resolution  
3. Task-specific pattern file based on context

### Medium Priority (Load as Needed)
- `standards/JJ_DECISION_TREES.md` - VCS operations
- `standards/AI_CODE_PATTERNS.md` - Code organization
- `languages/mojo/AI_PATTERNS.md` - Mojo development

### Low Priority (Reference Only)
- Advanced pattern files for specific optimization
- Language reference docs for syntax lookup

## SUBMODULE INTEGRATION

### Pattern: Access from Submodule
```
IF repository_has_submodule:
    @external/agent-contexts/AI_AGENT_INDEX.md     # This file
    @external/agent-contexts/ERROR_PATTERNS.md     # Error patterns
    Follow decision trees to specific pattern files
```

See `SUBMODULE_INTEGRATION.md` for complete integration patterns.