---
name: review
description: Use when evaluating code changes for correctness, regressions, safety, maintainability, or when the user explicitly asks for a review.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# Review

Find defects and risks before merge or handoff. Default to report mode. Edit only when the user asks to fix, refine, or apply the findings.

## Boundary

Review is not implementation planning, broad cleanup, or praise. It answers: "What can break, what evidence supports that, and what should change?"

Use `refactor` for behavior-preserving cleanup, `second-pass` for replacing a just-finished implementation with a cleaner one, and `rewrite` when the design itself may be wrong.

## Preflight

1. Define the review target: staged diff, branch diff, changed files, PR, or named files.
2. Read local instructions and relevant tests/callers before judging code.
3. Run a baseline build/test/lint when practical. If skipped, state the reason.
4. Prefer `hunk diff`/`hunk show` when available for human-facing diffs; use `git diff` as fallback.

## Analysis

Prioritize issues in this order:

1. Incorrect behavior, data loss, security exposure, crashes, races, resource leaks
2. API/contract regressions, persistence or migration risks, edge-case gaps
3. Missing tests for behavior that can realistically break
4. Maintainability problems that hide defects or make future changes risky
5. Style only when it causes confusion, inconsistency, or tooling failure

Do not list speculative concerns. Every finding needs a concrete file/line, failure mode, and fix direction.

## Modes

- **Report mode:** Findings first, ordered by severity. Do not edit. Include skipped checks and residual risk.
- **Refine mode:** Apply only targeted fixes for accepted findings. Use relevant language skills, keep behavior fixed unless the finding is a behavior bug, and rerun verification.

## Output

Use this shape:

1. Findings, ordered by severity: `[P0-P3] file:line - issue -> fix`
2. Open questions or assumptions
3. Verification run or skipped

If there are no findings, say that directly and name the remaining test gaps or residual risk.

## Anti-Rationalization

| Excuse | Reality |
| :--- | :--- |
| "Tests pass, so there are no issues." | Tests are evidence, not proof. Review contracts, edge cases, and integration paths. |
| "This is mostly style." | Style-only notes are noise unless they affect correctness, clarity, or local conventions. |
| "I should fix it while reviewing." | Report first unless the user asked for refinement. |
