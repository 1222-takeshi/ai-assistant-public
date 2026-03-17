# /pmo/write-minutes — 議事録自動生成エージェント

GCal イベント + Slack スレッド（+ Gmail）から会議情報を収集し、
Confluence に議事録ページを自動生成するエージェント。

## 引数

- `<meeting_name>` : 会議名（部分一致で検索）。省略時は今日の会議一覧を表示して選択
- `--date <YYYY-MM-DD>` : 会議の日付（デフォルト: 今日）
- `--dry-run` : Confluence に書き込まず、生成内容をターミナルに出力

## 実行フロー

### Step 1: 設定ファイルの読み込み

`config/confluence.yaml` を読み込む:
- `parent_pages.meeting_minutes` : 議事録の親ページID
- `default_space_key` : Confluence スペースキー
- `title_formats.meeting_minutes` : ページタイトルのフォーマット

### Step 2: GCal イベントの取得

`gcal_list_events` で対象日の全イベントを取得。

引数で `<meeting_name>` が指定された場合:
- タイトルの部分一致でイベントを絞り込む
- 複数ヒットした場合は選択を促す

指定がない場合:
- 今日のイベント一覧を表示し、ユーザーに選択を促す

取得するイベント情報:
- タイトル、開始/終了時刻、参加者リスト、説明、ミーティングURL

### Step 3: Slack スレッドの検索・収集

`slack_search_public_and_private` で会議名をキーワードに検索:
- 検索クエリ: `"{meeting_name}" after:{date} before:{date+1}`

見つかったスレッドに対して `slack_read_thread` で内容を取得。

複数スレッドが見つかった場合は関連度が高いものを優先。

### Step 4: Gmail の補完検索（オプション）

Slack で十分な情報が得られない場合、`gmail_search_messages` で補完:
- 検索クエリ: `subject:"{meeting_name}" after:{date}`

関連メールがあれば `gmail_read_message` で本文を取得。

### Step 5: 議事録の組み立て

`templates/meeting-minutes.md` の構造に従い、収集した情報から議事録を生成:

1. **基本情報** (GCal から): 日時、参加者、会議URL
2. **アジェンダ** (GCal の説明 / Slack の事前投稿から)
3. **議事内容** (Slack スレッド / Gmail から): 発言・決定事項を整理
4. **決定事項** : 議論から抽出
5. **アクションアイテム** : 担当者・期限付きで抽出
6. **次回** : 次回日程・議題（あれば）

### Step 6: Confluence ページの作成

`--dry-run` の場合: 生成した議事録をターミナルに出力して終了。

通常実行:
- `createConfluencePage` でページを作成
  - `spaceKey`: `confluence.yaml` の `default_space_key`
  - `parentId`: `confluence.yaml` の `parent_pages.meeting_minutes`
  - `title`: `title_formats.meeting_minutes` のフォーマットで生成
    例: `[議事録] 2026-03-17 週次定例MTG`
  - `content`: Step 5 で生成した議事録を Confluence ストレージ形式に変換

### Step 7: 結果の報告

```
## 議事録作成完了

- 会議: {meeting_name}
- 日時: {date} {start_time} - {end_time}
- Confluenceページ: {page_url}

### 収集した情報ソース
- GCal: イベントID {event_id}
- Slack: {n} スレッド
- Gmail: {n} メール

### アクションアイテム（要確認）
| 担当者 | 内容 | 期限 |
|--------|------|------|
| ...    | ...  | ...  |
```

## エラーハンドリング

- GCal に会議が見つからない: 日付・会議名を確認するよう案内
- Slack に関連スレッドがない: Gmail のみで議事録を生成（情報不足を明記）
- Confluence API エラー: エラー詳細を表示し、生成内容をファイルに保存
  - 保存先: `.gemini_temp/minutes_{date}_{meeting_name}.md`

## 使用する MCP ツール

- `gcal_list_events` — 当日の会議一覧取得
- `gcal_get_event` — 会議詳細取得
- `slack_search_public_and_private` — Slack 検索
- `slack_read_thread` — Slack スレッド読み込み
- `gmail_search_messages` — Gmail 検索（補完用）
- `gmail_read_message` — Gmail メール読み込み（補完用）
- `mcp__claude_ai_Atlassian__createConfluencePage` — Confluence ページ作成
- `mcp__claude_ai_Atlassian__getConfluenceSpaces` — スペース確認
