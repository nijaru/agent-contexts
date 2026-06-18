---
name: setup-ai
description: |
  Use when initializing, auditing, consolidating, or migrating repo AI context files
  such as AGENTS.md, CLAUDE.md, ai/, or related task state.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Setup AI Context

Initialize a new project's AI context, or audit and migrate an existing one. For ongoing operation within an established `ai/`, use `ai-context` instead.

## Detection Phase

Read in parallel:

- **Identity:** `git remote -v`, `README.md` (first paragraph)
- **Stack:** `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`
- **Existing context:** `ls -la ai/` if it exists, `AGENTS.md`, `CLAUDE.md`
- **Infrastructure:** `Makefile`, `justfile`, `.claude/settings.json`

Determine mode: **Init** (no ai/ exists) or **Audit** (ai/ exists).

## AGENTS.md / CLAUDE.md Configuration

| Scenario | Action |
|:---|:---|
| Neither file exists | Create `AGENTS.md`, symlink `./CLAUDE.md` → `AGENTS.md` |
| Only `CLAUDE.md` at root | Rename to `AGENTS.md`, create symlink (leave as-is for OSS repos) |
| Both exist | Merge to `AGENTS.md`, remove old `CLAUDE.md`, create symlink |

## Mode: Init (New Repo)

### 1. Scaffold

```bash
mkdir -p ai/research ai/design ai/tmp
echo '*' > ai/tmp/.gitignore
tk init
```

Keep ai/ local (not committed):

```bash
echo 'ai/' >> .git/info/exclude
echo '.tasks/' >> .git/info/exclude
```

### 2. Create Root Files

**ai/brief.md:**
```markdown
Task: [initial setup]
State: [what's been done]
Files: [key files]
Blockers: [none or specific]
Next: [next step]
```

**ai/journal.md:**
```markdown
# Session Journal

Write here before compaction or when switching agents. Append-only.
```

**ai/decisions.md:**
```markdown
# Decisions

## Principles

_Distilled from resolved decisions. Stable, load-bearing context._

## Log

_Recent decisions, ~20 entries max. Format: `[date] Context → Decision → Rationale`_
```

**ai/architecture.md:**
```markdown
# Architecture

## System Overview

[System overview]

## Components

[Component map]
```

**ai/research/index.md** and **ai/design/index.md:**
```markdown
# Research Topics

<!-- Entries added as topic files are created -->
```

### 3. Verify

```bash
ls -la AGENTS.md CLAUDE.md     # verify symlink
tk ready                        # verify task tracking
ls -R ai/                       # verify structure
```

## Mode: Audit (Existing Repo)

Run when ai/ is out of sync, overlapping, or bloated.

### 1. Inventory

```bash
find ai/ -name "*.md" | sort
```

Read all root files. List research topic files and check for overlap.

### 2. Structure Migration

Ensure current conventions from `ai-context` are in place:

- `ai/brief.md` exists and is <80 lines
- `ai/journal.md` exists and is append-only
- `ai/decisions.md` has **Principles** + **Log** sections
- `ai/architecture.md` exists
- `ai/research/` has an `index.md`
- Topic files follow the consolidated format (Findings / Applied / Open Questions)

### 3. Research Consolidation

The most common audit action. Research files tend to fragment over time:

- **Merge overlapping files.** `hashing-xxhash3.md` + `hashing-blake3.md` → `hashing.md`.
- **One file per topic area.** If two files cover related topics, merge them.
- **Check for stale files.** No updates in 3+ months and no references from decisions.md → verify relevance, archive or delete.
- **Rebuild index.md** after any merges or deletions.

### 4. Stale Detection

For each file in `research/`, `design/`:

- Last modified > 3 months → verify relevance
- No references from decisions.md or architecture.md → candidate for deletion
- Content fully absorbed into code or architecture → keep but note as applied

### 5. DECISIONS.md Compaction

If Log section exceeds ~20 entries, compact per `ai-context` rules.

### 6. brief.md Regeneration

Regenerate `ai/brief.md` from journal + decisions per `save` skill checklist.

## Anti-Patterns

| Excuse | Reality |
|:---|:---|
| "It's a small project" | Inconsistent structure causes context drift in 3 sessions |
| "I'll keep old research files just in case" | Overlapping files waste tokens. Consolidate. |
| "I'll clean this up after the PR" | Post-PR cleanup rarely happens. Clean now. |
| "This project doesn't need research/" | Then don't create it. Only add directories that will be used. |
