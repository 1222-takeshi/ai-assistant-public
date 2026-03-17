# 議事録テンプレート

> このテンプレートは `/pmo/write-minutes` コマンドが Confluence ページ生成時に参照する構造定義です。
> 実際の議事録は Confluence ストレージ形式（XHTML）に変換して作成されます。

---

## [議事録] {date} {meeting_name}

### 基本情報

| 項目 | 内容 |
|------|------|
| 日時 | {date} {start_time} 〜 {end_time} |
| 場所 / URL | {location_or_url} |
| 参加者 | {attendees} |
| 欠席者 | {absent} |
| 記録者 | {recorder} |

---

### アジェンダ

{agenda_items}

---

### 議事内容

#### {agenda_item_1}

{discussion_content_1}

#### {agenda_item_2}

{discussion_content_2}

---

### 決定事項

| # | 内容 | 決定者 |
|---|------|--------|
| 1 | {decision_1} | {decider_1} |
| 2 | {decision_2} | {decider_2} |

---

### アクションアイテム

| # | タスク | 担当者 | 期限 | ステータス |
|---|--------|--------|------|----------|
| 1 | {action_1} | {owner_1} | {due_1} | 未着手 |
| 2 | {action_2} | {owner_2} | {due_2} | 未着手 |

---

### 次回

| 項目 | 内容 |
|------|------|
| 日時 | {next_date} |
| 議題 | {next_agenda} |

---

### 参考資料

- {reference_1}
- {reference_2}

---

*自動生成: `/pmo/write-minutes` by Claude Code PMO Agent*
*情報ソース: {sources}*
