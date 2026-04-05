"""Claude Code 開発チーム運用ファイルのテストスイート。

対象:
- .claude/team-topology.yaml
- .claude/commands/dev/start-team.md
- .claude/commands/dev/status.md
- scripts/worktree-cleanup.sh
- scripts/setup-worktree.sh
- CLAUDE.md / README.md
"""

from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent
TEAM_TOPOLOGY = REPO_ROOT / ".claude" / "team-topology.yaml"
DEV_COMMANDS_DIR = REPO_ROOT / ".claude" / "commands" / "dev"
START_TEAM_COMMAND = DEV_COMMANDS_DIR / "start-team.md"
STATUS_COMMAND = DEV_COMMANDS_DIR / "status.md"
WORKTREE_CLEANUP = REPO_ROOT / "scripts" / "worktree-cleanup.sh"
WORKTREE_SETUP = REPO_ROOT / "scripts" / "setup-worktree.sh"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
README_MD = REPO_ROOT / "README.md"
PMO_PROFILE_DOC = REPO_ROOT / "docs" / "pmo-profile.md"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


class TestTeamTopologyFile:
    def test_file_exists(self):
        assert TEAM_TOPOLOGY.exists(), ".claude/team-topology.yaml が存在しません"

    def test_file_is_valid_yaml(self):
        data = load_yaml(TEAM_TOPOLOGY)
        assert isinstance(data, dict), "team-topology.yaml が dict として読めません"

    def test_required_top_level_keys_exist(self):
        data = load_yaml(TEAM_TOPOLOGY)
        required = {"team", "roles", "labels", "worktrees", "handoffs"}
        assert required.issubset(data), f"必須キー不足: {required - set(data)}"

    def test_team_topology_declares_core_boundary(self):
        data = load_yaml(TEAM_TOPOLOGY)
        boundary = data["team"]["product_boundary"]
        assert boundary["core"] == "dev workflow"
        assert "pmo" in boundary["optional_profiles"]


class TestTeamTopologyRoles:
    REQUIRED_ROLE_IDS = {
        "orchestrator",
        "requirements-analyst",
        "reviewer",
        "researcher-1",
        "researcher-2",
        "implementer-1",
        "implementer-2",
    }

    @pytest.fixture(scope="class")
    def roles(self):
        return load_yaml(TEAM_TOPOLOGY)["roles"]

    def test_required_roles_exist(self, roles):
        assert self.REQUIRED_ROLE_IDS.issubset(roles), \
            f"不足ロール: {self.REQUIRED_ROLE_IDS - set(roles)}"

    @pytest.mark.parametrize("role_id", sorted(REQUIRED_ROLE_IDS))
    def test_role_has_command(self, roles, role_id):
        assert roles[role_id]["command"].startswith("/dev/"), \
            f"{role_id} の command が /dev/ で始まっていません"

    @pytest.mark.parametrize("role_id", sorted(REQUIRED_ROLE_IDS))
    def test_role_has_capacity(self, roles, role_id):
        assert roles[role_id]["capacity"] >= 1

    @pytest.mark.parametrize("role_id", sorted(REQUIRED_ROLE_IDS))
    def test_role_has_summary(self, roles, role_id):
        summary = roles[role_id]["summary"]
        assert isinstance(summary, str) and summary.strip() != ""


class TestTeamTopologyHandoffs:
    REQUIRED_PATHS = {
        ("orchestrator", "requirements-analyst"),
        ("orchestrator", "researcher-1"),
        ("orchestrator", "researcher-2"),
        ("requirements-analyst", "reviewer"),
        ("reviewer", "orchestrator"),
        ("requirements-analyst", "implementer-1"),
        ("requirements-analyst", "implementer-2"),
        ("implementer-1", "reviewer"),
        ("implementer-2", "reviewer"),
    }

    @pytest.fixture(scope="class")
    def handoffs(self):
        return load_yaml(TEAM_TOPOLOGY)["handoffs"]

    def test_handoffs_are_non_empty_list(self, handoffs):
        assert isinstance(handoffs, list) and len(handoffs) > 0

    def test_required_paths_exist(self, handoffs):
        actual = {(item["from"], item["to"]) for item in handoffs}
        assert self.REQUIRED_PATHS.issubset(actual), \
            f"不足ハンドオフ: {self.REQUIRED_PATHS - actual}"

    def test_handoffs_have_trigger_and_artifact(self, handoffs):
        for handoff in handoffs:
            assert isinstance(handoff["trigger"], str) and handoff["trigger"].strip() != ""
            assert isinstance(handoff["artifact"], str) and handoff["artifact"].strip() != ""


class TestTeamCommands:
    @pytest.mark.parametrize("path", [START_TEAM_COMMAND, STATUS_COMMAND])
    def test_command_exists(self, path):
        assert path.exists(), f"{path.name} が存在しません"

    @pytest.mark.parametrize("path", [START_TEAM_COMMAND, STATUS_COMMAND])
    def test_command_starts_with_h1(self, path):
        assert path.read_text(encoding="utf-8").lstrip().startswith("# "), \
            f"{path.name} は H1 で始まる必要があります"

    @pytest.mark.parametrize("path", [START_TEAM_COMMAND, STATUS_COMMAND])
    def test_command_is_not_too_short(self, path):
        assert len(path.read_text(encoding="utf-8")) >= 500, \
            f"{path.name} の内容が短すぎます"


class TestStartTeamCommand:
    @pytest.fixture(scope="class")
    def content(self):
        return START_TEAM_COMMAND.read_text(encoding="utf-8")

    def test_mentions_claude_context(self, content):
        assert "CLAUDE.md" in content

    def test_mentions_team_topology(self, content):
        assert "team-topology.yaml" in content

    def test_mentions_status_command(self, content):
        assert "/dev/status" in content

    def test_mentions_github_issue_and_pr_checks(self, content):
        assert "gh issue list" in content
        assert "gh pr list" in content

    def test_mentions_role_assignment(self, content):
        assert "Researcher" in content
        assert "Requirements Analyst" in content
        assert "Reviewer" in content
        assert "Implementer" in content

    def test_mentions_blocker_handling(self, content):
        assert "blocked" in content
        assert "approved" in content


class TestStatusCommand:
    @pytest.fixture(scope="class")
    def content(self):
        return STATUS_COMMAND.read_text(encoding="utf-8")

    def test_mentions_team_topology(self, content):
        assert "team-topology.yaml" in content

    def test_mentions_worktrees(self, content):
        assert "git worktree list" in content

    def test_mentions_github_queries(self, content):
        assert "gh issue list" in content
        assert "gh pr list" in content

    def test_mentions_dashboard_sections(self, content):
        assert "Researcher" in content
        assert "Requirements Analyst" in content
        assert "Implementer" in content
        assert "Reviewer" in content
        assert "ブロッカー" in content


class TestWorktreeScripts:
    def test_cleanup_script_exists(self):
        assert WORKTREE_CLEANUP.exists(), "scripts/worktree-cleanup.sh が存在しません"

    def test_cleanup_script_mentions_prune(self):
        content = WORKTREE_CLEANUP.read_text(encoding="utf-8")
        assert "git worktree prune" in content

    def test_cleanup_script_mentions_list(self):
        content = WORKTREE_CLEANUP.read_text(encoding="utf-8")
        assert "git worktree list" in content

    def test_setup_script_calls_cleanup(self):
        content = WORKTREE_SETUP.read_text(encoding="utf-8")
        assert "worktree-cleanup.sh" in content


class TestDocumentation:
    def test_claude_md_mentions_new_team_files(self):
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert "/dev/start-team" in content
        assert "/dev/status" in content
        assert ".claude/team-topology.yaml" in content

    def test_readme_mentions_new_team_files(self):
        content = README_MD.read_text(encoding="utf-8")
        # README must mention both the examples catalog and at least one specific team example
        assert "team-catalog" in content
        assert "examples/dev-workflow" in content

    def test_readme_separates_core_and_optional(self):
        content = README_MD.read_text(encoding="utf-8")
        # Framework reposition: "Framework" and "Examples" sections replace old "Core/Optional" split
        assert ("Framework" in content or "Core Workflow" in content)
        assert ("Examples" in content or "Optional PMO Profile" in content)

    def test_claude_separates_core_and_optional(self):
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert "optional profile" in content or "opt-in" in content
        # Either old wording or new framework-oriented wording
        assert ("core は `dev` workflow" in content or "フレームワーク" in content)

    def test_quickstart_does_not_require_pmo(self):
        content = README_MD.read_text(encoding="utf-8")
        quickstart = content.split("## Quickstart", maxsplit=1)[1].split("## Development Team Workflow", maxsplit=1)[0]
        for forbidden in ("Notion MCP", "Atlassian MCP", "Google Calendar MCP", "Slack MCP", "Gmail MCP"):
            assert forbidden not in quickstart

    def test_pmo_profile_doc_exists(self):
        assert PMO_PROFILE_DOC.exists(), "docs/pmo-profile.md が存在しません"

    def test_pmo_profile_doc_is_opt_in(self):
        content = PMO_PROFILE_DOC.read_text(encoding="utf-8")
        assert "optional profile" in content
        assert "core" in content
