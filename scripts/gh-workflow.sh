#!/usr/bin/env bash
# ai-assistant: push / PR / Issue 操作の標準化ヘルパー。
#
# 使用例:
#   ./scripts/gh-workflow.sh push -b feat/my-feature
#   ./scripts/gh-workflow.sh pr --title "feat: add X" --body-file .gemini_temp/pr_body.md
#   ./scripts/gh-workflow.sh pr --title "feat: add X" --body-file .gemini_temp/pr_body.md --label "review-needed"
#   ./scripts/gh-workflow.sh issue --title "Bug: something wrong" --body-file .gemini_temp/issue_body.md
#   ./scripts/gh-workflow.sh issue --title "feat: plan" --body-file .gemini_temp/issue_body.md --label "requirements"

set -e

resolve_repo() {
  if [ -n "${GH_REPO:-}" ]; then
    printf '%s\n' "$GH_REPO"
    return 0
  fi

  if command -v gh >/dev/null 2>&1; then
    repo="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
    if [ -n "$repo" ]; then
      printf '%s\n' "$repo"
      return 0
    fi
  fi

  remote_url="$(git remote get-url origin 2>/dev/null || true)"
  if [ -n "$remote_url" ]; then
    repo="$(printf '%s\n' "$remote_url" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
    if [ -n "$repo" ]; then
      printf '%s\n' "$repo"
      return 0
    fi
  fi

  echo "Error: repository could not be resolved. Set GH_REPO or pass --repo." >&2
  exit 1
}

usage() {
  cat >&2 << 'EOF'
Usage:
  gh-workflow.sh push -b <branch>
  gh-workflow.sh pr   [--repo <owner/repo>] --title <title> --body-file <file> [--label <label>]
  gh-workflow.sh issue [--repo <owner/repo>] --title <title> --body-file <file> [--label <label>]
EOF
  exit 1
}

COMMAND="${1:-}"
shift || true

case "$COMMAND" in
  push)
    BRANCH=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        -b|--branch) BRANCH="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; usage ;;
      esac
    done
    if [ -z "$BRANCH" ]; then
      BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    fi
    git push -u origin "$BRANCH"
    ;;

  pr)
    REPO=""
    TITLE=""
    BODY_FILE=""
    LABEL=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --repo)      REPO="$2";      shift 2 ;;
        --title)     TITLE="$2";     shift 2 ;;
        --body-file) BODY_FILE="$2"; shift 2 ;;
        --label)     LABEL="$2";     shift 2 ;;
        *) echo "Unknown option: $1" >&2; usage ;;
      esac
    done
    if [ -z "$TITLE" ] || [ -z "$BODY_FILE" ]; then
      echo "Error: --title and --body-file are required" >&2
      usage
    fi
    if [ -z "$REPO" ]; then
      REPO="$(resolve_repo)"
    fi
    EXTRA_ARGS=()
    if [ -n "$LABEL" ]; then
      EXTRA_ARGS+=(--label "$LABEL")
    fi
    gh pr create \
      --repo "$REPO" \
      --title "$TITLE" \
      --body-file "$BODY_FILE" \
      "${EXTRA_ARGS[@]}"
    ;;

  issue)
    REPO=""
    TITLE=""
    BODY_FILE=""
    LABEL=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --repo)      REPO="$2";      shift 2 ;;
        --title)     TITLE="$2";     shift 2 ;;
        --body-file) BODY_FILE="$2"; shift 2 ;;
        --label)     LABEL="$2";     shift 2 ;;
        *) echo "Unknown option: $1" >&2; usage ;;
      esac
    done
    if [ -z "$TITLE" ] || [ -z "$BODY_FILE" ]; then
      echo "Error: --title and --body-file are required" >&2
      usage
    fi
    if [ -z "$REPO" ]; then
      REPO="$(resolve_repo)"
    fi
    EXTRA_ARGS=()
    if [ -n "$LABEL" ]; then
      EXTRA_ARGS+=(--label "$LABEL")
    fi
    gh issue create \
      --repo "$REPO" \
      --title "$TITLE" \
      --body-file "$BODY_FILE" \
      "${EXTRA_ARGS[@]}"
    ;;

  *)
    usage
    ;;
esac
