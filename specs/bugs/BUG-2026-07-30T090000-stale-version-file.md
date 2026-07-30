---
bug_id: BUG-2026-07-30T090000
status: closed
severity: high
scope: ci
title: VERSION file goes stale on releases and tests hardcode static version string
---

# BUG-2026-07-30T090000: VERSION file goes stale on releases and tests hardcode static version string

## Problem

- **Actual behavior**: When `big-release` cuts a new release tag (e.g. `v0.1.1`), the `VERSION` file in the repo is not updated automatically. The live site reads `VERSION` at request time and will display `0.1.0` indefinitely. Furthermore, `tests/test_smoke.py` hardcodes `assert b"0.1.0" in resp.data`, masking version drift in CI.
- **Expected behavior**:
  1. `test-build-release.yml` updates `VERSION` automatically after `big-release` runs and commits the updated `VERSION` file back to `main` with `[skip ci]`.
  2. `tests/test_smoke.py` reads `VERSION` dynamically at test execution time to assert that the HTTP endpoint renders the actual content of the `VERSION` file.
- **Security impact**: NONE — no security exploit path identified.

## Root Cause Analysis

- **Code paths involved**: `.github/workflows/test-build-release.yml` (release job) and `tests/test_smoke.py`.
- **Why current code fails**: `test-build-release.yml` finishes `big-release` without writing the tagged version back to the `VERSION` file. `test_smoke.py` checks for a fixed string `"0.1.0"` instead of reading `Path("VERSION").read_text().strip()`.
- **Risk level**: Low (isolated CI post-release step + test dynamic read).

## TDD Fix Plan

1. **RED**: Update `tests/test_smoke.py` to test that the homepage renders the content of `VERSION` dynamically instead of hardcoding `"0.1.0"`.
   **GREEN**: Change `tests/test_smoke.py` to read `Path("VERSION").read_text().strip()`.
   **verify**: `uv run pytest -q tests/test_smoke.py`

2. **RED**: Verify `.github/workflows/test-build-release.yml` contains the `Update VERSION file` step after `Run big-release`.
   **GREEN**: Add `Update VERSION file` step in `.github/workflows/test-build-release.yml` release job after `Run big-release`.
   **verify**: `grep -q "Update VERSION file" .github/workflows/test-build-release.yml && python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test-build-release.yml'))"`

## Acceptance Criteria

- [x] `tests/test_smoke.py` dynamically reads `VERSION` content.
- [x] `.github/workflows/test-build-release.yml` updates `VERSION` post-release via `git describe --tags --abbrev=0`.
- [x] All preflight tests pass (`uv run ruff check . && uv run mypy src/ && uv run pytest -q`).

## Resolution

- Updated `tests/test_smoke.py` to read `VERSION` dynamically using `Path("VERSION").read_text().strip()`.
- Added `Update VERSION file` step to `.github/workflows/test-build-release.yml` in the `release` job right after `Run big-release`, pushing `VERSION` updates back to `main` with `[skip ci]`.
- Verified preflight test suite and YAML syntax.
