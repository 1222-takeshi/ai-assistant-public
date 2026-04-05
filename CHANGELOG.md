# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **AI agent team framework repositioning** — Repo reframed as a scaffold framework; `dev/` workflow is now one opt-in example, not a mandate
- **8 new team examples** in `examples/`: executive-team (CEO/CTO/CFO), qa-team, field-engineering-team, admin-support-team (secretary/finance/HR/legal), security-team, data-science-team, dev-workflow (reference copy), pmo-workflow (reference copy)
- **`examples/team-catalog.md`** — Comprehensive 9-team comparison catalog
- **`docs/framework.md`** — Explicit framework vs examples boundary documentation

### Changed

- `README.md` / `README.en.md` — Reframed from "dev workflow template" to "AI agent team framework scaffold"
- `CLAUDE.md` — Reviewer policy now marked as "this repo's choice", not a universal mandate
- `AGENTS.md` — Added prominent notice that `dev/` configuration is one example, not required

## [1.0.0] - 2026-04-05

### Added

- **Multi-agent team template** — Orchestrator, 2× Researcher, Requirements Analyst, 2× Implementer, ultra-strict Reviewer roles defined in `.claude/team-topology.yaml`
- **Core workflow commands** — `/dev/start-team`, `/dev/status`, `/dev/orchestrate`, `/dev/research`, `/dev/define-requirements`, `/dev/implement`, `/dev/review`
- **Ultra-strict reviewer policy** — NG = immediate `gh pr close`, no fix loops; 🔴≥1 or 🟡≥3 triggers NG
- **GitHub-only happy path** — `examples/github-only-flow.md` and four example templates for issues, PRs, and review comments
- **AGENTS.md** — English-language context file for GitHub Copilot coding agent and Codex
- **`.github/copilot-setup-steps.yml`** — Copilot coding agent environment bootstrap (Python 3.11 + pip + bootstrap.sh)
- **`scripts/setup-labels.sh`** — Idempotent GitHub label setup (6 workflow labels) for any repository
- **`scripts/bootstrap.sh`** — Non-destructive environment initializer; `--setup-labels` flag added
- **`scripts/doctor.py`** — Environment health checker (success / warning / failure categories)
- **`scripts/validate-config.py`** — Config file integrity validator (`--tracked-only`, `--check-local`)
- **`scripts/setup-worktree.sh`** / `worktree-cleanup.sh` / `list-worktrees.sh` — Git worktree lifecycle helpers
- **PR review flow docs** — `docs/pr-review-flow.md` as source of truth for multi-stage review
- **Onboarding docs** — `docs/onboarding.md` with bootstrap, doctor, and label setup steps
- **Optional PMO profile** — Notion / Atlassian / GCal / Slack / Gmail integration templates (opt-in only)
- **Config layering** — `config/*.yaml` (public template) < `config/*.local.yaml` (untracked runtime values)
- **314 tests** — `pytest tests/ -q -p no:cacheprovider` baseline

### Security

- Public release sanitization — private repo slug, Atlassian domain, Notion IDs, and absolute paths removed from history via `detect-secrets` verified patch workflow

[Unreleased]: https://github.com/YOUR_ORG/YOUR_REPO/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/YOUR_ORG/YOUR_REPO/releases/tag/v1.0.0
