# Framework vs Examples

このドキュメントでは、**ai-assistant** の「フレームワーク部分」と「参考実装（Examples）部分」の境界を明確にします。

---

## 考え方

```
┌─────────────────────────────────────────────────────────┐
│                    Framework (共通基盤)                   │
│  ・git worktree による並列作業の仕組み                     │
│  ・GitHub Issues を調整レイヤーとして使うパターン           │
│  ・ラベルによる状態管理                                    │
│  ・設定ファイルの layering (local > tracked)              │
│  ・スクリプト群 (bootstrap / doctor / validate / worktree)│
│  ・.claude/commands/ のファイル構造                       │
└────────────────────┬────────────────────────────────────┘
                     │ 上に積み重ねる
┌────────────────────▼────────────────────────────────────┐
│              Examples (参考実装 — opt-in)                 │
│  ・examples/dev-workflow/     ソフトウェア開発チーム例     │
│  ・examples/pmo-workflow/     PMO チーム例                │
│  ・examples/executive-team/   経営チーム例                │
│  ・examples/qa-team/          QA チーム例                 │
│  ・examples/field-engineering-team/  FE チーム例          │
│  ・examples/admin-support-team/      管理部門チーム例      │
│  ・examples/security-team/    セキュリティチーム例         │
│  ・examples/data-science-team/ データサイエンスチーム例    │
└─────────────────────────────────────────────────────────┘
```

---

## フレームワーク部分（変更不要・汎用）

以下はどのチーム構成でも共通して使える基盤です。カスタマイズは不要です。

| ファイル / ディレクトリ | 役割 |
|----------------------|------|
| `scripts/bootstrap.sh` | 非破壊な環境初期化 |
| `scripts/doctor.py` | 環境ヘルスチェック |
| `scripts/validate-config.py` | 設定ファイル整合性確認 |
| `scripts/setup-worktree.sh` | git worktree 作成 |
| `scripts/worktree-cleanup.sh` | worktree 削除 |
| `scripts/setup-labels.sh` | GitHub ラベル作成 |
| `config/*.yaml` (テンプレート) | 設定の公開安全なテンプレート |
| `.github/workflows/test.yml` | CI |
| `.github/copilot-setup-steps.yml` | Copilot 環境 bootstrap |
| `.github/ISSUE_TEMPLATE/` | Issue テンプレート群 |

---

## 参考実装部分（カスタマイズ前提）

以下は **このリポジトリが採用している一例** であり、あなたのチームに合わせて自由に置き換えてください。

| ファイル / ディレクトリ | 内容 | 変更方法 |
|----------------------|------|---------|
| `.claude/commands/dev/` | ソフトウェア開発ワークフロー | `examples/` から別のワークフローをコピー |
| `.claude/commands/pmo/` | PMO ワークフロー | 不要なら削除 |
| `.claude/team-topology.yaml` | チーム構成定義 | `examples/` の topology を参考に書き換え |
| `CLAUDE.md` の開発ルール | このリポジトリの運用ルール | あなたのチームのルールに書き換え |
| `AGENTS.md` のロール定義 | エージェントへの説明 | あなたのチームの構成に書き換え |

---

## よくある質問

### Q: dev/ コマンドを使わないといけませんか？

**いいえ。** `dev/` ワークフローはこのリポジトリが採用している一例です。
`examples/` から自分のチームに合ったワークフローをコピーして `.claude/commands/` に置いてください。

### Q: Reviewer は超辛口にしないといけませんか？

**いいえ。** ultra-strict Reviewer ポリシーはこのリポジトリの設定です。
あなたのチームに合ったポリシーを `review.md` に書いてください。

### Q: Orchestrator や Researcher は必須ですか？

**いいえ。** ロール構成は自由です。
1人のエージェントが複数の役割を兼ねても、まったく異なる役割名を使っても問題ありません。
`examples/team-catalog.md` に様々なチーム構成例があります。

### Q: GitHub Issues を使わないといけませんか？

フレームワークとして GitHub Issues ベースのパターンを推奨していますが、
ローカルファイルベースや別の Issue トラッカーをコマンド内で参照することも可能です。

---

## 関連ドキュメント

- [examples/team-catalog.md](../examples/team-catalog.md) — チーム構成パターン一覧
- [docs/customization.md](customization.md) — カスタマイズ手順
- [docs/architecture.md](architecture.md) — システム構成図
