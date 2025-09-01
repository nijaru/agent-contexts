# Copy-Paste Prompts for AI Agents

## Quick Install Prompt

Copy and paste this into any AI coding assistant:

```
Add agent-contexts submodule for AI pattern recognition:

curl -s https://raw.githubusercontent.com/nickbytes/agent-contexts/main/install.sh | bash

This provides:
- Error → solution mappings (@external/agent-contexts/ERROR_PATTERNS.md)  
- Code organization patterns (@external/agent-contexts/standards/AI_CODE_PATTERNS.md)
- Version control workflows (@external/agent-contexts/standards/JJ_DECISION_TREES.md)
- Language-specific patterns (@external/agent-contexts/languages/)

Entry point: @external/agent-contexts/AI_AGENT_INDEX.md
```

## Manual Install Prompt

For projects where scripts aren't allowed:

```
Add AI agent context patterns to this project:

git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts
git submodule update --init --recursive

Then add to CLAUDE.md:
@external/agent-contexts/AI_AGENT_INDEX.md

This gives you access to:
- ❌ WRONG vs ✅ CORRECT pattern examples
- Decision trees for common coding choices  
- Error message → solution mappings
- Command sequences for automation
```

## Context Loading Prompt

For AI agents working on projects with the submodule:

```
Load AI context patterns:
@external/agent-contexts/AI_AGENT_INDEX.md

Follow the decision trees to load relevant patterns based on current task.
Apply ❌ WRONG vs ✅ CORRECT examples throughout.
Use command sequences for automation.
Check ERROR_PATTERNS.md if errors occur.
```

## Language-Specific Prompts

### Mojo Development
```
Working with Mojo - load optimization patterns:
@external/agent-contexts/languages/mojo/AI_PATTERNS.md
@external/agent-contexts/languages/mojo/advanced/

Focus on:
- Type conversion patterns (int → Int, str → String)
- Memory management (move semantics, ownership)
- Performance optimization patterns
```

### Version Control with JJ
```
Using JJ version control - load workflow patterns:
@external/agent-contexts/standards/JJ_DECISION_TREES.md

Apply decision trees for:
- AI agent session management
- Error recovery workflows  
- Clean history creation
```