"""PR review flow documentation and helper tests."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
README_MD = REPO_ROOT / "README.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
REVIEW_COMMAND = REPO_ROOT / ".claude" / "commands" / "dev" / "review.md"
FLOW_DOC = REPO_ROOT / "docs" / "pr-review-flow.md"
GH_WORKFLOW = REPO_ROOT / "scripts" / "gh-workflow.sh"


class TestPrReviewFlowDocs:
    def test_flow_doc_exists(self):
        assert FLOW_DOC.exists(), "docs/pr-review-flow.md が存在しません"

    def test_readme_links_flow_doc(self):
        content = README_MD.read_text(encoding="utf-8")
        assert "docs/pr-review-flow.md" in content
        assert "same identity" in content

    def test_claude_mentions_formal_approval_boundary(self):
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert "same identity" in content
        assert "docs/pr-review-flow.md" in content

    def test_review_command_mentions_temporary_fallback(self):
        content = REVIEW_COMMAND.read_text(encoding="utf-8")
        assert "same identity" in content
        assert "暫定運用" in content
        assert "--comment" in content
        assert "--remove-label \"review-needed\"" in content


class TestGhWorkflowReviewerSupport:
    def test_pr_command_supports_reviewer(self):
        content = GH_WORKFLOW.read_text(encoding="utf-8")
        assert "--reviewer" in content
        assert "gh pr create" in content

    def test_request_review_command_exists(self):
        content = GH_WORKFLOW.read_text(encoding="utf-8")
        assert "request-review)" in content
        assert "--add-reviewer" in content
        assert "separate-user-or-team" in content
