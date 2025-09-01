# Copy-Paste Prompts for AI Agents

## Quick Install Prompt

Copy and paste this into any AI coding assistant:

```
Add agent-contexts submodule for AI pattern recognition. Choose appropriate location based on project structure:

OPTION 1 - Projects with external/ or vendor/ directory:
git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts

OPTION 2 - Projects with docs/ or documentation structure:  
git submodule add https://github.com/nickbytes/agent-contexts docs/agent-contexts

OPTION 3 - Projects with tools/ or scripts/ directory:
git submodule add https://github.com/nickbytes/agent-contexts tools/agent-contexts

OPTION 4 - Root level (minimal projects):
git submodule add https://github.com/nickbytes/agent-contexts agent-contexts

Then: git submodule update --init --recursive

Add to CLAUDE.md: @{chosen-path}/AI_AGENT_INDEX.md

This provides:
- Error → solution mappings  
- Code organization decision trees
- Version control workflows
- Language-specific optimization patterns
```

## Context Loading Prompt

For AI agents working on projects with the submodule (adapt path as needed):

```
Load AI context patterns from submodule:
@{submodule-path}/AI_AGENT_INDEX.md

Common paths:
- @external/agent-contexts/AI_AGENT_INDEX.md
- @docs/agent-contexts/AI_AGENT_INDEX.md  
- @tools/agent-contexts/AI_AGENT_INDEX.md
- @agent-contexts/AI_AGENT_INDEX.md

Follow the decision trees to load relevant patterns based on current task.
Apply ❌ WRONG vs ✅ CORRECT examples throughout.
```

## Intelligent Install Prompt

For AI agents that should decide location automatically:

```
Add AI agent context patterns as a submodule. Analyze the project structure and choose the most appropriate location:

IF project has external/ or vendor/ directory:
  → git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts
ELIF project has docs/ or documentation/ directory:
  → git submodule add https://github.com/nickbytes/agent-contexts docs/agent-contexts  
ELIF project has tools/ or scripts/ directory:
  → git submodule add https://github.com/nickbytes/agent-contexts tools/agent-contexts
ELSE:
  → git submodule add https://github.com/nickbytes/agent-contexts agent-contexts

Then:
git submodule update --init --recursive

Add entry point to CLAUDE.md: @{chosen-path}/AI_AGENT_INDEX.md

This provides decision trees, error patterns, and optimization guides for AI agents.
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