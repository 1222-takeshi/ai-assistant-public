# QA Team — 品質保証チーム（参考実装）

> ⚠️ **これは参考実装です。** 自由に変更・拡張してください。

---

## 役割定義

| ロール | 主な責務 |
|--------|---------|
| QA Lead | テスト計画・品質基準定義・最終品質判断 |
| Test Engineer | テストケース設計・自動テスト実装・実行 |
| Coverage Analyst | カバレッジ計測・未テスト領域特定・レポート |
| Bug Triage Agent | バグ重要度分類・再現手順整理・エスカレーション |
| Quality Reviewer | テスト成果物の査読・品質ゲート判断 |

## 典型的なフロー

```
QA Lead: テスト計画 Issue 作成
    → Test Engineer x2: テストケース実装（parallel worktree）
    → Coverage Analyst: カバレッジレポート → ギャップ Issue
    → Quality Reviewer: 査読 → qa-approved / qa-NG
    → Bug Triage Agent: 発見バグを開発チームへ
```

## 開発チームとの連携

開発チームの `dev-workflow` と組み合わせる場合、  
`Bug Triage Agent` が `implementation` ラベルで開発チームへ Issue をハンドオフします。
