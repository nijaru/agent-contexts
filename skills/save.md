---
name: save
description: Use when persisting session state before compaction, session handoff, or completion of substantial work in a repo that already uses ai/ context or tk tasks.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Save (Session Persistence)

**Iron Law:** Persist only non-derivable state to the repo's existing memory surfaces. Never assume chat context survives compaction.

## Preflight

- Check which persistence surfaces exist: `ai/`, `.tasks/`, and `tk`.
- Do not create `ai/`, initialize `tk`, add new task systems, or commit purely because this skill ran.
- If neither `ai/` nor `tk` exists, summarize the handoff in the final response instead.

## Checklist

### 1. Tasks (`tk`)

- Only use when `tk` is installed and `.tasks/` exists.
- Log key findings before closing work: `tk log <id> "finding (file:line)"` - high-signal only, skip what's derivable from code.
- Close completed active tasks: `tk done <id>`.
- Add remaining work only when it is real, actionable follow-up: `tk add "title" -p N -d "context"`.

### 2. AI Context (`ai/`)

- Only update files that already exist or are required by the repo's documented `ai/` convention.
- **brief.md:** Regenerate from journal + decisions. Keep <80 lines, active context only.
- **journal.md:** Append timestamped session summary. Format: `- [YYYY-MM-DD] Action/Decision/Learning`.
- **decisions.md:** Append to Log section: `[date] Context -> Decision -> Rationale`. If Log exceeds ~20 entries, compact into Principles.
- **architecture.md:** Record architectural changes only.
- **research/:** Consolidate new findings into the appropriate topic file (Findings / Applied / Open Questions). Create new topic file only if no existing file covers it. Update index.md.
- **design/:** Update component docs as needed. Update index.md.

### 3. Source Control

- Check `git status` before and after edits.
- If repo policy says to commit and the persistence files are tracked, include them in the relevant logical commit.
- Prefer keeping `ai/` local via `.git/info/exclude` when repo policy allows it.
