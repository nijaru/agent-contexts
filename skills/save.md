---
name: save
description: Update ai/ files and tk tasks.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Context Save

Persist session state to ai/ and tk. Priority: tk and ai/ first (from context), git last.

**Trigger:** Before `/compact`, session end, context switch, or explicitly.

## 1. Update tk Tasks

```bash
tk ls
```

For each task:

- **Log findings first:** `tk log <id> "what was learned"` — errors, root cause, file paths. High-signal only; skip what's derivable from code.
- **Mark complete:** `tk done <id>`
- **Add new:** `tk add "title" -d "context"`

Don't leave stale tasks.

## 2. Update ai/

**README.md** (if files added, changed, or deleted): Update index pointers. Format: `- [Title](path) — one-line hook`. Verify all links are live; remove dead ones.

**STATUS.md** (always): Phase, active focus, blockers. Prune stale content.

**DESIGN.md** (if architecture changed): Components, patterns, interfaces.

**DECISIONS.md** (if decisions made): Append to Log section: `[date] Context → Decision → Rationale`. If Log exceeds ~20 entries, run `/setup-ai` next session to compact into Principles.

**PLAN.md** (if sprint progress): Update sprint status or task progress.

## 3. Commit

```bash
git add ai/ .tasks/
git commit -m "chore(ai): update session context"
```

## 4. Report

```
## Saved

Tasks: [N done, N added, N pending]
ai/: [what changed]

## Next Session

[2-4 bullets: what to do next based on pending tasks, blockers, incomplete work]
```
