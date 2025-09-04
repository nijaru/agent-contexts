# Python Patterns

*Actionable patterns for Python development with modern tools*

## Environment Management

### Use UV for Package Management
```bash
# ❌ WRONG - pip in global environment
pip install requests

# ✅ CORRECT - UV with project isolation
uv init myproject
cd myproject
uv add requests
uv run python main.py
```

### Python Version Management
```bash
# With mise (recommended)
mise install python@3.13
mise use python@3.13

# UV handles virtual environments automatically
uv sync  # Creates/updates venv from pyproject.toml
```

## Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Missing dependency | `uv add <package>` |
| `ImportError: cannot import name` | Circular import | Restructure imports |
| `TypeError: X takes Y positional arguments` | Wrong argument count | Check function signature |
| `AttributeError: 'NoneType'` | Null reference | Add null checks |

## Performance Patterns

### Async/Await for I/O
```python
# ❌ SLOW - Sequential I/O
for url in urls:
    response = requests.get(url)
    process(response)

# ✅ FAST - Concurrent I/O
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### Use Comprehensions
```python
# ❌ SLOWER
result = []
for x in items:
    if condition(x):
        result.append(transform(x))

# ✅ FASTER
result = [transform(x) for x in items if condition(x)]
```

## Type Hints (Python 3.10+)
```python
# Modern type hints
def process_data(
    items: list[str],
    config: dict[str, Any] | None = None
) -> tuple[int, str]:
    ...

# Type narrowing
def handle(value: str | None) -> str:
    if value is None:
        return "default"
    return value.upper()  # Type checker knows value is str here
```

## Testing Patterns
```bash
# UV-based testing
uv add --dev pytest pytest-cov
uv run pytest
uv run pytest --cov=mypackage
```

## Quick Commands
```bash
# Format code
uv run ruff format .

# Lint
uv run ruff check .

# Type check
uv add --dev mypy
uv run mypy .
```