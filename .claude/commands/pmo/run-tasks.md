# /pmo/run-tasks — Notion タスク自動実行エージェント

Notion Tasks DB に登録されたタスクを読み込み、Jira / Confluence を自動操作するエージェント。

## 引数

- `--dry-run` : 実行せずに分類結果のみ表示（デフォルト: false）
- `--date <YYYY-MM-DD>` : 対象日付を指定（デフォルト: 今日）
- `--task-id <Notion Page ID>` : 特定タスクのみ実行

## 実行フロー

### Step 1: 設定ファイルの読み込み

`config/notion.yaml` と `config/confluence.yaml` を読み込む。
- `tasks_db_id` : Notion Tasks DB の ID
- `project_key_map` : プロジェクト名 → Jira プロジェクトキーの対応表
- `automation` : 自動実行タグ・キーワード設定

### Step 2: Notion Tasks DB のクエリ

`notion-query-database` を使い、以下のフィルタで取得:
- `Scheduled Date` = 対象日付（または今日）
- `Status` が `Done` / `Cancelled` でない

取得したタスクを出力して確認。

### Step 3: タスク分類

各タスクを以下のルールで分類:

| 分類 | 条件 |
|------|------|
| **auto-jira** | `Tags` に `auto-jira` が含まれる |
| **auto-confluence** | `Tags` に `auto-confluence` が含まれる |
| **keyword-jira** | タイトル/説明に `jira_keywords` がマッチ（確認プロンプトあり） |
| **keyword-confluence** | タイトル/説明に `confluence_keywords` がマッチ（確認プロンプトあり） |
| **manual** | 上記いずれにも該当しない → 手動対応リストに追加 |

`--dry-run` の場合はここで終了し、分類結果を表示する。

### Step 4: Jira タスクの実行

`auto-jira` / `keyword-jira`（確認済み）の各タスクに対して:

1. `Source ID` プロパティが存在する場合:
   - `getJiraIssue(issueIdOrKey: source_id)` で現在の状態を取得
   - タスクの内容に応じて `updateJiraIssue` を実行
     - ステータス変更: `transitionJiraIssue`
     - 内容更新: `updateJiraIssue`

2. `Source ID` が空の場合:
   - `Project` プロパティを `notion.yaml` の `project_key_map` で Jira プロジェクトキーに変換
   - `createJiraIssue` でチケット作成
     - summary: タスクの `Name`
     - description: タスクの `Description`
     - priority: `Priority` プロパティをマッピング（高→High, 中→Medium, 低→Low）

3. 実行結果（Jira Issue URL）を記録

### Step 5: Confluence タスクの実行

`auto-confluence` / `keyword-confluence`（確認済み）の各タスクに対して:

1. `Source URL` プロパティが存在する場合:
   - `getConfluencePage(pageId)` で現在のページを取得
   - タスクの `Description` の内容でページを更新

2. `Source URL` が空の場合:
   - `confluence.yaml` の `pmo_docs` ページIDを親ページとして使用
   - `createConfluencePage` でページ作成
     - title: タスクの `Name`
     - spaceKey: `confluence.yaml` の `default_space_key`
     - content: タスクの `Description` を Confluence ストレージ形式に変換

3. 実行結果（Confluence Page URL）を記録

### Step 6: Notion ステータス更新

実行完了したタスクに対して `notion-update-page` を実行:
- `Status` → `Done`
- `Source URL` → 作成/更新した Jira Issue URL または Confluence Page URL
- `Source ID` → Jira Issue Key（Jiraタスクの場合）

### Step 7: 実行結果レポートの出力

```
## /pmo/run-tasks 実行結果 (YYYY-MM-DD)

### 完了タスク
| タスク名 | 種別 | 成果物URL |
|---------|------|----------|
| ...     | Jira | https://... |

### 手動対応が必要なタスク
| タスク名 | 理由 |
|---------|------|
| ...     | タグ未設定 |

### エラー
（あれば表示）
```

## エラーハンドリング

- Notion API エラー: エラー内容を表示し、該当タスクをスキップ
- Jira/Confluence API エラー: Notion のステータスを `Blocked` に更新し、エラー詳細を `Description` に追記
- 設定ファイルが見つからない: `config/notion.yaml` と `config/confluence.yaml` のセットアップを案内

## 使用する MCP ツール

- `notion-query-database` — Tasks DB クエリ
- `notion-retrieve-page` — タスク詳細取得
- `notion-update-page` — ステータス・Source URL 更新
- `mcp__claude_ai_Atlassian__createJiraIssue` — Jira チケット作成
- `mcp__claude_ai_Atlassian__getJiraIssue` — Jira チケット取得
- `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql` — Jira 検索
- `mcp__claude_ai_Atlassian__createConfluencePage` — Confluence ページ作成
- `mcp__claude_ai_Atlassian__getConfluencePage` — Confluence ページ取得
