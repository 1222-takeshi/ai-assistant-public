"""Bootstrap and doctor onboarding tests."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
BOOTSTRAP = REPO_ROOT / "scripts" / "bootstrap.sh"
DOCTOR = REPO_ROOT / "scripts" / "doctor.py"
VALIDATOR = REPO_ROOT / "scripts" / "validate-config.py"


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def build_minimal_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    (repo_root / "scripts").mkdir(parents=True)
    (repo_root / "config").mkdir(parents=True)

    for path in (
        BOOTSTRAP,
        DOCTOR,
        VALIDATOR,
        REPO_ROOT / "config" / "notion.yaml",
        REPO_ROOT / "config" / "notion.example.yaml",
        REPO_ROOT / "config" / "confluence.yaml",
        REPO_ROOT / "config" / "confluence.example.yaml",
        REPO_ROOT / "README.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "requirements-dev.txt",
    ):
        relative = path.relative_to(REPO_ROOT)
        copy_file(path, repo_root / relative)
    return repo_root


def make_stub_command(bin_dir: Path, name: str, body: str) -> None:
    path = bin_dir / name
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)


def run_doctor(repo_root: Path, path_env: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if path_env is not None:
        env["PATH"] = path_env
    return subprocess.run(
        [sys.executable, str(DOCTOR), "--repo-root", str(repo_root)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


class TestBootstrap:
    def test_bootstrap_is_non_destructive_for_existing_local_configs(self, tmp_path: Path):
        repo_root = build_minimal_repo(tmp_path)
        notion_local = repo_root / "config" / "notion.local.yaml"
        notion_local.write_text("tasks_db_id: keep-me\n", encoding="utf-8")

        result = subprocess.run(
            ["bash", str(BOOTSTRAP), "--init-pmo-config"],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert notion_local.read_text(encoding="utf-8") == "tasks_db_id: keep-me\n"
        assert "[warning] Skip existing file" in result.stdout

    def test_bootstrap_creates_local_configs_only_when_requested(self, tmp_path: Path):
        repo_root = build_minimal_repo(tmp_path)

        result = subprocess.run(
            ["bash", str(BOOTSTRAP), "--init-pmo-config"],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert (repo_root / "config" / "notion.local.yaml").exists()
        assert (repo_root / "config" / "confluence.local.yaml").exists()
        assert "[success] Created local config" in result.stdout


class TestDoctor:
    def test_readme_mentions_bootstrap_and_doctor(self):
        content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        assert "./scripts/bootstrap.sh" in content
        assert "python3 scripts/doctor.py" in content

    def test_doctor_returns_warning_when_optional_local_config_is_missing(self, tmp_path: Path):
        repo_root = build_minimal_repo(tmp_path)
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        make_stub_command(
            bin_dir,
            "gh",
            "#!/usr/bin/env bash\nif [ \"$1\" = \"auth\" ] && [ \"$2\" = \"status\" ]; then exit 0; fi\nexit 0\n",
        )
        path_env = f"{bin_dir}:{os.environ['PATH']}"

        result = run_doctor(repo_root, path_env)

        assert result.returncode == 0
        assert "[warning] local config:" in result.stdout
        assert "Optional PMO profile is not configured" in result.stdout

    def test_doctor_fails_when_gh_auth_is_not_ready(self, tmp_path: Path):
        repo_root = build_minimal_repo(tmp_path)
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        make_stub_command(
            bin_dir,
            "gh",
            "#!/usr/bin/env bash\nif [ \"$1\" = \"auth\" ] && [ \"$2\" = \"status\" ]; then exit 1; fi\nexit 0\n",
        )
        path_env = f"{bin_dir}:{os.environ['PATH']}"

        result = run_doctor(repo_root, path_env)

        assert result.returncode != 0
        assert "[failure] gh auth:" in result.stdout
        assert "gh auth login" in result.stdout

    def test_doctor_fails_when_local_config_validation_fails(self, tmp_path: Path):
        repo_root = build_minimal_repo(tmp_path)
        (repo_root / "config" / "notion.local.yaml").write_text(
            "tasks_db_id: YOUR_TASKS_DB_ID\nweekly_pages:\n  root_page_id: YOUR_WEEKLY_ROOT_PAGE_ID\n",
            encoding="utf-8",
        )
        (repo_root / "config" / "confluence.local.yaml").write_text(
            "atlassian_domain: YOUR_ATLASSIAN_DOMAIN\ndefault_space_key: YOUR_SPACE_KEY\nparent_pages:\n  pmo_docs: YOUR_PMO_DOCS_PAGE_ID\n",
            encoding="utf-8",
        )
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        make_stub_command(
            bin_dir,
            "gh",
            "#!/usr/bin/env bash\nif [ \"$1\" = \"auth\" ] && [ \"$2\" = \"status\" ]; then exit 0; fi\nexit 0\n",
        )
        path_env = f"{bin_dir}:{os.environ['PATH']}"

        result = run_doctor(repo_root, path_env)

        assert result.returncode != 0
        assert "[failure] local config:" in result.stdout
        assert "Fix the reported files" in result.stdout
