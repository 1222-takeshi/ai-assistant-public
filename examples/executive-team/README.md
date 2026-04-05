# Executive Team — 経営・戦略チーム（参考実装）

> ⚠️ **これは参考実装です。** 自由に変更・拡張してください。

---

## 役割定義

| ロール | 主な責務 |
|--------|---------|
| CEO | ビジョン策定・最終意思決定・ステークホルダー報告 |
| CTO | 技術戦略・アーキテクチャ判断・技術リスク評価 |
| CFO | 予算管理・コスト分析・財務レポート |
| Chief of Staff | 情報集約・アジェンダ管理・フォローアップ |
| Strategy Analyst | 市場調査・競合分析・戦略オプション整理 |

## 典型的なフロー

```
Strategy Analyst: 市場調査 → Issue に調査結果
    → Chief of Staff: 情報集約 → 経営会議アジェンダ作成
    → CEO + CTO + CFO: 意思決定
    → Chief of Staff: Action Item を Issue 化 → 各部門へハンドオフ
```

## セットアップ手順

```bash
cp examples/executive-team/team-topology.yaml .claude/team-topology.yaml
# topology を自社の経営体制に合わせて編集
```

コマンドファイルは含まれていません。  
[docs/customization.md](../../docs/customization.md) を参考に `.claude/commands/exec/` を作成してください。
