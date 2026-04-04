#!/usr/bin/env python3
"""Non-destructive onboarding doctor for OSS users."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SUCCESS = "success"
WARNING = "warning"
FAILURE = "failure"


@dataclass
class CheckResult:
    level: str
    name: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run non-destructive onboarding checks.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root to inspect.",
    )
    return parser.parse_args()


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def check_command_exists(command_name: str, install_hint: str) -> CheckResult:
    if shutil.which(command_name):
        return CheckResult(SUCCESS, command_name, f"`{command_name}` is available.")
    return CheckResult(FAILURE, command_name, f"`{command_name}` is missing. {install_hint}")


def check_gh_auth(repo_root: Path) -> CheckResult:
    if not shutil.which("gh"):
        return CheckResult(FAILURE, "gh auth", "`gh` is missing. Install GitHub CLI first.")

    result = run_command(["gh", "auth", "status"], repo_root)
    if result.returncode == 0:
        return CheckResult(SUCCESS, "gh auth", "`gh auth status` succeeded.")
    return CheckResult(
        FAILURE,
        "gh auth",
        "`gh auth status` failed. Run `gh auth login` before using the GitHub workflow.",
    )


def check_pytest(repo_root: Path) -> CheckResult:
    result = run_command([sys.executable, "-m", "pytest", "--version"], repo_root)
    if result.returncode == 0:
        return CheckResult(SUCCESS, "pytest", "Python test runner is available.")
    return CheckResult(
        FAILURE,
        "pytest",
        "Pytest is not runnable. Install dependencies with `python -m pip install -r requirements-dev.txt`.",
    )


def check_worktree_docs(repo_root: Path) -> CheckResult:
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    claude = (repo_root / "CLAUDE.md").read_text(encoding="utf-8")
    if "git worktree" in readme and "git worktree" in claude:
        return CheckResult(SUCCESS, "worktree docs", "Worktree usage is documented in README and CLAUDE.")
    return CheckResult(
        FAILURE,
        "worktree docs",
        "Worktree usage is not documented consistently. README and CLAUDE should mention `git worktree`.",
    )


def check_validation(repo_root: Path, *extra_args: str) -> CheckResult:
    command = [sys.executable, str(repo_root / "scripts" / "validate-config.py"), *extra_args]
    result = run_command(command, repo_root)
    if result.returncode == 0:
        return CheckResult(SUCCESS, "config validation", "Config validation succeeded.")
    return CheckResult(FAILURE, "config validation", result.stderr.strip() or "Config validation failed.")


def check_local_config(repo_root: Path) -> CheckResult:
    notion_local = repo_root / "config" / "notion.local.yaml"
    confluence_local = repo_root / "config" / "confluence.local.yaml"

    if not notion_local.exists() and not confluence_local.exists():
        return CheckResult(
            WARNING,
            "local config",
            "Optional PMO profile is not configured. Run `./scripts/bootstrap.sh --init-pmo-config` if you need it.",
        )

    validation = check_validation(repo_root, "--check-local")
    if validation.level == SUCCESS:
        return CheckResult(SUCCESS, "local config", "Local PMO config is present and valid.")
    return CheckResult(
        FAILURE,
        "local config",
        "Local PMO config exists but is invalid. "
        "Fix the reported files and rerun `python3 scripts/validate-config.py --check-local`. "
        f"Details: {validation.message}",
    )


def print_result(result: CheckResult) -> None:
    print(f"[{result.level}] {result.name}: {result.message}")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()

    gh_result = check_command_exists("gh", "Install GitHub CLI and ensure it is on PATH.")
    results = [gh_result]
    results.append(check_gh_auth(repo_root) if gh_result.level == SUCCESS else CheckResult(WARNING, "gh auth", "Skipped because `gh` is not installed."))
    results.extend(
        [
            check_command_exists("git", "Install git and ensure it is on PATH."),
            check_pytest(repo_root),
            check_worktree_docs(repo_root),
            check_validation(repo_root, "--tracked-only"),
            check_local_config(repo_root),
        ]
    )

    for result in results:
        print_result(result)

    failures = [result for result in results if result.level == FAILURE]
    warnings = [result for result in results if result.level == WARNING]
    successes = [result for result in results if result.level == SUCCESS]

    print(
        f"Summary: success={len(successes)} warning={len(warnings)} failure={len(failures)}"
    )

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
