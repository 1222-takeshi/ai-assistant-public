#!/usr/bin/env bash
# ai-assistant: worktree のメタデータを整理し、残骸を見つけやすくする。

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

WORKTREE_ROOT="${REPO_ROOT}/.claude/worktrees"

echo "[worktree-cleanup] pruning stale git worktree metadata"
git worktree prune

echo "[worktree-cleanup] registered worktrees"
git worktree list

if [ ! -d "$WORKTREE_ROOT" ]; then
  exit 0
fi

registered_worktrees="$(git worktree list --porcelain | awk '/^worktree / {print $2}')"

while IFS= read -r directory; do
  [ -z "$directory" ] && continue

  if ! printf '%s\n' "$registered_worktrees" | grep -Fxq "$directory"; then
    echo "[worktree-cleanup] warning: unregistered directory remains: $directory"
    echo "[worktree-cleanup] remove it manually if no longer needed"
  fi
done <<EOF
$(find "$WORKTREE_ROOT" -mindepth 1 -maxdepth 1 -type d | sort)
EOF
