# Quick Install for Projects

## Copy-Paste Prompt for AI Agents

```
Add agent-contexts as a submodule to provide AI agents with pattern recognition and decision trees:

git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts
git submodule update --init --recursive

Then update your CLAUDE.md to include:
@external/agent-contexts/AI_AGENT_INDEX.md

This provides AI agents with:
- Error → solution pattern mappings
- Code organization decision trees  
- Language-specific optimization patterns
- Version control workflow automation
```

## One-Command Install

```bash
# Run in your project root
curl -s https://raw.githubusercontent.com/nickbytes/agent-contexts/main/install.sh | bash
```

## Manual Steps

```bash
# 1. Add submodule
git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts

# 2. Initialize submodule  
git submodule update --init --recursive

# 3. Commit the addition
git add .gitmodules external/agent-contexts
git commit -m "Add AI agent context patterns submodule"

# 4. Update your CLAUDE.md with entry point
echo "@external/agent-contexts/AI_AGENT_INDEX.md" >> CLAUDE.md
```

## Verification

After installation, AI agents can access:
- `@external/agent-contexts/AI_AGENT_INDEX.md` - Navigation
- `@external/agent-contexts/ERROR_PATTERNS.md` - Error solutions
- `@external/agent-contexts/standards/` - Universal patterns
- `@external/agent-contexts/languages/` - Language-specific patterns