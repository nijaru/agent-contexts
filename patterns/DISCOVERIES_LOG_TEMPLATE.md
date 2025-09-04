# 🔬 Discoveries Log Template
*Append-only record of important findings, patterns, and learnings*

## Purpose
Track breakthrough discoveries that impact future development:
- **Technical solutions** that solve hard problems
- **Performance insights** that unlock optimizations
- **Architecture patterns** that improve design
- **Tool capabilities** previously unknown

## Template Structure

```markdown
---

## YYYY-MM-DD | Discovery Title

### Discovery
[Clear statement of what was discovered]

### Evidence/Code Pattern
```language
// Code example showing the discovery
```

### Impact
- [How this changes the approach]
- [Performance improvement achieved]
- [Problems this solves]

### Source/Reference
[Where this was found - docs, experimentation, paper]

---
```

## Categories of Discoveries

### Performance Breakthroughs
- Algorithm optimizations
- Memory reduction techniques  
- Parallelization opportunities
- I/O improvements

### Architecture Patterns
- Design patterns that work well
- Anti-patterns to avoid
- Integration strategies
- Scalability solutions

### Tool Capabilities
- Hidden features
- Undocumented APIs
- Workarounds for limitations
- Configuration optimizations

### Bug Root Causes
- Subtle issues found
- System limitations discovered
- Environmental factors
- Race conditions identified

## Example Entries

```markdown
---

## 2025-02-04 | Zero-Copy Memory Access Pattern

### Discovery
Direct memory access to external data without copying.

### Evidence/Code Pattern
```python
# Generic pattern for zero-copy access
def process_external_data(data_object):
    # Get memory pointer directly
    memory_ptr = data_object.get_memory_address()
    size = data_object.get_size()
    
    # Process without copying
    for i in range(0, size, batch_size):
        process_batch(memory_ptr + i)
```

### Impact
- Reduces memory overhead by 100x
- Eliminates copy operations
- Enables real-time processing
- Critical for performance-sensitive applications

### Source/Reference
Language documentation on memory interfaces

---

## 2025-02-04 | Double Buffer Pattern for Async Operations

### Discovery
Implement async behavior using double buffering and threads.

### Evidence/Code Pattern  
```python
class DoubleBuffer:
    def __init__(self):
        self.active = Buffer()
        self.background = Buffer()
        self.worker = Thread(target=self._process)
        
    def add(self, item):
        self.active.add(item)
        if self.active.full():
            # Swap buffers atomically
            self.active, self.background = self.background, self.active
            # Process in background
            self.notify_worker()
```

### Impact
- Non-blocking operations at any scale
- No synchronous bottlenecks
- Works without async/await support
- Pattern applicable to any language

### Source/Reference
Common systems programming pattern

---
```

## Best Practices

### DO
- ✅ Record immediately when discovered
- ✅ Include working code examples
- ✅ Measure actual impact
- ✅ Note the source/reference
- ✅ Explain why it matters

### DON'T
- ❌ Record minor optimizations
- ❌ Include discoveries without verification
- ❌ Forget to note limitations
- ❌ Skip the impact section

## Integration

- Referenced by `SESSION_LOG.md` entries
- Feeds into `ERROR_FIXES.md` when solving bugs  
- Influences `ACTION_PLAN.md` priorities
- Becomes patterns in language-specific docs