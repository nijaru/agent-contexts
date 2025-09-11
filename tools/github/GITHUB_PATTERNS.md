# AI Agent GitHub Projects Integration

*Decision trees for AI agent project management*

## CORE DECISION: Projects vs Issues vs TodoWrite

```
IF multi_session_development_task:
    → GitHub Projects (internal planning)
ELIF user_reported_problem OR community_request:
    → GitHub Issues (external visibility) 
ELIF single_session_task:
    → TodoWrite only
```

**Project Items**: Development tasks, features, refactoring  
**Issues**: Bug reports, user requests, community contributions  
**TodoWrite**: Session tracking with optional sync

## ESSENTIAL COMMANDS

### Project Setup
```bash
gh project create "Development" --view-title "Board" --view-type board
gh auth refresh -s read:project -s project
```

### TodoWrite → Project Sync
```bash
# Create project item from todo
gh issue create --title "AI: [todo_content]" --assignee @me --draft
gh project item-add PROJECT_NUM --url $ISSUE_URL

# Update status  
gh project item-edit PROJECT_NUM --id ITEM_ID --field "Status" --value "Done"
```

## DECISION: Session Management
```
IF new_ai_session AND existing_project:
    → Load active project items into TodoWrite
ELIF session_complete AND todos_finished:
    → Sync completed todos to project items  
ELIF session_interrupted:
    → Update project items to "In Progress"
```

## AI AGENT PATTERNS

**❌ WRONG: Use Issues for development tasks**
- Creates noise in issue tracker  
- Confuses external users with internal work

**✅ CORRECT: Use Projects for development, Issues for problems**
- Projects = Internal planning and coordination
- Issues = External community interaction

## INTEGRATION DECISION TREES

### When to Create Project Items
```
IF todo_count > 3 AND multi_session_work:
    → Create project items for persistence
ELIF collaborative_work:
    → Create project items for visibility
ELIF single_developer_quick_task:
    → Keep in TodoWrite only
```

### Status Sync Decision
```  
IF todo_marked_completed:
    → gh project item-edit --field "Status" --value "Done"
IF todo_marked_in_progress:
    → gh project item-edit --field "Status" --value "In Progress"
IF todo_created:
    → Consider creating project item if complex
```