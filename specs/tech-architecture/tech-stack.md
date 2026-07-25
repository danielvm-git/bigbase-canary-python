# Tech Stack — bigbase-canary-python

- **Language/runtime:** Python 3.12+, Flask, managed with `uv`.
- **Layout:** `src/bigbase_canary_python/app.py` — one route, reads `VERSION`, writes an HTML footer. `tests/test_smoke.py`.
- **CI:** GitHub Actions, `.github/workflows/test-build-release.yml` (lint → typecheck → test → build → release) + `.github/workflows/deploy.yml` (via `workflow_run`), copied from `danielvm-git/.github`'s `test-build-release-python.yml`/`deploy-python.yml` templates.
- **Release:** [big-release](https://github.com/danielvm-git/big-release), replacing the template's default `semantic-release` step.
- **Deploy:** `danielvm-git/.github/actions/bigbase-deploy@v1` → bigbase site `python` → `https://python.bigbase.click`, `app_type: python`.
- **Gray areas:** none load-bearing.
