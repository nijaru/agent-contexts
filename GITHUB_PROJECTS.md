# AI Agent GitHub Projects Integration

*Decision trees and automation patterns for AI agent project management*

## DECISION: AI Agent Task Classification
```
IF task_complexity > 3_steps OR multi_session_work:
    → CREATE_GITHUB_ISSUE
ELIF collaborative_work OR needs_tracking:
    → CREATE_GITHUB_ISSUE  
ELIF simple_fix OR single_file_change:
    → USE_TODOWRITE_ONLY
ELSE:
    → WORK_DIRECTLY
```

## DECISION: TodoWrite → GitHub Sync
```
IF todo_status == "completed" AND github_issue_exists:
    → gh issue close ISSUE_NUM --comment "✅ AI: [todo.content]"
ELIF todo_status == "in_progress" AND github_issue_exists:
    → gh issue comment ISSUE_NUM --body "🤖 Working: [todo.activeForm]"
ELIF todo_items > 5 AND no_github_issues:
    → BULK_CREATE_ISSUES
```

## DECISION: Session Management
```
IF new_ai_session AND existing_project:
    → gh issue list --assignee @me --state open --project PROJECT_ID
    → MAP_TO_TODOWRITE
ELIF session_complete AND todos_finished:
    → SYNC_GITHUB_STATUS
    → CLOSE_COMPLETED_ISSUES
ELIF session_interrupted:
    → UPDATE_ISSUE_COMMENTS_WITH_PROGRESS
```

## COMMAND SEQUENCES

### SEQUENCE: AI Session Start with GitHub Sync
```bash
# Load existing work into TodoWrite
PROJECT_ID=1  # Main project
gh issue list --assignee @me --state open --project $PROJECT_ID \
  --json number,title,body,labels --jq '.[] | {number, title, body}' > /tmp/github_issues.json

# Map to TodoWrite items
while IFS= read -r issue; do
  TITLE=$(echo $issue | jq -r '.title')
  NUM=$(echo $issue | jq -r '.number')
  echo "TodoWrite item: $TITLE (GitHub #$NUM)"
done < /tmp/github_issues.json
```

### SEQUENCE: TodoWrite → GitHub Issue Creation
```bash
# Batch create issues from TodoWrite items
create_github_issues_from_todos() {
  local TODO_ITEMS=("$@")
  for todo in "${TODO_ITEMS[@]}"; do
    ISSUE_NUM=$(gh issue create \
      --title "AI: $todo" \
      --body "Auto-created from AI agent TodoWrite\n\n- [ ] $todo" \
      --label "ai-generated" \
      --assignee @me \
      --project 1 \
      --json number -q '.number')
    echo "Created issue #$ISSUE_NUM for: $todo"
  done
}
```

### SEQUENCE: Sync Completed Work
```bash
# Close GitHub issues for completed todos
sync_completed_todos() {
  local COMPLETED_TODOS=("$@")
  for todo in "${COMPLETED_TODOS[@]}"; do
    # Find matching GitHub issue
    ISSUE_NUM=$(gh issue list --search "AI: $todo in:title" \
      --json number -q '.[0].number')
    
    if [ "$ISSUE_NUM" != "null" ]; then
      gh issue close $ISSUE_NUM \
        --comment "✅ AI agent completed: $todo"
    fi
  done
}
```

### SEQUENCE: AI Agent Complex Feature Implementation
```bash
# Break complex task into GitHub-tracked subtasks
implement_complex_feature() {
  local FEATURE="$1"
  local PARENT_ISSUE=$(gh issue create \
    --title "AI: Implement $FEATURE" \
    --body "Complex feature broken into AI agent subtasks" \
    --label "ai-epic" \
    --assignee @me \
    --project 1 \
    --json number -q '.number')
  
  # Create subtask issues
  declare -a SUBTASKS=(
    "Research existing $FEATURE patterns"
    "Design $FEATURE architecture" 
    "Implement core $FEATURE functionality"
    "Add $FEATURE tests"
    "Update $FEATURE documentation"
  )
  
  for subtask in "${SUBTASKS[@]}"; do
    gh issue create \
      --title "AI: $subtask" \
      --body "Subtask of #$PARENT_ISSUE\n\n- [ ] $subtask" \
      --label "ai-subtask" \
      --assignee @me \
      --project 1
  done
  
  echo "Created parent issue #$PARENT_ISSUE with ${#SUBTASKS[@]} subtasks"
}
```

## AI AGENT PATTERNS

### ❌ WRONG vs ✅ CORRECT Integration

**❌ WRONG: Create GitHub issue for every todo**
```bash
# Creates noise, overwhelming project board
for todo in "${ALL_TODOS[@]}"; do
  gh issue create --title "$todo"
done
```

**✅ CORRECT: Strategic issue creation**
```bash
# Only create issues for complex, trackable work
IF todo_complexity > simple_task:
  gh issue create --title "AI: $todo" --label "ai-generated"
ELSE:
  # Keep in TodoWrite only
FI
```

**❌ WRONG: Ignore existing GitHub issues**
```bash
# AI agent starts fresh, duplicates work
TodoWrite new items without checking GitHub
```

**✅ CORRECT: Sync with existing work**
```bash
# Check for existing issues first
gh issue list --assignee @me --state open | \
  while read issue; do
    # Add to TodoWrite as pending
  done
```

**❌ WRONG: Manual status updates**
```bash
# Requires human intervention
gh issue edit 123 --add-label "in-progress"
```

**✅ CORRECT: Automated status sync**
```bash
# TodoWrite status changes trigger GitHub updates
on_todo_status_change() {
  local TODO="$1" STATUS="$2"
  case $STATUS in
    "in_progress") update_github_status "$TODO" "In Progress" ;;
    "completed")   close_github_issue "$TODO" ;;
  esac
}
```

## AI SESSION MANAGEMENT

### PATTERN: Session Initialization
```bash
# AI agent session starts
ai_session_init() {
  echo "🤖 AI Agent Session Start: $(date)"
  
  # 1. Check for existing work
  OPEN_ISSUES=$(gh issue list --assignee @me --state open --project 1 --json number,title)
  
  # 2. Convert to TodoWrite format
  echo "$OPEN_ISSUES" | jq -r '.[] | "\(.title) (GitHub #\(.number))"' > /tmp/ai_todos.txt
  
  # 3. Mark session active
  gh issue comment --body "🤖 AI agent session started" $(echo "$OPEN_ISSUES" | jq -r '.[0].number' 2>/dev/null || echo "")
}
```

### PATTERN: Session Completion
```bash
# AI agent session ends
ai_session_complete() {
  local COMPLETED_TODOS=("$@")
  
  echo "🤖 AI Agent Session Complete: $(date)"
  
  # 1. Close completed GitHub issues
  for todo in "${COMPLETED_TODOS[@]}"; do
    sync_completed_todo "$todo"
  done
  
  # 2. Update in-progress issues
  for todo in "${IN_PROGRESS_TODOS[@]}"; do
    update_github_progress "$todo"
  done
  
  # 3. Create issues for new pending todos
  for todo in "${NEW_TODOS[@]}"; do
    create_github_issue_if_complex "$todo"
  done
}
```

## ERROR → SOLUTION MAPPINGS

| AI Agent Error | GitHub Command Fix | When |
|----------------|--------------------|----- |
| `No GitHub token` | `gh auth login --scopes project` | First run |
| `Issue already exists` | `gh issue list --search "title:$TITLE"` | Before create |
| `Project not found` | `gh project list --owner @me` | Check project ID |
| `Rate limit exceeded` | `sleep 60 && retry_command` | Batch operations |
| `TodoWrite out of sync` | `ai_session_sync_github` | After interruption |

## AUTOMATION TRIGGERS

### GitHub Actions Integration
```yaml
# .github/workflows/ai-agent-sync.yml
name: AI Agent Sync
on:
  issue_comment:
    types: [created]
  
jobs:
  ai-sync:
    if: contains(github.event.comment.body, '🤖')
    runs-on: ubuntu-latest
    steps:
      - name: Parse AI agent comment
        run: |
          COMMENT="${{ github.event.comment.body }}"
          if [[ $COMMENT == *"Working:"* ]]; then
            gh issue edit ${{ github.event.issue.number }} --add-label "ai-in-progress"
          elif [[ $COMMENT == *"Completed:"* ]]; then
            gh issue close ${{ github.event.issue.number }}
          fi
```

## INTEGRATION UTILITIES

### TodoWrite ↔ GitHub Sync Functions
```bash
# Core integration functions for AI agents

# Convert GitHub issues to TodoWrite format
github_to_todowrite() {
  gh issue list --assignee @me --state open --project 1 \
    --json number,title,body,labels | \
    jq -r '.[] | "\(.title) (GitHub #\(.number))"'
}

# Create GitHub issue from TodoWrite item
todowrite_to_github() {
  local TODO="$1"
  local COMPLEXITY="$2"  # simple|complex|epic
  
  case $COMPLEXITY in
    "complex"|"epic")
      gh issue create \
        --title "AI: $TODO" \
        --body "Auto-created from AI agent TodoWrite" \
        --label "ai-generated" \
        --assignee @me \
        --project 1
      ;;
    *)
      echo "Keep in TodoWrite only: $TODO"
      ;;
  esac
}

# Sync TodoWrite completion to GitHub
sync_completed_todo() {
  local TODO="$1"
  local ISSUE_NUM=$(gh issue list --search "AI: $TODO in:title" \
    --state open --json number -q '.[0].number')
  
  if [ "$ISSUE_NUM" != "null" ] && [ "$ISSUE_NUM" != "" ]; then
    gh issue close $ISSUE_NUM \
      --comment "✅ AI agent completed: $TODO"
  fi
}
```

## QUICK COMMAND REFERENCE

### Essential AI Agent Commands
```bash
# Session initialization
gh issue list --assignee @me --state open --project 1 --json number,title

# Create AI task issue
gh issue create --title "AI: [task]" --label "ai-generated" --assignee @me --project 1

# Update issue progress
gh issue comment [ISSUE_NUM] --body "🤖 Working: [current_status]"

# Close completed issue
gh issue close [ISSUE_NUM] --comment "✅ AI agent completed"

# Bulk status check
gh issue list --search "label:ai-generated assignee:@me" --state open --json number,title,labels

# Clean up AI issues
gh issue list --label "ai-generated" --state closed --search "closed:<30days" \
  --json number | jq -r '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "archived"
```

### MCP Integration Setup
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {"GITHUB_TOKEN": "ghp_..."}
    }
  }
}
```

## PROJECT CONFIGURATION

### User Settings (nijaru)
```bash
# Default configuration for AI agent integration
USER="nijaru"
DEFAULT_PROJECT=1
AI_LABELS=("ai-generated" "ai-in-progress" "ai-completed")
PRIORITY_LABELS=("P0" "P1" "P2" "P3")
TYPE_LABELS=("feat" "bug" "task" "docs" "perf" "chore")

# AI-specific branch naming
AI_BRANCH_PREFIX="ai/"
BRANCH_FORMAT="${AI_BRANCH_PREFIX}[issue-num]-[description]"
```

### State Transitions for AI Agents
```
TodoWrite "pending" → GitHub "Backlog"
TodoWrite "in_progress" → GitHub "In Progress" + comment
TodoWrite "completed" → GitHub "Done" + close issue

AI Session Start → Load GitHub issues to TodoWrite
AI Session End → Sync TodoWrite status to GitHub
AI Session Interrupt → Update GitHub with current progress
```

---
*Optimized for AI agent automation and integration patterns*