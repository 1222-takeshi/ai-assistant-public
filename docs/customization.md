# Customization Guide

This guide explains how to adapt **ai-assistant** to your own team's workflow.

## 1. Rename Agent Roles

Edit `.claude/team-topology.yaml` to match your team structure.
Each role entry controls the lane name, worktree path, and handoff rules.

```yaml
# Example: rename "impl-1" lane to "frontend"
lanes:
  - id: frontend
    role: implementer
    worktree: .claude/worktrees/frontend
    branch_prefix: feat/
```

You do not need to change the command files — they reference roles generically.

## 2. Add or Remove Workflow Labels

`scripts/setup-labels.sh` creates 6 default labels.
To add your own, append entries to the script:

```bash
# In scripts/setup-labels.sh, add inside the labels loop:
create_label "in-review"       "0052cc" "Currently under peer review"
create_label "needs-design"    "e4e669" "Requires design decision before implementation"
```

Run after editing:

```bash
./scripts/setup-labels.sh
```

## 3. Change the Reviewer Strictness

The reviewer policy is defined in `.claude/commands/dev/review.md`.

Default thresholds:
- 🔴 required ≥ 1 → NG (PR closed immediately)
- 🟡 recommended ≥ 3 → NG

To relax the policy, edit the threshold section near the top of that file.
For example, to allow up to 1 🟡 finding:

```markdown
| 🟡 recommended | ≥ 4 | NG |
```

> **Caution**: Lowering strictness increases the risk of low-quality PRs accumulating.

## 4. Use a Different Branch Naming Convention

`scripts/setup-worktree.sh` defaults to the branch name you specify.
The convention `feat/<feature-name>` is a recommendation, not a hard requirement.
Change the prefix in `team-topology.yaml`:

```yaml
branch_prefix: "fix/"    # or "chore/", "task/", etc.
```

## 5. Add PMO Profile Commands

The PMO profile is opt-in. To activate:

1. Install required MCPs (Notion, Atlassian, GCal, Slack, Gmail).
2. Copy config templates:
   ```bash
   ./scripts/bootstrap.sh --init-pmo-config
   ```
3. Edit `config/notion.local.yaml` and `config/confluence.local.yaml` with your real values.
4. Verify:
   ```bash
   python3 scripts/validate-config.py --check-local
   ```
5. Dry-run:
   ```bash
   /pmo/run-tasks --dry-run
   ```

See [docs/pmo-profile.md](pmo-profile.md) for full details.

## 6. Adjust config Layering

The config system follows this priority order:

```
config/*.local.yaml  (highest, git-ignored)
    ↓
config/*.yaml        (tracked template, public-safe)
    ↓
config/*.example.yaml (copy-source only, not loaded at runtime)
```

To add a new config key:

1. Add it with a `YOUR_*` placeholder to the tracked `config/*.yaml`.
2. Add the real value to `config/*.local.yaml`.
3. Update `scripts/validate-config.py` if structural validation is needed.

## 7. Scale to More Implementers

Add more lanes in `team-topology.yaml` and create corresponding worktrees:

```bash
./scripts/setup-worktree.sh impl-3 feat/my-feature-c
./scripts/setup-worktree.sh impl-4 feat/my-feature-d
```

There is no hard limit on the number of concurrent worktrees.

## 8. Integrate with CI

`.github/copilot-setup-steps.yml` bootstraps the environment for GitHub Copilot coding agents.
For standard CI (GitHub Actions), the existing `.github/workflows/test.yml` runs `pytest` on every push and PR.

To add lint or type-check steps, extend `test.yml`:

```yaml
- name: Lint
  run: pip install ruff && ruff check .
```

## Related Documents

- [docs/architecture.md](architecture.md) — System overview and agent flow diagrams
- [docs/onboarding.md](onboarding.md) — First-time setup
- [docs/faq.md](faq.md) — Common questions
