# Admin Support Team — 管理・バックオフィスチーム（参考実装）

> ⚠️ **これは参考実装です。** 自由に変更・拡張してください。

---

## 役割定義

| ロール | 主な責務 |
|--------|---------|
| Executive Secretary | スケジュール管理・議事録作成・メール下書き |
| Finance Analyst | 経費精算チェック・予算実績管理・財務レポート |
| Budget Controller | 予算超過アラート・コスト配分分析・承認フロー |
| HR Coordinator | 採用管理・オンボーディング資料整備・勤怠集計 |
| Legal Checker | 契約書レビュー・コンプライアンス確認 |
| Procurement Agent | 発注・見積比較・ベンダー管理・稟議資料 |

## 典型的なフロー（財務）

```
Finance Analyst: 月次経費集計 Issue
    → Budget Controller: 予算比較・超過チェック
    → Legal Checker: 契約上の支払い条件確認
    → Executive Secretary: 承認依頼メール作成 → 経営層へ
```

## 典型的なフロー（秘書業務）

```
Executive Secretary: 会議アジェンダ Issue
    → 参加者調整・日程候補整理
    → 議事録ドラフト → Reviewer
    → 承認後、Action Item を各担当 Issue に変換
```

## 外部連携オプション

- カレンダー管理 → Google Calendar MCP
- メール下書き → Gmail MCP
- 稟議フロー → Notion MCP または社内ワークフローツール
