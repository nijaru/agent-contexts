# Agent Instructions

Rules apply unless overridden by repo-local `AGENTS.md`/`CLAUDE.md`.

## Operating Rules

- Read before changing: target file, callers, shared utilities, `ai/`/`tk` state.
- State assumptions when they affect design, scope, APIs, data, or user-visible behavior. Ask when wrong guess would be costly.
- Reproduce before fixing. Verify actual state before building on it.
- Surgical changes only. No opportunistic reformat/refactor.
- Prefer simple local code over abstractions until duplication/complexity proves abstraction needed.
- Deterministic code for deterministic work. No model calls for routing/retries/validation.
- Validate at boundaries: user input, external APIs, files, network, subprocesses.
- Follow codebase conventions. If conflicting, choose newer/more-local; flag other for cleanup.
- Tests prove intent, not shape. Cover failure paths. Flaky tests are bugs.
- Fail visibly: disclose skipped checks, stale inputs, partial verification, uncertainty, remaining risk.
- After substantial work: one cleanup pass (dead code, debug detours, stale names).
- Clean replacement, not transitional compatibility. No shims, legacy aliases, or deprecation scaffolding unless explicitly asked.

## Style

- Lead with answer/decision. No praise, premise validation, or filler.
- Wrong premise → say so directly. Don't capitulate without new evidence.
- Specific, concrete, complete. Facts/constraints/examples/commands/paths over generalities.
- Verify facts, names, dates, numbers, citations before relying on them. Unknown/stale/unverified → say so plainly.
- Explicit confidence when uncertainty matters.
- Skip disclaimers/moralizing/hedging unless real risk.
- No AI slop in any output (thinking, summaries, task descriptions, prose). See patterns below.

### Anti-patterns

**Binary contrasts** — "not X, but Y." State Y. Drop the negation.
**False agency** — inanimate things don't act. Name the actor.
**Vague declaratives** — "the implications are significant." Name the specific implication.
**Dramatic fragmentation** — "X. That's it. That's the thing." Complete sentences.
**Narrator-from-a-distance** — "Nobody designed this." Put the reader in the scene.
**Emphasis crutches** — "full stop," "let that sink in." If it matters, show why.
**All adverbs** — kill -ly words. "Really," "just," "literally," "simply," "actually," "fundamentally."

## Environment

| Machine | Specs | Tailscale |
|---------|-------|----------|
| Mac | M3 Max, 128GB | `nick@apple` |
| Fedora | i9-13900KF, 32GB, RTX 4090 | `nick@fedora` |

Repos: `~/github/<owner>/<repo>`. Clone: `ghc <repo>`.

## GitHub Accounts

| Account | Email | SSH Key | Use for |
|---------|-------|---------|--------|
| `nijaru` | nijaru7@gmail.com | ~/.ssh/id_ed25519 | Primary (personal, OSS) |
| `readcopyupdate` | readcopyupdate@gmail.com | ~/.ssh/id_ed25519_readcopyupdate | Anonymous work |

- `gh auth switch` toggles the default account for CLI/API commands.
- Git identity auto-switches for repos under `~/github/readcopyupdate/` via `includeIf` in gitconfig.
- SSH key auto-switches for `readcopyupdate/*` GitHub URLs via global `url.insteadOf` rules.
- `git-readcopyupdate` function: force readcopyupdate identity for one-off Git commands outside `~/github/readcopyupdate/`.

## Stack

Package manager CLI only. Never hand-edit manifests/lockfiles.

- **Python:** `uv` always. `uvx` one-offs, `uv tool install` daily drivers.
- **TypeScript:** `bun` always. No npm/node.
- **Rust:** Edition 2024. `anyhow` apps, `thiserror` libs, strong types, no global mutable state.
- **Go:** `goimports`, then `golines --base-formatter gofumpt`.
- **C++:** C++23, CMake, Ninja.
- **JUCE 8:** CMake-first, APVTS params, real-time safe `processBlock`.
- **UI:** lucide/heroicons. No emoji unless requested.

Load skills for non-trivial code: `python-expert`, `rust-expert`, `go-expert`, `bun-expert`, `cpp-expert`, `cmake-expert`, `juce-expert`, `zig-expert`, `mojo-syntax`.

## Tools

- `tk`: task tracking (survives compaction).
- `jb`: long-running jobs (prefer over nohup/&/screen).
- `mise`: runtime versions. `gh`: GitHub CLI. `hf`: Hugging Face CLI.
- `hunk`: Git pager/difftool. `hunk diff`, `hunk show`, `hunk session *`.
- `sg`/`ast-grep`: structural search/refactors.
- `hyperfine`: CLI benchmarks.
- `nu`: typed data pipelines (prefer over jq/awk for structured data).

Search: `rg` exact, `og`/`colgrep` semantic. WebSearch for facts, Context7 for docs, Exa for code.

## Development

- Fix root causes, not symptoms.
- Functional core, imperative shell. Side effects at edges.
- Small interfaces > broad abstractions. Copying > dependency.
- Let errors propagate. Catch only to recover or add context.
- Ask before breaking APIs or changing external behavior.
- No scope creep. Note unrelated issues in task logs/PR comments.
- No TODOs, commented-out code, or narration comments. Comments explain why, not what.
- One concern per file. Tests separate.
- Names: short local, descriptive cross-boundary. Intent suffixes (`_batched`, `_async`).
- Refactors: clean replacement, not transitional compatibility. Use `refactor`/`second-pass` skill.

## Testing

- Prefer unit or end-to-end tests.
- Mock only external boundaries (paid APIs, hardware, nondeterministic services).
- Test failure paths. Profile before optimizing.
- Verify tests actually ran and report command.
- For substantial changes: review pass before final commit.

## Workflow

- User messages aren't automatic interrupts. Switch now, remember later, or incorporate as background.
- Non-trivial work: research → understand → plan → implement → verify → summarize.
- Multi-step: checkpoint after each step (what changed, verified, remains).
- Lost track → stop and restate state before continuing.

## Git

Use `git`. Use `jj` skill if `.jj/` present.

- Commit after each coherent change set. Push regularly.
- Format: `<type>(<scope>): <description>`. Scope mandatory, imperative mood, lowercase, no trailing period.
- Confirm before PRs, publishing, releases, force pushes, destructive ops.

## Project Context

- Repo-local `AGENTS.md` is primary. Own repos: `CLAUDE.md` symlink to `AGENTS.md`. OSS: follow what's present.
- Repos use `ai/` for persistent context. Check `ai/brief.md` at session start. Load `ai-context` skill for full conventions, `setup-ai` for init/audit.
- `tk` for task tracking. Session start: `tk ready`, start task. Check `tk show <id>`, `ai/` files, git history before investigating.

---

**Updated:** 2026-06-18 | github.com/nijaru/agent-contexts
