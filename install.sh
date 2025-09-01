#!/bin/bash

# AI Agent Context Patterns - Quick Install Script
# Adds agent-contexts as submodule and updates CLAUDE.md

set -e

echo "🤖 Installing AI Agent Context Patterns..."

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository. Run 'git init' first."
    exit 1
fi

# Add submodule
echo "📦 Adding agent-contexts submodule..."
git submodule add https://github.com/nickbytes/agent-contexts external/agent-contexts

# Initialize submodule
echo "🔄 Initializing submodule..."
git submodule update --init --recursive

# Update or create CLAUDE.md
if [ -f CLAUDE.md ]; then
    echo "📝 Updating existing CLAUDE.md..."
    if ! grep -q "external/agent-contexts" CLAUDE.md; then
        echo "" >> CLAUDE.md
        echo "# AI Agent Context" >> CLAUDE.md
        echo "@external/agent-contexts/AI_AGENT_INDEX.md" >> CLAUDE.md
    fi
else
    echo "📝 Creating CLAUDE.md..."
    cat > CLAUDE.md << 'EOF'
# Project Context for AI Agents

## AI Agent Patterns
@external/agent-contexts/AI_AGENT_INDEX.md

## Project-Specific Information
- Build: [add your build command]
- Test: [add your test command]  
- Lint: [add your lint command]
EOF
fi

# Commit the changes
echo "💾 Committing changes..."
git add .gitmodules external/agent-contexts CLAUDE.md
git commit -m "Add AI agent context patterns submodule

- Provides error → solution mappings
- Code organization decision trees
- Language-specific optimization patterns
- Version control workflow automation"

echo "✅ Installation complete!"
echo ""
echo "🎯 AI agents can now access:"
echo "   @external/agent-contexts/AI_AGENT_INDEX.md    # Navigation"
echo "   @external/agent-contexts/ERROR_PATTERNS.md    # Error solutions"
echo "   @external/agent-contexts/standards/           # Universal patterns"
echo ""
echo "💡 To update patterns later:"
echo "   git submodule update --remote external/agent-contexts"