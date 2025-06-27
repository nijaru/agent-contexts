# Documentation Organization for AI-Assisted Development

*Efficient, tool-friendly documentation structure for any software project*

## Core Principles

1. **AI-First Design**: Entry point file (`AGENTS.md` or `CLAUDE.md`) provides concise overview with tool-based detail access
2. **Single Sources of Truth**: Each concept has one authoritative location, no duplication
3. **Progressive Loading**: Essential context upfront, detailed specs fetched as needed
4. **JSON Task Management**: Structured data enabling programmatic updates by AI agents

## Directory Structure

```
project_root/
├── AGENTS.md                    # AI agent entry point (or CLAUDE.md)
└── docs/
    ├── README.md               # Navigation guide
    ├── core/                   # Essential project context
    │   ├── MASTER_SPEC.md     # Complete specifications
    │   └── DEVELOPER_GUIDE.md # Standards and patterns
    ├── tasks/                  # JSON-based task management
    │   ├── tasks.json         # Active tasks (single source of truth)
    │   ├── completed.json     # Completed task archive
    │   └── README.md          # Task system guide
    ├── architecture/           # Technical specifications by component
    │   ├── core/              # System architecture, data structures
    │   ├── api/               # Interfaces, endpoints, protocols
    │   ├── processing/        # Business logic, algorithms
    │   └── deployment/        # Infrastructure, scaling, operations
    ├── development/            # Development guides
    │   ├── setup/             # Environment, dependencies
    │   ├── workflow/          # Git, testing, CI/CD
    │   └── troubleshooting/   # Common issues, debugging
    └── reference/              # Quick access materials
        ├── patterns/          # Code examples, best practices
        ├── commands/          # Build, debug commands
        └── validation/        # Critical requirement checklists
```

## Key Components

### 1. AI Agent Entry Point (`AGENTS.md`)
- **Concise Overview**: Project summary, key constraints
- **Task Navigation Table**: Maps coding tasks → documentation files
- **Essential References**: Always-consult core documents
- **Quick Commands**: Build, test, debug instructions
- **Workflow Protocol**: Step-by-step AI development process

### 2. JSON Task Management (`docs/tasks/`)
**Revolutionary improvement over Markdown task tracking**

```json
{
  "project": {...},           // Metadata, goals, constraints
  "metrics": {...},           // Progress tracking, KPIs
  "tasks": {
    "TASK-001": {
      "title": "Implementation name",
      "status": "pending|in_progress|blocked|completed",
      "priority": "critical|high|medium|low",
      "acceptance_criteria": {
        "criterion_1": {"completed": false, "description": "..."}
      }
    }
  }
}
```

**Benefits**: Programmatic updates, structured queries, historical tracking, no merge conflicts

### 3. Architecture Adaptation by Project Type

| Project Type | Architecture Subdirs | Key Validations |
|--------------|---------------------|-----------------|
| **Backend/API** | `api/`, `data/`, `auth/`, `deployment/` | Security, performance, compatibility |
| **Frontend** | `ui/`, `state/`, `routing/`, `build/` | Cross-browser, accessibility, performance |
| **CLI Tool** | `commands/`, `config/`, `output/`, `plugins/` | Cross-platform, usability, extensibility |  
| **Library** | `core/`, `api/`, `integrations/`, `performance/` | API stability, documentation, compatibility |
| **Mobile** | `ui/`, `data/`, `platform/`, `distribution/` | Platform compatibility, UX, performance |
| **ML/Data** | `models/`, `data/`, `training/`, `inference/` | Reproducibility, performance, data quality |

## AI Workflow Protocol

1. **Read** `docs/tasks/tasks.json` for current priorities
2. **Check** task navigation table in `AGENTS.md` for relevant docs
3. **Validate** against `docs/reference/validation/` checklists
4. **Update** task status: `pending` → `in_progress` → `completed`
5. **Archive** completed tasks to `completed.json` with details

## Implementation Checklist

### Phase 1: Core Structure
```bash
mkdir -p docs/{core,tasks,architecture,development,reference}
```
- [ ] Create `AGENTS.md` at project root
- [ ] Set up `docs/tasks/tasks.json` with project structure
- [ ] Write `docs/core/MASTER_SPEC.md` with complete specifications
- [ ] Create task navigation table mapping tasks to documentation

### Phase 2: Architecture Documentation
- [ ] Choose appropriate `docs/architecture/` subdirectories for project type
- [ ] Document core system design and patterns
- [ ] Create validation checklists for critical requirements
- [ ] Set up cross-references between specifications

### Phase 3: Development Resources
- [ ] Environment setup and troubleshooting guides
- [ ] Code patterns and examples
- [ ] Build/debug command references
- [ ] Establish maintenance protocols

## Key Benefits

### For AI Agents
- **Fast Context Loading**: Essential info in entry point, details via tools
- **Structured Updates**: JSON task management enables programmatic status changes  
- **Efficient Navigation**: Direct task → documentation mapping
- **Validation Framework**: Built-in requirement checklists

### For Developers
- **Clear Organization**: Purpose-driven directory structure
- **No Duplication**: Single sources of truth with cross-references
- **Comprehensive Coverage**: Architecture, development, and reference materials
- **Historical Tracking**: Complete audit trail of completed work

## Migration from Traditional Docs

1. **Consolidate** scattered task tracking into `tasks.json`
2. **Create** AI entry point with task navigation table  
3. **Organize** existing docs into core/architecture/development/reference
4. **Establish** single sources of truth, remove duplicates
5. **Add** validation checklists for critical project requirements

This system optimizes documentation for AI-assisted development while maintaining human usability and comprehensive project coverage.