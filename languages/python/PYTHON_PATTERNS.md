# Python Patterns

*Modern Python patterns for AI-assisted development*

## DECISION TREES

### Environment Selection
```
IF new_project → uv init && uv sync
IF existing_project → uv sync
IF global_tool → uv tool install [tool]
IF quick_script → uv run --inline-script 'deps' script.py
IF python_version → mise install python@3.13 && mise use python@3.13
```

### Async Pattern Selection
```
IF io_bound_task → Use asyncio
IF cpu_bound_task → Use multiprocessing
IF mixed_workload → Use ProcessPoolExecutor with asyncio
IF simple_parallel → Use concurrent.futures
```

## MODERN PYTHON FEATURES (3.10+)

### Pattern Matching (3.10+)
```python
# ✅ Pattern matching for clean control flow
match command:
    case ["quit"]:
        sys.exit()
    case ["load", filename]:
        return load_file(filename)
    case ["save", filename, *data]:
        save_file(filename, data)
    case _:
        print("Unknown command")
```

### Type Hints (3.12+)
```python
# Generic types with new syntax
type Point[T] = tuple[T, T]
type Connection[T] = T | None

# Type parameter syntax
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# TypedDict for structured data
from typing import TypedDict

class Config(TypedDict, total=False):
    host: str
    port: int
    debug: NotRequired[bool]  # 3.11+
```

### Dataclasses & Pydantic
```python
# ✅ MODERN - Use dataclasses for simple data
from dataclasses import dataclass, field

@dataclass(slots=True)  # slots for memory efficiency
class Point:
    x: float
    y: float = 0.0
    tags: list[str] = field(default_factory=list)

# ✅ MODERN - Use Pydantic for validation
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
```

## PERFORMANCE PATTERNS

### Comprehensions & Generators
```python
# ❌ SLOW - Multiple passes
filtered = [x for x in data if condition(x)]
transformed = [transform(x) for x in filtered]

# ✅ FAST - Generator expression
result = [transform(x) for x in data if condition(x)]

# ✅ MEMORY EFFICIENT - Generator for large data
def process_large_file(path):
    with open(path) as f:
        yield from (line.strip() for line in f if line.strip())
```

### Async Best Practices
```python
# ✅ MODERN - Async context managers and comprehensions
async with asyncio.TaskGroup() as tg:  # 3.11+
    tasks = [tg.create_task(fetch(url)) for url in urls]
# All tasks complete or exception raised

# Async comprehension
results = [x async for x in async_generator()]
```

### Exception Groups (3.11+)
```python
# Handle multiple exceptions
try:
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(operation1())
        task2 = tg.create_task(operation2())
except* ValueError as eg:
    for e in eg.exceptions:
        log_error(f"Value error: {e}")
except* TypeError as eg:
    for e in eg.exceptions:
        log_error(f"Type error: {e}")
```

## UV PACKAGE MANAGEMENT

### Common Commands
```bash
# Project setup
uv init                    # Create new project
uv add pandas numpy        # Add dependencies
uv add --dev pytest ruff   # Add dev dependencies
uv sync                    # Install all dependencies

# Running code
uv run python main.py      # Run with managed env
uv run pytest             # Run tests
uv run --with jupyter -- jupyter lab  # Temporary dep

# Dependency management
uv pip compile requirements.in > requirements.txt
uv tree                    # Show dependency tree
uv tool install ruff       # Install global tool
```

## ERROR → SOLUTION PATTERNS

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | `uv add [package]` |
| `ImportError: circular import` | Restructure imports, use TYPE_CHECKING |
| `RuntimeError: asyncio.run() cannot be called` | Already in async context, use await |
| `TypeError: 'coroutine' object is not iterable` | Missing await keyword |
| `AttributeError: __aenter__` | Use async with for async context managers |

## AI AGENT PATTERNS

### ❌ WRONG vs ✅ CORRECT

```python
# ❌ WRONG - Old string formatting
"%s %d" % (name, count)
"{} {}".format(name, count)

# ✅ CORRECT - F-strings
f"{name} {count}"

# ❌ WRONG - Dict.get() with mutable default
config = settings.get('config', {})  # Same dict for all!

# ✅ CORRECT - Create new default
config = settings.get('config') or {}

# ❌ WRONG - Mutable default arguments
def add_item(item, items=[]):  # Shared list!
    items.append(item)

# ✅ CORRECT - None default with check
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
```

## TESTING PATTERNS

### Pytest Best Practices
```python
# Fixtures for reusable test data
@pytest.fixture
def sample_data():
    return {"key": "value"}

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected

# Async tests
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == expected
```

## COMMAND PATTERNS

```bash
# Modern Python setup
mise install python@latest
mise use python@latest

# UV workflow
uv init project
cd project
uv add fastapi uvicorn
uv run uvicorn main:app --reload

# Quality checks
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest --cov

# Build & publish
uv build
uv publish
```