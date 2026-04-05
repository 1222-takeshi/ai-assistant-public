"""GitHub-only happy path の静的検証テスト（Issue #14）。

UT-001: examples/github-only-flow.md が存在し、必須ステップを全て含む
UT-002: scripts が repo 固有値なしで実行可能
UT-003: examples/templates/ に全サンプル成果物が揃っている
IT-001: GitHub-only dry-run の再現手順が成立する（構文・依存チェック）
"""

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
TEMPLATES_DIR = EXAMPLES_DIR / "templates"
FLOW_DOC = EXAMPLES_DIR / "github-only-flow.md"
SETUP_WORKTREE = REPO_ROOT / "scripts" / "setup-worktree.sh"
GH_WORKFLOW = REPO_ROOT / "scripts" / "gh-workflow.sh"
README = REPO_ROOT / "README.md"


# ---------------------------------------------------------------------------
# UT-001: フロー文書の存在と必須ステップ
# ---------------------------------------------------------------------------

class TestFlowDocumentExists:
    def test_examples_dir_exists(self):
        assert EXAMPLES_DIR.is_dir(), "examples/ ディレクトリが存在しない"

    def test_flow_doc_exists(self):
        assert FLOW_DOC.is_file(), "examples/github-only-flow.md が存在しない"

    def test_flow_doc_covers_issue_creation(self):
        content = FLOW_DOC.read_text()
        assert "gh issue create" in content, "Issue 作成ステップが記述されていない"

    def test_flow_doc_covers_requirements_review(self):
        content = FLOW_DOC.read_text()
        assert "requirements" in content.lower(), "requirements review ステップが記述されていない"

    def test_flow_doc_covers_worktree_setup(self):
        content = FLOW_DOC.read_text()
        assert "setup-worktree" in content, "worktree セットアップが記述されていない"

    def test_flow_doc_covers_pr_creation(self):
        content = FLOW_DOC.read_text()
        assert "gh pr" in content, "PR 作成ステップが記述されていない"

    def test_flow_doc_covers_review(self):
        content = FLOW_DOC.read_text()
        assert "gh pr review" in content, "review ステップが記述されていない"

    def test_flow_doc_covers_merge(self):
        content = FLOW_DOC.read_text()
        assert "gh pr merge" in content, "merge ステップが記述されていない"

    def test_flow_doc_covers_ng_close(self):
        content = FLOW_DOC.read_text()
        assert "gh pr close" in content, "NG 時の PR Close が記述されていない"

    def test_flow_doc_distinguishes_auto_and_manual(self):
        content = FLOW_DOC.read_text()
        assert "自動化" in content and "手作業" in content, \
            "自動化と手作業の境界が明示されていない"

    def test_flow_doc_has_dry_run_section(self):
        content = FLOW_DOC.read_text()
        assert "dry-run" in content.lower() or "dry_run" in content.lower(), \
            "dry-run / 検証方法が記述されていない"

    def test_flow_doc_has_no_hardcoded_repo(self):
        content = FLOW_DOC.read_text()
        hardcoded = re.search(
            r'--repo\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\s|$)',
            content
        )
        assert not hardcoded, \
            f"flow doc にハードコードされたリポジトリが見つかった: {hardcoded.group() if hardcoded else ''}"


# ---------------------------------------------------------------------------
# UT-002: スクリプトが repo 固有値なしで動作する
# ---------------------------------------------------------------------------

HARDCODED_REPO_PATTERN = re.compile(
    r'^\s*REPO="[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"',
    re.MULTILINE,
)
HARDCODED_REPO_FLAG_PATTERN = re.compile(
    r"--repo\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
)


class TestScriptsHaveNoHardcodedValues:
    def test_gh_workflow_no_hardcoded_repo_assignment(self):
        content = GH_WORKFLOW.read_text()
        match = HARDCODED_REPO_PATTERN.search(content)
        assert not match, f"gh-workflow.sh にハードコードされた REPO 代入がある: {match.group() if match else ''}"

    def test_gh_workflow_no_hardcoded_repo_flag(self):
        content = GH_WORKFLOW.read_text()
        matches = HARDCODED_REPO_FLAG_PATTERN.findall(content)
        assert not matches, f"gh-workflow.sh にハードコードされた --repo フラグがある: {matches}"

    def test_setup_worktree_no_hardcoded_values(self):
        content = SETUP_WORKTREE.read_text()
        assert "1222-takeshi" not in content, \
            "setup-worktree.sh に特定のアカウント名がハードコードされている"
        # コメント行以外に owner/repo 形式の文字列がないことを確認
        non_comment_lines = [
            line for line in content.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        non_comment_text = "\n".join(non_comment_lines)
        hardcoded = re.search(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+-assistant', non_comment_text)
        assert not hardcoded, \
            f"setup-worktree.sh のコメント外にリポジトリ固有値がある: {hardcoded.group() if hardcoded else ''}"

    def test_gh_workflow_syntax(self):
        result = subprocess.run(
            ["bash", "-n", str(GH_WORKFLOW)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, \
            f"gh-workflow.sh に構文エラーがある: {result.stderr}"

    def test_setup_worktree_syntax(self):
        result = subprocess.run(
            ["bash", "-n", str(SETUP_WORKTREE)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, \
            f"setup-worktree.sh に構文エラーがある: {result.stderr}"


# ---------------------------------------------------------------------------
# UT-003: サンプル成果物が揃っている
# ---------------------------------------------------------------------------

REQUIRED_TEMPLATES = [
    "issue-body.md",
    "pr-body.md",
    "review-ok.md",
    "review-ng.md",
]


class TestSampleArtifactsExist:
    def test_templates_dir_exists(self):
        assert TEMPLATES_DIR.is_dir(), "examples/templates/ ディレクトリが存在しない"

    @pytest.mark.parametrize("filename", REQUIRED_TEMPLATES)
    def test_template_file_exists(self, filename):
        f = TEMPLATES_DIR / filename
        assert f.is_file(), f"examples/templates/{filename} が存在しない"

    @pytest.mark.parametrize("filename", REQUIRED_TEMPLATES)
    def test_template_file_not_empty(self, filename):
        f = TEMPLATES_DIR / filename
        content = f.read_text().strip()
        assert len(content) > 50, f"examples/templates/{filename} が短すぎる（空のテンプレートの可能性）"

    def test_review_ng_template_mentions_close(self):
        content = (TEMPLATES_DIR / "review-ng.md").read_text()
        assert "Close" in content, "review-ng.md に Close の指示が含まれていない"

    def test_review_ng_template_forbids_reopen(self):
        content = (TEMPLATES_DIR / "review-ng.md").read_text()
        assert "再オープン" in content or "reopen" in content.lower(), \
            "review-ng.md に再オープン禁止の記述がない"

    def test_review_ok_template_mentions_ok(self):
        content = (TEMPLATES_DIR / "review-ok.md").read_text()
        assert "✅" in content or "OK" in content, "review-ok.md に OK 判定の記述がない"

    def test_pr_body_template_has_checklist(self):
        content = (TEMPLATES_DIR / "pr-body.md").read_text()
        assert "- [ ]" in content, "pr-body.md にチェックリストがない"

    def test_issue_body_template_has_acceptance_criteria(self):
        content = (TEMPLATES_DIR / "issue-body.md").read_text()
        assert "受け入れ条件" in content or "acceptance" in content.lower(), \
            "issue-body.md に受け入れ条件セクションがない"


# ---------------------------------------------------------------------------
# IT-001: README から examples/ への導線確認
# ---------------------------------------------------------------------------

class TestReadmeLinks:
    def test_readme_links_to_flow_doc(self):
        content = README.read_text()
        assert "examples/github-only-flow.md" in content, \
            "README に examples/github-only-flow.md へのリンクがない"

    def test_readme_links_to_templates(self):
        content = README.read_text()
        assert "examples/templates" in content, \
            "README に examples/templates/ への参照がない"

    def test_readme_mentions_reviewer_policy(self):
        content = README.read_text()
        assert "超辛口" in content or "NG" in content, \
            "README にレビューポリシーの記述がない"
