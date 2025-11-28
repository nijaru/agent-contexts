# Agent Contexts

Standardized organization patterns for AI coding agents.

AI agents know how to code. What they need: consistent structure for tracking context across sessions.

## Try It (One Project)

Point your AI agent at this repo:

```
Read github.com/nijaru/agent-contexts - the README, then PRACTICES.md.
Set up ai/ context management for this project following those patterns.
```

The agent will create:
- `AGENTS.md` - Project config for AI agents
- `ai/STATUS.md` - Current state
- `ai/DECISIONS.md` - Architectural choices
- `ai/` subdirs for research, design, etc.

## What You Get

```
your-project/
├── AGENTS.md              # AI entry point
└── ai/                    # AI session context
    ├── STATUS.md         # Current state (always)
    ├── TODO.md           # Tasks (or use beads)
    ├── DECISIONS.md      # Architectural choices
    ├── RESEARCH.md       # Research index
    ├── research/         # Detailed research (on demand)
    ├── design/           # Specifications (on demand)
    └── tmp/              # Temporary artifacts (gitignored)
```

## Key Concepts

**Token efficiency**: Session files (ai/ root) load every session—keep under 500 lines. Subdirectories load only when needed.

**Task tracking**: [Beads](https://github.com/steveyegge/beads) (`bd`) recommended for dependency graphs. Falls back to TODO.md.

**Separation**: `ai/` = AI workspace (tables, lists). `docs/` = Human docs (prose).

## Integration Options

### Option 1: Project-Level (one repo)

Add the patterns to your project's AI config file:

| Tool | Config File |
|------|-------------|
| Claude Code | `CLAUDE.md` (or `AGENTS.md` with symlink) |
| Cursor | `.cursorrules` |
| Cline | `.clinerules` |
| Windsurf | `.windsurfrules` |
| Other | `AGENTS.md` |

Copy relevant sections from `global/CLAUDE.md` into your config.

### Option 2: User-Level (all projects)

**For Claude Code:**
```bash
# Copy global config
cp global/CLAUDE.md ~/.claude/CLAUDE.md

# Copy commands (optional)
mkdir -p ~/.claude/commands
cp commands/*.md ~/.claude/commands/

# Now in any project:
/setup-ai
```

**For other tools:** Check if your tool supports user-level config files.

## Files

| File | Audience | Purpose |
|------|----------|---------|
| `README.md` | Humans + AI | Quick start, overview |
| `PRACTICES.md` | AI agents | Detailed organization patterns (~900 words) |
| `global/CLAUDE.md` | AI agents | Template for user/project config |
| `commands/*.md` | Claude Code | Slash commands (`/setup-ai`, `/save`) |

## License

Apache 2.0
