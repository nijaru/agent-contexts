#!/bin/bash

# AI Agent Context Patterns - Flexible Install Script
# Analyzes project structure and chooses appropriate submodule location

set -e

echo "🤖 Installing AI Agent Context Patterns..."

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository. Run 'git init' first."
    exit 1
fi

# Analyze project structure and choose location
SUBMODULE_PATH=""
RATIONALE=""

if [ -d "external" ] || [ -d "vendor" ]; then
    SUBMODULE_PATH="external/agent-contexts"
    RATIONALE="Found external/ or vendor/ directory (common for dependencies)"
elif [ -d "docs" ] || [ -d "documentation" ]; then
    SUBMODULE_PATH="docs/agent-contexts"  
    RATIONALE="Found docs/ directory (good fit for context patterns)"
elif [ -d "tools" ] || [ -d "scripts" ]; then
    SUBMODULE_PATH="tools/agent-contexts"
    RATIONALE="Found tools/ directory (good fit for AI tooling)"
else
    SUBMODULE_PATH="agent-contexts"
    RATIONALE="No standard directories found, using root level"
fi

echo "📍 Chosen location: $SUBMODULE_PATH"
echo "💡 Rationale: $RATIONALE"

# Add submodule
echo "📦 Adding agent-contexts submodule..."
git submodule add https://github.com/nickbytes/agent-contexts "$SUBMODULE_PATH"

# Initialize submodule
echo "🔄 Initializing submodule..."
git submodule update --init --recursive

# Update or create CLAUDE.md
if [ -f CLAUDE.md ]; then
    echo "📝 Updating existing CLAUDE.md..."
    if ! grep -q "$SUBMODULE_PATH" CLAUDE.md; then
        echo "" >> CLAUDE.md
        echo "# AI Agent Context" >> CLAUDE.md
        echo "@$SUBMODULE_PATH/AI_AGENT_INDEX.md" >> CLAUDE.md
    fi
else
    echo "📝 Creating CLAUDE.md..."
    cat > CLAUDE.md << EOF
# Project Context for AI Agents

## AI Agent Patterns
@$SUBMODULE_PATH/AI_AGENT_INDEX.md

## Project-Specific Information
- Build: [add your build command]
- Test: [add your test command]  
- Lint: [add your lint command]
EOF
fi

# Commit the changes
echo "💾 Committing changes..."
git add .gitmodules "$SUBMODULE_PATH" CLAUDE.md
git commit -m "Add AI agent context patterns submodule at $SUBMODULE_PATH

- Provides error → solution mappings
- Code organization decision trees
- Language-specific optimization patterns
- Version control workflow automation
- Location: $RATIONALE"

echo "✅ Installation complete!"
echo ""
echo "🎯 AI agents can now access:"
echo "   @$SUBMODULE_PATH/AI_AGENT_INDEX.md    # Navigation"
echo "   @$SUBMODULE_PATH/ERROR_PATTERNS.md    # Error solutions"  
echo "   @$SUBMODULE_PATH/standards/           # Universal patterns"
echo ""
echo "💡 To update patterns later:"
echo "   git submodule update --remote $SUBMODULE_PATH"