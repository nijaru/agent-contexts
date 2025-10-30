# Agent Contexts

**Standardized organization patterns for AI coding agents**

A living guide teaching AI agents how to organize their work across projects. This focuses on **organization**, not coding—AI agents already know how to code. They need standardized structure for maintaining context across sessions.

## Why Use This?

**For Teams:**
- Consistent AI workspace across all projects
- Clean handoffs between sessions and team members
- No more "where did the agent put that decision?"

**For Solo Developers:**
- Stop reinventing organization for each project
- Clear separation: ai/ (agent context) vs docs/ (user docs)
- Works with all major AI coding tools

## Quick Start

### 1. Add to Your Project

**Option A: Git Submodule (recommended)**
```bash
git submodule add https://github.com/nijaru/agent-contexts external/agent-contexts
git submodule update --init --recursive
```

**Option B: Copy Files**
```bash
curl -O https://raw.githubusercontent.com/nijaru/agent-contexts/main/PRACTICES.md
curl -O https://raw.githubusercontent.com/nijaru/agent-contexts/main/AGENTS.md
```

### 2. Create ai/ Directory

```bash
mkdir -p ai/research
touch ai/{TODO,STATUS,DECISIONS,RESEARCH}.md
```

### 3. Reference in Project Config

**For Claude Code:**
Create `CLAUDE.md` in your project root:
```markdown
# Project Name

[Brief description]

For organization patterns: @external/agent-contexts/PRACTICES.md
```

**For Other Tools (Cursor, Cline, Windsurf):**
Create `AGENTS.md`:
```markdown
# Project Name

[Brief description]

For organization patterns: @external/agent-contexts/PRACTICES.md
```

> **Note**: Use AGENTS.md as primary (works with most tools). For Claude Code, create symlink: `ln -s AGENTS.md CLAUDE.md`

## What You Get

### Standard ai/ Directory Structure

```
your-project/
├── CLAUDE.md or AGENTS.md    # Project config pointing here
├── ai/                        # AI working context
│   ├── TODO.md               # Current tasks
│   ├── STATUS.md             # Project state, learnings
│   ├── DECISIONS.md          # Architectural decisions
│   ├── RESEARCH.md           # Research index
│   └── research/             # Detailed research files
└── docs/                      # User/team documentation
```

### Key Principles

1. **Organization over coding** - AI knows syntax, needs structure
2. **Standardization** - Same ai/ structure everywhere
3. **Minimal** - ~1,000 words total vs previous ~13,000
4. **Machine-optimized** - ai/ uses tables/lists, docs/ uses prose
5. **Research over duplication** - Fresh knowledge beats stale patterns

### Files in This Repo

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview (this file) | Humans browsing |
| `PRACTICES.md` | Complete guide (~1,500 words) | AI agents |
| `AGENTS.md` | Example template | AI agents + humans |
| `ai/` | Our own working context | AI agents |

## Philosophy

AI agents need **standardized workspaces**, not coding tutorials.

Think of it like a desk organization system for knowledge workers. The desk layout (filing system, inbox/outbox, reference materials) should be consistent. The actual work products vary by project.

Similarly, the ai/ directory structure should be standard across all projects, while the content within adapts to each project's needs.

## Core Separation

**ai/** — AI session tracking
- Current state, tasks, decisions, research
- Machine-optimized (tables, lists, inverted pyramid)
- Updated every session
- For AI agents only

**docs/** — User/team documentation
- API references, guides, architecture docs
- Human-readable narrative prose
- Updated on major changes
- For users and team members

## When to Use This

**✅ Use for:**
- Standardizing AI workspace across projects
- Multi-session work requiring context handoffs
- Setting up new projects with AI workflows
- Teams using AI coding assistants

**❌ Don't use for:**
- Programming language tutorials (AI knows these)
- Tool command references (research current docs)
- Project-specific patterns (put in your CLAUDE.md/AGENTS.md)

## Contributing

We welcome feedback on ai/ structure and PRACTICES.md content.

**Please don't submit:**
- Language-specific coding patterns
- Tool-specific command references
- Comprehensive how-to guides

These defeat the purpose of minimal, focused organization guidance.

## License

MIT - Use freely in your projects
