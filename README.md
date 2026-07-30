# bigbase-canary-python

Minimal Python HTTP canary site proving that [big-release](https://github.com/danielvm-git/big-release) and the [bigbase-deploy](https://github.com/danielvm-git/.github) GitHub Action still work end-to-end.

**Live:** https://python.bigbase.click

## Stack

- Python 3.12+
- Flask
- Managed with [uv](https://docs.astral.sh/uv/)

## Commands

| Action | Command |
|--------|---------|
| Run | `uv run python -m bigbase_canary_python.app` |
| Test | `uv run pytest -q` |
| Build | `uv build` |
| Lint | `uv run ruff check .` |
| Typecheck | `uv run mypy src/` |
| Preflight | `uv run ruff check . && uv run mypy src/ && uv run pytest -q` |

## Architecture

`src/bigbase_canary_python/app.py` — one Flask route reads the `VERSION` file at request time and renders it into an HTML footer. No persistence, no auth, no routing beyond the single route.

## License

[MIT](LICENSE)
