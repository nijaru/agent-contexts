# JJ Decision Trees for AI Agents

## DECISION: AI Agent Starting Work
```
IF existing_repo:
    IF .jj_exists:
        → jj new                    # Create sandbox revision
    ELSE:
        → jj git init --colocate    # Initialize with Git compat
        → jj new                    # Create sandbox
ELSE:
    → jj init                       # New repo
    → jj new                        # Create sandbox
```

### DECISION: AI Agent Made Mistakes
```
IF minor_mistakes:
    → jj squash                     # Clean up commits
ELIF major_mistakes:
    → jj op undo                    # Undo last operation  
ELIF complete_disaster:
    → jj op log                     # Find good state
    → jj op restore --to=<id>       # Restore to known good
```

### DECISION: Ready to Share Work
```
IF commits_messy:
    → jj squash                     # Clean up first
    → jj git push                   # Then share
ELSE:
    → jj git push                   # Direct push
```

## COMMAND SEQUENCES

### SEQUENCE: AI Agent Auto-Management (Preferred)
```bash
# AI agents should proactively manage jj at logical boundaries:

# 1. Check if jj is initialized:
if [ -d .jj ]; then
    # Already initialized, create checkpoint
    jj new -m "starting: [task description]"
elif [ -d .git ]; then
    # Git repo exists, colocate jj
    jj git init --colocate
    jj new -m "starting: [task description]"
fi

# 2. During work - checkpoint at major milestones:
jj describe -m "feat: implemented X"     # After feature
jj new -m "fix: addressing Y"            # Before switching tasks
jj new -m "refactor: improving Z"        # Before major changes

# 3. No cleanup needed - user can organize later
# jj tracks everything automatically
```

### SEQUENCE: Manual Fallback
```bash
# If auto-management fails, use simple flow:
jj st                               # Check current state
jj new                              # Create sandbox
# AI agent does work here
```

### SEQUENCE: Emergency Recovery
```bash
jj op log -l 10                     # Show recent operations
jj op undo                          # Try simple undo first
# If that doesn't work:
jj op restore --to=<good_state_id>  # Nuclear option
```

## ERROR → SOLUTION MAPPINGS
| Error | Fix Command | When |
|-------|-------------|------|
| `No current bookmark` | `jj new main` | After init |
| `Working copy contains conflicts` | `jj resolve` | After merge |
| `Working copy is stale` | `jj edit @` | After operations |
| Terminal escape codes | `jj config set ui.diff-editor ':builtin'` | On setup |

## STATE RECOGNITION
```
STATUS: "No bookmarks"
ACTION: jj bookmark create main

STATUS: "Working copy changed"  
ACTION: jj new (if want to preserve)

STATUS: "@ [hash] (empty) description"
ACTION: Normal - ready for work
```