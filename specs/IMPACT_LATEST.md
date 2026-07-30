## Target
`.github/workflows/test-build-release.yml` & `.github/workflows/deploy.yml` (CI/CD Pipeline Adaptation to v4.1.0 Central Template Pattern)

## Dependents (4)
- `AGENTS.md`: Documents CI/CD pipeline architecture and verification commands
- `specs/tech-architecture/tech-stack.md`: Documents CI workflow architecture
- `specs/product/SCOPE_LATEST.yaml`: Scopes CI/CD integration with `.github` templates
- GitHub Actions Runtime: Triggers deploy on push to main and handles artifact passing

## Affected Stories
- Story e01s01: Stand up canary site

## Test Coverage
- Local preflight: `uv run ruff check . && uv run mypy src/ && uv run pytest -q`
- Workflow YAML validation: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test-build-release.yml'))"`

## Risk: Low
Configuration update to upgrade CI/CD from v3.0.0 to v4.1.0 central template standards. Python application code is untouched.

## Recommended action
Proceed to `plan-work` to create detailed execution tasks in `specs/epics/e01-canary-site/e01s01-tasks.yaml`.
