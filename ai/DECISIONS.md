# Decisions

## 2025-01-21: Use ai/ directory instead of internal/ or .ai/

**Context**: Needed standard location for AI agent working context

**Decision**: Use `ai/` (visible directory)

**Rationale**:
- Visible to all agents (hidden directories get ignored/require confirmation)
- Clear purpose, short name (token-efficient)
- Unlikely to collide with actual code
- Follows pattern of docs/, tests/, etc.

**Alternatives Considered**:
- `.ai/` - Would be ignored by many agents
- `internal/` - Too generic, not AI-specific
- `agents/` - Potential collision with multi-agent systems

---

## 2025-01-21: Remove all language and tool patterns

**Context**: Repository was 17 files with language/tool-specific patterns

**Decision**: Remove all coding patterns, focus only on organization

**Rationale**:
- AI agents already know how to code from training data
- Best practices evolve - agents should research current SOTA
- Reduces token usage from ~17,500 to ~2,500 (85%)
- Clearer purpose: teach organization, not coding

**Tradeoffs**: Users must reference archived tag (v0.0.3-archive) for old patterns

---

## 2025-01-21: Consolidate into PRACTICES.md

**Context**: Had scattered patterns across DOC_PATTERNS, AI_CODE_PATTERNS, etc.

**Decision**: Single PRACTICES.md file with all essential guidance

**Rationale**:
- Easier to load and reference
- Reduces navigation overhead
- More concise and focused
- Better token efficiency

**Structure**: ~600 words covering file purposes, update modes, context management