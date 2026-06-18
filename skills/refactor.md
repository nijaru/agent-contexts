---
name: refactor
description: Use when improving existing code structure while preserving behavior, including duplication, deep nesting, unclear names, dead code, or misplaced responsibility.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# Refactor

Improve structure without changing externally visible behavior.

## Boundary

Refactoring preserves behavior and design. Use `second-pass` when a just-finished implementation should be re-derived cleanly. Use `rewrite` when the data model, API, or architecture may need replacement.

## Preflight

1. Identify the concrete smell before editing.
2. Read immediate callers, tests, and shared helpers for the affected surface.
3. Establish behavior with existing tests or a focused manual check when practical.
4. If the public API, persisted data, or external integration contract may change, stop and surface the tradeoff first.

## Rules

- Prefer deletion, simplification, and moving responsibility to the right owner over new abstractions.
- Change internal APIs completely across callers in the same patch.
- Delete dead code, speculative generality, duplicated paths, and discovery-era names.
- Do not add or preserve compatibility shims, legacy aliases, fallback branches, deprecation scaffolding, temporary feature flags, or workaround paths unless explicitly asked.
- Use final names. Do not create `_old`, `_new`, `_v2`, `legacy`, or `compat` variants.
- Keep edits scoped to the smell. Do not reformat or redesign adjacent code opportunistically.

## Common Moves

- Extract helpers only when they name a real concept or remove meaningful duplication.
- Flatten nested control flow with guard clauses or clearer data flow.
- Replace primitive obsession with small domain types only when the type prevents mistakes.
- Split large functions when they mix responsibilities; keep cohesive long functions intact.
- Move side effects to edges when it makes the core easier to test or reason about.

## Verification

Run the behavior-preservation check from preflight, plus formatting/linting required by the repo. If no automated check exists, name the manual path inspected.

## Output

State the smell, the structural change, behavior-preservation evidence, and verification result. If no edit is warranted, say why the current structure is acceptable.

## Anti-Rationalization

| Excuse | Reality |
| :--- | :--- |
| "A wrapper lets us migrate later." | Internal compatibility layers become permanent. Change all callers now or do not change the interface. |
| "This is cleaner because it is more abstract." | Abstractions must remove real complexity or encode a real domain concept. |
| "I touched the file, so I should clean nearby code." | Adjacent cleanup is scope creep unless it is required for the refactor. |
