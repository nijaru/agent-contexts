# Agent Contexts

Standardized organization patterns for AI coding agents.

AI agents know how to code. What they need: consistent structure for tracking context across sessions.

## Try It (One Project)

Point your AI agent at this repo:

```
Read github.com/nijaru/agent-contexts - the README, then PATTERNS.md.
Set up ai/ context management for this project following those patterns.
```

The agent will create:

- `AGENTS.md` - Project config for AI agents
- `ai/brief.md` - Current state (always, <80 lines)
- `ai/architecture.md` - System architecture (recommended)
- `ai/decisions.md` - Architectural choices (recommended)
- `ai/` subdirs for research, component designs

## What You Get

```
your-project/
├── AGENTS.md              # AI entry point
├── CLAUDE.md → AGENTS.md  # Symlink for Claude Code
├── .tasks/                # Task tracking (tk CLI)
└── ai/                    # AI session context
    ├── brief.md           # Current state (always, <80 lines)
    ├── journal.md         # Append-only session log
    ├── architecture.md    # System architecture (recommended)
    ├── decisions.md       # Architectural choices — Principles + Log
    ├── PLAN.md            # Active plan or sprint index (situational)
    ├── research/          # External research (on demand)
    ├── design/            # Component specs (on demand)
    └── tmp/               # Temporary artifacts (gitignored)
```

## Key Concepts

**Token efficiency**: Session files (ai/ root) load every session—keep minimal. Subdirectories load only when needed.

**Task tracking**: Use `tk` CLI for task tracking. Tasks stored in `.tasks/` directory.

**Separation**: `ai/` = AI workspace (tables, lists). `docs/` = Human docs (prose).

**File tiers**:

| Tier        | Files                              |
| ----------- | ---------------------------------- |
| Always      | brief.md, journal.md               |
| Recommended | architecture.md, decisions.md      |
| Situational | PLAN.md (multi-phase planning)     |

## Files

| File               | Purpose                            |
| ------------------ | ---------------------------------- |
| `README.md`        | This file                          |
| `PATTERNS.md`      | Detailed organization patterns     |
| `global/AGENTS.md` | Template to copy into your project |
| `agents/*.md`      | Reference subagent implementations |
| `skills/*.md`      | Operational skills (setup-ai, save)|

## Integration

Copy `global/AGENTS.md` into your project's config file:

| Tool        | Config File                               |
| ----------- | ----------------------------------------- |
| Claude Code | `AGENTS.md` (or `CLAUDE.md` symlink)      |
| pi          | `AGENTS.md`                               |
| Codex       | `AGENTS.md`                               |
| Cursor      | `.cursorrules`                            |
| Cline       | `.clinerules`                             |
| Windsurf    | `.windsurfrules`                          |

## License

Apache 2.0
