#!/usr/bin/env bash
# ai-assistant: non-destructive onboarding bootstrap helper.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INIT_PMO_CONFIG=0

usage() {
  cat <<'EOF'
Usage:
  bootstrap.sh [--init-pmo-config]

Options:
  --init-pmo-config   Copy PMO example config files to *.local.yaml if they do not exist.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --init-pmo-config)
      INIT_PMO_CONFIG=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

copy_if_missing() {
  local source_file="$1"
  local target_file="$2"

  if [[ -f "$target_file" ]]; then
    echo "[warning] Skip existing file: $target_file"
    return 0
  fi

  cp "$source_file" "$target_file"
  echo "[success] Created local config: $target_file"
}

echo "[success] Repository root: $REPO_ROOT"
echo "[success] Install dependencies with: python3 -m pip install -r requirements-dev.txt"
echo "[success] Validate tracked config with: python3 scripts/validate-config.py --tracked-only"
echo "[success] Run doctor with: python3 scripts/doctor.py"

if [[ "$INIT_PMO_CONFIG" -eq 1 ]]; then
  copy_if_missing "$REPO_ROOT/config/notion.example.yaml" "$REPO_ROOT/config/notion.local.yaml"
  copy_if_missing "$REPO_ROOT/config/confluence.example.yaml" "$REPO_ROOT/config/confluence.local.yaml"
else
  echo "[warning] PMO local config was not generated. Re-run with --init-pmo-config if you need the optional PMO profile."
fi
