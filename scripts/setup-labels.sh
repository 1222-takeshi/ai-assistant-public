#!/usr/bin/env bash
# ai-assistant: 開発 workflow に必要な GitHub Labels を作成する。
# 使用例: ./scripts/setup-labels.sh
#         GH_REPO=owner/repo ./scripts/setup-labels.sh
# 前提: gh が認証済みであること。

set -euo pipefail

resolve_repo() {
  if [ -n "${GH_REPO:-}" ]; then
    printf '%s\n' "$GH_REPO"
    return 0
  fi
  repo="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
  if [ -n "$repo" ]; then
    printf '%s\n' "$repo"
    return 0
  fi
  echo "Error: repository could not be resolved. Set GH_REPO or run inside a git repo." >&2
  exit 1
}

REPO="$(resolve_repo)"
echo "Setting up labels for: $REPO"

create_label() {
  local name="$1" color="$2" description="$3"
  if gh label list --repo "$REPO" --json name -q '.[].name' 2>/dev/null | grep -qx "$name"; then
    echo "  [skip] label already exists: $name"
  else
    gh label create "$name" \
      --repo "$REPO" \
      --color "$color" \
      --description "$description" 2>/dev/null
    echo "  [created] $name"
  fi
}

echo "Creating workflow labels..."
create_label "research"         "0075ca" "Researcher が成果物を記録する調査 Issue"
create_label "requirements"     "e4e669" "Requirements Analyst が管理する要件 Issue"
create_label "implementation"   "d876e3" "Implementer 向けの実装依頼 Issue"
create_label "review-needed"    "f9d0c4" "Reviewer の確認待ち"
create_label "approved"         "0e8a16" "Reviewer の承認済み"
create_label "blocked"          "b60205" "Orchestrator が優先的に扱うブロッカー"

echo "Done. Labels are ready for: $REPO"
