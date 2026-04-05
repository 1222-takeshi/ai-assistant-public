# Data Science Team — 参考実装

> ⚠️ **これは参考実装です。** このチーム構成・ポリシーが唯一の正解ではありません。  
> あなたの組織に合わせて自由に変更してください。

## チーム概要

データ分析・機械学習・インサイト提供に特化したチームパターンです。  
「分析設計 → データ整備 → モデル開発 → レビュー → ビジネス共有」の流れを想定しています。

## ロール構成

| ロール | ID | 主な責任 |
|--------|-----|---------|
| Data Scientist | `data-scientist` | 仮説設定・分析設計・モデル評価・ビジネス示唆抽出 |
| ML Engineer | `ml-engineer` | モデル実装・チューニング・推論パイプライン |
| Data Engineer | `data-engineer` | データ収集・前処理・パイプライン整備 |
| Model Reviewer | `model-reviewer` | 公平性・精度・バイアスレビュー・本番投入可否判断 |
| Insight Reporter | `insight-reporter` | 分析結果のビジネス向けレポート・ダッシュボード仕様 |

## ワークフロー例

```
ビジネス課題 / 仮説
    ↓
Data Scientist: 分析設計・データ要件定義
    ↓
Data Engineer: データパイプライン構築
    ↓ (データ整備完了後)
ML Engineer: モデル実装・チューニング
    ↓ (実装完了後)
Model Reviewer: バイアス・精度・再現性レビュー
    ↓ NG → ML Engineer に差し戻し
    ↓ OK
Insight Reporter: ビジネス向けレポート・ダッシュボード
```

## セットアップ

```bash
cp examples/data-science-team/team-topology.yaml .claude/team-topology.yaml
```

ラベルを設定：

```bash
gh label create analysis --color 0075CA
gh label create model --color E4E669
gh label create data-pipeline --color 1D76DB
gh label create model-review-needed --color FBCA04
gh label create model-approved --color 0E8A16
gh label create bias-risk --color D93F0B
gh label create insight --color C2E0C6
```

## カスタマイズのポイント

- **レビュー基準**: Model Reviewer の NG 条件（バイアス閾値・精度要件）をチームで定義する
- **再現性要件**: 実験管理ツール（MLflow / DVC など）との連携を追加可能
- **モデルレジストリ**: 本番投入ゲートとして approval ラベルをモデルレジストリトリガーに使う構成も可能
- **少人数構成**: Data Scientist と ML Engineer を 1 名が兼務する構成も valid

## 関連ドキュメント

- [team-topology.yaml](team-topology.yaml)
- [examples/team-catalog.md](../team-catalog.md)
- [docs/framework.md](../../docs/framework.md)
