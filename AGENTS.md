# Agent Contexts

*Standardized patterns for AI agent organization*

## Purpose

This repository teaches AI agents **how to organize their work** across projects, not how to code. It provides a minimal, standardized structure for AI working context that works across all AI coding tools (Claude Code, Cursor, Copilot, etc.).

## Quick Start

**For AI agents working on projects:**
1. Load `@PRACTICES.md` for complete guidance
2. Create `ai/` directory structure in your project
3. Maintain TODO, STATUS, DECISIONS, and RESEARCH files
4. Use this repo's AGENTS.md as a template

**For humans setting up projects:**
1. Copy this AGENTS.md to your project as a starting template
2. Create `ai/` directory for agent working context
3. Let AI agents maintain their workspace
4. Reference `PRACTICES.md` for details

## Project Structure

This repository follows its own practices:

```
agent-contexts/
├── README.md        # Project overview
├── AGENTS.md        # This file (serves as example template)
├── PRACTICES.md     # Core guidance for AI agents
├── CLAUDE.md        # Symlink to AGENTS.md for compatibility
├── ai/              # Our own working context
│   ├── TODO.md
│   ├── STATUS.md
│   ├── DECISIONS.md
│   ├── RESEARCH.md
│   └── research/    # Detailed research files
└── VERSION
```

## Core Principles

1. **Organization over coding** - AI agents already know how to code
2. **Standardization over customization** - Same structure across all projects
3. **Minimal over comprehensive** - Keep token usage low
4. **Research over duplication** - Fresh knowledge over stale patterns

## When to Use This Repo

**✅ Use when:**
- Starting work on a new project
- Setting up AI working context
- Need guidance on file organization
- Doing multi-session work requiring handoff

**❌ Don't use for:**
- Language syntax (use training data + research)
- Tool commands (research current docs)
- Project-specific patterns (belongs in project's AGENTS.md)
- Comprehensive coding guides (defeats the purpose)

## Development Workflow

See `ai/TODO.md` for current work on this repository.