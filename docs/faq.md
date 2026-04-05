# FAQ

Frequently asked questions about **ai-assistant**.

---

## General

### Q: What is ai-assistant?

A template for running a multi-agent AI development team using Claude Code, GitHub Copilot coding agent, or Codex.
It defines roles (Orchestrator, Researcher, Requirements Analyst, Implementer, Reviewer), workflow commands, and conventions so agents can collaborate autonomously on GitHub-hosted projects.

### Q: Do I need all the agents running at once?

No. You can start with just one agent acting as the Orchestrator and pick up other roles as needed.
The commands (`/dev/implement`, `/dev/review`, etc.) are prompts you can run in any Claude Code session.

### Q: Is this only for Claude Code?

No. The core workflow is designed for any LLM-backed coding agent that can run shell commands and call the `gh` CLI.
`AGENTS.md` is written in plain English for Codex and GitHub Copilot coding agent compatibility.
`.github/copilot-setup-steps.yml` bootstraps the environment specifically for GitHub Copilot.

---

## Setup

### Q: What do I need before running `bootstrap.sh`?

- Python 3.9+ (3.11 recommended)
- `git` and `gh` CLI authenticated to your GitHub account
- A GitHub repository (public or private)

Run `python3 scripts/doctor.py` to check your environment before starting.

### Q: How do I set up the workflow labels in my repository?

```bash
./scripts/setup-labels.sh
# or with a specific repo:
GH_REPO=your-org/your-repo ./scripts/setup-labels.sh
```

This creates 6 labels: `research`, `requirements`, `implementation`, `review-needed`, `approved`, `blocked`.
The script is idempotent — safe to run multiple times.

### Q: The `doctor.py` reports a warning. Should I fix it?

Warnings indicate optional features that are not configured (e.g., PMO profile MCPs).
Core workflow (`dev/`) works fine with `success=6 warning=N failure=0`.
Fix warnings only if you intend to use the corresponding feature.

---

## Workflow

### Q: What is the difference between `review-needed` and GitHub's formal APPROVED review?

`review-needed` / `approved` are **workflow labels** managed by the agent team.
They are not the same as a GitHub pull request review status.
This distinction is intentional: label-based state management works without requiring specific GitHub user permissions.

### Q: Why does the Reviewer close PRs immediately on NG?

Fix-loops produce incremental patches on a flawed baseline, which accumulates technical debt.
Closing immediately and requiring a fresh branch forces the Implementer to revisit the problem from a clean state.
This is the "ultra-strict" policy and is intentional.

### Q: Can I reopen a closed PR?

No. The reviewer policy explicitly prohibits reopening closed PRs.
If the NG was a mistake, the Implementer creates a new branch and new PR from scratch.

### Q: How do I run two Implementers in parallel?

```bash
# Implementer 1
./scripts/setup-worktree.sh impl-1 feat/feature-a

# Implementer 2
./scripts/setup-worktree.sh impl-2 feat/feature-b
```

Each agent works in its own directory and branch independently.

---

## Configuration

### Q: Why does `validate-config.py` fail with "local override missing"?

If you run `--check-local`, the script expects `config/*.local.yaml` files to exist with real values.
If you haven't set up the PMO profile, this is expected.
Use `--tracked-only` for core workflow validation:

```bash
python3 scripts/validate-config.py --tracked-only
```

### Q: Where should I put real API keys and credentials?

In `config/*.local.yaml` files, which are git-ignored.
**Never** put real credentials in tracked `config/*.yaml` files.
The tracked files use `YOUR_*` placeholders as a reminder.

### Q: What is the difference between `config/*.yaml`, `config/*.example.yaml`, and `config/*.local.yaml`?

| File | Purpose | Git tracked | Loaded at runtime |
|------|---------|-------------|------------------|
| `config/*.yaml` | Public-safe template with `YOUR_*` placeholders | ✅ | ✅ (lowest priority) |
| `config/*.example.yaml` | Copy-source for new local files | ✅ | ❌ |
| `config/*.local.yaml` | Real values for your environment | ❌ | ✅ (highest priority) |

---

## Public / OSS

### Q: Is it safe to fork this repo and make it public?

Yes, if you follow the config layering rules (real values in `*.local.yaml`, never in tracked files).
Run `detect-secrets scan` and `python3 scripts/validate-config.py --tracked-only` before publishing.

### Q: How do I sync changes from a private fork to a public mirror?

Use `git format-patch` to create patches, sanitize with `sed` replacements (see `.tmp/public-release-replacements.txt` as a template), then apply with `git am` in the public checkout.
See [docs/public-release-checklist.md](public-release-checklist.md) for the full procedure.

---

## Related Documents

- [docs/architecture.md](architecture.md) — System overview
- [docs/customization.md](customization.md) — How to adapt the template
- [docs/onboarding.md](onboarding.md) — First-time setup
- [docs/pr-review-flow.md](pr-review-flow.md) — PR review process
