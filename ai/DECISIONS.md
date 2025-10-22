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

---

## 2025-01-21: Use docs/ for permanent, ai/ for evolving context

**Context**: Needed clear guidance on where different types of documentation belong

**Decision**: Two-directory model with clear separation
- `docs/` — Permanent, human-facing documentation
- `ai/` — Evolving, AI-optimized working context

**Rationale**:
- Aligns with industry standards (docs/ is ubiquitous)
- Clear mental model: permanent vs temporary
- Token efficiency: AI loads ai/ by default, docs/ as needed
- "Knowledge graduation" flow: findings move from ai/ → docs/ when permanent

**Alternatives Considered**:
- Three directories (docs/, internal/, ai/) — Too complex for most projects
- Just ai/ — Doesn't align with existing project conventions
- Just docs/ — AI working context would bloat human docs

**Optional directories**:
- `docs/adr/` — Only for projects with formal ADR process
- `internal/` — Only for public vs private doc separation (corporate)
- `.github/` — Only if using GitHub

---

## 2025-01-21: Recommend starting minimal, add as needed

**Context**: Uncertain whether to prescribe full directory structure upfront

**Decision**: Start with just `docs/` + `ai/`, add subdirs only when needed

**Rationale**:
- Most projects don't need formal ADRs (docs/adr/)
- Small projects don't need internal/
- Better to add structure when it's needed vs create empty dirs
- Respects existing project structures during discovery

**Guidance**: "Respect existing" — if project has internal/, wiki/, use them