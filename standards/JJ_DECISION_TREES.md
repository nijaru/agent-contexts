# JJ Decision Trees for AI Agents

## CRITICAL: JJ vs Git Detection (ALWAYS CHECK FIRST)
```
IF directory_contains(.jj/):
    → USE_JJ_COMMANDS_ONLY
    → NEVER_USE_GIT_COMMANDS
ELIF directory_contains(.git/) AND user_prefers_jj:
    → ASK_TO_INITIALIZE_JJ
ELSE:
    → USE_GIT_COMMANDS
```

## DECISION: AI Agent Starting Work
```
IF existing_repo:
    IF .jj/ directory exists:
        → jj new -m "ai: starting [task]"  # Create sandbox revision
    ELIF .git/ exists AND want_jj:
        → CONFIRM: "Initialize JJ in existing Git repo?"
        → jj git init --colocate
        → jj new -m "ai: starting [task]"
    ELSE:
        → USE_GIT_WORKFLOW
ELSE:
    → jj init                           # New repo
    → jj new -m "ai: starting [task]"    # Create sandbox
```

## DECISION: AI Agent Made Mistakes (SAFETY FIRST)
```
IF minor_mistakes (typos, small changes):
    → jj squash                     # Safe - just cleans commits
ELIF major_mistakes (wrong logic, but recent):
    → jj op log -l 5               # Show recent operations FIRST
    → CONFIRM: "Undo operation [X]?"
    → jj op undo                    # Then undo
ELIF complete_disaster:
    → jj op log -l 20              # Show more history
    → IDENTIFY good state ID
    → CONFIRM: "Restore to [ID]? This will lose current work"
    → jj op restore --to=<id>       # Nuclear option
```

## SAFETY: Before Destructive Operations
```
BEFORE jj op undo:
    → jj op log -l 3               # Show what will be undone
    → CHECK: "Will this lose important work?"
    
BEFORE jj op restore:
    → jj log -r 'all()'            # Show all revisions
    → VERIFY: Target state is correct
    
BEFORE jj abandon:
    → jj show [revision]           # Show what will be abandoned
    → CONFIRM: "Delete this work?"
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

## GIT → JJ COMMAND MAPPING (For AI Agents)
| Git Command | JJ Equivalent | Notes |
|-------------|---------------|-------|
| `git status` | `jj st` | Same info |
| `git log --oneline` | `jj log` | Better by default |
| `git add .` | *(automatic)* | JJ tracks everything |
| `git commit -m "msg"` | `jj describe -m "msg"` | Updates current change |
| `git commit -am "msg"` | `jj new -m "msg"` | Creates new change |
| `git push` | `jj git push` | Must use jj git |
| `git pull` | `jj git fetch && jj rebase` | Two steps |
| `git checkout -b name` | `jj bookmark create name` | Different concept |
| `git reset --hard HEAD~1` | `jj op undo` | Much safer |
| `git rebase -i` | `jj squash` or `jj reorder` | Interactive |

## ERROR → SOLUTION MAPPINGS
| Error | Fix Command | When | Safety |
|-------|-------------|------|--------|
| `No current bookmark` | `jj bookmark create main -r @` | After init | Safe |
| `Working copy contains conflicts` | `jj resolve` | After merge | Check files first |
| `Working copy is stale` | `jj edit @` | After operations | Safe |
| `Error: No changes to squash` | `jj new -m "description"` | When no commits | Safe |
| `Refusing to move bookmark backwards` | `jj bookmark set name -r @ --allow-backwards` | Branch conflicts | Confirm first |
| Terminal escape codes | `jj config set ui.diff-editor ':builtin'` | On setup | Safe |

## STATE RECOGNITION PATTERNS
```
# Check if JJ is active
COMMAND: ls -la | grep -E "^\.jj"
IF found:
    → JJ is active, use JJ commands
ELSE:
    → Use Git commands

# Check current JJ state
COMMAND: jj st
OUTPUT: "Working copy changes:"
    → Has uncommitted work
OUTPUT: "No changes"
    → Clean state, ready for work
OUTPUT: "@ [hash] (empty)"
    → Empty change, can add description

# Check bookmark state
COMMAND: jj bookmark list
OUTPUT: "(no bookmarks)"
    → ACTION: jj bookmark create main -r @
OUTPUT: "main: [hash]"
    → Has main bookmark, good to go
```

## CLAUDE CODE + JJ INTEGRATION PATTERNS

### PATTERN: Session Start
```bash
# Claude Code should run this at conversation start
if [ -d .jj ]; then
    echo "🎯 JJ repository detected - using JJ commands"
    jj st                                    # Show current state
    jj new -m "claude: session $(date +%H:%M)"  # Create session checkpoint
else
    echo "📁 Git repository - using Git commands"
fi
```

### PATTERN: Before Major Operations
```bash
# Before large changes, create checkpoint
jj describe -m "claude: about to [describe task]"
jj new -m "claude: implementing [task]"

# This creates a checkpoint you can return to
```

### PATTERN: After Completing Tasks
```bash
# Don't auto-squash - let user decide
jj describe -m "claude: completed [task summary]"

# Show what was done
jj show @
```

### PATTERN: When Things Go Wrong
```bash
# SAFE recovery - show recent history first
jj op log -l 5
echo "Recent operations above. Which looks like a good restore point?"

# Then user can choose
# jj op restore --to=[chosen-id]
```

### PATTERN: Submodule Updates + JJ
```bash
# After submodule updates, create clean checkpoint
if [ -d .jj ]; then
    # JJ handles the tracking automatically
    jj describe -m "chore: update submodules"
    # Don't auto-push - let user decide
else
    # Fallback to Git
    git add . && git commit -m "chore: update submodules"
fi
```

## AI AGENT SAFETY CHECKLIST
```
BEFORE any JJ command:
1. ✅ Verify .jj/ directory exists
2. ✅ Run 'jj st' to see current state  
3. ✅ If destructive operation, show what will change
4. ✅ For 'jj op' commands, show 'jj op log' first

NEVER do these without confirmation:
- jj op undo (shows last operation first)
- jj op restore (shows target state first) 
- jj abandon (shows what will be deleted)

ALWAYS prefer:
- jj new -m "desc" over jj describe when creating work
- jj squash over jj abandon for cleanup
- jj bookmark set over jj bookmark move

CLAUDE CODE SPECIFIC:
- Create session checkpoints with jj new
- Use descriptive commit messages with "claude:" prefix
- Show jj op log before any recovery operations
- Let users decide when to squash/clean history
- Handle submodule updates gracefully
```