# GitHub Projects Workflow Guide

*Project management patterns for AI agents - focused on non-intrinsic knowledge*

## Quick Reference (For Other LLMs)

### MCP Setup
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

### Essential Commands
```bash
# These work with any LLM that has GitHub access
gh issue create --title "Title" --body "Description" --label "type"
gh pr create --title "Title" --body "Closes #123"
gh project item-add PROJECT_ID --issue ISSUE_NUMBER
gh workflow run workflow.yml
gh issue list --json number,title,state --jq '.[]'
```

## User-Specific Conventions

### Project Structure
```yaml
username: nijaru
default_project: 1  # Main project board
sprint_duration: 2 weeks
priority_labels: [P0, P1, P2, P3]
type_labels: [feat, bug, task, docs, perf, chore]
```

### Branch Naming
```bash
feat/ISSUE_NUM-description   # New features
fix/ISSUE_NUM-description    # Bug fixes  
docs/ISSUE_NUM-description   # Documentation
chore/ISSUE_NUM-description  # Maintenance
```

### Commit Message Format
```bash
type: Short description

Longer explanation if needed.

Closes #ISSUE_NUM
```

## Complex Multi-Step Workflows

### New Project Setup (Complete)
```bash
# Full project initialization with all conventions
PROJECT="new-project"

# 1. Create repo and project
gh repo create "$PROJECT" --private --clone
cd "$PROJECT"
PROJECT_ID=$(gh project create --owner @me --title "$PROJECT" --format json | jq -r '.number')
gh repo edit --add-project "$PROJECT_ID"

# 2. Set up labels (one-time)
for label in P0:FF0000 P1:FF6600 P2:FFCC00 P3:99CC00; do
  IFS=: read -r name color <<< "$label"
  gh label create "$name" --color "$color"
done

for label in feat bug task docs perf chore; do
  gh label create "$label"
done

# 3. Configure project fields
gh project field-create $PROJECT_ID --name "Priority" \
  --data-type SINGLE_SELECT --single-select-options "P0,P1,P2,P3"
gh project field-create $PROJECT_ID --name "Size" \
  --data-type NUMBER
gh project field-create $PROJECT_ID --name "Sprint" \
  --data-type ITERATION

# 4. Create standard views
gh project view-create $PROJECT_ID --title "Current" --filter "iteration:@current"
gh project view-create $PROJECT_ID --title "Backlog" --filter "status:Backlog"
gh project view-create $PROJECT_ID --title "Bugs" --filter "label:bug"
```

### Feature Development Flow
```bash
# Complete flow from idea to deployment
FEATURE="user authentication"

# 1. Create and assign issue
ISSUE=$(gh issue create \
  --title "feat: Add $FEATURE" \
  --body "## Requirements\n- OAuth2\n- JWT tokens\n- Session management" \
  --label "feat,P1" \
  --assignee @me \
  --project 1 \
  --json number -q '.number')

# 2. Create feature branch
git checkout -b "feat/$ISSUE-$(echo $FEATURE | tr ' ' '-')"

# 3. Link to project and update status
ITEM_ID=$(gh project item-list 1 --format json | \
  jq -r ".items[] | select(.content.number == $ISSUE) | .id")
gh project item-edit 1 --id "$ITEM_ID" \
  --field-id STATUS_FIELD --single-select-option-id "In Progress"

# 4. After implementation, create PR
gh pr create \
  --title "feat: Add $FEATURE" \
  --body "Closes #$ISSUE\n\n## Changes\n- OAuth2 implementation\n- JWT handling\n- Session management" \
  --assignee @me

# 5. Auto-merge when ready
gh pr merge --auto --squash --delete-branch
```

## Error Recovery Patterns

### Common Failure Scenarios
```bash
# Workflow failure recovery
recover_failed_workflow() {
  local RUN_ID=$(gh run list --workflow "$1" --limit 1 --json databaseId -q '.[0].databaseId')
  
  # Check failure reason
  gh run view $RUN_ID --log-failed | head -20
  
  # Common fixes
  case $(gh run view $RUN_ID --json conclusion -q '.conclusion') in
    "failure")
      gh run rerun $RUN_ID --failed  # Retry failed jobs only
      ;;
    "cancelled")
      gh run rerun $RUN_ID  # Rerun entire workflow
      ;;
    "timed_out")
      gh workflow run "$1" --ref main  # Start fresh
      ;;
  esac
}

# Merge conflict resolution
resolve_pr_conflicts() {
  local PR=$1
  gh pr checkout $PR
  git fetch origin main
  git rebase origin/main
  # After manual conflict resolution
  git push --force-with-lease
  gh pr comment $PR --body "✅ Resolved merge conflicts"
}

# Fix orphaned project items
cleanup_project() {
  local PROJECT=$1
  # Remove items with deleted issues
  gh project item-list $PROJECT --format json | \
    jq -r '.items[] | select(.content == null) | .id' | \
    xargs -I {} gh project item-delete $PROJECT --id {}
}
```

## Sprint Management

### Sprint Planning Automation
```bash
# Weekly sprint setup
start_sprint() {
  local SPRINT_NAME="Sprint $(date +%U)"
  local PROJECT_ID=1
  
  # Close previous sprint
  gh issue list --search "project:@me/$PROJECT_ID iteration:@current -status:Done" \
    --json number | jq -r '.[].number' | \
    while read -r issue; do
      gh issue comment $issue --body "📦 Moved to $SPRINT_NAME"
      # Move to new sprint via project board
    done
  
  # Pull in prioritized backlog
  gh issue list --label "P0,P1" --state open \
    --search "project:@me/$PROJECT_ID status:Backlog" \
    --limit 10 --json number | jq -r '.[].number' | \
    while read -r issue; do
      echo "Adding issue #$issue to sprint"
      # Update iteration field
    done
}

# Sprint metrics
sprint_velocity() {
  gh issue list --state closed \
    --search "project:@me/1 iteration:\"$1\"" \
    --json labels,closedAt | \
    jq '[.[] | 
      if any(.labels[].name; . == "P0") then 8
      elif any(.labels[].name; . == "P1") then 5  
      elif any(.labels[].name; . == "P2") then 3
      else 1 end
    ] | add'
}
```

## Batch Operations

### Bulk Updates
```bash
# Update all bugs to P1
gh issue list --label bug --state open --json number | \
  jq -r '.[].number' | \
  xargs -I {} gh issue edit {} --add-label P1

# Archive completed items older than 30 days
gh issue list --state closed \
  --search "closed:<$(date -d '30 days ago' '+%Y-%m-%d')" \
  --json number | jq -r '.[].number' | \
  xargs -I {} gh issue edit {} --add-label archived
```

### Dependency Management
```bash
# Find and mark blocking issues
find_blockers() {
  gh issue list --state open --json number,body | \
    jq -r '.[] | select(.body | test("Blocks #\\d+")) | .number' | \
    while read -r blocker; do
      BLOCKED=$(gh issue view $blocker --json body | \
        grep -oP 'Blocks #\K\d+')
      gh issue edit $BLOCKED --add-label blocked
      gh issue comment $BLOCKED --body "⚠️ Blocked by #$blocker"
    done
}
```

## Performance Optimizations

### API Call Batching
```bash
# Cache frequently used data
CACHE_DIR="$HOME/.cache/gh"
mkdir -p "$CACHE_DIR"

get_project_id() {
  local CACHE_FILE="$CACHE_DIR/projects.json"
  if [ ! -f "$CACHE_FILE" ] || [ $(find "$CACHE_FILE" -mmin +60) ]; then
    gh project list --owner @me --format json > "$CACHE_FILE"
  fi
  jq -r ".projects[] | select(.title==\"$1\") | .number" "$CACHE_FILE"
}

# Single call instead of multiple
gh issue list --limit 100 \
  --json number,title,body,labels,assignees,projectItems | \
  jq '.[] | {
    number,
    title,
    priority: .labels[] | select(.name | startswith("P")) | .name,
    project_status: .projectItems[0].status
  }'
```

## GitHub Actions Integration

### Auto-Update Project Board
```yaml
# .github/workflows/project-sync.yml
name: Sync Project Board
on:
  pull_request:
    types: [opened, ready_for_review, closed]
  
jobs:
  update-status:
    runs-on: ubuntu-latest
    steps:
      - name: Update project item status
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          ISSUE=$(echo "${{ github.event.pull_request.body }}" | \
            grep -oP '(?:Closes|Fixes) #\K\d+' | head -1)
          
          if [ -n "$ISSUE" ]; then
            case "${{ github.event.action }}" in
              "opened")
                gh issue edit $ISSUE --add-label "in-progress"
                ;;
              "ready_for_review")
                gh issue edit $ISSUE --add-label "in-review"
                ;;
              "closed")
                if [ "${{ github.event.pull_request.merged }}" = "true" ]; then
                  gh issue close $ISSUE
                fi
                ;;
            esac
          fi
```

### Scheduled Maintenance
```yaml
# .github/workflows/maintenance.yml
name: Weekly Maintenance
on:
  schedule:
    - cron: '0 0 * * 0'  # Sunday midnight
    
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Close stale issues
        run: |
          gh issue list --repo ${{ github.repository }} \
            --state open \
            --search "updated:<$(date -d '90 days ago' '+%Y-%m-%d')" \
            --json number | \
            jq -r '.[].number' | \
            xargs -I {} gh issue close {} \
              --comment "Auto-closed: 90 days inactive"
```

## State Management

### Issue State Machine
```
Backlog → Ready → In Progress → In Review → Done
           ↓           ↓            ↓
        Blocked    Blocked      Changes Requested
           ↓           ↓            ↓
         Ready    In Progress   In Progress
```

### Automated State Transitions
```bash
# Hook these to GitHub Actions or webhooks
on_pr_open() {
  ISSUE=$(gh pr view $1 --json body | grep -oP '(?:Closes|Fixes) #\K\d+')
  [ -n "$ISSUE" ] && gh issue edit $ISSUE \
    --remove-label "ready" \
    --add-label "in-progress"
}

on_pr_merged() {
  ISSUE=$(gh pr view $1 --json body | grep -oP '(?:Closes|Fixes) #\K\d+')
  [ -n "$ISSUE" ] && gh issue close $ISSUE \
    --comment "✅ Completed in PR #$1"
}
```

---
*Focused on patterns and workflows not intrinsic to AI agents*