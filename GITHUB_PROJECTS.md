# AI Agent GitHub Projects Integration

*Decision trees and automation patterns for AI agent project management*

## CORE PRINCIPLE: Projects vs Issues

**GitHub Projects** = Internal development planning and task tracking
- Sprint planning and milestone management  
- Feature implementation tasks
- Architecture decisions and technical work
- AI agent development coordination

**GitHub Issues** = External problem reporting and community interaction
- Bug reports from users
- Feature requests from community  
- Problems that need fixing
- External contributions and discussions

**TodoWrite** = AI session task tracking with optional Project sync

## DECISION: AI Agent Task Classification
```
IF development_task OR feature_implementation OR sprint_planning:
    → CREATE_PROJECT_ITEM (in development project)
ELIF bug_report OR user_request OR external_contribution:
    → CREATE_GITHUB_ISSUE (for community/support)
ELIF simple_single_session_task:
    → USE_TODOWRITE_ONLY
ELSE:
    → WORK_DIRECTLY
```

**Key Decision Factors:**
- Multi-session work → Project Item
- External visibility needed → Issue  
- Internal planning → Project Item
- User-reported problem → Issue
- AI development task → Project Item

## DECISION: TodoWrite → GitHub Project Sync
```
IF todo_status == "completed" AND project_item_exists:
    → gh project item-edit PROJECT_NUM --id ITEM_ID --field "Status" --value "Done"
ELIF todo_status == "in_progress" AND project_item_exists:
    → gh project item-edit PROJECT_NUM --id ITEM_ID --field "Status" --value "In Progress"  
ELIF complex_todo_items > 3 AND no_project_items:
    → BULK_CREATE_PROJECT_ITEMS
```

## DECISION: Session Management
```
IF new_ai_session AND existing_project:
    → gh project item-list PROJECT_NUM --owner @me --format json
    → MAP_ACTIVE_ITEMS_TO_TODOWRITE
ELIF session_complete AND todos_finished:
    → SYNC_PROJECT_ITEM_STATUS
    → MARK_COMPLETED_ITEMS_DONE
ELIF session_interrupted:
    → UPDATE_PROJECT_ITEM_STATUS_TO_IN_PROGRESS
```

## PROJECT SETUP COMMANDS

### Create Development Project
```bash
# One-time setup for AI agent development
gh project create --owner @me --title "Aircher Development"

# Get project number for future commands  
PROJECT_NUM=$(gh project list --owner @me --format json | jq -r '.[] | select(.title=="Aircher Development") | .number')
echo "Project Number: $PROJECT_NUM"
```

### Add Required Scopes
```bash
# Required permissions for project management
gh auth refresh --hostname github.com -s read:project -s project
```

## COMMAND SEQUENCES

### SEQUENCE: AI Session Start with Project Sync
```bash
# Load existing development work into TodoWrite
PROJECT_NUM=1  # Your development project number

# Get active project items  
ACTIVE_ITEMS=$(gh project item-list $PROJECT_NUM --owner @me --format json)

# Convert to TodoWrite format
echo "$ACTIVE_ITEMS" | jq -r '.[] | select(.status != "Done") | "\(.title) (Project #\(.number))"' > /tmp/ai_todos.txt

# Load into TodoWrite session
while IFS= read -r item; do
  echo "TodoWrite item: $item"
done < /tmp/ai_todos.txt
```

### SEQUENCE: TodoWrite → Project Item Creation  
```bash
# Create project items from TodoWrite tasks
create_project_items_from_todos() {
  local PROJECT_NUM="$1"
  local TODO_ITEMS=("${@:2}")
  
  for todo in "${TODO_ITEMS[@]}"; do
    # Create draft issue first (project items need to link to something)
    ISSUE_URL=$(gh issue create \
      --title "AI: $todo" \
      --body "Development task created from AI agent TodoWrite

## Task Description
$todo

## Status  
- [ ] In Progress
- [ ] Testing
- [ ] Complete

Auto-created for project management." \
      --assignee @me \
      --draft)
    
    # Add to project
    gh project item-add $PROJECT_NUM --url "$ISSUE_URL"
    echo "Created project item for: $todo"
  done
}
```

### SEQUENCE: Sync Completed Work to Project
```bash
# Update project item status for completed todos
sync_completed_todos_to_project() {
  local PROJECT_NUM="$1"
  local COMPLETED_TODOS=("${@:2}")
  
  for todo in "${COMPLETED_TODOS[@]}"; do
    # Find matching project item
    ITEM_ID=$(gh project item-list $PROJECT_NUM --format json | \
      jq -r --arg todo "$todo" '.[] | select(.title | contains($todo)) | .id')
    
    if [ "$ITEM_ID" != "null" ] && [ "$ITEM_ID" != "" ]; then
      # Mark as Done in project
      gh project item-edit $PROJECT_NUM --id "$ITEM_ID" \
        --field "Status" --value "Done"
        
      # Close associated issue if exists
      ISSUE_NUM=$(gh project item-list $PROJECT_NUM --format json | \
        jq -r --arg id "$ITEM_ID" '.[] | select(.id == $id) | .content.number')
      
      if [ "$ISSUE_NUM" != "null" ]; then
        gh issue close "$ISSUE_NUM" \
          --comment "✅ AI agent completed: $todo"
      fi
      
      echo "✅ Completed: $todo"
    fi
  done
}
```

### SEQUENCE: AI Agent Feature Development (Full Lifecycle)
```bash
# Complete development workflow for major features
implement_feature_with_project_tracking() {
  local FEATURE="$1"
  local PROJECT_NUM="$2"
  
  echo "🚀 Starting feature development: $FEATURE"
  
  # 1. Create epic issue for the feature
  EPIC_ISSUE=$(gh issue create \
    --title "Feature: $FEATURE" \
    --body "# $FEATURE Implementation

## Overview
AI agent feature development with full project tracking.

## Development Phases
- [ ] Architecture Design
- [ ] Core Implementation  
- [ ] Testing & Validation
- [ ] Documentation
- [ ] Integration

## Success Criteria
- Feature works as specified
- Tests pass
- Documentation updated
- Performance benchmarks met

Epic for project management." \
    --assignee @me)
    
  # 2. Add epic to project
  EPIC_ITEM_ID=$(gh project item-add $PROJECT_NUM --url "$EPIC_ISSUE" --format json | jq -r '.id')
  
  # 3. Create subtasks
  declare -a SUBTASKS=(
    "Research existing $FEATURE patterns and approaches"
    "Design $FEATURE architecture and interfaces"
    "Implement core $FEATURE functionality"
    "Add comprehensive $FEATURE tests"
    "Update $FEATURE documentation"
    "Performance optimization for $FEATURE"
    "Integration testing with existing systems"
  )
  
  echo "📋 Creating subtasks..."
  for subtask in "${SUBTASKS[@]}"; do
    SUBTASK_ISSUE=$(gh issue create \
      --title "AI: $subtask" \
      --body "Subtask of $EPIC_ISSUE

## Task
$subtask

## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests passing  
- [ ] Code reviewed
- [ ] Documentation updated

Part of $FEATURE development." \
      --assignee @me)
      
    # Add subtask to project
    gh project item-add $PROJECT_NUM --url "$SUBTASK_ISSUE"
  done
  
  echo "✅ Created epic and ${#SUBTASKS[@]} subtasks for $FEATURE"
  echo "📊 Project URL: https://github.com/users/$(gh api user --jq .login)/projects/$PROJECT_NUM"
}
```

## AI AGENT PATTERNS

### ❌ WRONG vs ✅ CORRECT Project Management

**❌ WRONG: Use Issues for development tasks**
```bash
# Creates noise in issue tracker, confuses external users
gh issue create --title "Refactor authentication module"
gh issue create --title "Add error handling to parser"
gh issue create --title "Optimize search performance"
```

**✅ CORRECT: Use Projects for development, Issues for problems**
```bash
# Development planning in Projects
create_project_items_from_todos 1 \
  "Refactor authentication module" \
  "Add error handling to parser" \
  "Optimize search performance"

# Issues only for bugs/user requests  
gh issue create --title "Bug: Authentication fails on Windows" \
  --body "User reported authentication not working..."
```

**❌ WRONG: Mix development tasks with user issues**
```bash
# Issues list becomes unusable for external contributors
Issues:
#1: "Bug: Crash on startup" (user report)
#2: "Refactor database layer" (internal dev task) 
#3: "Feature request: Dark mode" (user request)
#4: "Update CI pipeline" (internal dev task)
```

**✅ CORRECT: Clear separation of concerns**
```bash
# Issues for external/community interaction
Issues:
#1: "Bug: Crash on startup" (user report)
#2: "Feature request: Dark mode" (user request)

# Projects for internal development planning
Project "Aircher Development":
- Refactor database layer (In Progress)
- Update CI pipeline (Todo)
- Add error handling (Done)
```

**❌ WRONG: Ignore existing project structure**
```bash
# AI agent creates duplicate work
TodoWrite items without checking existing project items
```

**✅ CORRECT: Sync with existing project state**
```bash
# Load existing project items into TodoWrite
gh project item-list 1 --format json | \
  jq -r '.[] | select(.status != "Done") | .title' | \
  while read item; do
    # Add to TodoWrite as pending
    echo "Existing: $item"
  done
```

## AI SESSION MANAGEMENT

### PATTERN: Session Initialization with Project Sync
```bash
# AI agent session starts with project awareness
ai_session_init_with_project() {
  local PROJECT_NUM="$1"
  
  echo "🤖 AI Agent Session Start: $(date)"
  echo "📊 Loading project: $PROJECT_NUM"
  
  # 1. Get current project state
  ACTIVE_ITEMS=$(gh project item-list $PROJECT_NUM --owner @me --format json)
  
  # 2. Load in-progress items to TodoWrite
  echo "$ACTIVE_ITEMS" | jq -r '.[] | select(.status == "In Progress") | "\(.title) (Project Item)"' > /tmp/ai_active.txt
  
  # 3. Load todo items to TodoWrite  
  echo "$ACTIVE_ITEMS" | jq -r '.[] | select(.status == "Todo") | "\(.title) (Project Item)"' > /tmp/ai_todo.txt
  
  # 4. Show summary
  IN_PROGRESS=$(cat /tmp/ai_active.txt | wc -l)
  TODO_COUNT=$(cat /tmp/ai_todo.txt | wc -l)
  
  echo "📈 Status: $IN_PROGRESS in progress, $TODO_COUNT pending"
  echo "🔗 Project: https://github.com/users/$(gh api user --jq .login)/projects/$PROJECT_NUM"
}
```

### PATTERN: Session Completion with Project Updates
```bash
# AI agent session ends with full project sync
ai_session_complete_with_project() {
  local PROJECT_NUM="$1"
  local COMPLETED_TODOS=("${@:2}")
  
  echo "🤖 AI Agent Session Complete: $(date)"
  
  # 1. Update completed items in project
  for todo in "${COMPLETED_TODOS[@]}"; do
    sync_completed_todos_to_project $PROJECT_NUM "$todo"
  done
  
  # 2. Update in-progress items status
  for todo in "${IN_PROGRESS_TODOS[@]}"; do
    update_project_item_status $PROJECT_NUM "$todo" "In Progress"
  done
  
  # 3. Add new todos as project items if complex
  for todo in "${NEW_TODOS[@]}"; do
    if is_complex_task "$todo"; then
      create_project_items_from_todos $PROJECT_NUM "$todo"
    fi
  done
  
  # 4. Generate session summary
  echo "✅ Session Summary:"
  echo "   - Completed: ${#COMPLETED_TODOS[@]} items"
  echo "   - In Progress: ${#IN_PROGRESS_TODOS[@]} items"  
  echo "   - New Items: ${#NEW_TODOS[@]} items"
  echo "🔗 Updated project: https://github.com/users/$(gh api user --jq .login)/projects/$PROJECT_NUM"
}
```

## ERROR → SOLUTION MAPPINGS

| AI Agent Error | GitHub Command Fix | When |
|----------------|--------------------|----- |
| `No GitHub token` | `gh auth login --scopes project` | First run |
| `Missing project scope` | `gh auth refresh -s project -s read:project` | Project operations |
| `Project not found` | `gh project list --owner @me` | Check project exists |
| `Item not found` | `gh project item-list PROJECT_NUM` | Verify item exists |
| `Rate limit exceeded` | `sleep 60 && retry_command` | Batch operations |
| `TodoWrite out of sync` | `ai_session_init_with_project PROJECT_NUM` | After interruption |

## PROJECT STATUS MANAGEMENT

### Status Field Values
```bash
# Standard project status values
PROJECT_STATUSES=("Todo" "In Progress" "Done" "Backlog")

# Update item status
update_project_item_status() {
  local PROJECT_NUM="$1"
  local ITEM_TITLE="$2"  
  local NEW_STATUS="$3"
  
  ITEM_ID=$(gh project item-list $PROJECT_NUM --format json | \
    jq -r --arg title "$ITEM_TITLE" '.[] | select(.title | contains($title)) | .id')
    
  if [ "$ITEM_ID" != "null" ]; then
    gh project item-edit $PROJECT_NUM --id "$ITEM_ID" \
      --field "Status" --value "$NEW_STATUS"
    echo "Updated $ITEM_TITLE → $NEW_STATUS"
  fi
}
```

### Priority and Labels Management
```bash
# Add custom fields for project management
setup_project_fields() {
  local PROJECT_NUM="$1"
  
  # Priority field (if not exists)
  gh project field-create $PROJECT_NUM --name "Priority" \
    --type "single_select" \
    --options "P0,P1,P2,P3" 2>/dev/null || true
    
  # Phase field for development tracking
  gh project field-create $PROJECT_NUM --name "Phase" \
    --type "single_select" \
    --options "Design,Implementation,Testing,Review,Done" 2>/dev/null || true
}
```

## INTEGRATION UTILITIES

### TodoWrite ↔ Project Sync Functions
```bash
# Core integration functions for AI agents

# Convert project items to TodoWrite format
project_to_todowrite() {
  local PROJECT_NUM="$1"
  gh project item-list $PROJECT_NUM --owner @me --format json | \
    jq -r '.[] | select(.status != "Done") | "\(.title) (Project #\(.number))"'
}

# Create project item from TodoWrite task
todowrite_to_project() {
  local PROJECT_NUM="$1"
  local TODO="$2"
  local COMPLEXITY="$3"  # simple|complex|epic
  
  case $COMPLEXITY in
    "complex"|"epic")
      # Create issue first
      ISSUE_URL=$(gh issue create \
        --title "AI: $TODO" \
        --body "Auto-created from AI agent TodoWrite

## Task
$TODO

## Status
- [ ] Todo
- [ ] In Progress  
- [ ] Testing
- [ ] Done

Development task for project tracking." \
        --assignee @me)
      
      # Add to project
      gh project item-add $PROJECT_NUM --url "$ISSUE_URL"
      echo "Created project item: $TODO"
      ;;
    *)
      echo "Keep in TodoWrite only: $TODO"
      ;;
  esac
}

# Sync TodoWrite completion to project
sync_completed_todo_to_project() {
  local PROJECT_NUM="$1"
  local TODO="$2"
  
  update_project_item_status $PROJECT_NUM "$TODO" "Done"
}
```

## QUICK COMMAND REFERENCE

### Essential AI Agent Project Commands
```bash
# Project setup
gh project create --owner @me --title "Development Project"
gh auth refresh --hostname github.com -s project -s read:project

# Session management  
gh project item-list PROJECT_NUM --owner @me --format json
PROJECT_SUMMARY=$(gh project item-list 1 --format json | jq -r 'group_by(.status) | map({status: .[0].status, count: length}) | .[]')

# Task creation
gh issue create --title "AI: [task]" --assignee @me
gh project item-add PROJECT_NUM --url ISSUE_URL

# Status updates
gh project item-edit PROJECT_NUM --id ITEM_ID --field "Status" --value "In Progress"
gh project item-edit PROJECT_NUM --id ITEM_ID --field "Status" --value "Done"

# Bulk operations
gh project item-list PROJECT_NUM --format json | jq -r '.[] | select(.status == "Todo") | .id' | \
  xargs -I {} gh project item-edit PROJECT_NUM --id {} --field "Status" --value "In Progress"
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

### User Settings (Example)
```bash
# Default configuration for AI agent project integration
USER="your-username"
DEFAULT_PROJECT=1  # Main development project
PROJECT_STATUSES=("Todo" "In Progress" "Done" "Backlog")
PRIORITY_LABELS=("P0" "P1" "P2" "P3")
PHASE_LABELS=("Design" "Implementation" "Testing" "Review" "Done")

# Project field setup
setup_project_fields $DEFAULT_PROJECT
```

### State Transitions for AI Agents
```
TodoWrite "pending" → Project "Todo"
TodoWrite "in_progress" → Project "In Progress" 
TodoWrite "completed" → Project "Done" + close linked issue

AI Session Start → Load active project items to TodoWrite
AI Session End → Sync TodoWrite status to project items
AI Session Interrupt → Update project items to "In Progress"
```

## WORKFLOW EXAMPLES

### Example 1: Feature Development Workflow
```bash
# 1. Start feature development
implement_feature_with_project_tracking "Python Intelligence Bridge" 1

# 2. AI session works on subtasks (TodoWrite tracks progress)
# 3. Complete subtasks and sync to project

# 4. Session end - mark completed items  
ai_session_complete_with_project 1 \
  "Research existing Python bridge patterns" \
  "Design Python bridge architecture"
```

### Example 2: Sprint Planning Workflow
```bash
# 1. Load current sprint items
SPRINT_ITEMS=$(gh project item-list 1 --format json | \
  jq -r '.[] | select(.status != "Done") | .title')

# 2. Estimate and prioritize in project board

# 3. AI sessions work through items with TodoWrite sync

# 4. Sprint review - check completion status
gh project item-list 1 --format json | \
  jq -r 'group_by(.status) | map({status: .[0].status, count: length})'
```

---
*Optimized for proper GitHub Projects workflow with AI agent automation*