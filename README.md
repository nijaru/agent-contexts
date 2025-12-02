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
- `ai/STATUS.md` - Current state (always)
- `ai/DESIGN.md` - System architecture (recommended)
- `ai/DECISIONS.md` - Architectural choices (recommended)
- `ai/` subdirs for research, component designs

## What You Get

```
your-project/
├── AGENTS.md              # AI entry point
└── ai/                    # AI session context
    ├── STATUS.md         # Current state (always)
    ├── DESIGN.md         # System architecture (recommended)
    ├── DECISIONS.md      # Architectural choices (recommended)
    ├── ROADMAP.md        # Phases, milestones (situational)
    ├── research/         # External research (on demand)
    ├── design/           # Component specs (on demand)
    └── tmp/              # Temporary artifacts (gitignored)
```

## Key Concepts

**Token efficiency**: Session files (ai/ root) load every session—keep under 500 lines. Subdirectories load only when needed.

**Task tracking**: [Beads](https://github.com/steveyegge/beads) (`bd`) recommended for dependency graphs. Falls back to TODO.md.

**Separation**: `ai/` = AI workspace (tables, lists). `docs/` = Human docs (prose).

**File tiers**:
| Tier | Files |
|------|-------|
| Always | STATUS.md |
| Recommended | DESIGN.md, DECISIONS.md |
| Situational | ROADMAP.md (multi-phase), TODO.md (no beads) |

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
# Append patterns to existing config
cat global/CLAUDE.md >> ~/.claude/CLAUDE.md

# Or if starting fresh
cp global/CLAUDE.md ~/.claude/CLAUDE.md

# Copy commands (optional)
mkdir -p ~/.claude/commands
cp commands/*.md ~/.claude/commands/

# Now in any project:
/setup-ai
```

**For other tools:** Append `global/CLAUDE.md` to your tool's config file.

## Files

| File | Audience | Purpose |
|------|----------|---------|
| `README.md` | Humans + AI | Quick start, overview |
| `PRACTICES.md` | AI agents | Detailed organization patterns |
| `global/CLAUDE.md` | AI agents | Template for user/project config |
| `commands/*.md` | Claude Code | Slash commands (`/setup-ai`, `/save`) |

## License

Apache 2.0
