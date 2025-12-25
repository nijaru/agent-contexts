# Agent Contexts

**Organization patterns and templates for AI coding agents**

## Purpose

Standardized structure for AI working context. Use to set up any project with ai/ context management.

## Quick Reference

**For complete guidance:** @PATTERNS.md

**Core pattern:**

- **ai/** — AI session context (state, design, decisions)
- **docs/** — User documentation (guides, API, specs)
- **Task tracking:** Beads (`bd`) recommended, or ai/TODO.md

## Project Structure

```
agent-contexts/
├── README.md              # Quick start (humans + AI)
├── PATTERNS.md            # Detailed patterns (AI reference)
├── AGENTS.md              # This file
├── CLAUDE.md              # Symlink → AGENTS.md
├── global/
│   └── CLAUDE.md          # Template → ~/.claude/CLAUDE.md or project config
├── agents/                # Reference subagent implementations
│   ├── researcher.md
│   ├── designer.md
│   ├── developer.md
│   └── reviewer.md
└── commands/
    ├── setup-ai.md        # /setup-ai command
    └── save.md            # /save command
```

## ai/ Structure

| File         | When            | Purpose                               |
| ------------ | --------------- | ------------------------------------- |
| STATUS.md    | **Always**      | Current state, blockers (read FIRST)  |
| DESIGN.md    | **Recommended** | System architecture, components       |
| DECISIONS.md | **Recommended** | Architectural decisions               |
| ROADMAP.md   | Situational     | Phases, milestones (multi-phase only) |
| TODO.md      | Situational     | Tasks (if no beads)                   |

**Subdirectories (on demand):**

- research/ — External research findings
- design/ — Component specifications
- review/ — Review findings
- tmp/ — Temporary artifacts (gitignored)

## Subagents

For context isolation, parallelism, fresh perspective. ai/ files are shared memory.

| Agent        | Purpose                          | Persists to  |
| ------------ | -------------------------------- | ------------ |
| `researcher` | External knowledge, synthesis    | ai/research/ |
| `designer`   | Architecture, planning           | ai/design/   |
| `developer`  | Well-scoped implementation       | —            |
| `reviewer`   | Full validation (build/run/test) | ai/review/   |

See `agents/` for reference implementations.

## Core Principles

1. **Organization over coding** - AI knows syntax, needs structure
2. **Token efficiency** - Session files minimal, subdirs on demand
3. **Standardization** - Same ai/ structure across projects
4. **Machine-optimized** - Tables/lists, not prose
5. **Single source of truth** - Each type of info has one home

## Usage

**One project:** Read PATTERNS.md, apply patterns to target project

**All projects:** Copy `global/CLAUDE.md` to user-level config, use `/setup-ai` command
