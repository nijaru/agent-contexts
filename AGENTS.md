# Agent Contexts

**Example project configuration for AI coding agents**

## Purpose

This repository teaches AI agents **how to organize their work** across projects. It provides standardized structure for AI working context that works across all AI coding tools.

## Organization Patterns

**For complete guidance:** @PRACTICES.md

**Quick reference:**
- **ai/** — AI session tracking (tasks, state, decisions, research)
- **docs/** — User/team documentation (guides, API, specs)

## Project Structure

```
agent-contexts/
├── README.md        # Project overview (for humans browsing GitHub)
├── AGENTS.md        # This file (example project config)
├── CLAUDE.md        # Symlink to AGENTS.md (Claude Code compatibility)
├── PRACTICES.md     # Complete guide for AI agents (~900 words)
└── ai/              # Our own working context
    ├── PLAN.md      # Strategic roadmap for this repo
    ├── TODO.md      # Current work on this repo
    ├── STATUS.md    # State of this repo
    ├── DECISIONS.md # Decisions about this repo's structure
    └── RESEARCH.md  # Research on AI agent patterns
```

## Core Principles

1. **Organization over coding** - AI agents know syntax, need structure
2. **Standardization** - Same ai/ structure across all projects
3. **Minimal** - ~1,000 total words vs previous ~13,000
4. **Machine-optimized** - ai/ uses tables/lists, docs/ uses prose
5. **Research over duplication** - Fresh knowledge beats stale patterns

## Development Workflow

**For humans:**
1. Browse README.md for project overview
2. Read PRACTICES.md to understand organization patterns
3. Use AGENTS.md as template for your own projects

**For AI agents:**
1. Load @PRACTICES.md for organization guidance
2. Read ai/STATUS.md for current state of this repo
3. Check ai/TODO.md for active work
4. Review ai/PLAN.md for strategic roadmap
5. Reference ai/DECISIONS.md for architectural rationale

## When to Use This Repo

**✅ Use for:**
- Standardizing AI working context across projects
- Multi-session work requiring clean handoffs
- Setting up new projects with AI agent workflows
- Learning how to structure ai/ directory

**❌ Don't use for:**
- Programming language tutorials (AI knows syntax)
- Tool commands (research current docs)
- Project-specific patterns (put in your CLAUDE.md/AGENTS.md)

## Current Focus

See ai/STATUS.md for current state and active work.
