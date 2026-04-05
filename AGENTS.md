# AGENTS.md

This file provides context for AI coding agents (Codex, Copilot, Claude Code, etc.)
working in this repository.

> **Japanese users**: See [CLAUDE.md](CLAUDE.md) for the full Japanese operational guide.

## Purpose

This repository is a **framework for building and operating AI agent teams** — for Claude Code, Codex, GitHub Copilot, or any LLM-based coding agent.

It provides:
- A scaffold for defining agent roles, lanes, and handoffs (`team-topology.yaml`)
- `git worktree`-based parallel work patterns
- GitHub Issue-driven coordination layer
- Scripts for environment setup, health checks, and label management
- **Reference implementations** in `examples/` for various team types

> ⚠️ **Important**: The `dev/` commands in `.claude/commands/dev/` are **this repository's chosen configuration** — one example of the framework in use.
> You are NOT required to use this team structure, review policy, or workflow.
> See `examples/team-catalog.md` for alternative team patterns.

## Available Team Examples

| Example | Description |
|---------|-------------|
| `examples/dev-workflow/` | Software development team (Orchestrator / Researcher / Implementer / Reviewer) |
| `examples/executive-team/` | Executive team (CEO / CTO / CFO / Chief of Staff) |
| `examples/qa-team/` | QA / quality assurance team |
| `examples/field-engineering-team/` | Field engineering / customer-facing team |
| `examples/admin-support-team/` | Admin / back-office (secretary, finance, HR, legal) |
| `examples/security-team/` | Security review team |
| `examples/data-science-team/` | Data science / ML team |
| `examples/pmo-workflow/` | PMO team (requires external MCP integrations) |

## Quick Commands

```bash
# Install dependencies
python3 -m pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v -p no:cacheprovider

# Environment health check
python3 scripts/doctor.py

# Non-destructive bootstrap
./scripts/bootstrap.sh

# Config validation
python3 scripts/validate-config.py --tracked-only
```

## Repository Structure

```
.claude/
  commands/dev/          # Core workflow commands (start-team, implement, review, …)
  commands/pmo/          # Optional PMO commands
  team-topology.yaml     # Roles, lanes, worktrees, handoffs
examples/
  github-only-flow.md    # Step-by-step GitHub-only happy path
  templates/             # Issue / PR / review sample artifacts
scripts/
  bootstrap.sh           # Non-destructive repo initializer
  doctor.py              # Environment health checker
  gh-workflow.sh         # Standardized push / PR / issue helper
  setup-worktree.sh      # Create worktrees under .claude/worktrees/
  setup-labels.sh        # Create required GitHub labels in a repo
  validate-config.py     # Config template consistency checker
tests/                   # pytest test suite (299 passed baseline)
docs/                    # onboarding, pr-review-flow, pmo-profile, architecture, …
config/                  # Public-safe config templates (notion.yaml, confluence.yaml)
```

## Agent Team Roles

| Role | Count | Command | Responsibility |
|------|-------|---------|----------------|
| Orchestrator | 1 | `/dev/orchestrate` | Prioritize, gate implementation, decide merges |
| Researcher | 2 | `/dev/research` | Parallel research, record in GitHub Issues |
| Requirements Analyst | 1 | `/dev/define-requirements` | Convert requests to requirements + test specs |
| Reviewer | 1 | `/dev/review` | **Ultra-strict** gatekeeper (see policy below) |
| Implementer | 2 | `/dev/implement` | Implement in dedicated worktrees, create PRs |

## Reviewer Policy (Ultra-Strict)

- **NG** if any 🔴 required issue exists, OR if 🟡 recommended issues ≥ 3
- **NG action**: PR is **immediately closed** — no fix loops
- Implementer must create a **new branch + new PR** from scratch
- Never reopen a closed PR

## Development Rules

- **No direct push to `main`**
- Commit messages and PR titles: English, Conventional Commits format
- PR bodies, code comments, docs: Japanese is acceptable
- Tests: `pytest tests/ -v -p no:cacheprovider`
- Same-identity `COMMENTED` review is NOT a formal approval gate
- Config: tracked `config/*.yaml` are public-safe templates; real values go in `*.local.yaml` (gitignored)

## Prohibited Actions

- Do NOT commit secrets, tokens, internal IDs, or private URLs
- Do NOT push directly to `main`
- Do NOT hardcode `owner/repo` values in scripts (use `GH_REPO` env var or `gh repo view`)
- Do NOT reopen a NG-closed PR; create a new one
- Do NOT merge without Reviewer `approved` label + CI pass

## Worktree Convention

```bash
# Create a worktree for implementation
./scripts/setup-worktree.sh impl-1 feat/my-feature
cd .claude/worktrees/impl-1

# List all worktrees
./scripts/list-worktrees.sh
```

Worktrees are created under `.claude/worktrees/`. Remove after PR merge:
```bash
git worktree remove .claude/worktrees/impl-1
git branch -d feat/my-feature
```

## GitHub Labels Required

Run `./scripts/setup-labels.sh` to create these in a new repo:

| Label | Purpose |
|-------|---------|
| `research` | Research Issues |
| `requirements` | Requirements Issues |
| `implementation` | Implementation request Issues |
| `review-needed` | Waiting for review |
| `approved` | Reviewer approved |
| `blocked` | Blocker — Orchestrator handles first |

## Source of Truth

- `CLAUDE.md` — Full operational guide (Japanese)
- `.claude/team-topology.yaml` — Role / lane / worktree / handoff definitions
- `docs/pr-review-flow.md` — PR review flow details
- `docs/onboarding.md` — Onboarding steps
