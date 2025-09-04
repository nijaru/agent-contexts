# 🔧 Error Fixes Template
*Quick lookup for common problems and their solutions*

## Purpose
Fast problem resolution by maintaining a searchable database of:
- **Error messages** → exact fixes
- **Common issues** → proven solutions
- **Workarounds** → temporary fixes
- **Root causes** → permanent solutions

## Template Structure

```markdown
## Error: [Exact error message or symptom]

### Context
[When/where this error occurs]

### Root Cause
[Why this happens]

### Quick Fix
```bash
# Immediate workaround
command_to_run
```

### Proper Solution
```language
// Permanent fix in code
code_changes_needed
```

### Prevention
[How to avoid this in future]

---
```

## Categories

### Build Errors
Compilation failures, dependency issues, configuration problems

### Runtime Errors
Crashes, exceptions, memory issues, performance problems

### Environment Issues
Path problems, permissions, missing tools, version conflicts

### Integration Problems
API failures, library incompatibilities, FFI issues

## Example Entries

```markdown
## Error: "Module not found: example_module"

### Context
Occurs when running Python scripts that import local modules

### Root Cause
Python path doesn't include current directory

### Quick Fix
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Or in script:
import sys
sys.path.insert(0, '.')
```

### Proper Solution
```python
# Use proper package structure
from . import example_module
# Or use setup.py/pyproject.toml
```

### Prevention
Always use virtual environments and proper package structure

---

## Error: "Segmentation fault (core dumped)"

### Context  
Application crashes when processing large datasets

### Root Cause
Stack overflow or null pointer dereference

### Quick Fix
```bash
# Increase stack size
ulimit -s unlimited
# Enable core dumps for debugging
ulimit -c unlimited
```

### Proper Solution
```c
// Check pointers before use
if (ptr != NULL) {
    // use ptr
}
// Use heap for large data
data = malloc(size);
```

### Prevention
- Always validate pointers
- Use heap for large allocations
- Enable warnings: -Wall -Wextra

---

## Error: "Permission denied"

### Context
Cannot access file or run command

### Root Cause
Insufficient permissions for file/directory

### Quick Fix  
```bash
# Check permissions
ls -la file_path
# Add execute permission
chmod +x script.sh
# Change ownership
sudo chown $(whoami) file_path
```

### Proper Solution
Set correct permissions during creation:
```python
import os
# Create with specific permissions
os.makedirs(path, mode=0o755)
# Create file with permissions
with open(file, 'w') as f:
    os.chmod(file, 0o644)
```

### Prevention
- Use proper umask settings
- Create files with correct permissions
- Don't run as root unless necessary

---
```

## Search Patterns

### By Error Message
```bash
grep -i "error message" ERROR_FIXES.md
```

### By Category
```bash
grep -A 10 "## Build Errors" ERROR_FIXES.md
```

### By Solution Type
```bash
grep -B 5 "Quick Fix" ERROR_FIXES.md
```

## Best Practices

### DO
- ✅ Include exact error messages
- ✅ Provide both quick and proper fixes
- ✅ Explain why the error occurs
- ✅ Add prevention tips
- ✅ Test solutions before documenting

### DON'T
- ❌ Document one-off issues
- ❌ Skip root cause analysis
- ❌ Provide only workarounds
- ❌ Forget platform-specific notes

## Contributing

When adding new fixes:
1. Verify the solution works
2. Include minimal reproduction
3. Note environment details
4. Link to relevant documentation
5. Tag with keywords for search