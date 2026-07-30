---
name: setup-ai
description: Initialize, audit, consolidate, or migrate a repository's AI context and instruction wiring.
---

# Setup AI Context

Use this skill when initializing a repository with AI context or auditing an established `ai/` directory. For routine work inside an established context, use `ai-context` and `save` instead.

## Principles

- `ai/` stores non-derivable context, not source code or API specifications.
- Preserve existing instruction files and harness wiring until they have been audited.
- Create only the surfaces the repository will use.
- Do not initialize a task system, rename instruction files, create symlinks, or exclude files automatically without repository policy or explicit user direction.
- Verify current source, Git state, tests, and live configuration before treating context as correct.

## Detection

Inspect:

- `git remote -v` and the README
- the complete instruction chain and symlinks
- existing `ai/`, `.tasks/`, and task tooling
- project manifests and build/test commands
- harness configuration and templates

Choose **Init** when no `ai/` exists. Choose **Audit** when it does.

## Init

Create only the required surfaces. A standard small project may use:

```text
ai/
├── brief.md
├── journal.md
├── decisions.md
└── architecture.md
```

Add `research/`, `design/`, or `tmp/` only when current work needs them. Use the repository's policy for tracking or excluding `ai/`. Initialize `.tasks/` only when the user or repository has chosen `tk`.

The initial files should state their roles and contain no invented project facts. Keep `brief.md` short, make `journal.md` append-only, and give `decisions.md` `Principles` and `Log` sections.

If both Claude Code and Codex/Pi use the repository, preserve or add a symlink only after checking the existing wiring. Do not rename or merge instruction files automatically.

## Audit

1. Inventory `ai/`, instruction files, symlinks, templates, and task state.
2. Read all root context files and the topic indexes.
3. Check for duplicated or contradictory current state.
4. Ensure `brief.md` is a small curated hot view.
5. Ensure `journal.md` is factual, append-only, and cold.
6. Ensure `decisions.md` has stable principles and a bounded recent log.
7. Ensure `architecture.md` describes the current system rather than a stale implementation.
8. Merge overlapping research before creating files.
9. Rewrite stale current-state claims; preserve historical rationale when useful.
10. Search the full instruction chain for obsolete names and contradictory mandates.
11. Verify rendered templates, symlinks, and destinations.

Topic files should use `Findings`, `Applied`, and `Open Questions` sections and cite sources. No universal frontmatter, IDs, expiry system, or candidate database is required. Add metadata only when a demonstrated workflow needs it.

## Promotion boundary

Treat compaction summaries, provider-managed memories, and subagent reports as inputs to validate. The parent agent promotes only verified, future-relevant material into canonical context.

## Verification

Report:

- files created, preserved, changed, or intentionally omitted;
- the authority chain and loading order;
- task-system and tracking decisions;
- stale or contradictory material found;
- rendered or linked destinations checked;
- remaining open questions.
