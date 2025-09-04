# Agent Contexts

**Actionable patterns for AI-assisted development**

Version: 0.0.1

## What is this?

A curated collection of decision trees, error patterns, and best practices optimized for AI coding assistants (Claude, Cursor, Copilot, etc.). These patterns help AI agents make better decisions and write better code.

## Quick Start

### 1. Add as Submodule
```bash
git submodule add https://github.com/USERNAME/agent-contexts external/agent-contexts
git submodule update --init --recursive
```

### 2. Reference in Your AI Assistant

**For Claude Code (CLAUDE.md):**
```markdown
@external/agent-contexts/AI_AGENT_INDEX.md
```

**For Cursor/Windsurf (.cursorules):**
```
Include: @external/agent-contexts/AI_AGENT_INDEX.md
```

## Core Files

| File | Purpose |
|------|---------|
| `AI_AGENT_INDEX.md` | Entry point with navigation decision trees |
| `ERROR_PATTERNS.md` | Error message → solution mappings |
| `standards/AI_CODE_PATTERNS.md` | Code organization and naming patterns |
| `standards/JJ_DECISION_TREES.md` | Version control workflow patterns |

## Language-Specific Patterns

- `languages/mojo/MOJO_PATTERNS.md` - Mojo performance and memory patterns
- `languages/python/PYTHON_PATTERNS.md` - Modern Python with UV patterns
- `languages/go/GO_PATTERNS.md` - Go concurrency and testing patterns

## Key Principles

1. **Actionable over Informational** - Every pattern leads to a specific action
2. **Timeless over Trendy** - Focus on patterns that won't become outdated
3. **Universal over Personal** - All patterns work for any developer
4. **Concise over Comprehensive** - Optimized for AI context windows

## Usage Pattern

```
IF error_encountered:
    → Check ERROR_PATTERNS.md
IF organizing_code:
    → Check standards/AI_CODE_PATTERNS.md
IF language_specific_task:
    → Check languages/[language]/[LANGUAGE]_PATTERNS.md
```

## Contributing

1. Keep patterns actionable and timeless
2. Use decision tree format (IF/THEN)
3. Include ❌ WRONG vs ✅ CORRECT examples
4. Remove outdated content regularly
5. No personal information or specific usernames

## License

MIT - Use these patterns freely in your projects