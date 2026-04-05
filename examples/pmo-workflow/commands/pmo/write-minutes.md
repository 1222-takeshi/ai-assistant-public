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
- `meeting_minutes_map` : 会議名キーワード → 親ページID のマッピング一覧
- `default_space_key` : Confluence デフォルトスペースキー
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

### Step 3: 親ページの解決

`meeting_minutes_map` から会議名に対応する親ページを特定する:

1. GCal イベントタイトルを `meeting_minutes_map` の各エントリの `keywords` と部分一致で照合
2. 最初にマッチしたエントリの `parent_id` と `space_key` を使用
3. マッチしない場合は `keywords: ["__default__"]` のエントリを使用
4. `__default__` もない場合はユーザーに親ページURLを確認

`copy_from` の解決:
- `"latest"` の場合:
  1. `getConfluencePage(parent_id)` で子ページ一覧を取得
  2. 作成日時が最新の子ページIDを特定
  3. `getConfluencePage(latest_child_id)` で構造を取得し、議事録の骨格として使用
- 具体的なページIDの場合: `getConfluencePage(copy_from)` で構造を取得
- 省略の場合: `templates/meeting-minutes.md` を骨格として使用

### Step 4: Slack スレッドの検索・収集

`slack_search_public_and_private` で会議名をキーワードに検索:
- 検索クエリ: `"{meeting_name}" after:{date} before:{date+1}`

見つかったスレッドに対して `slack_read_thread` で内容を取得。

複数スレッドが見つかった場合は関連度が高いものを優先。

### Step 5: Gmail の補完検索（オプション）

Slack で十分な情報が得られない場合、`gmail_search_messages` で補完:
- 検索クエリ: `subject:"{meeting_name}" after:{date}`

関連メールがあれば `gmail_read_message` で本文を取得。

### Step 6: 議事録の組み立て

`copy_from` ページの構造（または `templates/meeting-minutes.md`）に従い、収集した情報から議事録を生成:

1. **基本情報** (GCal から): 日時、参加者、会議URL
2. **アジェンダ** (GCal の説明 / Slack の事前投稿から)
3. **議事内容** (Slack スレッド / Gmail から): 発言・決定事項を整理
4. **決定事項** : 議論から抽出
5. **アクションアイテム** : 担当者・期限付きで抽出
6. **次回** : 次回日程・議題（あれば）

### Step 7: Confluence ページの作成

`--dry-run` の場合: 生成した議事録をターミナルに出力して終了。

通常実行:
- `createConfluencePage` でページを作成
  - `spaceKey`: マッピングの `space_key`（未設定時は `default_space_key`）
  - `parentId`: マッピングの `parent_id`
  - `title`: `title_formats.meeting_minutes` のフォーマットで生成
    例: `[議事録] 2026-03-17 週次定例MTG`
  - `content`: Step 6 で生成した議事録を Confluence ストレージ形式に変換

### Step 8: 結果の報告

```
## 議事録作成完了

- 会議: {meeting_name}
- 日時: {date} {start_time} - {end_time}
- Confluenceページ: {page_url}
- 格納先: {space_key} / 親ページ {parent_id}

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
- 親ページが `YOUR_PAGE_ID` のまま: `config/confluence.yaml` の `meeting_minutes_map` を設定するよう案内
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
- `mcp__claude_ai_Atlassian__getConfluencePage` — コピー元ページ取得
- `mcp__claude_ai_Atlassian__createConfluencePage` — Confluence ページ作成
- `mcp__claude_ai_Atlassian__getConfluenceSpaces` — スペース確認
