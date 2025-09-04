# 📓 Session Log Template
*Append-only record of AI agent work sessions*

## Why Session Logs Matter
- **Context persistence** between AI conversations
- **Learning from history** - what worked, what didn't  
- **Progress tracking** - see evolution over time
- **Handoff clarity** - next session knows exactly where to start

## Template Structure

```markdown
---

## YYYY-MM-DD | Agent Name | Session Title

### Context
[What situation/problem started this session]

### Completed
- ✅ Task 1 with specific outcome
- ✅ Task 2 with specific outcome
- ⚠️ Task 3 partially done (explain)

### Discovered  
- **Finding 1**: [Important discovery with impact]
- **Finding 2**: [Pattern or solution found]
- **Bug found**: [Issue and workaround]

### Key Code Locations
- Feature X: `path/to/file.ext:line_number`
- Bug fix: `path/to/file.ext:line_range`
- Pattern: `path/to/example.ext`

### Decisions Made
1. **Chose X over Y** because [rationale]
2. **Deferred Z** until [condition]

### Blocked On
- [Blocker description] - need [what's needed]
- Nothing currently blocked ✅

### Next Session Should
1. [Specific task to continue]
2. [New task to start]
3. [Investigation needed]

### Session Stats
- Duration: ~X hours
- Files created: N
- Files modified: M  
- Tests added: T
- Tokens used: ~XXK

---
```

## Best Practices

### DO
- ✅ Update immediately after session
- ✅ Be specific about file locations
- ✅ Include rationale for decisions
- ✅ Note partial progress honestly
- ✅ List concrete next steps

### DON'T  
- ❌ Write vague summaries
- ❌ Skip "blocked on" section
- ❌ Forget to note discoveries
- ❌ Leave out failure attempts

## Example Entry

```markdown
---

## 2025-02-04 | Claude | Performance Optimization Session

### Context
Application hitting performance bottleneck at scale, blocking deployment.

### Completed
- ✅ Root caused issue to synchronous I/O operation
- ✅ Found zero-copy pattern for data transfer
- ✅ Researched industry best practices
- ⚠️ Started async implementation (30% done)

### Discovered
- **Zero-copy technique**: Direct memory access without copying
- **Threading pattern**: Background threads for async operations
- **Memory issue**: Standard library collections using excessive memory

### Key Code Locations
- Bottleneck: `src/core/processor.ext:1850-2000`
- Pattern found: `docs/patterns/async.md:214`
- Reference: `external/library/docs/memory.md`

### Decisions Made
1. **Chose approach A over B** - better performance characteristics
2. **Adopted proven pattern** - industry standard solution
3. **Documentation strategy** - markdown files for AI agents

### Blocked On
- Nothing blocked ✅

### Next Session Should  
1. Complete async implementation
2. Test with larger dataset
3. Update benchmark suite

### Session Stats
- Duration: ~2 hours
- Files created: 5
- Files modified: 3
- Tests added: 0
- Tokens used: ~50K

---
```

## Integration with Other Patterns

- Links to `DISCOVERIES.md` for detailed findings
- References `TASKS.md` for task status
- Points to `ACTION_PLAN.md` for priorities
- Updates feed into `DECISIONS.md` rationale