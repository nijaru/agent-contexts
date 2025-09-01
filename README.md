# AI Agent Context Repository

*Pattern-based documentation optimized for LLM consumption and code generation*

## START HERE: `@AI_AGENT_INDEX.md`

Navigation file with decision trees for loading the right patterns based on your task.

## Repository Purpose

**Pure AI agent optimization** - No human-friendly prose, maximum pattern density:
- **❌ WRONG vs ✅ CORRECT** examples for pattern recognition
- **Decision trees** for algorithmic decision making  
- **Command sequences** for automated execution
- **Error → solution mappings** for problem resolution

## Structure for AI Agents

### Universal Patterns (Load First)
- `ERROR_PATTERNS.md` - Error recognition → solution mapping
- `standards/AI_CODE_PATTERNS.md` - Code organization patterns
- `standards/JJ_DECISION_TREES.md` - Version control decision logic

### Language-Specific Patterns
- `languages/mojo/AI_PATTERNS.md` - Mojo-specific pattern recognition
- `languages/mojo/advanced/` - High-performance optimization patterns  
- `languages/mojo/core/` - Reference docs (built-ins, style guide)

### Tool-Specific Patterns
- `tools/modular/` - MAX/Magic command sequences
- `tools/python/uv/` - UV package manager automation

## AI Agent Usage

```
TASK_START:
1. @AI_AGENT_INDEX.md              # Load navigation
2. Follow decision tree → specific pattern file
3. Apply ❌ WRONG vs ✅ CORRECT patterns
4. Execute command sequences
5. Check ERROR_PATTERNS.md if issues

ERROR_ENCOUNTERED:
1. @ERROR_PATTERNS.md              # Find error → solution mapping
2. Apply fix pattern
3. Load language/tool-specific patterns if needed
```

## File Types
- **Decision Trees**: IF/THEN logic for AI decision making
- **Pattern Recognition**: Anti-pattern examples with corrections
- **Command Sequences**: Bash/tool automation scripts
- **Reference Lookups**: Structured API/syntax information

## Installation

### One-Command Install (Recommended)

**Smart location detection:**
```bash
curl -s https://raw.githubusercontent.com/nickbytes/agent-contexts/main/install-flexible.sh | bash
```
Analyzes your project structure and chooses the best location (`external/`, `docs/`, `tools/`, or root).

**Fixed location (external/):**  
```bash
curl -s https://raw.githubusercontent.com/nickbytes/agent-contexts/main/install.sh | bash
```

Both scripts automatically:
- Add submodule at appropriate location
- Create/update your `CLAUDE.md` with entry point  
- Commit changes with descriptive message

### Manual Install
Choose location based on your project structure:
```bash
# Option 1: External dependencies
git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts

# Option 2: Documentation  
git submodule add https://github.com/nickbytes/agent-contexts docs/agent-contexts

# Option 3: Development tools
git submodule add https://github.com/nickbytes/agent-contexts tools/agent-contexts

# Then initialize and update CLAUDE.md
git submodule update --init --recursive
echo "@{chosen-path}/AI_AGENT_INDEX.md" >> CLAUDE.md
```

### Copy-Paste Prompts for AI Agents
See [PROMPT.md](PROMPT.md) for ready-to-use prompts you can give AI agents to install this in any project.

### Verification
After installation, AI agents can access (adapt path to your chosen location):
```
@{submodule-path}/AI_AGENT_INDEX.md    # Navigation decision trees
@{submodule-path}/ERROR_PATTERNS.md    # Error → solution mappings  
@{submodule-path}/standards/           # Universal patterns
@{submodule-path}/languages/           # Language-specific patterns
```

Complete documentation: [INSTALL.md](INSTALL.md) | [SUBMODULE_INTEGRATION.md](SUBMODULE_INTEGRATION.md)

## Contributing

Contributions are welcome! Please follow these guidelines:
- Use clear, concise language optimized for AI consumption
- Format using standard markdown following our [Style Guide](./STYLE-GUIDE.md)
- Focus on technical accuracy and current best practices
- Include relevant code examples where helpful
- Run validation tools mentioned in the [Style Guide](./STYLE-GUIDE.md) before submitting

## License

This repository is licensed under the [Apache License, Version 2.0](./LICENSE). You are free to use, modify, and distribute these context files for any AI coding assistant in accordance with the terms of this license.
