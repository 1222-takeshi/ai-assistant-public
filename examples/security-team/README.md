# Security Team — 参考実装

> **これは参考実装です。** このチーム構成・ポリシーが唯一の正解ではありません。  
> あなたの組織に合わせて自由に変更してください。

## チーム概要

セキュリティレビュー・脆弱性管理・コンプライアンス対応に特化したチームパターンです。

## ロール構成

| ロール | ID | 主な責任 |
|--------|-----|---------|
| Security Architect | `security-architect` | 設計レビュー・脅威モデリング・最終リスク判断 |
| Penetration Tester | `pen-tester` | 脆弱性スキャン・OWASP チェック・依存監査 |
| Compliance Reviewer | `compliance-reviewer` | 法規制準拠確認（GDPR / SOC2 / PCI-DSS）|
| Incident Responder | `incident-responder` | インシデント初動対応・ポストモーテム |

## ワークフロー例

```
定期スキャン / 脆弱性報告
    ↓
Pen Tester: スキャン・調査・Issue 作成
    ↓ (脆弱性発見後)
Security Architect: リスク評価・対応方針決定
    ↓
Compliance Reviewer: 法規制視点でのチェック
    ↓ (インシデント発生時は並行して)
Incident Responder: 初動対応・影響範囲特定
```

## セットアップ

```bash
cp examples/security-team/team-topology.yaml .claude/team-topology.yaml
```

ラベルを設定：

```bash
gh label create security-review --color C01A1A
gh label create vulnerability --color FF0000
gh label create compliance --color E99695
gh label create incident --color B60205
gh label create severity-critical --color B60205
gh label create severity-high --color D93F0B
gh label create severity-medium --color E4E669
gh label create severity-low --color 0E8A16
```

## カスタマイズのポイント

- **重大度基準**: severity-critical の定義を自組織のポリシーに合わせて調整
- **コンプライアンス要件**: GDPR / SOC2 / PCI-DSS 以外の規制が必要な場合はラベルと責任を追加
- **レビューポリシー**: severity-critical は即時対応必須などの SLA をチームで決める
- **外部ツール連携**: Snyk / Dependabot / Trivy などとの連携は各自の環境に合わせて設定

## 関連ドキュメント

- [team-topology.yaml](team-topology.yaml)
- [examples/team-catalog.md](../team-catalog.md)
- [docs/framework.md](../../docs/framework.md)
