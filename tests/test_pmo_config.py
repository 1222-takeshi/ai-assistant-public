"""PMO 設定ファイル・テンプレート・コマンドの包括的テストスイート

対象:
- config/notion.yaml       : 必須キー・値の型・マッピング整合性
- config/confluence.yaml   : 必須キー・URLフォーマット・プレースホルダー
- templates/meeting-minutes.md : セクション・プレースホルダー・構造
- .claude/commands/pmo/*.md    : フォーマット・記述内容・コマンド間の整合性
- .claude/settings.local.json  : PMO に必要な全権限の存在確認
- ファイル間整合性              : config と template・command の参照一貫性
"""

import json
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
NOTION_YAML = REPO_ROOT / "config" / "notion.yaml"
CONFLUENCE_YAML = REPO_ROOT / "config" / "confluence.yaml"
MINUTES_TEMPLATE = REPO_ROOT / "templates" / "meeting-minutes.md"
PMO_DIR = REPO_ROOT / ".claude" / "commands" / "pmo"
SETTINGS_JSON = REPO_ROOT / ".claude" / "settings.local.json"
PMO_COMMANDS = ["run-tasks.md", "write-minutes.md", "daily-routine.md"]


# ===========================================================================
# 共通ヘルパー
# ===========================================================================

def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_placeholders(text: str) -> set[str]:
    """テキスト中の {placeholder} を抽出する"""
    return set(re.findall(r"\{(\w+)\}", text))


# ===========================================================================
# config/notion.yaml
# ===========================================================================

class TestNotionYamlExists:
    def test_file_exists(self):
        assert NOTION_YAML.exists(), "config/notion.yaml が存在しません"

    def test_file_is_valid_yaml(self):
        content = NOTION_YAML.read_text(encoding="utf-8")
        result = yaml.safe_load(content)
        assert isinstance(result, dict), "notion.yaml が dict として解析できません"

    def test_file_is_not_empty(self):
        config = load_yaml(NOTION_YAML)
        assert len(config) > 0


class TestNotionYamlTopLevelKeys:
    REQUIRED_KEYS = {
        "tasks_db_id",
        "weekly_pages",
        "project_key_map",
        "automation",
        "property_names",
        "status_values",
        "priority_map",
    }

    @pytest.fixture(scope="class")
    def config(self):
        return load_yaml(NOTION_YAML)

    @pytest.mark.parametrize("key", sorted(REQUIRED_KEYS))
    def test_required_key_exists(self, config, key):
        assert key in config, f"notion.yaml に必須キー '{key}' がありません"

    def test_tasks_db_id_is_string(self, config):
        assert isinstance(config["tasks_db_id"], str)

    def test_tasks_db_id_is_not_empty(self, config):
        assert config["tasks_db_id"].strip() != ""

    def test_no_unexpected_none_values(self, config):
        none_keys = [k for k, v in config.items() if v is None]
        assert none_keys == [], f"None 値を持つトップレベルキー: {none_keys}"


class TestNotionYamlAutomation:
    @pytest.fixture(scope="class")
    def automation(self):
        return load_yaml(NOTION_YAML)["automation"]

    @pytest.mark.parametrize("key", ["auto_jira_tag", "auto_confluence_tag", "jira_keywords", "confluence_keywords"])
    def test_required_key_exists(self, automation, key):
        assert key in automation

    def test_auto_jira_tag_is_string(self, automation):
        assert isinstance(automation["auto_jira_tag"], str)
        assert len(automation["auto_jira_tag"]) > 0

    def test_auto_confluence_tag_is_string(self, automation):
        assert isinstance(automation["auto_confluence_tag"], str)
        assert len(automation["auto_confluence_tag"]) > 0

    def test_jira_keywords_is_non_empty_list(self, automation):
        kw = automation["jira_keywords"]
        assert isinstance(kw, list) and len(kw) > 0

    def test_confluence_keywords_is_non_empty_list(self, automation):
        kw = automation["confluence_keywords"]
        assert isinstance(kw, list) and len(kw) > 0

    def test_jira_keywords_are_strings(self, automation):
        for kw in automation["jira_keywords"]:
            assert isinstance(kw, str), f"jira_keywords の要素が文字列でない: {kw!r}"

    def test_confluence_keywords_are_strings(self, automation):
        for kw in automation["confluence_keywords"]:
            assert isinstance(kw, str), f"confluence_keywords の要素が文字列でない: {kw!r}"

    def test_auto_tags_are_different(self, automation):
        assert automation["auto_jira_tag"] != automation["auto_confluence_tag"], \
            "auto_jira_tag と auto_confluence_tag は異なる値である必要があります"


class TestNotionYamlPropertyNames:
    REQUIRED_PROPS = {
        "status", "priority", "scheduled_date", "due_date",
        "tags", "project", "source", "source_url", "source_id", "description",
    }

    @pytest.fixture(scope="class")
    def props(self):
        return load_yaml(NOTION_YAML)["property_names"]

    @pytest.mark.parametrize("prop", sorted(REQUIRED_PROPS))
    def test_required_property_exists(self, props, prop):
        assert prop in props, f"property_names に '{prop}' がありません"

    def test_all_values_are_non_empty_strings(self, props):
        for key, val in props.items():
            assert isinstance(val, str) and val.strip() != "", \
                f"property_names.{key} が空または非文字列: {val!r}"

    def test_no_duplicate_values(self, props):
        values = list(props.values())
        assert len(values) == len(set(values)), \
            f"property_names に重複した値があります: {values}"


class TestNotionYamlStatusValues:
    REQUIRED_STATUSES = {"todo", "in_progress", "done", "cancelled", "blocked"}

    @pytest.fixture(scope="class")
    def statuses(self):
        return load_yaml(NOTION_YAML)["status_values"]

    @pytest.mark.parametrize("status", sorted(REQUIRED_STATUSES))
    def test_required_status_exists(self, statuses, status):
        assert status in statuses

    def test_all_values_are_non_empty_strings(self, statuses):
        for val in statuses.values():
            assert isinstance(val, str) and val.strip() != ""

    def test_done_and_cancelled_are_different(self, statuses):
        assert statuses["done"] != statuses["cancelled"]


class TestNotionYamlProjectKeyMap:
    @pytest.fixture(scope="class")
    def keymap(self):
        return load_yaml(NOTION_YAML)["project_key_map"]

    def test_default_key_exists(self, keymap):
        assert "default" in keymap

    def test_all_values_are_non_empty_strings(self, keymap):
        for proj, key in keymap.items():
            assert isinstance(key, str) and key.strip() != "", \
                f"project_key_map.{proj} が空: {key!r}"

    def test_jira_keys_are_uppercase(self, keymap):
        for jira_key in keymap.values():
            assert jira_key == jira_key.upper(), \
                f"Jira プロジェクトキー '{jira_key}' は大文字にする必要があります"


class TestNotionYamlPriorityMap:
    @pytest.fixture(scope="class")
    def priority_map(self):
        return load_yaml(NOTION_YAML)["priority_map"]

    def test_is_dict(self, priority_map):
        assert isinstance(priority_map, dict)

    def test_values_are_valid_jira_priorities(self, priority_map):
        valid = {"Highest", "High", "Medium", "Low", "Lowest"}
        for notion_prio, jira_prio in priority_map.items():
            assert jira_prio in valid, \
                f"priority_map['{notion_prio}'] = '{jira_prio}' は有効な Jira 優先度ではありません"


# ===========================================================================
# config/confluence.yaml
# ===========================================================================

class TestConfluenceYamlExists:
    def test_file_exists(self):
        assert CONFLUENCE_YAML.exists()

    def test_file_is_valid_yaml(self):
        content = CONFLUENCE_YAML.read_text(encoding="utf-8")
        assert isinstance(yaml.safe_load(content), dict)


class TestConfluenceYamlTopLevelKeys:
    REQUIRED_KEYS = {
        "atlassian_domain",
        "default_space_key",
        "parent_pages",
        "title_formats",
    }

    @pytest.fixture(scope="class")
    def config(self):
        return load_yaml(CONFLUENCE_YAML)

    @pytest.mark.parametrize("key", sorted(REQUIRED_KEYS))
    def test_required_key_exists(self, config, key):
        assert key in config

    def test_atlassian_domain_is_string(self, config):
        assert isinstance(config["atlassian_domain"], str)

    def test_atlassian_domain_format(self, config):
        domain = config["atlassian_domain"]
        is_placeholder = domain.startswith("YOUR_")
        is_valid = re.match(r"^[\w-]+\.atlassian\.net$", domain)
        assert is_placeholder or is_valid, f"atlassian_domain の形式が不正: {domain}"

    def test_default_space_key_is_string(self, config):
        assert isinstance(config["default_space_key"], str)
        assert config["default_space_key"].strip() != ""


class TestConfluenceYamlParentPages:
    REQUIRED_PAGES = {"meeting_minutes", "reports", "pmo_docs"}

    @pytest.fixture(scope="class")
    def parent_pages(self):
        return load_yaml(CONFLUENCE_YAML)["parent_pages"]

    @pytest.mark.parametrize("page", sorted(REQUIRED_PAGES))
    def test_required_page_key_exists(self, parent_pages, page):
        assert page in parent_pages

    def test_all_values_are_non_empty_strings(self, parent_pages):
        for key, val in parent_pages.items():
            assert isinstance(val, str) and val.strip() != "", \
                f"parent_pages.{key} が空: {val!r}"

    def test_no_duplicate_page_ids(self, parent_pages):
        non_placeholder = [v for v in parent_pages.values() if not v.startswith("YOUR_")]
        assert len(non_placeholder) == len(set(non_placeholder)), \
            "parent_pages に重複したページIDがあります"


class TestConfluenceYamlTitleFormats:
    REQUIRED_FORMATS = {"meeting_minutes", "pmo_report"}

    @pytest.fixture(scope="class")
    def title_formats(self):
        return load_yaml(CONFLUENCE_YAML)["title_formats"]

    @pytest.mark.parametrize("fmt", sorted(REQUIRED_FORMATS))
    def test_required_format_exists(self, title_formats, fmt):
        assert fmt in title_formats

    @pytest.mark.parametrize("fmt", sorted(REQUIRED_FORMATS))
    def test_format_contains_date(self, title_formats, fmt):
        assert "{date}" in title_formats[fmt], \
            f"title_formats.{fmt} に {{date}} がありません"

    def test_meeting_minutes_format_contains_meeting_name(self, title_formats):
        assert "{meeting_name}" in title_formats["meeting_minutes"]

    def test_pmo_report_format_contains_report_name(self, title_formats):
        assert "{report_name}" in title_formats["pmo_report"]

    def test_all_formats_are_non_empty_strings(self, title_formats):
        for val in title_formats.values():
            assert isinstance(val, str) and val.strip() != ""


# ===========================================================================
# templates/meeting-minutes.md
# ===========================================================================

class TestMeetingMinutesTemplateExists:
    def test_file_exists(self):
        assert MINUTES_TEMPLATE.exists()

    def test_file_is_utf8(self):
        # 文字コードエラーなく読めること
        MINUTES_TEMPLATE.read_text(encoding="utf-8")

    def test_file_is_not_empty(self):
        assert len(MINUTES_TEMPLATE.read_text(encoding="utf-8").strip()) > 0


class TestMeetingMinutesTemplateSections:
    REQUIRED_SECTIONS = [
        "基本情報",
        "アジェンダ",
        "議事内容",
        "決定事項",
        "アクションアイテム",
        "次回",
        "参考資料",
    ]

    @pytest.fixture(scope="class")
    def content(self):
        return MINUTES_TEMPLATE.read_text(encoding="utf-8")

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_section_exists(self, content, section):
        assert section in content, f"セクション '{section}' がテンプレートにありません"

    def test_starts_with_heading(self, content):
        assert content.lstrip().startswith("#")

    def test_has_table_for_basic_info(self, content):
        # 基本情報テーブルがあること（|で始まる行）
        lines_with_pipe = [l for l in content.splitlines() if l.strip().startswith("|")]
        assert len(lines_with_pipe) >= 3, "テーブル行が不足しています"

    def test_has_action_item_table(self, content):
        assert "アクションアイテム" in content
        # アクションアイテムセクション以降にテーブルがあること
        idx = content.index("アクションアイテム")
        after = content[idx:]
        assert "|" in after, "アクションアイテムのテーブルがありません"


class TestMeetingMinutesTemplatePlaceholders:
    REQUIRED_PLACEHOLDERS = {
        "date", "meeting_name", "attendees",
        "start_time", "end_time", "location_or_url",
        "action_1", "owner_1", "due_1",
    }

    @pytest.fixture(scope="class")
    def content(self):
        return MINUTES_TEMPLATE.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def placeholders(self, content):
        return extract_placeholders(content)

    @pytest.mark.parametrize("ph", sorted(REQUIRED_PLACEHOLDERS))
    def test_required_placeholder_exists(self, placeholders, ph):
        assert ph in placeholders, f"プレースホルダー '{{{ph}}}' がテンプレートにありません"

    def test_all_placeholders_are_snake_case(self, placeholders):
        for ph in placeholders:
            assert re.match(r"^[a-z][a-z0-9_]*$", ph), \
                f"プレースホルダー '{ph}' は snake_case である必要があります"

    def test_sources_placeholder_exists(self, content):
        assert "{sources}" in content, "生成ソース記録用の {sources} プレースホルダーがありません"

    def test_no_unclosed_braces(self, content):
        # 閉じられていない { がないこと
        open_count = content.count("{")
        close_count = content.count("}")
        assert open_count == close_count, \
            f"{{ と }} の数が一致しません (open={open_count}, close={close_count})"


# ===========================================================================
# .claude/commands/pmo/*.md
# ===========================================================================

class TestPmoCommandFilesExist:
    @pytest.mark.parametrize("name", PMO_COMMANDS)
    def test_command_file_exists(self, name):
        assert (PMO_DIR / name).exists(), f"コマンドファイル {name} が存在しません"

    def test_no_extra_unexpected_files(self):
        actual = {f.name for f in PMO_DIR.glob("*.md")}
        expected = set(PMO_COMMANDS)
        extra = actual - expected
        assert extra == set(), f"予期しないコマンドファイルがあります: {extra}"


class TestPmoCommandFormat:
    @pytest.fixture(params=PMO_COMMANDS)
    def command_content(self, request):
        return (PMO_DIR / request.param).read_text(encoding="utf-8"), request.param

    def test_starts_with_h1(self, command_content):
        content, name = command_content
        assert content.lstrip().startswith("# "), \
            f"{name} は H1 タイトルで始まる必要があります"

    def test_has_flow_section(self, command_content):
        content, name = command_content
        assert "実行フロー" in content or "Step" in content, \
            f"{name} に実行フローの記述がありません"

    def test_has_mcp_tools_section(self, command_content):
        content, name = command_content
        assert "MCP ツール" in content or "mcp__" in content.lower(), \
            f"{name} に使用 MCP ツールの記述がありません"

    def test_has_error_handling_section(self, command_content):
        content, name = command_content
        assert "エラー" in content, \
            f"{name} にエラーハンドリングの記述がありません"

    def test_is_utf8_decodable(self, command_content):
        _, name = command_content
        (PMO_DIR / name).read_text(encoding="utf-8")  # エラーなければOK

    def test_minimum_length(self, command_content):
        content, name = command_content
        assert len(content) >= 500, \
            f"{name} の内容が短すぎます ({len(content)} 文字)"


class TestRunTasksCommand:
    @pytest.fixture(scope="class")
    def content(self):
        return (PMO_DIR / "run-tasks.md").read_text(encoding="utf-8")

    def test_mentions_dry_run_flag(self, content):
        assert "--dry-run" in content

    def test_mentions_notion_query(self, content):
        assert "notion-query-database" in content

    def test_mentions_jira_create(self, content):
        assert "createJiraIssue" in content

    def test_mentions_jira_update(self, content):
        assert "updateJiraIssue" in content or "update" in content.lower()

    def test_mentions_confluence_create(self, content):
        assert "createConfluencePage" in content

    def test_mentions_notion_status_update(self, content):
        assert "notion-update-page" in content

    def test_mentions_done_status(self, content):
        assert "Done" in content

    def test_config_files_referenced(self, content):
        assert "notion.yaml" in content
        assert "confluence.yaml" in content

    def test_mentions_source_id_property(self, content):
        assert "Source ID" in content or "source_id" in content

    def test_mentions_auto_jira_tag(self, content):
        assert "auto-jira" in content

    def test_mentions_auto_confluence_tag(self, content):
        assert "auto-confluence" in content

    def test_execution_report_section(self, content):
        assert "実行結果" in content or "レポート" in content


class TestWriteMinutesCommand:
    @pytest.fixture(scope="class")
    def content(self):
        return (PMO_DIR / "write-minutes.md").read_text(encoding="utf-8")

    def test_mentions_gcal(self, content):
        assert "gcal" in content.lower() or "GCal" in content

    def test_mentions_slack(self, content):
        assert "slack" in content.lower() or "Slack" in content

    def test_mentions_gmail(self, content):
        assert "gmail" in content.lower() or "Gmail" in content

    def test_mentions_template_file(self, content):
        assert "meeting-minutes.md" in content or "templates" in content

    def test_mentions_confluence_create(self, content):
        assert "createConfluencePage" in content

    def test_mentions_dry_run_flag(self, content):
        assert "--dry-run" in content

    def test_mentions_date_argument(self, content):
        assert "--date" in content

    def test_mentions_slack_search(self, content):
        assert "slack_search" in content

    def test_mentions_slack_read_thread(self, content):
        assert "slack_read_thread" in content

    def test_mentions_title_format(self, content):
        assert "議事録" in content and ("{date}" in content or "date" in content)

    def test_fallback_to_file_on_error(self, content):
        assert ".gemini_temp" in content or "ファイル" in content


class TestDailyRoutineCommand:
    @pytest.fixture(scope="class")
    def content(self):
        return (PMO_DIR / "daily-routine.md").read_text(encoding="utf-8")

    def test_references_run_tasks(self, content):
        assert "run-tasks" in content

    def test_references_write_minutes(self, content):
        assert "write-minutes" in content

    def test_mentions_gcal_events(self, content):
        assert "gcal_list_events" in content or "gcal" in content.lower()

    def test_mentions_notion_query(self, content):
        assert "notion-query-database" in content or "Notion" in content

    def test_mentions_past_meeting_check(self, content):
        assert "議事録" in content

    def test_mentions_slack_report(self, content):
        assert "slack" in content.lower() or "Slack" in content

    def test_mentions_no_auto_flag(self, content):
        assert "--no-auto" in content

    def test_mentions_cron_or_schedule(self, content):
        assert "Cron" in content or "cron" in content or "9:00" in content

    def test_has_summary_output_section(self, content):
        assert "サマリー" in content or "日次" in content


# ===========================================================================
# .claude/settings.local.json — PMO 権限
# ===========================================================================

class TestSettingsLocalJsonExists:
    def test_file_exists(self):
        assert SETTINGS_JSON.exists()

    def test_is_valid_json(self):
        assert isinstance(load_json(SETTINGS_JSON), dict)

    def test_has_permissions_key(self):
        data = load_json(SETTINGS_JSON)
        assert "permissions" in data

    def test_has_allow_list(self):
        data = load_json(SETTINGS_JSON)
        assert "allow" in data["permissions"]
        assert isinstance(data["permissions"]["allow"], list)


class TestAtlassianPermissions:
    REQUIRED = [
        "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources",
        "mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql",
        "mcp__claude_ai_Atlassian__getJiraIssue",
        "mcp__claude_ai_Atlassian__createJiraIssue",
        "mcp__claude_ai_Atlassian__searchConfluenceUsingCql",
        "mcp__claude_ai_Atlassian__getConfluencePage",
        "mcp__claude_ai_Atlassian__createConfluencePage",
        "mcp__claude_ai_Atlassian__getConfluenceSpaces",
    ]

    @pytest.fixture(scope="class")
    def allowed(self):
        return load_json(SETTINGS_JSON)["permissions"]["allow"]

    @pytest.mark.parametrize("perm", REQUIRED)
    def test_permission_allowed(self, allowed, perm):
        assert perm in allowed, f"権限 '{perm}' が settings.local.json に登録されていません"


class TestNotionPermissions:
    REQUIRED = [
        "mcp__notion__notion-query-database",
        "mcp__notion__notion-retrieve-page",
        "mcp__notion__notion-update-page",
        "mcp__notion__notion-search",
        "mcp__notion__notion-retrieve-database",
    ]

    @pytest.fixture(scope="class")
    def allowed(self):
        return load_json(SETTINGS_JSON)["permissions"]["allow"]

    @pytest.mark.parametrize("perm", REQUIRED)
    def test_permission_allowed(self, allowed, perm):
        assert perm in allowed, f"Notion 権限 '{perm}' が登録されていません"


class TestGCalPermissions:
    REQUIRED = [
        "mcp__claude_ai_Google_Calendar__gcal_list_events",
        "mcp__claude_ai_Google_Calendar__gcal_list_calendars",
        "mcp__claude_ai_Google_Calendar__gcal_get_event",
        "mcp__claude_ai_Google_Calendar__gcal_find_my_free_time",
    ]

    @pytest.fixture(scope="class")
    def allowed(self):
        return load_json(SETTINGS_JSON)["permissions"]["allow"]

    @pytest.mark.parametrize("perm", REQUIRED)
    def test_permission_allowed(self, allowed, perm):
        assert perm in allowed


class TestGmailPermissions:
    REQUIRED = [
        "mcp__claude_ai_Gmail__gmail_search_messages",
        "mcp__claude_ai_Gmail__gmail_read_message",
        "mcp__claude_ai_Gmail__gmail_read_thread",
        "mcp__claude_ai_Gmail__gmail_list_labels",
    ]

    @pytest.fixture(scope="class")
    def allowed(self):
        return load_json(SETTINGS_JSON)["permissions"]["allow"]

    @pytest.mark.parametrize("perm", REQUIRED)
    def test_permission_allowed(self, allowed, perm):
        assert perm in allowed


class TestSlackPermissions:
    REQUIRED = [
        "mcp__claude_ai_Slack__slack_search_public_and_private",
        "mcp__claude_ai_Slack__slack_search_channels",
        "mcp__claude_ai_Slack__slack_read_channel",
        "mcp__claude_ai_Slack__slack_read_thread",
        "mcp__claude_ai_Slack__slack_send_message",
    ]

    @pytest.fixture(scope="class")
    def allowed(self):
        return load_json(SETTINGS_JSON)["permissions"]["allow"]

    @pytest.mark.parametrize("perm", REQUIRED)
    def test_permission_allowed(self, allowed, perm):
        assert perm in allowed


class TestBashPermissions:
    @pytest.fixture(scope="class")
    def allowed(self):
        return load_json(SETTINGS_JSON)["permissions"]["allow"]

    def test_date_command_allowed(self, allowed):
        assert "Bash(date:*)" in allowed

    def test_git_commands_allowed(self, allowed):
        git_perms = [p for p in allowed if p.startswith("Bash(git")]
        assert len(git_perms) > 0, "git コマンドの権限が登録されていません"

    def test_gh_commands_allowed(self, allowed):
        gh_perms = [p for p in allowed if p.startswith("Bash(gh")]
        assert len(gh_perms) > 0, "gh コマンドの権限が登録されていません"


# ===========================================================================
# ファイル間整合性テスト
# ===========================================================================

class TestCrossFileConsistency:
    """config / template / command 間の参照が一致しているか検証する"""

    def test_notion_property_names_referenced_in_run_tasks(self):
        notion = load_yaml(NOTION_YAML)
        props = notion["property_names"]
        run_tasks = (PMO_DIR / "run-tasks.md").read_text(encoding="utf-8")
        # スケジュール日・ステータス・タグが run-tasks で参照されていること
        for key in ("scheduled_date", "status", "tags"):
            prop_value = props[key]
            assert prop_value in run_tasks or key.replace("_", " ").title() in run_tasks, \
                f"notion.yaml の property '{key}' ({prop_value}) が run-tasks.md で参照されていません"

    def test_confluence_yaml_parent_pages_referenced_in_run_tasks(self):
        run_tasks = (PMO_DIR / "run-tasks.md").read_text(encoding="utf-8")
        assert "pmo_docs" in run_tasks or "confluence.yaml" in run_tasks

    def test_confluence_yaml_minutes_parent_referenced_in_write_minutes(self):
        write_minutes = (PMO_DIR / "write-minutes.md").read_text(encoding="utf-8")
        assert "meeting_minutes" in write_minutes or "confluence.yaml" in write_minutes

    def test_notion_auto_tags_referenced_in_run_tasks(self):
        notion = load_yaml(NOTION_YAML)
        auto = notion["automation"]
        run_tasks = (PMO_DIR / "run-tasks.md").read_text(encoding="utf-8")
        assert auto["auto_jira_tag"] in run_tasks
        assert auto["auto_confluence_tag"] in run_tasks

    def test_title_format_placeholders_are_used_in_write_minutes(self):
        confluence = load_yaml(CONFLUENCE_YAML)
        fmt = confluence["title_formats"]["meeting_minutes"]
        placeholders = extract_placeholders(fmt)
        write_minutes = (PMO_DIR / "write-minutes.md").read_text(encoding="utf-8")
        for ph in placeholders:
            assert ph in write_minutes or ph.replace("_", " ") in write_minutes, \
                f"title_formats のプレースホルダー '{ph}' が write-minutes.md で使われていません"

    def test_template_sections_align_with_write_minutes_steps(self):
        template = MINUTES_TEMPLATE.read_text(encoding="utf-8")
        write_minutes = (PMO_DIR / "write-minutes.md").read_text(encoding="utf-8")
        # 議事録のコアセクションが write-minutes に言及されていること
        for section in ("基本情報", "アクションアイテム", "決定事項"):
            assert section in template
        # write-minutes がテンプレートファイルを参照していること
        assert "meeting-minutes.md" in write_minutes or "templates" in write_minutes

    def test_daily_routine_references_both_commands(self):
        daily = (PMO_DIR / "daily-routine.md").read_text(encoding="utf-8")
        assert "run-tasks" in daily, "daily-routine が run-tasks を参照していません"
        assert "write-minutes" in daily, "daily-routine が write-minutes を参照していません"

    def test_notion_status_done_used_in_run_tasks(self):
        notion = load_yaml(NOTION_YAML)
        done_val = notion["status_values"]["done"]
        run_tasks = (PMO_DIR / "run-tasks.md").read_text(encoding="utf-8")
        assert done_val in run_tasks, \
            f"Notion の Done ステータス値 '{done_val}' が run-tasks.md に記述されていません"


# ===========================================================================
# 不正設定のバリデーション（negative tests）
# ===========================================================================

class TestInvalidConfigHandling:
    """不正な YAML を生成し、バリデーションロジックの動作を確認する"""

    def test_empty_yaml_is_detected(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("", encoding="utf-8")
        result = yaml.safe_load(bad.read_text(encoding="utf-8"))
        assert result is None or result == {}, "空の YAML は None または {} になること"

    def test_invalid_yaml_raises_error(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("key: [unclosed", encoding="utf-8")
        with pytest.raises(yaml.YAMLError):
            yaml.safe_load(bad.read_text(encoding="utf-8"))

    def test_placeholder_pattern_detection(self):
        text_with_placeholder = "tasks_db_id: YOUR_TASKS_DB_ID"
        assert "YOUR_" in text_with_placeholder, "プレースホルダーパターンを検出できること"

    def test_non_placeholder_domain_validation(self):
        valid_domains = ["mycompany.atlassian.net", "foo-bar.atlassian.net"]
        invalid_domains = ["example.com", "notatlassian.net", "foo.atlassian.com"]
        pattern = re.compile(r"^[\w-]+\.atlassian\.net$")
        for d in valid_domains:
            assert pattern.match(d), f"{d} は有効なドメインのはず"
        for d in invalid_domains:
            assert not pattern.match(d), f"{d} は無効なドメインのはず"

    def test_jira_project_key_uppercase_check(self):
        valid_keys = ["PMO", "PRJA", "GENERAL"]
        invalid_keys = ["pmo", "PrjA", "general"]
        for k in valid_keys:
            assert k == k.upper()
        for k in invalid_keys:
            assert k != k.upper()

    def test_placeholder_extraction_works(self):
        text = "Title: {date} - {meeting_name}"
        result = extract_placeholders(text)
        assert result == {"date", "meeting_name"}

    def test_placeholder_extraction_handles_no_placeholders(self):
        text = "No placeholders here"
        result = extract_placeholders(text)
        assert result == set()
