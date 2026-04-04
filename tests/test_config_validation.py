"""Config layering and validation tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).parent.parent
README_MD = REPO_ROOT / "README.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
CONTRIBUTING_MD = REPO_ROOT / "CONTRIBUTING.md"
GITIGNORE = REPO_ROOT / ".gitignore"
VALIDATOR = REPO_ROOT / "scripts" / "validate-config.py"


def copy_public_configs(target_root: Path) -> None:
    (target_root / "config").mkdir(parents=True, exist_ok=True)
    for name in (
        "notion.yaml",
        "notion.example.yaml",
        "confluence.yaml",
        "confluence.example.yaml",
    ):
        shutil.copy2(REPO_ROOT / "config" / name, target_root / "config" / name)


def run_validator(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


class TestConfigDocumentation:
    def test_gitignore_ignores_local_config_glob(self):
        content = GITIGNORE.read_text(encoding="utf-8")
        assert "config/*.local.yaml" in content

    def test_docs_define_roles_and_precedence(self):
        for path in (README_MD, CLAUDE_MD, CONTRIBUTING_MD):
            content = path.read_text(encoding="utf-8")
            assert "config/*.yaml" in content
            assert "config/*.example.yaml" in content
            assert "config/*.local.yaml" in content
            assert "local > tracked template" in content

    def test_readme_mentions_validation_commands(self):
        content = README_MD.read_text(encoding="utf-8")
        assert "python3 scripts/validate-config.py --tracked-only" in content
        assert "python3 scripts/validate-config.py --check-local" in content


class TestConfigValidator:
    def test_tracked_only_validation_passes_for_public_templates(self, tmp_path: Path):
        copy_public_configs(tmp_path)

        result = run_validator(tmp_path, "--tracked-only")

        assert result.returncode == 0
        assert "Config validation passed" in result.stdout

    def test_tracked_only_validation_fails_when_tracked_template_contains_concrete_value(self, tmp_path: Path):
        copy_public_configs(tmp_path)
        notion_path = tmp_path / "config" / "notion.yaml"
        notion = yaml.safe_load(notion_path.read_text(encoding="utf-8"))
        notion["tasks_db_id"] = "abcd1234efgh5678ijkl9012mnop3456"
        write_yaml(notion_path, notion)

        result = run_validator(tmp_path, "--tracked-only")

        assert result.returncode != 0
        assert "must stay as a YOUR_* placeholder" in result.stderr
        assert "config/notion.local.yaml" in result.stderr

    def test_check_local_fails_when_local_files_are_missing(self, tmp_path: Path):
        copy_public_configs(tmp_path)

        result = run_validator(tmp_path, "--check-local")

        assert result.returncode != 0
        assert "config/notion.local.yaml" in result.stderr
        assert "config/confluence.local.yaml" in result.stderr

    def test_check_local_fails_when_placeholder_values_remain(self, tmp_path: Path):
        copy_public_configs(tmp_path)
        write_yaml(
            tmp_path / "config" / "notion.local.yaml",
            {
                "tasks_db_id": "YOUR_TASKS_DB_ID",
                "weekly_pages": {"root_page_id": "YOUR_WEEKLY_ROOT_PAGE_ID"},
            },
        )
        write_yaml(
            tmp_path / "config" / "confluence.local.yaml",
            {
                "atlassian_domain": "YOUR_ATLASSIAN_DOMAIN",
                "default_space_key": "YOUR_SPACE_KEY",
                "spaces": [{"key": "YOUR_SPACE_KEY"}],
                "parent_pages": {"pmo_docs": "YOUR_PMO_DOCS_PAGE_ID"},
                "meeting_minutes_map": [
                    {
                        "parent_id": "YOUR_TEAM_MEETING_PARENT_PAGE_ID",
                        "space_key": "YOUR_SPACE_KEY",
                        "copy_from": "YOUR_TEMPLATE_PAGE_ID",
                    },
                    {
                        "parent_id": "YOUR_PMO_DOCS_PAGE_ID",
                        "space_key": "YOUR_SPACE_KEY",
                    },
                ],
            },
        )

        result = run_validator(tmp_path, "--check-local")

        assert result.returncode != 0
        assert "still a placeholder" in result.stderr
        assert "Replace YOUR_*" in result.stderr

    def test_check_local_passes_with_concrete_overrides(self, tmp_path: Path):
        copy_public_configs(tmp_path)
        write_yaml(
            tmp_path / "config" / "notion.local.yaml",
            {
                "tasks_db_id": "abcd1234efgh5678ijkl9012mnop3456",
                "weekly_pages": {"root_page_id": "qrst1234uvwx5678yzab9012cdef3456"},
            },
        )
        write_yaml(
            tmp_path / "config" / "confluence.local.yaml",
            {
                "atlassian_domain": "example-team.atlassian.net",
                "default_space_key": "TEAM",
                "spaces": [{"key": "TEAM"}],
                "parent_pages": {"pmo_docs": "12345678"},
                "meeting_minutes_map": [
                    {
                        "parent_id": "23456789",
                        "space_key": "TEAM",
                        "copy_from": "34567890",
                    },
                    {
                        "parent_id": "12345678",
                        "space_key": "TEAM",
                    },
                ],
            },
        )

        result = run_validator(tmp_path, "--check-local")

        assert result.returncode == 0
        assert "Config validation passed" in result.stdout

    def test_tracked_only_fails_with_invalid_yaml(self, tmp_path: Path):
        copy_public_configs(tmp_path)
        notion_path = tmp_path / "config" / "notion.yaml"
        notion_path.write_text("tasks_db_id: [broken\n", encoding="utf-8")

        result = run_validator(tmp_path, "--tracked-only")

        assert result.returncode != 0
        assert "contains invalid YAML" in result.stderr
