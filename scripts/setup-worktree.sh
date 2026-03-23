#!/usr/bin/env bash
# ai-assistant: worktree を .claude/worktrees/ に追加する。
# 使用例: ./scripts/setup-worktree.sh impl-1 feat/my-feature
# 前提: リポジトリルートで実行し、main が最新であること。

set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

"${REPO_ROOT}/scripts/worktree-cleanup.sh"

if [ -n "$1" ] && [ -n "$2" ]; then
  WT_NAME="$1"
  BRANCH="$2"
else
  echo "Usage: $0 <worktree-name> <branch>" >&2
  echo "  worktree-name: impl-1, impl-2, req-1, research-1 など" >&2
  echo "  branch: feat/xxx, fix/xxx, research/xxx など" >&2
  echo "Example: $0 impl-1 feat/add-feature" >&2
  exit 1
fi

WT_DIR="${REPO_ROOT}/.claude/worktrees/${WT_NAME}"
mkdir -p "$(dirname "$WT_DIR")"

if [ -e "$WT_DIR" ]; then
  echo "Error: worktree directory already exists: $WT_DIR" >&2
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  echo "Error: branch already exists locally: $BRANCH" >&2
  exit 1
fi

git fetch origin main
git worktree add "$WT_DIR" -b "$BRANCH" origin/main
echo "Created worktree: $WT_DIR (branch: $BRANCH)"
echo "  cd $WT_DIR"
