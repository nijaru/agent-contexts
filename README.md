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

**Subagents**: Main agent handles most work. Subagents for context isolation and parallel execution. See `agents/` for reference implementations.

**File tiers**:

| Tier        | Files                              |
| ----------- | ---------------------------------- |
| Always      | brief.md, journal.md               |
| Recommended | architecture.md, decisions.md      |
| Situational | PLAN.md (multi-phase planning)     |

## Integration Options

### Option 1: Project-Level (one repo)

Add the patterns to your project's AI config file:

| Tool        | Config File                               |
| ----------- | ----------------------------------------- |
| Claude Code | `AGENTS.md` (or `CLAUDE.md` symlink)      |
| pi          | `AGENTS.md`                               |
| Codex       | `AGENTS.md`                               |
| Cursor      | `.cursorrules`                            |
| Cline       | `.clinerules`                             |
| Windsurf    | `.windsurfrules`                          |
| Other       | `AGENTS.md`                               |

Copy relevant sections from `global/AGENTS.md` into your config.

### Option 2: User-Level (all projects)

```bash
# Append patterns to existing config
cat global/AGENTS.md >> ~/.agents/AGENTS.md

# Or if starting fresh
mkdir -p ~/.agents
cp global/AGENTS.md ~/.agents/AGENTS.md

# Copy skills (optional)
mkdir -p ~/.agents/skills
cp skills/*.md ~/.agents/skills/

# Copy agent definitions (optional)
mkdir -p ~/.agents/agents
cp agents/*.md ~/.agents/agents/
```

**For other tools:** Append `global/AGENTS.md` to your tool's config file (`.cursorrules`, `.clinerules`, etc.).

## Files

| File               | Audience    | Purpose                            |
| ------------------ | ----------- | ---------------------------------- |
| `README.md`        | Humans + AI | Quick start, overview              |
| `PATTERNS.md`      | AI agents   | Detailed organization patterns     |
| `global/AGENTS.md` | AI agents   | Template for user/project config   |
| `agents/*.md`      | AI agents   | Reference subagent implementations |
| `skills/*.md`      | Claude Code | Skills (`/setup-ai`, `/save`)      |

## Subagents

Reference implementations in `agents/`:

| Agent        | Purpose                | Trigger                                           |
| ------------ | ---------------------- | ------------------------------------------------- |
| `researcher` | External knowledge     | Need library docs, best practices, current info   |
| `designer`   | Architecture, planning | Complex task decomposition, system design         |
| `reviewer`   | Quality validation     | After implementation, before commit               |
| `profiler`   | Performance analysis   | Bottlenecks, optimization, benchmarking           |

## License

Apache 2.0
