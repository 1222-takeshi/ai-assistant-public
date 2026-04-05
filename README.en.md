# ai-assistant

**A multi-agent AI development team template** for Claude Code, GitHub Copilot coding agent, and Codex.

[![CI](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What Is This?

**ai-assistant** is a GitHub repository template that defines:

- A **team of specialized AI agents** (Orchestrator, Researchers, Requirements Analyst, Implementers, Reviewer)
- **Workflow commands** for each agent role (`/dev/start-team`, `/dev/implement`, `/dev/review`, …)
- Conventions for **GitHub Issue-driven development** with `git worktree` for parallel work
- An **ultra-strict Reviewer** policy: NG = PR closed immediately, no fix loops
- An optional **PMO profile** (Notion, Atlassian, GCal, Slack, Gmail)

---

## Quickstart

### Prerequisites

- Python 3.9+ (3.11 recommended)
- `git` and `gh` CLI authenticated to GitHub
- Claude Code, GitHub Copilot coding agent, or Codex

### 1. Clone and Initialize

```bash
git clone https://github.com/YOUR_ORG/YOUR_REPO.git
cd YOUR_REPO
./scripts/bootstrap.sh
```

### 2. Check the Environment

```bash
python3 scripts/doctor.py
# Expected: success=6 warning=N failure=0
```

### 3. Set Up Workflow Labels

```bash
./scripts/bootstrap.sh --setup-labels
# or: GH_REPO=your-org/your-repo ./scripts/setup-labels.sh
```

### 4. Start the Agent Team

Open a Claude Code (or Copilot) session in the repository root and run:

```
/dev/start-team
```

The Orchestrator will guide you through assigning roles and starting the first sprint.

---

## Agent Roles

| Role | Count | Responsibility |
|------|-------|---------------|
| Orchestrator | 1 | Sprint planning, merge decisions, agent coordination |
| Researcher | 2 | Technical investigation, findings documented as GitHub Issues |
| Requirements Analyst | 1 | Requirements Issues with test spec and acceptance criteria |
| Implementer | 2 | Implementation on isolated `git worktree` branches, PR creation |
| Reviewer | 1 | Ultra-strict code review; NG = immediate `gh pr close` |

## Reviewer Policy

| Finding | Threshold | Result |
|---------|-----------|--------|
| 🔴 Required | ≥ 1 | **NG** → PR closed immediately |
| 🟡 Recommended | ≥ 3 | **NG** → PR closed immediately |
| 🟡 Recommended | ≤ 2 | ✅ OK → `approved` label + merge |
| 🔴 = 0, 🟡 = 0 | — | ✅ OK → `approved` label + merge |

When NG: the Implementer **must create a new branch and a new PR** from scratch. Closed PRs are never reopened.

---

## Repository Layout

```text
ai-assistant/
├── AGENTS.md                        # Agent context for Copilot / Codex
├── CLAUDE.md                        # Claude Code global conventions
├── CHANGELOG.md
├── .github/
│   ├── copilot-setup-steps.yml      # Copilot coding agent bootstrap
│   ├── ISSUE_TEMPLATE/
│   │   ├── requirements.md          # Requirements Issue template
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/test.yml           # CI
├── .claude/
│   ├── commands/
│   │   ├── dev/                     # Core workflow commands
│   │   └── pmo/                     # Optional PMO commands
│   ├── worktrees/                   # git worktree directories
│   └── team-topology.yaml           # Role / lane / handoff definitions
├── config/
│   ├── notion.yaml                  # PMO config template
│   └── confluence.yaml
├── docs/
│   ├── architecture.md              # System diagram
│   ├── customization.md             # How to adapt the template
│   ├── faq.md
│   ├── onboarding.md
│   └── pr-review-flow.md
├── examples/
│   ├── github-only-flow.md          # Step-by-step happy path
│   └── templates/                   # Issue / PR / Review comment templates
├── scripts/
│   ├── bootstrap.sh                 # Environment initializer
│   ├── doctor.py                    # Environment health check
│   ├── validate-config.py           # Config integrity check
│   ├── setup-labels.sh              # Create GitHub workflow labels
│   ├── setup-worktree.sh
│   ├── worktree-cleanup.sh
│   └── list-worktrees.sh
└── tests/                           # 314 tests (pytest)
```

---

## GitHub-Only Happy Path

No MCP tools needed for core workflow — only `gh` CLI.

```
GitHub Issue (#N, label: requirements, approved)
    → Implementer: git worktree + implementation
    → gh pr create --label review-needed
    → Reviewer: /dev/review → approved label
    → gh pr merge --squash
    → Orchestrator: pulls main, closes Issue
```

See [examples/github-only-flow.md](examples/github-only-flow.md) for the complete walkthrough.

---

## Core Workflow Commands

| Command | Description |
|---------|-------------|
| `/dev/start-team` | Context check, daily startup, lane assignment |
| `/dev/status` | Visualize team status, blockers, review queue |
| `/dev/orchestrate` | Oversee all agents, make merge/priority decisions |
| `/dev/research` | Technical investigation → findings in GitHub Issue |
| `/dev/define-requirements` | Requirements + test spec → `requirements` Issue |
| `/dev/implement` | Implement from Issue → PR |
| `/dev/review` | Multi-stage ultra-strict review |

---

## Optional PMO Profile

For teams using Notion, Jira, Confluence, Google Calendar, Slack, or Gmail:

```bash
./scripts/bootstrap.sh --init-pmo-config
```

See [docs/pmo-profile.md](docs/pmo-profile.md) for setup instructions.

---

## Configuration

Config files follow a layered priority system:

```
config/*.local.yaml  ← your real values (git-ignored, highest priority)
config/*.yaml        ← public-safe template (tracked, YOUR_* placeholders)
config/*.example.yaml ← copy-source only (not loaded at runtime)
```

After editing local files:

```bash
python3 scripts/validate-config.py --check-local
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/architecture.md](docs/architecture.md) | Mermaid diagrams of agent flow and state machine |
| [docs/customization.md](docs/customization.md) | Adapting the template to your team |
| [docs/faq.md](docs/faq.md) | Frequently asked questions |
| [docs/onboarding.md](docs/onboarding.md) | First-time setup guide |
| [docs/pr-review-flow.md](docs/pr-review-flow.md) | PR review process details |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE)
