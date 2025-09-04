# 📊 Decision Log Template
*Append-only record of architectural and technical decisions*

## Purpose
Document the rationale behind important choices to:
- **Prevent revisiting** settled decisions
- **Understand context** of past choices
- **Learn from outcomes** of decisions
- **Onboard new contributors** quickly

## Template Structure

```markdown
---

## YYYY-MM-DD | Decision Title

### Context
[What situation required a decision]

### Options Considered
1. **Option A**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   
2. **Option B**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]

3. **Option C**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]

### Decision
**Chosen: Option X**

### Rationale
[Why this option was selected over others]

### Consequences
- [Expected positive outcomes]
- [Accepted trade-offs]
- [Risks to monitor]

### Review Date
[When to revisit this decision, if applicable]

---
```

## Categories of Decisions

### Architecture
- System design choices
- Technology stack selection
- API design decisions
- Data model choices

### Development Process
- Workflow decisions
- Tool selections
- Testing strategies
- Documentation approaches

### Performance Trade-offs
- Optimization vs maintainability
- Memory vs speed
- Latency vs throughput
- Accuracy vs performance

### Technical Debt
- Shortcuts taken deliberately
- Temporary solutions
- Migration strategies
- Refactoring priorities

## Example Entry

```markdown
---

## 2025-02-04 | Documentation Strategy for AI Agents

### Context
Need efficient way for AI agents to maintain context between sessions and track work.

### Options Considered
1. **GitHub Issues/Projects**
   - Pros: Standard tool, good for collaboration, API access
   - Cons: Network latency, not in AI context, complexity
   
2. **Database/JSON files**
   - Pros: Structured data, queryable
   - Cons: Overhead to maintain, schema changes, parsing needed

3. **Markdown files in repo**
   - Pros: Instant access, version controlled, human readable
   - Cons: Less structured, manual updates

### Decision
**Chosen: Markdown files with specific structure**

### Rationale
- AI agents need immediate access without API calls
- Version control provides history automatically
- Human readable for debugging and review
- Simple to update and maintain
- Works offline

### Consequences
- Excellent AI agent workflow
- All changes tracked in git
- May need tooling for complex queries later
- Team must follow documentation patterns

### Review Date
After 3 months of usage

---
```

## Best Practices

### DO
- ✅ Document while memory is fresh
- ✅ Include all serious options
- ✅ Be honest about trade-offs
- ✅ Set review dates for big decisions
- ✅ Link to relevant research/data

### DON'T
- ❌ Document trivial choices
- ❌ Skip the "cons" of chosen option
- ❌ Forget to note assumptions
- ❌ Make it a debate record

## Integration

- Referenced by `SESSION_LOG.md` when decisions are made
- Influences `ACTION_PLAN.md` priorities
- Prevents duplicate discussions
- Provides context for new team members