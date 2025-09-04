# MAX/Mojo Coding Assistant Integration

## DECISION: Documentation Source Selection
```
IF need_api_reference:
    → @docs.modular.com/llms-mojo.txt
ELIF need_python_interop:
    → @docs.modular.com/llms-python.txt  
ELIF need_complete_context:
    → @docs.modular.com/llms-full.txt
ELIF working_offline:
    → @external/agent-contexts/languages/mojo/
```

## PATTERN: Project Setup for AI Assistants
```bash
# Quick setup for any MAX/Mojo project
setup_ai_context() {
  # 1. Add Modular's cursorules
  mkdir -p .cursor
  curl -o .cursor/rules https://docs.modular.com/max/cursorules
  
  # 2. Create CLAUDE.md for Claude Code
  cat > CLAUDE.md << 'EOF'
# MAX/Mojo Project

## Documentation Sources
- @docs.modular.com/llms-mojo.txt - Mojo language reference
- @external/agent-contexts/languages/mojo/ - Local patterns

## Project Conventions
- Use `fn` for performance-critical code
- Use `def` for Python interop
- Prefer native Mojo types over Python types
EOF

  # 3. Add agent-contexts submodule
  git submodule add https://github.com/USERNAME/agent-contexts external/agent-contexts
  git submodule update --init --recursive
}
```

## DECISION: Error Resolution Strategy
```
ERROR_TYPE:
  "use of unknown declaration" → Check type capitalization (Int vs int)
  "cannot implicitly convert" → Add explicit conversion or ^transfer
  "lifetime of reference" → Use owned or add lifetime parameters
  "cannot move out of value" → Add ^ for transfer or use borrowed
```

## PATTERN: AI Context Loading Order
```
1. Load project CLAUDE.md or .cursorules
2. Load @docs.modular.com/llms-mojo.txt for API reference
3. Load error patterns from agent-contexts if debugging
4. Load performance patterns if optimizing
```

## ❌ WRONG vs ✅ CORRECT AI Integration

**❌ WRONG: Loading everything at once**
```
@docs.modular.com/llms-full.txt
@external/agent-contexts/
@all-project-files
# Context overflow, slow responses
```

**✅ CORRECT: Selective context loading**
```
# For error fixing
@external/agent-contexts/languages/mojo/ERROR_PATTERNS.md
@current-error-file

# For new feature
@docs.modular.com/llms-mojo.txt
@relevant-module-only
```

## COMMAND SEQUENCES

### SEQUENCE: Debug Mojo Build Errors
```bash
# 1. Capture error
pixi run mojo build main.mojo 2>&1 | tee build_error.log

# 2. Extract error patterns
grep -E "error:|note:" build_error.log

# 3. Load specific fix patterns
# AI loads: @external/agent-contexts/languages/mojo/ERROR_PATTERNS.md

# 4. Apply fixes based on patterns
```

### SEQUENCE: Optimize Performance
```bash
# 1. Profile current code
pixi run mojo build -O3 --profile main.mojo

# 2. Identify bottlenecks
# AI loads: @external/agent-contexts/languages/mojo/advanced/MOJO_BEST_PRACTICES.md

# 3. Apply optimization patterns
# - Quantization for memory reduction
# - SIMD for parallel processing
# - Move semantics for ownership
```

## INTEGRATION WITH EXISTING TOOLS

### Cursor/Windsurf
```json
{
  "context_sources": [
    "@docs.modular.com/llms-mojo.txt",
    "@external/agent-contexts/languages/mojo/"
  ],
  "rules_path": ".cursor/rules",
  "auto_context": true
}
```

### Claude Code
```markdown
# In CLAUDE.md
@external/agent-contexts/AI_AGENT_INDEX.md
@docs.modular.com/llms-mojo.txt
```

### GitHub Copilot
```yaml
# .github/copilot.yml
documentation:
  - https://docs.modular.com/llms-mojo.txt
  - external/agent-contexts/languages/mojo/
```

## STATE RECOGNITION PATTERNS
```
PROJECT_STATE:
  No pixi.toml → Run: pixi init
  No pyproject.toml → Missing MAX project config
  Build errors → Check ERROR_PATTERNS.md
  Slow performance → Check MOJO_BEST_PRACTICES.md
  Python interop issues → Use def instead of fn
```

---
*Optimized for AI coding assistant integration with MAX/Mojo projects*