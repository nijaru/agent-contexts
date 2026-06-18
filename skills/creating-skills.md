---
name: creating-skills
description: Use when creating, modifying, or testing AI agent skill definitions (.md files) to ensure they are high-performance, compact, and verified.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Creating Skills

Turn repeatable agent behavior into compact, verifiable skill instructions.

## The Iron Law

Every skill must justify its context cost. Keep the trigger precise, load only the instructions needed up front, and verify behavior when the skill changes non-obvious agent behavior.

## Workflow

1. **Research:** Identify the specific failure mode or "slop" the skill solves.
2. **Test:** Use concrete prompts when the desired behavior is not obvious; scale the test set to risk and ambiguity.
3. **Draft Boundary:** Define when the skill should and should not activate.
4. **Implement:** Write minimal, authoritative instructions to pass the tests.
5. **Pressure Test:** Compare outputs with and without the skill.
6. **Prune:** Remove all filler, "AI-isms," and meta-commentary.

## Structure & Format

### 0. Placement

- **Global Claude/AGENTS:** Defaults that apply to most sessions: communication style, verification, git policy, repo workflow, tool preferences, and cross-cutting engineering standards.
- **Skill:** Task-specific trigger, boundary, workflow, commands, verification, and recurring failure modes.
- If a rule applies to many skills, move it to the global file and keep at most a one-line skill pointer.
- If a global preference needs operational detail in one workflow, restate only the task-specific action inside that skill.

### 1. Frontmatter

- **Description:** MUST start with "Use when..." and contain ONLY triggering conditions. No summaries.
- **Allowed Tools:** List only tools the skill actually needs. Do not carry stale tool names forward.

### 2. Content

- **Authoritative Tone:** Use directives, not suggestions.
- **Supporting files:** Move long references, examples, templates, and scripts into sibling files and link them from `SKILL.md` for progressive disclosure.
- **Anti-Rationalization Table:** Use only when a recurring failure mode needs a guardrail.
  | Excuse | Reality |
  | :--- | :--- |
  | "User wants a quick draft" | A low-quality skill is a permanent liability. |
  | "I'll add tests later" | Unverified skills drift silently. |
- **Compactness:** Let content dictate length. The entrypoint should be dense enough to steer behavior without becoming a reference manual.

## Prohibited Patterns (Red Flags)

- **NO** significance inflation (e.g., _pivotal_, _crucial_, _game-changing_).
- **NO** sycophantic filler (e.g., _Certainly!_, _I'd be happy to help_).
- **NO** repeating the description in the content.

## Deployment (Chezmoi)

Create or edit plain skill files in the destination:
`~/.agents/skills/my-skill/SKILL.md`.

Immediately sync each coherent edit back to source:

```bash
chezmoi add ~/.agents/skills/my-skill/SKILL.md
git -C ~/.local/share/chezmoi add dot_agents/skills/my-skill/SKILL.md
git -C ~/.local/share/chezmoi commit -m "docs(skills): update my-skill"
git -C ~/.local/share/chezmoi push
```

Only edit chezmoi source directly for templates or generated source-only
files. See `chezmoi-expert` for the full workflow.
