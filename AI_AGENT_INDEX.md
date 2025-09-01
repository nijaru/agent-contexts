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
IF language_specific_task:
    → languages/{language}/                # Language-specific patterns
IF tool_specific_task:  
    → tools/{tool}/                        # Tool-specific command sequences
```

### Choose Documentation by Language
```
IF working_with_mojo:
    → languages/mojo/AI_PATTERNS.md        # Mojo pattern recognition
    → languages/mojo/advanced/             # Performance patterns
IF working_with_python:
    → languages/python/                    # Python patterns
IF working_with_go:
    → languages/go/                        # Go patterns
```

### Choose by Context Type
```
IF setting_up_workflow:
    → standards/JJ_DECISION_TREES.md       # VCS workflow
    → standards/AI_CODE_PATTERNS.md        # Code standards
IF debugging_issue:
    → ERROR_PATTERNS.md                    # Error diagnosis
    → languages/mojo/AI_PATTERNS.md        # Mojo-specific fixes
IF optimizing_performance:
    → languages/mojo/advanced/             # Advanced patterns  
    → languages/mojo/AI_PATTERNS.md        # Quick fixes
```

## PATTERN TYPES BY FILE

### `ERROR_PATTERNS.md` - Error Recognition
- Compilation error → fix mappings
- Runtime error → diagnostic commands  
- Performance issue → optimization patterns
- Recovery procedures for common mistakes

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

### `languages/mojo/AI_PATTERNS.md` - Mojo-Specific
- Type conversion patterns
- Memory management decisions
- Function type selection logic
- Performance optimization triggers

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