# /pmo/daily-routine — 毎朝 PMO デイリールーティン

毎朝実行するルーティンコマンド。今日の会議・タスクを確認し、
自動実行可能なものを処理して日次サマリーを出力する。

## 引数

- `--date <YYYY-MM-DD>` : 対象日付（デフォルト: 今日）
- `--no-auto` : 自動実行をスキップ（確認のみ）
- `--slack-report` : 日次サマリーを Slack に投稿

## 実行フロー

### Step 1: 今日の会議一覧を取得

`gcal_list_calendars` で利用可能なカレンダーを確認。
`gcal_list_events` で今日の全イベントを取得:
- 会議タイトル、開始/終了時刻、参加者数、ミーティングURL の有無

```
## 今日の会議 (YYYY-MM-DD)
| 時刻 | 会議名 | 参加者 | 議事録 |
|------|--------|--------|--------|
| 10:00-11:00 | 週次定例 | 5名 | 未作成 |
```

### Step 2: Notion タスクの確認（dry-run）

`notion-query-database` で今日のタスクを取得:
- `Scheduled Date` = 今日
- `Status` が `Done` / `Cancelled` でない

タスクを自動実行可否で分類（実行はしない）:

```
## 今日のタスク
### 自動実行可能
| タスク名 | 種別 | 優先度 |
|---------|------|--------|
| ...     | auto-jira | 高 |

### 手動対応が必要
| タスク名 | 理由 |
|---------|------|
| ...     | タグ未設定 |
```

### Step 3: 自動実行の確認と実行

`--no-auto` フラグがない場合:

自動実行可能なタスクがあれば確認を求める（`--no-auto` でスキップ）:

```
自動実行可能なタスクが {n} 件あります。実行しますか？ [Y/n]
```

承認された場合: `/pmo/run-tasks` の実行フローを実行
（内部的に run-tasks と同じ Step 4〜7 を実行）

### Step 4: 議事録未作成会議のチェック

過去 2 日間（昨日・一昨日）の会議について議事録作成状況を確認:

`mcp__claude_ai_Atlassian__searchConfluenceUsingCql` でタイトル検索:
- `title ~ "[議事録]" AND created >= "{2_days_ago}"`

GCal の過去会議リストと照合し、議事録が未作成の会議を特定:

```
## 議事録未作成の会議
| 日付 | 会議名 | アクション |
|------|--------|----------|
| 2026-03-16 | 〇〇MTG | `/pmo/write-minutes --date 2026-03-16 "〇〇MTG"` |
```

### Step 5: 日次サマリーの出力

```
## PMO 日次サマリー (YYYY-MM-DD)

### 今日の会議 ({n}件)
（会議一覧）

### タスク実行結果
- 自動実行完了: {n}件
- 手動対応待ち: {n}件

### 議事録作成が必要な会議
（未作成リスト）

### 推奨アクション
1. 手動対応タスクの確認
2. 議事録未作成会議の対応
3. （その他の提案）
```

### Step 6: Slack への投稿（オプション）

`--slack-report` フラグがある場合:
`slack_send_message` で日次サマリーを PMO チャンネルに投稿。

チャンネルは `config/confluence.yaml` の `slack_report_channel` を参照
（未設定の場合は投稿先を確認）。

## 推奨実行タイミング

毎朝 9:00 に実行することを推奨。
Cron 設定例（CronCreate ツールで登録可能）:
```
0 9 * * 1-5  # 平日 9:00
```

## エラーハンドリング

- GCal 取得エラー: エラー内容を表示し、カレンダー接続を確認するよう案内
- Notion API エラー: エラー内容を表示し、タスク確認をスキップして手動対応を案内
- Atlassian MCP エラー: 自動実行をスキップし、手動対応リストに追加
- Slack 投稿エラー: ターミナルにサマリーを出力して継続
- 設定ファイル不在: `config/notion.yaml` と `config/confluence.yaml` のセットアップを案内して終了

## 使用する MCP ツール

- `gcal_list_calendars` — カレンダー一覧
- `gcal_list_events` — 今日・過去の会議取得
- `notion-query-database` — Notion タスク取得
- `notion-retrieve-page` — タスク詳細取得
- `mcp__claude_ai_Atlassian__searchConfluenceUsingCql` — 議事録確認
- `mcp__claude_ai_Atlassian__createJiraIssue` — Jira 自動実行
- `mcp__claude_ai_Atlassian__createConfluencePage` — Confluence 自動実行
- `notion-update-page` — ステータス更新
- `slack_send_message` — 日次レポート投稿（--slack-report 時）
