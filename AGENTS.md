# AGENTS.md

This file provides context for AI coding agents (Codex, Copilot, Claude Code, etc.)
working in this repository.

> **Japanese users**: See [CLAUDE.md](CLAUDE.md) for the full Japanese operational guide.

## Purpose

This repository is a **multi-agent development workflow template** for Claude Code / Codex.
It provides:
- Custom slash commands for a 7-role agent team (`/dev/` commands)
- `git worktree`-based parallel development patterns
- GitHub Issue-driven flow: research → requirements → review → implement → PR → review → merge
- Optional PMO profile (Notion / Jira / Confluence integration)

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
