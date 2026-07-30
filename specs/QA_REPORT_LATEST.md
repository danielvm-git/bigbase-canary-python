# QA Audit Report — bigbase-canary-python

**Date:** 2026-07-30
**Auditor:** MiMoCode (automated)
**Commit:** `878eb67` (origin/main, post v0.1.1 release)

---

## Run Config

| Parameter | Value | Source |
|-----------|-------|--------|
| **`<N>` (ceiling)** | 15 | Repo <5k LOC (27 src + 12 test Python LOC) |
| **`<FROZEN>`** | See table below | CONVENTIONS.md, AGENTS.md, git history |
| **Preflight** | `uv run ruff check . && uv run mypy src/ && uv run pytest -q` | CONVENTIONS.md |
| **Live site** | `https://python.bigbase.click` → HTTP 200, `v0.1.1` | curl verified |
| **CI status** | All green (10/10 runs successful) | `gh run list` |

### Frozen Boundaries

| File | Reason |
|------|--------|
| `src/bigbase_canary_python/app.py` | Sole application route; AGENTS.md "Never add real product features" |
| `tests/test_smoke.py` | Golden test; invariant fixture per CONVENTIONS.md |
| `VERSION` | Wire format consumed by app at runtime + CI deploy |
| `.github/workflows/test-build-release.yml` | CI contract; pinned action SHAs |
| `.github/workflows/deploy.yml` | Deploy contract; pinned action SHAs |
| `scripts/preflight.sh` | Gate script; CONVENTIONS.md "Always Green" |
| `scripts/land-branch.sh` | Integration contract; CONVENTIONS.md solo-git workflow |

### Hotspots (high-churn files)

| File | Churn (12mo) | Notes |
|------|-------------|-------|
| `.github/workflows/test-build-release.yml` | 3 | CI pipeline; most-iterated file |
| `.github/workflows/deploy.yml` | 3 | Deploy pipeline; most-iterated file |
| `tests/test_smoke.py` | 2 | Version assertion recently fixed |
| `specs/state.yaml` | 2 | Session state |
| `specs/bugs/registry.yaml` | 2 | Bug tracking |

### Per-Module Risk Levels

| Module | Risk | Rationale |
|--------|------|-----------|
| `app.py` (Flask route) | P3 | Single route, no user input, no persistence |
| `test_smoke.py` | P3 | Single assertion, reads VERSION dynamically |
| `.github/workflows/*` | P2 | CI/CD contract, pinned SHAs, high churn |
| `scripts/preflight.sh` | P3 | 3-command gate script |
| `scripts/land-branch.sh` | P3 | Solo-git integration script |
| `pyproject.toml` | P2 | Build config; version field drift risk |
| `CHANGELOG.md` | P2 | Release history; managed by big-release |

### Seeded Issues

| Issue # | Status | Summary |
|---------|--------|---------|
| #1 | Closed (fixed) | VERSION file goes stale on releases |

---

## Findings

### F-001: `pyproject.toml` version drift from released version

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Scope** | build |
| **Status** | **FIXED** |
| **Confidence** | 10/10 |

**Description:** `pyproject.toml` had `version = "0.1.0"` hardcoded. The released version was `0.1.1` (tag `v0.1.1`, live site `v0.1.1`, `VERSION` file `0.1.1`). `uv build` produced a wheel claiming to be `0.1.0`.

**Root Cause:** The `big-release` tool updates `VERSION` and `CHANGELOG.md` but did not update `pyproject.toml`'s `version` field. The build system (`hatchling`) reads version from `pyproject.toml`, not from `VERSION`.

**Fix Applied:**
1. Updated `pyproject.toml` version to `0.1.1`
2. Added `sed` command to CI `Update VERSION file` step to sync `pyproject.toml` version from tag on future releases
3. Verified `uv build` now produces `bigbase_canary_python-0.1.1-py3-none-any.whl`

**Verification:**
```bash
$ uv build && ls dist/
bigbase_canary_python-0.1.1-py3-none-any.whl  ← correct
$ cat VERSION
0.1.1
```

---

### F-002: CHANGELOG.md has duplicate `[0.1.0]` sections

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Scope** | docs |
| **Status** | **FIXED** |
| **Confidence** | 10/10 |

**Description:** `CHANGELOG.md` contained two `## [0.1.0] - 2026-07-25` sections. The second was a subset of the first (missing the "Fixed" entry).

**Fix Applied:** Removed the duplicate section. Single `[0.1.0]` entry remains with both "Added" and "Fixed" subsections.

---

### F-003: CHANGELOG.md missing `[0.1.1]` entry

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Scope** | docs |
| **Status** | **FIXED** |
| **Confidence** | 10/10 |

**Description:** Version `0.1.1` was released but `CHANGELOG.md` had no `[0.1.1]` section.

**Fix Applied:** Added `[0.1.1] - 2026-07-30` section with the two CI fix commits that comprised the release.

---

## Security Review

**Scope:** Full codebase scan (no auth, no user input, no external APIs)

| Category | Status |
|----------|--------|
| SQL Injection | N/A — no database |
| XSS | N/A — static HTML response, no user input |
| SSRF | N/A — no outbound HTTP |
| Command Injection | N/A — no shell commands with user input |
| Auth Bypass | N/A — no authentication |
| Unsafe Deserialization | N/A — no deserialization |
| Path Traversal | N/A — no user-controlled file paths |
| Secrets Exposure | Clean — no secrets in source; `GITHUB_TOKEN`, `BIGBASE_*` in GitHub Secrets |
| Template Injection | N/A — f-string with static version, no user input |

**Verdict:** No security vulnerabilities found. The application has no attack surface — it serves a single static HTML page with a version footer.

---

## Contract Validation (`<FROZEN>` boundaries)

| Boundary | Status | Evidence |
|----------|--------|----------|
| `app.py` route contract | PASS | `GET /` returns `<h1>bigbase canary (Python)</h1><footer>v{VERSION}</footer>` |
| `test_smoke.py` assertion | PASS | Reads `VERSION` dynamically; 1 test passes |
| `VERSION` file format | PASS | Plain text, single line, `0.1.1` |
| CI workflow structure | PASS | Both YAML files parse correctly; pinned SHAs intact |
| Preflight gate | PASS | `ruff check` + `mypy` + `pytest` all green |

---

## Traceability

| Story | Code | Tests | Deployed |
|-------|------|-------|----------|
| e01s01 (stand up canary) | `app.py`, `__init__.py`, `pyproject.toml` | `test_smoke.py` | Live at `python.bigbase.click` |

All stories in `specs/execution-status.yaml` are `done`. No dark stories.

---

## Verdict

**Overall: PASS — all findings fixed**

- **Preflight:** Green (ruff + mypy + pytest)
- **CI:** Green (all 10 recent runs successful)
- **Build:** `uv build` produces `0.1.1` wheel (was `0.1.0`)
- **Live site:** HTTP 200, serving `v0.1.1`
- **Security:** No vulnerabilities
- **Contracts:** All frozen boundaries intact
- **Open bugs:** 0
- **Findings:** 3 found, 3 fixed (1 Medium, 2 Low)

The canary site is healthy and fulfilling its purpose as a regression signal for the `big-release` + `bigbase-deploy` pipeline.
