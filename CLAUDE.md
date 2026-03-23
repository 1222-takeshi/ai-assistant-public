# ai-assistant

Claude Code を中心とした AI アシスタント機能の開発・実験プロジェクト。

## プロジェクト概要

- **目的**: Claude API / MCP ツールを活用した自動化・エージェント機能の開発
- **アーキテクチャ**: マルチエージェント開発フロー（Orchestrator / Researcher / Requirements Analyst / Implementer / Reviewer）
- **設計方針**: GitHub Issue 駆動・git worktree による並列開発

## ディレクトリ構成

```
ai-assistant/
├── CLAUDE.md                   # このファイル（Claude Code 用）
├── .gitignore
├── .gemini_temp/               # PR本文・一時ドキュメント（git管理外）
├── scripts/
│   ├── gh-workflow.sh          # push / PR / Issue 操作ヘルパー
│   ├── setup-worktree.sh       # worktree 作成ヘルパー
│   ├── worktree-cleanup.sh     # stale worktree の整理と残骸チェック
│   └── list-worktrees.sh       # worktree 一覧表示
└── .claude/
    ├── team-topology.yaml      # 開発チームの役割・レーン・handoff の source of truth
    ├── settings.local.json     # MCPツール権限設定
    ├── worktrees/              # 実装者用 worktree（git管理外）
    └── commands/
        └── dev/
            ├── start-team.md   # /dev/start-team
            ├── status.md       # /dev/status
            ├── orchestrate.md  # /dev/orchestrate
            ├── research.md     # /dev/research
            ├── define-requirements.md  # /dev/define-requirements
            ├── implement.md    # /dev/implement
            └── review.md       # /dev/review
```

## カスタムコマンド一覧

### 機能開発（dev/）

| コマンド | 用途 |
|---------|------|
| `/dev/start-team` | Claude Code のコンテキスト確認・日次起動・担当レーン割り当て |
| `/dev/status` | チームの稼働状況・ブロッカー・review待ちを可視化 |
| `/dev/orchestrate` | 全エージェント状態俯瞰・開発着手判断・PRマージ判断 |
| `/dev/research` | 技術調査・成果物をGitHub Issueに記録 |
| `/dev/define-requirements` | 要件定義・テスト仕様設計・実装依頼発行 |
| `/dev/implement` | GitHub Issueから実装・PR作成 |
| `/dev/review` | 要件・設計・テスト仕様・PRの多段レビュー |

## マルチエージェント開発アーキテクチャ

```
Orchestrator (1名)
  ├─→ Requirements Analyst (1名) → Reviewer → Implementer x2
  └─→ Researcher x2 (常時稼働・調査サポート)
```

### 運用の source of truth

- `CLAUDE.md`: 全体方針、ラベル、基本ルール
- `.claude/team-topology.yaml`: ロール定義、担当レーン、worktree、handoff
- `/dev/start-team`: 起動時の入口
- `/dev/status`: 稼働状況の可視化

### git worktree 戦略

```bash
# 管理用リポジトリ (main ブランチ)
/mnt/takeshi/hdd/workspace/ai-assistant/

# 実装者1用 worktree
./scripts/setup-worktree.sh impl-1 feat/<機能名A>

# 実装者2用 worktree
./scripts/setup-worktree.sh impl-2 feat/<機能名B>
```

- worktree はすべて `.claude/worktrees/` 配下（`.gitignore` で除外済み）
- 同一ディレクトリでの頻繁な `git checkout` は禁止

## GitHub Labels

| Label | 用途 |
|-------|------|
| `research` | 調査者が作成した Issue |
| `requirements` | 要件定義者が作成した要件 Issue |
| `implementation` | 実装依頼 Issue |
| `review-needed` | レビュー待ち |
| `approved` | Reviewer OK 済み |
| `blocked` | ブロッカーあり |

## 補助スクリプト

```bash
# ブランチを指定して push
./scripts/gh-workflow.sh push -b feat/my-feature

# PR 作成（タイトルと body ファイル指定）
./scripts/gh-workflow.sh pr --title "feat: add X" --body-file .gemini_temp/pr_body.md

# Issue 作成（タイトルと body ファイル指定）
./scripts/gh-workflow.sh issue --title "Bug: something wrong" --body-file .gemini_temp/issue_body.md
```

## 開発ルール

- **ブランチ戦略**: `feat/<機能名>` / `fix/<修正内容>` の専用ブランチで作業
- **main 直接 push 禁止**
- **コミットメッセージ**: 英語・Conventional Commits 形式
- **PR タイトル**: 英語・Conventional Commits 形式
- **PR 本文**: 日本語で詳細に記述
- **テストカバレッジ**: 最低 80% を維持

---

## PMO（プロジェクト管理オフィス）機能

### 概要

Claude Code を PMO エージェントとして動作させ、Notion タスクをトリガーに
Jira / Confluence を自動操作し、会議の議事録を自動生成する機能。

**接続先**:
- **Notion MCP** — タスク読み書き（`mcp__notion__*`）
- **Atlassian MCP** — Jira / Confluence 操作（`mcp__claude_ai_Atlassian__*`）
- **Google Calendar MCP** — 会議情報取得
- **Slack MCP** — 議事録情報収集・レポート投稿
- **Gmail MCP** — 議事録情報補完

### PMO コマンド一覧

| コマンド | 用途 |
|---------|------|
| `/pmo/run-tasks` | Notion タスクを読み込み Jira/Confluence を自動実行 |
| `/pmo/write-minutes` | GCal + Slack → Confluence 議事録生成 |
| `/pmo/daily-routine` | 毎朝ルーティン（確認→自動実行→日次レポート） |

### ディレクトリ構成（PMO 関連）

```
ai-assistant/
├── config/
│   ├── notion.yaml         # Notion DB ID / プロジェクトキーマッピング
│   └── confluence.yaml     # Confluenceスペース・親ページID設定
└── templates/
    └── meeting-minutes.md  # 議事録テンプレート（構造定義）
```

### Notion Tasks DB プロパティ設計

| プロパティ名 | 型 | 用途 |
|------------|-----|------|
| `Name` | Title | タスク名 |
| `Status` | Select | Todo / In Progress / Done / Cancelled / Blocked |
| `Priority` | Select | 緊急 / 高 / 中 / 低 |
| `Scheduled Date` | Date | 実行予定日（当日タスクとして認識） |
| `Due Date` | Date | 期限 |
| `Tags` | Multi-select | `auto-jira` / `auto-confluence` で自動実行 |
| `Project` | Select | プロジェクト名（Jiraプロジェクトキーに変換） |
| `Source` | Select | `jira` / `confluence` / `manual` |
| `Source URL` | URL | 成果物 URL（自動入力） |
| `Source ID` | Rich text | Jira Issue Key 等（自動入力） |
| `Description` | Rich text | 詳細説明・Confluence 本文 |

### 自動実行の条件

- `Tags` に `auto-jira` → Jira チケット作成/更新を自動実行
- `Tags` に `auto-confluence` → Confluence ページ作成/更新を自動実行
- タイトル/説明のキーワードマッチ → 確認プロンプトあり

### セットアップ手順

1. **Notion MCP の追加**: Claude Code の MCP 設定に Notion MCP サーバーを追加
   ```json
   // ~/.claude/settings.json の mcpServers に追加
   "notion": {
     "command": "npx",
     "args": ["-y", "@notionhq/notion-mcp-server"],
     "env": { "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer YOUR_NOTION_TOKEN\"}" }
   }
   ```

2. **config/notion.yaml の設定**:
   - `tasks_db_id`: Notion Tasks DB の ID（URL末尾32文字）
   - `project_key_map`: プロジェクト名 → Jira キーの対応を実値に更新

3. **config/confluence.yaml の設定**:
   - `atlassian_domain`: 実際のドメインに更新
   - `default_space_key`: 使用するスペースキーに更新
   - `parent_pages.*`: 各親ページの ID を実値に更新

4. **Notion Tasks DB に `auto-jira` / `auto-confluence` タグを追加**

5. **接続確認**:
   ```
   /pmo/run-tasks --dry-run
   ```
