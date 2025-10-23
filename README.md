# Agent Contexts

**Standardized organization patterns for AI coding agents**

Version: 0.1.3

## What is this?

A minimal guide teaching AI agents **how to organize their work** across projects. This is NOT a coding guide - AI agents already know how to code. This teaches them how to maintain consistent working context using a standardized `ai/` directory structure.

## Quick Start

### For AI Agents

Include this in your project context:
```markdown
@external/agent-contexts/PRACTICES.md
```

Then create and maintain:
```
ai/
├── TODO.md       # Active tasks
├── STATUS.md     # Current state
├── DECISIONS.md  # Architectural choices
├── RESEARCH.md   # Research index
└── research/     # Detailed research files
```

### For Humans

Add as submodule to your projects:
```bash
git submodule add https://github.com/nijaru/agent-contexts external/agent-contexts
git submodule update --init --recursive
```

Reference in your AGENTS.md or CLAUDE.md:
```markdown
For organization patterns: @external/agent-contexts/PRACTICES.md
```

## Core Files

| File | Purpose | Audience |
|------|---------|----------|
| `PRACTICES.md` | Complete guide for AI agent organization (~800 words) | AI agents |
| `AGENTS.md` | Example template for projects (~300 words) | AI agents |
| `README.md` | Project overview and usage | Humans |
| `ai/` | This repo's own working context | AI agents |

## Key Principles

1. **Organization over coding** - AI knows syntax, needs structure guidance
2. **Standardization over customization** - Same `ai/` structure everywhere
3. **Minimal over comprehensive** - ~1,000 total words vs previous ~13,000
4. **Research over duplication** - Fresh knowledge beats stale patterns

## What Changed (v0.1.0 Refactor)

**Removed** (archived at tag `v0.0.3-archive`):
- All language-specific patterns (Python, Go, Mojo, Rust)
- All tool-specific patterns (UV, JJ, GitHub, Modular)
- All coding standards (ERROR, DOC, CODE, RELEASE patterns)

**Why**: AI agents should research current best practices, not rely on potentially outdated static patterns. This repo now focuses solely on **how to organize work**, not **how to code**.

**Token reduction**: ~17,500 → ~2,500 tokens (85% reduction)

## When to Use This

**✅ Use for:**
- Standardizing AI working context across projects
- Multi-session work requiring clean handoffs
- Setting up new projects with AI agent workflows
- Learning how to structure `ai/` directory

**❌ Don't use for:**
- Learning programming languages (use training data + research)
- Tool commands (research current documentation)
- Project-specific patterns (belongs in your AGENTS.md)
- Comprehensive coding guides (that's not the purpose)

## File Structure

```
agent-contexts/
├── README.md         # This file
├── AGENTS.md         # Example template
├── CLAUDE.md         # Symlink for compatibility
├── PRACTICES.md      # Core guidance (~600 words)
├── ai/               # Our own working context
│   ├── TODO.md
│   ├── STATUS.md
│   ├── DECISIONS.md
│   ├── RESEARCH.md
│   └── research/     # Detailed research files
└── VERSION
```

## Philosophy

This repository embodies a simple idea: **AI agents need standardized workspaces, not coding tutorials**.

Think of it like a desk organization system for knowledge workers. The desk layout (filing system, inbox/outbox, reference materials) should be consistent. The actual work products vary by project.

Similarly, the `ai/` directory structure should be standard across all projects, while the content within adapts to each project's needs.

## Contributing

We welcome feedback on the `ai/` directory structure and PRACTICES.md content. However, please **do not** submit:
- Language-specific coding patterns
- Tool-specific command references
- Comprehensive how-to guides

These defeat the purpose of minimal, focused organization guidance.

## License

MIT - Use freely in your projects

## Previous Patterns

Need the old language/tool patterns? See tag `v0.0.3-archive`:
```bash
git show v0.0.3-archive:languages/python/PYTHON_PATTERNS.md
```