# ADR 0001 — Stack and tooling choices

- **Status:** accepted
- **Date:** 2026-10-15

## Context

Phase 0 sets up a public portfolio repository that will grow into a Web3 threat
monitor feeding Microsoft Sentinel. Decisions here should minimize friction on a
Windows machine while staying professional and reproducible.

## Decisions

1. **Language / runtime:** Python, baseline **3.11** (`requires-python = ">=3.11"`).
   The developer's machine runs 3.11.6 and all target libraries (web3.py,
   FastAPI, SQLAlchemy) fully support it. Can be bumped to 3.12+ later.
2. **Dependency management:** **pip + PEP 621** (`pyproject.toml`), installable
   with `pip install -e ".[dev]"`. `uv` is recommended as a faster drop-in later,
   but is not required to build or run the project.
3. **Quality tooling:** `ruff` (lint + format), `mypy` (strict types), `bandit`
   (Python SAST), `pytest`.
4. **Two-tier CI/CD:**
   - Local `pre-commit`: hygiene hooks, `ruff`, `bandit`, and `gitleaks`
     (secret scanning). Fast and reliable on first run.
   - GitHub Actions: installs the package and runs `ruff`, `mypy`, `bandit`,
     and `pytest`. **`mypy` and `pytest` live in CI** (not pre-commit) because
     they need the installed environment and third-party type stubs.
5. **GitHub-native security:** CodeQL (default setup), secret scanning + push
   protection. Free for public repos.
6. **Branching:** git-flow style — `develop` is the integration/default branch,
   `main` is the release branch, work happens on `feature/*` branches.
7. **Layout:** `src/` layout with a single import root `web3_threat_monitor`.

## Consequences

- Everything runs with tools the developer already has; no new installs are
  required to validate the scaffold.
- Reproducibility is good but not pinned to a lockfile yet; adopting `uv.lock`
  (or pip-tools) is a tracked future improvement.
