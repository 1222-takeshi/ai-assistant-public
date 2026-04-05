# Field Engineering Team — フィールドエンジニアリングチーム（参考実装）

> ⚠️ **これは参考実装です。** 自由に変更・拡張してください。

---

## 役割定義

| ロール | 主な責務 |
|--------|---------|
| Field Lead | 現場訪問計画・エスカレーション判断・顧客折衝 |
| Site Engineer | 現場作業ドキュメント・技術報告書・手順書整備 |
| Customer Success Agent | 顧客フィードバック収集・満足度分析・改善提案 |
| Escalation Handler | 重大障害の社内エスカレーション・一次対応 |
| Knowledge Base Agent | 現場知見のナレッジ化・FAQ 更新・マニュアル整備 |

## 典型的なフロー

```
Site Engineer: 現場報告 Issue（作業ログ・問題点）
    → Customer Success Agent: フィードバック整理
    → Escalation Handler: 重大度判断 → 必要なら開発チームへ
    → Knowledge Base Agent: 解決策をナレッジベースに反映
    → Field Lead: 最終承認・次回訪問計画
```

## 他チームとの連携

- 重大障害 → `dev-workflow` の Implementer へ `implementation` ラベルでハンドオフ
- セキュリティリスク → `security-team` へエスカレーション
