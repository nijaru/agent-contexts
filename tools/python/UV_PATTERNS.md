# UV Python Package Manager Patterns

*Decision trees for modern Python environment management*

## CORE DECISION: UV vs Traditional Tools

```
IF new_python_project:
    → uv init && uv add [packages]
ELIF existing_pip_project:
    → uv pip compile requirements.in > requirements.txt
ELIF global_tool_needed:
    → uv tool install [tool]
ELIF quick_script_run:
    → uv run --inline-script 'dependencies' script.py
```

## ESSENTIAL COMMANDS

### Project Setup
```bash
uv init                     # Initialize project
uv add requests fastapi     # Add dependencies
uv add --dev pytest ruff    # Add dev dependencies
uv sync                     # Install all dependencies
uv run python main.py       # Run with managed env
```

### Dependency Management
```bash
uv pip compile requirements.in    # Lock dependencies
uv pip sync requirements.txt      # Install locked deps
uv tree                          # Show dependency tree
```

## DECISION TREES

### Project Type Selection
```
IF application_project:
    → uv init --app
ELIF library_project:
    → uv init --lib
ELIF packaging_existing:
    → uv init --package
```

### Python Version Management
```
IF specific_version_needed:
    → uv python install 3.12
ELIF project_requires_version:
    → Edit .python-version file
ELIF system_default_ok:
    → Use without version specification
```

### Environment Activation
```
IF uv_managed_project:
    → No activation needed, use `uv run`
ELIF traditional_venv_needed:
    → uv venv && source .venv/bin/activate
ELIF ci_environment:
    → uv pip install --system
```

## ERROR → SOLUTION MAPPINGS

| Error | Solution |
|-------|----------|
| `No virtual environment found` | Run `uv sync` first |
| `Conflicting dependencies` | Use `uv pip compile --resolver=backtrack` |
| `Python version not found` | `uv python install [version]` |
| `Package not in index` | Add `--index-url` or `--extra-index-url` |

## AI AGENT PATTERNS

**❌ WRONG: Mix pip and uv in same project**
```bash
pip install requests
uv add fastapi  # Conflicts with pip-managed env
```

**✅ CORRECT: Use uv exclusively**
```bash
uv add requests fastapi
uv run python app.py
```

**❌ WRONG: Manually activate venv with uv projects**
```bash
source .venv/bin/activate
python main.py
```

**✅ CORRECT: Let uv manage activation**
```bash
uv run python main.py
```