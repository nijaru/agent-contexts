# Error Pattern Recognition for AI Agents

## COMPILATION ERROR PATTERNS

### Mojo Errors
| Error Message | Root Cause | Fix Pattern |
|---------------|------------|-------------|
| `use of unknown declaration 'int'` | Python syntax in Mojo | `int()` → `Int()` |
| `use of unknown declaration 'str'` | Python syntax in Mojo | `str()` → `String()` |
| `cannot implicitly convert` | Type mismatch | Add explicit conversion |
| `use of uninitialized value` | Variable not set | Initialize at declaration |
| `'fn' functions cannot be called from generic context` | Wrong function type | Use `def` for Python interop |

### Git/JJ Errors  
| Error Message | Root Cause | Fix Command |
|---------------|------------|-------------|
| `No current bookmark` | After jj init | `jj bookmark create main` |
| `Working copy contains conflicts` | Merge conflicts | `jj resolve` |
| `Working copy is stale` | Out of sync | `jj edit @` |
| `fatal: not a git repository` | Wrong directory | `cd` to repo or `git init` |

### Build Errors
| Error Pattern | Root Cause | Fix Pattern |
|---------------|------------|-------------|
| `module not found` | Missing dependency | Check `package.json`/`requirements.txt` |
| `permission denied` | File permissions | `chmod +x` or run as admin |
| `port already in use` | Service running | `lsof -ti:PORT | xargs kill` |
| `out of memory` | Resource exhaustion | Reduce batch size/data |

## RUNTIME ERROR PATTERNS

### Memory Errors
```
PATTERN: "segmentation fault"
CAUSE: Invalid pointer access
ACTIONS:
1. Check pointer initialization
2. Verify array bounds  
3. Look for use-after-free
4. Add null checks
```

### Performance Issues
```
PATTERN: Slow response times
DIAGNOSTIC COMMANDS:
top -p $(pgrep -f your_app)        # CPU usage
free -h                            # Memory usage
iostat -x 1                        # I/O stats
netstat -i                         # Network stats
```

## DEBUGGING DECISION TREES

### High Memory Usage
```
IF memory_growing_continuously:
    → Memory leak - check object cleanup
    → Add garbage collection calls
    → Profile memory allocations
ELIF memory_spike_then_stable:
    → Large data loading - consider streaming
    → Batch processing instead of bulk
ELIF memory_usage_random:
    → Check for memory fragmentation
    → Review data structure choices
```

### Slow Performance  
```
IF CPU_usage_high:
    IF single_threaded_bottleneck:
        → Parallelize operations
        → Use async/await patterns
    ELIF algorithm_complexity:
        → Review algorithm choice (O(n²) → O(n log n))
        → Add caching/memoization
ELIF IO_wait_high:
    → Database query optimization  
    → File I/O batching
    → Network request batching
```

## ERROR PREVENTION PATTERNS

### Code Removal Anti-Patterns
```
❌ WRONG: Leaving removal artifacts
# gc section removed
// authentication removed  
/* old implementation */

✅ CORRECT: Clean deletion
# Delete code completely
# Version control tracks history
```

### Before Committing Code
```bash
# Check for common issues
rg "TODO|FIXME|HACK" .              # Temporary code
rg "console\.log|print\(" .          # Debug statements  
rg "password|secret|key" . -i        # Hardcoded secrets
rg "localhost|127\.0\.0\.1" .        # Local URLs
rg "# (removed|deleted)" . -i       # Removal artifacts
```

### Before Deploying
```bash
# Environment checks
grep -r "NODE_ENV.*development" .   # Dev settings
grep -r "DEBUG.*true" .              # Debug flags
grep -r "http://" . | grep -v test  # Insecure URLs
```

## RECOVERY PATTERNS

### Git Recovery
```
SITUATION: Committed wrong files
SOLUTION: git reset --soft HEAD~1   # Undo commit, keep changes

SITUATION: Lost local changes  
SOLUTION: git reflog                 # Find lost commits
          git checkout <hash>        # Recover state
```

### JJ Recovery  
```
SITUATION: Messed up commits
SOLUTION: jj op log                  # See operations
          jj op undo                 # Undo last op

SITUATION: Need clean slate
SOLUTION: jj op restore --to=<id>    # Restore to known good
```