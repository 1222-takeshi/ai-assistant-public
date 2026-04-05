# PMO Workflow — プロジェクト管理チーム（参考実装）

> ⚠️ **これは参考実装です。** 外部サービス（Notion / Atlassian / GCal / Slack / Gmail）との連携が前提です。

---

## 必要な外部サービス

| サービス | 用途 |
|---------|------|
| Notion MCP | タスク管理 |
| Atlassian MCP | Jira / Confluence 連携 |
| Google Calendar MCP | 会議スケジュール取得 |
| Slack MCP | メッセージ取得 |
| Gmail MCP | メール取得 |

## コマンド一覧

| コマンド | 用途 |
|---------|------|
| `/pmo/run-tasks` | Notion タスクを読み込み Jira / Confluence を自動実行 |
| `/pmo/write-minutes` | GCal + Slack + Gmail から議事録の草案を生成 |
| `/pmo/daily-routine` | 毎朝ルーティン（確認 → 自動実行 → 日次レポート） |

## セットアップ手順

```bash
# 1. PMO config を初期化
./scripts/bootstrap.sh --init-pmo-config

# 2. config/notion.local.yaml と config/confluence.local.yaml に実値を入力

# 3. 検証
python3 scripts/validate-config.py --check-local

# 4. コマンドをコピー（まだない場合）
cp -r examples/pmo-workflow/commands/pmo/ .claude/commands/pmo/

# 5. ドライラン
/pmo/run-tasks --dry-run
```

詳細は [docs/pmo-profile.md](../../docs/pmo-profile.md) を参照してください。
