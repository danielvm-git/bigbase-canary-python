# Conventions — bigbase-canary-python

Governed by the [bigpowers](https://github.com/danielvm-git/bigpowers) methodology. This file is the project-local subset relevant to a minimal single-route canary — see bigpowers `CONVENTIONS.md` for the full doctrine.

## Conventional Commits & Semantic Versioning

All changes MUST follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Versioning follows [Semantic Versioning 2.0.0](https://semver.org/), decided at release time by `big-release` from commit history — never hand-tracked.

**Format:** `<type>(<scope>): <description>` (space after colon mandatory).

- `feat`: Minor bump — new feature
- `fix`: Patch bump — bug fix
- `perf`: Patch bump — performance improvement
- `docs`, `chore`, `style`, `refactor`, `test`: No bump (unless breaking)
- `BREAKING CHANGE:` (or `!` after type): Major bump

## GitHub & Git Operations

- No direct work on `main`. Every task starts with a feature branch/worktree via `kickoff-branch`.
- Integrate (solo-git profile): `bash scripts/land-branch.sh <branch> "<conventional message>"` after `release-branch` gates — local squash to `main`, then push.
- Use `gh repo clone`, not `git clone`. Use `gh run watch` / `gh pr checks` for CI status.
- **Git Attribution:** NEVER include `Co-authored-by:` or any AI-agent attribution footer.
- Never call GitHub REST API directly (curl/fetch) — use `gh`. (bigbase's own REST API is a separate service and is fine to curl directly for provisioning.)
- Never create GitHub issues from automated workflows — produce local `.md` files in `specs/bugs/` instead.

## Pre-commit hook (`hook-commits`, adapted)

Fresh clone: `git config core.hooksPath .githooks`. `.githooks/pre-commit` runs `scripts/preflight.sh` before every commit.

## Always Green / Shift Left

Preflight and CI MUST be green before any forward work.

**Preflight:** `uv run ruff check . && uv run mypy src/ && uv run pytest -q` — must pass before kickoff, develop, or verify phases advance.

**CI green:** `gh pr checks` (or the Actions tab) must show passing before merge/land.

## Discovered Defects

1. **quick-fix** — trivial, single-file fixes within guardrails.
2. **fix-bug** — needs investigation (`specs/bugs/BUG-*.md` + TDD).
3. **Log** — only when reproduction is blocked after a good-faith attempt.

Discovered fixes ship in the same land as the original work, in separate commits.

**Banned dismissive phrases:** "pre-existing", "unrelated to this session", "not introduced by my changes", "out of scope" (when ignoring a red gate).

## specs/ — All Planning Output Goes Here

- `specs/state.yaml` — active session, handoff
- `specs/release-plan.yaml` — release index, story BCPs
- `specs/execution-status.yaml` — sole source of truth for story done/pending status
- `specs/epics/e01-canary-site/` — this repo's one epic
- `specs/bugs/BUG-*.md` + `specs/bugs/registry.yaml` — bug investigations (never GitHub issues)
- `specs/tech-architecture/tech-stack.md` — stack notes

## Defensive Code Categories

None apply. Static version-footer endpoint, no untrusted input beyond the HTTP request, no external dependencies to guard.

## Risk Tier

P2 — infrastructure/regression-signal repo. `plan-tests` still runs (pipeline correctness is the point) but BCP sizing stays lightweight.
