---
description: Update ai/ files before compaction or session end
allowed-tools: Read, Write, Edit, Glob, Grep
---

Update ai/ files to preserve session context.

## Steps

1. **Read current state**: Check ai/STATUS.md, ai/DESIGN.md, ai/DECISIONS.md
2. **Update STATUS.md**: Current metrics, active work, blockers, what worked/didn't
3. **Update DESIGN.md**: If architecture changed
4. **Update DECISIONS.md**: If new decisions were made (append-only)
5. **Prune historical content**: Trust git history, keep files current-focused
6. **Mark tasks complete**: Update any finished tasks

Keep session files under 500 lines. Move details to subdirs (research/, design/).
