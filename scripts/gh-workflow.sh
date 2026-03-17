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
REPO="YOUR_ORG/YOUR_REPO"

usage() {
  cat >&2 << 'EOF'
Usage:
  gh-workflow.sh push -b <branch>
  gh-workflow.sh pr   --title <title> --body-file <file> [--label <label>]
  gh-workflow.sh issue --title <title> --body-file <file> [--label <label>]
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
    TITLE=""
    BODY_FILE=""
    LABEL=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
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
    TITLE=""
    BODY_FILE=""
    LABEL=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
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
