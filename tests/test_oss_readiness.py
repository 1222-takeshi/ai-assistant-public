"""OSS 公開向けの公開安全性テスト。"""

from pathlib import Path
import re

import yaml


REPO_ROOT = Path(__file__).parent.parent
README_MD = REPO_ROOT / "README.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
LICENSE = REPO_ROOT / "LICENSE"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
CODE_OF_CONDUCT = REPO_ROOT / "CODE_OF_CONDUCT.md"
SECURITY = REPO_ROOT / "SECURITY.md"
REQUIREMENTS_DEV = REPO_ROOT / "requirements-dev.txt"
GH_WORKFLOW = REPO_ROOT / "scripts" / "gh-workflow.sh"
NOTION_YAML = REPO_ROOT / "config" / "notion.yaml"
CONFLUENCE_YAML = REPO_ROOT / "config" / "confluence.yaml"
NOTION_EXAMPLE = REPO_ROOT / "config" / "notion.example.yaml"
CONFLUENCE_EXAMPLE = REPO_ROOT / "config" / "confluence.example.yaml"

UUID_PATTERN = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
LONG_NUMERIC_ID_PATTERN = re.compile(r"\b\d{8,}\b")
ATLASSIAN_DOMAIN_PATTERN = re.compile(r"\b(?!YOUR_ATLASSIAN_DOMAIN\b)[A-Za-z0-9-]+\.atlassian\.net\b")
LOCAL_WORKSPACE_PATH_PATTERN = re.compile(r"/(?:mnt|Users)/[^\\s]+/workspace/ai-assistant")
HARDCODED_REPO_ASSIGNMENT_PATTERN = re.compile(r'^\s*REPO="[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"', re.MULTILINE)
HARDCODED_GH_REPO_FLAG_PATTERN = re.compile(r"--repo\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
CONCRETE_GITHUB_REMOTE_PATTERN = re.compile(
    r"(?:git@github\.com:|https://github\.com/)[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?"
)


def public_text_files() -> list[Path]:
    files = [
        README_MD,
        CLAUDE_MD,
        GH_WORKFLOW,
        NOTION_YAML,
        CONFLUENCE_YAML,
        NOTION_EXAMPLE,
        CONFLUENCE_EXAMPLE,
        REPO_ROOT / ".claude" / "team-topology.yaml",
    ]
    files.extend(sorted((REPO_ROOT / ".claude" / "commands").rglob("*.md")))
    return files


def numeric_id_sensitive_files() -> list[Path]:
    """長い数値 ID を検査する対象。

    PMO コマンドの説明文には Confluence の URL 例として 9 桁程度の数値が含まれるため、
    そこは検査対象から外す。
    """

    return [
        README_MD,
        CLAUDE_MD,
        GH_WORKFLOW,
        NOTION_YAML,
        CONFLUENCE_YAML,
        NOTION_EXAMPLE,
        CONFLUENCE_EXAMPLE,
        REPO_ROOT / ".claude" / "team-topology.yaml",
    ]


class TestOssMetadata:
    def test_required_public_docs_exist(self):
        for path in (README_MD, CLAUDE_MD, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY):
            assert path.exists(), f"{path.name} が存在しません"

    def test_requirements_dev_exists(self):
        assert REQUIREMENTS_DEV.exists(), "requirements-dev.txt が存在しません"

    def test_example_configs_exist(self):
        assert NOTION_EXAMPLE.exists()
        assert CONFLUENCE_EXAMPLE.exists()

    def test_readme_mentions_oss_docs(self):
        content = README_MD.read_text(encoding="utf-8")
        assert "MIT" in content
        assert "CONTRIBUTING.md" in content
        assert "SECURITY.md" in content


class TestNoInternalIdentifiersInPublicFiles:
    def test_no_uuid_like_identifiers(self):
        for path in public_text_files():
            content = path.read_text(encoding="utf-8")
            assert not UUID_PATTERN.search(content), f"{path} に UUID 形式の実 ID が残っています"

    def test_no_long_numeric_identifiers(self):
        for path in numeric_id_sensitive_files():
            content = path.read_text(encoding="utf-8")
            assert not LONG_NUMERIC_ID_PATTERN.search(content), f"{path} に長い数値 ID が残っています"

    def test_no_internal_atlassian_domain(self):
        for path in public_text_files():
            content = path.read_text(encoding="utf-8")
            assert not ATLASSIAN_DOMAIN_PATTERN.search(content), f"{path} に具体的な Atlassian ドメインが残っています"

    def test_no_local_workspace_path(self):
        for path in public_text_files():
            content = path.read_text(encoding="utf-8")
            assert not LOCAL_WORKSPACE_PATH_PATTERN.search(content), f"{path} にローカル絶対パスが残っています"

    def test_no_hardcoded_repo_assignment(self):
        content = GH_WORKFLOW.read_text(encoding="utf-8")
        assert not HARDCODED_REPO_ASSIGNMENT_PATTERN.search(content), "scripts/gh-workflow.sh に固定 repo 代入が残っています"

    def test_no_hardcoded_repo_flag(self):
        for path in public_text_files():
            content = path.read_text(encoding="utf-8")
            assert not HARDCODED_GH_REPO_FLAG_PATTERN.search(content), f"{path} に固定 --repo 指定が残っています"

    def test_no_concrete_github_remote(self):
        for path in public_text_files():
            content = path.read_text(encoding="utf-8")
            assert not CONCRETE_GITHUB_REMOTE_PATTERN.search(content), f"{path} に具体的な GitHub remote が残っています"


class TestPublicSafeConfigTemplates:
    def test_notion_ids_are_placeholders(self):
        config = yaml.safe_load(NOTION_YAML.read_text(encoding="utf-8"))
        assert config["tasks_db_id"].startswith("YOUR_")
        assert config["weekly_pages"]["root_page_id"].startswith("YOUR_")

    def test_confluence_ids_are_placeholders(self):
        config = yaml.safe_load(CONFLUENCE_YAML.read_text(encoding="utf-8"))
        assert config["atlassian_domain"].startswith("YOUR_")
        assert config["default_space_key"].startswith("YOUR_")
        assert config["parent_pages"]["pmo_docs"].startswith("YOUR_")
        assert config["meeting_minutes_map"][0]["parent_id"].startswith("YOUR_")


class TestDynamicRepoResolution:
    def test_gh_workflow_uses_dynamic_repo_resolution(self):
        content = GH_WORKFLOW.read_text(encoding="utf-8")
        assert "GH_REPO" in content
        assert "resolve_repo" in content
        assert "git remote get-url origin" in content
