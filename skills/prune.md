---
name: prune
description: Clean up temp files, stale tasks, and organize ai/ directory.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Prune

Clean up project cruft and keep ai/ healthy. Run when things feel cluttered.

## 1. Survey

```bash
ls -la
ls -R ai/
tk ls
git status --short
```

## 2. Clean Files

For each file in root or unexpected locations:

- **No purpose** → delete it
- **Has purpose, wrong location** → move (`scripts/`, `tests/`, etc.)
- **Has purpose, right location** → keep

Don't touch: `.git/`, config files, source code.

## 3. Organize ai/

Goal: every file is findable via `ai/README.md`. One doc per topic, no scattered duplicates.

**Root files:**

- `README.md` — index only (pointers, ~150 chars/entry). Rebuild after any changes.
- `STATUS.md` — prune aggressively: remove resolved blockers, completed work, outdated state.
- `DESIGN.md` — remove descriptions of deleted/changed components.
- `DECISIONS.md` — never delete Log entries. If Log > ~20 entries, distill oldest into Principles section.
- `PLAN.md` — update sprint status if progress was made.

**Subdirs (research/, design/, review/, sprints/):**

- Add missing frontmatter (`date`, `summary`, `status: active|resolved|stale`).
- `status: resolved` or `status: stale` → delete (don't archive).
- Consolidate files on the same topic into one focused doc.
- Split multi-topic files into single-topic docs.

**After changes:** Rewrite `ai/README.md` to reflect what actually exists. Remove dead links.

## 4. Tasks

Mark completed done (`tk done <id>`), delete stale ones, consolidate duplicates.

## 5. Finish

```bash
git add ai/ .tasks/
git diff --cached --stat  # review what changed
git commit -m "chore(ai): prune workspace"
```

Report what was removed, reorganized, or left alone.
