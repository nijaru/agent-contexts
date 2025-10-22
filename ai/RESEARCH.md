# Research

## AI Agent Context Optimization (researched 2025-01-21)

**Sources**:
- Claude Code context window best practices
- Documentation-driven development patterns
- Token optimization strategies

**Key Findings**:
- Claude performs poorly after 80% context usage
- Well-crafted AGENTS.md essential but bloated versions waste tokens
- Intentional compaction keeps agents focused
- 60% of AI tool usage is context identification/retrieval
- Documentation creates "temporary expertise" in domains

**Applied**:
- Reduced repo from ~17,500 to ~2,500 tokens (85% reduction)
- Focus on organization patterns only
- Push agents to research technical knowledge fresh

## Common Directory Naming (researched 2025-01-21)

**Sources**: GitHub conventions, ML project structures

**Key Findings**:
- Standard patterns: docs/, src/, tests/, tools/
- Hidden directories (.ai/, .agents/) often ignored by agents
- Short lowercase names preferred for token efficiency

**Decision**: Use `ai/` (visible, clear, short)

## Multi-Agent Collaboration Patterns (researched 2025-01-21)

**Sources**: Multi-agent AI workflows 2024-2025

**Key Findings**:
- Specialized agents working together becoming standard
- Handoff mechanisms route tasks to appropriate agents
- 40% reduction in communication overhead with proper patterns

**Relevance**: Our TODO/STATUS/DECISIONS structure enables clean handoffs