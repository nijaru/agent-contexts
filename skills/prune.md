---
name: prune
description: |
  Use when cleaning workspace clutter, organizing ai/ context, removing stale task files,
  reducing root-directory sprawl, or deleting redundant temporary scripts.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Prune (Workspace Hygiene)

## Core Mandates

- **Root Zero:** No temporary files in the project root. Move to `scripts/` or delete.
- **Single Source:** Consolidate scattered `ai/` notes into single-topic documents.
- **Index Integrity:** `ai/research/index.md` and `ai/design/index.md` must reflect what actually exists — no dead links, no missing entries.
- **Task Integrity:** Mark completed tasks (`tk done`) and delete duplicates.

## Cleanup Standards

### 1. File Triage

For every file in the root or unexpected locations:

- **No purpose:** Delete immediately.
- **Useful tool:** Move to `scripts/` or `bin/`.
- **Useful test:** Move to `tests/`.
- **Core config:** Keep in root.

### 2. AI Directory Cleanup

Reference `ai-context` for structure and conventions. When cleaning:

- **Research consolidation:** Merge overlapping topic files. One comprehensive file per topic area. Rebuild index.md.
- **Stale files:** No updates in 3+ months and no references → verify, archive or delete.
- **Index sync:** After any deletions or consolidations, rebuild `index.md` to match reality.

### 3. Task Management

- Mark finished tasks as done: `tk done <id>`.
- Delete stale or irrelevant tasks.

## Execution Workflow

1. **Survey:** `ls -R ai/`, `tk ls`, `git status --short`.
2. **Triage:** Delete, move, and consolidate files per standards above.
3. **Rebuild index:** Rewrite `ai/research/index.md` and `ai/design/index.md` to match reality.
4. **Commit:** Stage all changes with `chore(ai): prune workspace`.

## Anti-Rationalization

| Excuse | Reality |
|:---|:---|
| "I'll clean this up after the PR." | Post-PR cleanup rarely happens; debt starts with "just one temp file." |
| "I might need this debug script." | If useful, it belongs in `scripts/` with a descriptive name. |
| "The ai/ directory is fine as is." | Scattered notes force future agents to waste tokens on redundant content. |
| "I'll keep the file just in case." | Stale files pollute context. Consolidate or delete. |

## Safe Exclusions

- **NEVER** touch `.git/` or core project configuration files.
- **NEVER** delete source code unless specifically instructed.
- **NEVER** delete DECISIONS.md Log entries — distill into Principles instead (per `ai-context`).
