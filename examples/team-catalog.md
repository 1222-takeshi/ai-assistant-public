# Team Catalog — チーム構成パターン一覧

AI エージェントチームの構成例をカタログ形式で掲載しています。  
これらは**参考実装です**。あなたのチームに合わせて自由に組み合わせ・改変してください。

> ⚠️ このカタログに記載されたロール名・構成・ポリシーはすべて **提案** です。
> 強要するものではありません。

---

## 目次

| カテゴリ | 構成例 |
|---------|--------|
| [経営・戦略](#executive-team) | CEO / CTO / CFO / Chief of Staff |
| [ソフトウェア開発](#dev-team) | Orchestrator / Researcher / Requirements Analyst / Implementer / Reviewer |
| [QA・品質保証](#qa-team) | QA Lead / Test Engineer / Coverage Analyst / Quality Reviewer |
| [セキュリティ](#security-team) | Security Architect / Pen Tester / Compliance Reviewer |
| [フィールドエンジニアリング](#field-engineering-team) | Field Lead / Site Engineer / Customer Success / Escalation Handler |
| [管理・バックオフィス](#admin-support-team) | Executive Secretary / Finance Analyst / HR Coordinator / Legal Checker |
| [データサイエンス](#data-science-team) | Data Scientist / ML Engineer / Data Engineer / Model Reviewer |
| [ドキュメント・技術広報](#docs-team) | Tech Writer / API Doc Specialist / Reviewer / Publisher |
| [PMO（プロジェクト管理）](#pmo-team) | PMO Lead / Task Tracker / Minutes Writer / Status Reporter |
| [自由構成の例](#custom-examples) | 1人運用 / 小規模チーム / ハイブリッド |

---

## 経営・戦略チーム {#executive-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **CEO** (Chief Executive Agent) | ビジョン策定・最終意思決定・ステークホルダーへの報告 |
| **CTO** (Chief Technology Agent) | 技術戦略・アーキテクチャ判断・技術リスク評価 |
| **CFO** (Chief Finance Agent) | 予算管理・コスト分析・財務レポート作成 |
| **Chief of Staff** | 情報集約・アジェンダ作成・フォローアップ管理 |
| **Strategy Analyst** | 市場調査・競合分析・戦略オプション整理 |

### 典型的なフロー

```
Strategy Analyst: 市場調査 → Issue に調査結果を記録
    → Chief of Staff: 情報集約 → 経営会議アジェンダ作成
    → CEO + CTO + CFO: 意思決定セッション
    → Chief of Staff: 決定事項を Action Item として Issue 化
    → 各部門エージェントへハンドオフ
```

### 推奨ラベル

```
strategic-review  / budget-approval / architecture-decision
pending-ceo       / pending-cto      / pending-cfo
approved-exec     / blocked-exec
```

### topology スニペット

```yaml
lanes:
  - id: ceo
    role: decision-maker
    responsibility: final decisions, stakeholder reporting
  - id: cto
    role: tech-strategy
    responsibility: architecture, tech risk, vendor decisions
  - id: cfo
    role: finance-strategy
    responsibility: budget, cost analysis, financial reports
  - id: chief-of-staff
    role: coordinator
    responsibility: agenda, follow-up, information aggregation
  - id: strategy-analyst
    role: researcher
    responsibility: market research, competitive analysis
```

### 参考実装

→ [examples/executive-team/](executive-team/)

</details>

---

## ソフトウェア開発チーム {#dev-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **Orchestrator** | スプリント計画・エージェント調整・merge 判断 |
| **Researcher** | 技術調査・調査結果を GitHub Issue に記録 |
| **Requirements Analyst** | 要件定義・テスト仕様作成 |
| **Implementer** | 実装・PR 作成（git worktree で並列作業） |
| **Reviewer** | コードレビュー（ポリシーは自由に設定） |

### 典型的なフロー

```
Orchestrator → Researcher (調査) → Requirements Analyst (要件定義)
    → Implementer (実装 + PR) → Reviewer (レビュー) → Orchestrator (merge)
```

### レビューポリシーの例

> ポリシーは自由です。以下は一例です。

```yaml
# 例A: 超辛口（このリポジトリのデフォルト）
ng_threshold: "🔴>=1 OR 🟡>=3"
on_ng: "gh pr close immediately, no reopen"

# 例B: 標準
ng_threshold: "🔴>=1"
on_ng: "request changes, allow fix"

# 例C: 寛容（学習・実験目的）
ng_threshold: "🔴>=3"
on_ng: "suggest improvements, merge anyway with note"
```

### 参考実装（完全版）

→ [examples/dev-workflow/](dev-workflow/)  
コマンド実装・topology・demo を含む完全な参考実装です。

</details>

---

## QA・品質保証チーム {#qa-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **QA Lead** | テスト計画立案・品質基準定義・最終品質判断 |
| **Test Engineer** | テストケース設計・自動テスト実装・実行 |
| **Coverage Analyst** | カバレッジ計測・未テスト領域特定・レポート |
| **Bug Triage Agent** | バグ重要度分類・再現手順整理・開発チームへのエスカレ |
| **Quality Reviewer** | テスト成果物の査読・品質ゲート判断 |

### 典型的なフロー

```
QA Lead: テスト計画 Issue 作成
    → Test Engineer x2: テストケース設計・実装（parallel worktree）
    → Coverage Analyst: カバレッジレポート → ギャップ Issue 作成
    → Quality Reviewer: 査読 → approved / NG
    → Bug Triage Agent: 発見バグを開発チームへハンドオフ
```

### 推奨ラベル

```
test-plan / test-case / coverage-gap / bug / triage
qa-review-needed / qa-approved / qa-blocked
```

### 参考実装

→ [examples/qa-team/](qa-team/)

</details>

---

## セキュリティチーム {#security-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **Security Architect** | セキュリティ設計レビュー・脅威モデリング |
| **Pen Tester** | 脆弱性調査・OWASP チェック・依存パッケージ監査 |
| **Compliance Reviewer** | 法規制・社内ポリシー準拠確認（GDPR / SOC2 等） |
| **Incident Responder** | インシデント発生時の初動対応・影響範囲特定 |

### 典型的なフロー

```
Security Architect: 設計レビュー Issue
    → Pen Tester: 脆弱性スキャン → 発見 Issue 作成
    → Compliance Reviewer: 法規制チェック → 非準拠 Issue 作成
    → Security Architect: 総合判断 → approved / NG (escalate)
```

### 推奨ラベル

```
security-review / vulnerability / compliance / incident
severity-critical / severity-high / severity-low
```

### 参考実装

→ [examples/security-team/](security-team/)

</details>

---

## フィールドエンジニアリングチーム {#field-engineering-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **Field Lead** | 現場訪問計画・エスカレーション判断・顧客折衝 |
| **Site Engineer** | 現場作業ドキュメント作成・技術報告書・手順書整備 |
| **Customer Success Agent** | 顧客フィードバック収集・満足度分析・改善提案 |
| **Escalation Handler** | 重大障害の社内エスカレーション・一次対応手順作成 |
| **Knowledge Base Agent** | 現場知見のナレッジ化・FAQ 更新・マニュアル整備 |

### 典型的なフロー

```
Site Engineer: 現場報告 Issue 作成（作業ログ・問題点）
    → Customer Success Agent: 顧客フィードバック整理
    → Escalation Handler: 重大度判断 → 必要なら開発チームへ
    → Knowledge Base Agent: 解決策をナレッジベースに反映
    → Field Lead: 最終承認・次回訪問計画
```

### 推奨ラベル

```
field-report / customer-feedback / escalation / knowledge-base
site-visit / resolved / pending-dev
```

### 参考実装

→ [examples/field-engineering-team/](field-engineering-team/)

</details>

---

## 管理・バックオフィスチーム {#admin-support-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **Executive Secretary** | スケジュール管理・議事録作成・メール下書き・調整業務 |
| **Finance Analyst** | 経費精算チェック・予算実績管理・財務レポート作成 |
| **Budget Controller** | 予算超過アラート・コスト配分分析・承認フロー管理 |
| **HR Coordinator** | 採用管理・オンボーディング資料整備・勤怠集計 |
| **Legal Checker** | 契約書レビュー・コンプライアンス確認・リスク洗い出し |
| **Procurement Agent** | 発注・見積比較・ベンダー管理・稟議資料作成 |

### 典型的なフロー（財務）

```
Finance Analyst: 月次経費集計 → Issue 化
    → Budget Controller: 予算比較・超過チェック
    → Legal Checker: 契約上の支払い条件確認
    → Executive Secretary: 承認依頼メール作成 → 経営層へ
```

### 典型的なフロー（秘書業務）

```
Executive Secretary: 会議アジェンダ作成 Issue
    → 参加者調整・日程候補整理
    → 議事録ドラフト → Reviewer
    → 承認後、Action Item を各担当 Issue に変換
```

### 推奨ラベル

```
finance / budget / expense / legal / hr / procurement
pending-approval / approved-exec / requires-signature
```

### 参考実装

→ [examples/admin-support-team/](admin-support-team/)

</details>

---

## データサイエンスチーム {#data-science-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **Data Scientist** | 仮説設定・分析設計・モデル評価 |
| **ML Engineer** | モデル実装・パイプライン構築・パフォーマンス最適化 |
| **Data Engineer** | データ収集・前処理・データパイプライン整備 |
| **Model Reviewer** | モデルの公平性・精度・バイアスレビュー |
| **Insight Reporter** | 分析結果をビジネス向けレポートに変換 |

### 参考実装

→ [examples/data-science-team/](data-science-team/)

</details>

---

## ドキュメント・技術広報チーム {#docs-team}

<details>
<summary>詳細を表示</summary>

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **Tech Writer** | API ドキュメント・ユーザーガイド・リリースノート作成 |
| **API Doc Specialist** | OpenAPI / コードコメントからドキュメント自動生成 |
| **Doc Reviewer** | 正確性・一貫性・可読性レビュー |
| **Localization Agent** | 多言語翻訳・ローカライズ品質確認 |
| **Publisher** | ドキュメントサイト更新・バージョン管理・公開承認 |

### 参考実装

> ⚠️ **TODO**: `examples/docs-team/` は現時点では未作成です。  
> 構成例は [examples/dev-workflow/](dev-workflow/) の review / implement コマンドを参考にドキュメント用途向けに改変してください。

</details>

---

## PMO（プロジェクト管理）チーム {#pmo-team}

<details>
<summary>詳細を表示</summary>

> 外部サービス（Notion / Atlassian / GCal / Slack / Gmail）との連携が前提です。

### 役割定義

| ロール | 主な責務 |
|--------|---------|
| **PMO Lead** | プロジェクト状態管理・リスク管理・ステークホルダー報告 |
| **Task Tracker** | Notion / Jira タスクの自動同期・ステータス更新 |
| **Minutes Writer** | 会議議事録の自動生成（GCal + Slack + Gmail 連携） |
| **Status Reporter** | 日次・週次レポート自動生成 |

### 参考実装（完全版）

→ [examples/pmo-workflow/](pmo-workflow/)  
Notion MCP / Atlassian MCP を使った完全な参考実装です。

</details>

---

## 自由構成の例 {#custom-examples}

### 1人運用（ソロ Orchestrator）

```yaml
# 1人のエージェントがすべての役割を担う最小構成
lanes:
  - id: solo
    role: all-rounder
    responsibility: research, plan, implement, review (自己レビュー)
```

> 自己レビューはバイアスがかかりやすいため、重要な変更は別セッションで実施することを推奨します。

### 小規模チーム（3エージェント）

```yaml
lanes:
  - id: planner
    role: orchestrator + requirements-analyst
    responsibility: prioritize, define requirements
  - id: builder
    role: implementer
    responsibility: implement, create PR
  - id: checker
    role: reviewer + qa
    responsibility: review + basic QA
```

### ハイブリッド（開発 × 経営）

```yaml
# 経営判断が必要な機能開発に有効
lanes:
  - id: cto-agent
    role: tech-strategy
    responsibility: architecture decisions, prioritization
  - id: implementer
    role: implementer
    responsibility: implementation
  - id: cfo-agent
    role: cost-review
    responsibility: infrastructure cost impact review before merge
```

---

## チーム構成を選ぶ指針

| あなたの状況 | 推奨パターン |
|------------|-------------|
| ソフトウェア開発チームを運用したい | `dev-workflow` |
| 品質・テストに特化したい | `qa-team` |
| 経営・戦略意思決定を自動化したい | `executive-team` |
| 現場作業のドキュメント化・ナレッジ化 | `field-engineering-team` |
| 秘書・財務・HR 業務の補助 | `admin-support-team` |
| セキュリティレビューを組み込みたい | `security-team` を `dev-workflow` に追加 |
| 複数チームをまたいだプロジェクト管理 | `pmo-team` |
| 小さく始めたい | 1人運用 or 小規模チームから開始 |

---

## セットアップ手順

1. このカタログから自分のチームに合ったパターンを選ぶ
2. 対応する `examples/<team>/` ディレクトリを参照する
3. `team-topology.yaml` を `.claude/team-topology.yaml` にコピーして編集
4. コマンドファイルを `.claude/commands/<category>/` にコピーして編集
5. 必要に応じてラベルをカスタマイズして `./scripts/setup-labels.sh` を実行

詳細は [docs/customization.md](../docs/customization.md) を参照してください。
