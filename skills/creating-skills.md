---
name: creating-skills
description: Use when wanting to turn a technique into a reusable skill, create a new skill, or make current work available for future sessions
---

# Creating Skills

Turn techniques into reusable skills for future sessions.

## Decide: Project vs Global

| Scope   | Location                             | When                                           |
| ------- | ------------------------------------ | ---------------------------------------------- |
| Project | `.claude/skills/my-skill/SKILL.md`   | Project-specific patterns, commands, workflows |
| Global  | `~/.claude/skills/my-skill/SKILL.md` | Cross-project techniques                       |

## SKILL.md Format

```markdown
---
name: my-skill
description: Use when [specific triggering conditions]
---

# My Skill

Brief overview - what this does.

## When to Use

- Specific symptoms or situations
- NOT: what the skill does (that goes in content)

## The Pattern / Steps

[Main content - technique, steps, reference]

## Common Mistakes

[What goes wrong + fixes]
```

## When to Use

- User says "make this a skill", "save this for later", "I want to reuse this"
- Technique worked well and applies beyond current project
- NOT: one-off solutions, project-specific conventions (use CLAUDE.md instead)

## Quick Create

```bash
# Project-local skill
mkdir -p .claude/skills/my-skill
$EDITOR .claude/skills/my-skill/SKILL.md

# Global skill
mkdir -p ~/.claude/skills/my-skill
$EDITOR ~/.claude/skills/my-skill/SKILL.md
```

## Key Rules

1. **Description = when to use, never what it does** (Claude may skip reading if description summarizes workflow)
2. **Start description with "Use when..."**
3. **Name uses only letters, numbers, hyphens**
4. **One excellent example beats many mediocre ones**
5. **Test the skill** before committing

## After Creating

```bash
# Commit project skill
git add .claude/skills/ && git commit -m "Add my-skill"
```
