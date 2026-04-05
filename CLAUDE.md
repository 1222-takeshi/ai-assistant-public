# ai-assistant

Claude Code / Codex / GitHub Copilot 向けの **AI エージェントチーム運用フレームワーク**。  
このリポジトリの core は「仕組み（フレームワーク）」であり、`dev` workflow は参考実装の一つです。

## プロジェクト概要

- **目的**: AI エージェントチームの運用に必要な仕組みを提供するフレームワーク
- **アーキテクチャ**: マルチエージェント並列作業 + GitHub Issues 調整レイヤー
- **設計方針**: フレームワーク部分は汎用的に、チーム構成・ポリシーは利用者が自由に定義する
- **このリポジトリの設定**: `dev` workflow を採用（参考実装。置き換え可）。`pmo` は opt-in profile

## ディレクトリ構成

```text
ai-assistant/
├── CLAUDE.md
├── .gitignore
├── .gemini_temp/               # 一時ドキュメント（git 管理外）
├── scripts/
│   ├── gh-workflow.sh
│   ├── setup-worktree.sh
│   ├── worktree-cleanup.sh
│   └── list-worktrees.sh
└── .claude/
    ├── team-topology.yaml
    ├── settings.local.json     # ローカル環境用。通常は git 管理外
    ├── worktrees/
    └── commands/
        ├── dev/
        └── pmo/
```

## カスタムコマンド一覧

### Core Workflow（dev/）

| コマンド | 用途 |
|---------|------|
| `/dev/start-team` | Claude Code のコンテキスト確認・日次起動・担当レーン割り当て |
| `/dev/status` | チームの稼働状況・ブロッカー・review 待ちを可視化 |
| `/dev/orchestrate` | 全エージェント状態俯瞰・開発着手判断・PR マージ判断 |
| `/dev/research` | 技術調査・成果物を GitHub Issue に記録 |
| `/dev/define-requirements` | 要件定義・テスト仕様設計・実装依頼発行 |
| `/dev/implement` | GitHub Issue から実装・PR 作成 |
| `/dev/review` | 要件・設計・テスト仕様・PR の多段レビュー |

### Optional Profile（pmo/）

| コマンド | 用途 |
|---------|------|
| `/pmo/run-tasks` | Notion タスクを読み込み Jira / Confluence を自動実行 |
| `/pmo/write-minutes` | GCal + Slack + Gmail から議事録の草案を生成 |
| `/pmo/daily-routine` | 毎朝ルーティン（確認→自動実行→日次レポート） |

PMO の詳細は `docs/pmo-profile.md` を参照すること。core workflow の開始条件には含めない。

## マルチエージェント開発アーキテクチャ

```text
Orchestrator (1名)
  ├─→ Requirements Analyst (1名) → Reviewer → Implementer x2
  └─→ Researcher x2
```

### 運用の source of truth

- `CLAUDE.md`: 全体方針、ラベル、基本ルール
- `.claude/team-topology.yaml`: ロール定義、担当レーン、worktree、handoff
- `/dev/start-team`: 起動時の入口
- `/dev/status`: 稼働状況の可視化

PMO profile は補助的な opt-in profile であり、上記 source of truth を置き換えない。

### git worktree 戦略

```bash
# 管理用リポジトリ
<repo-root>/

# 実装者用 worktree
./scripts/setup-worktree.sh impl-1 feat/<feature-a>
./scripts/setup-worktree.sh impl-2 feat/<feature-b>
```

- worktree は `.claude/worktrees/` 配下に作成する
- 同一ディレクトリでの頻繁な `git checkout` は避ける

## GitHub Labels

| Label | 用途 |
|-------|------|
| `research` | 調査者が作成した Issue |
| `requirements` | 要件定義者が作成した Issue |
| `implementation` | 実装依頼 Issue |
| `review-needed` | レビュー待ち |
| `approved` | Reviewer OK 済み |
| `blocked` | ブロッカーあり |

## 補助スクリプト

```bash
# origin から対象 repo を推定、または GH_REPO/--repo を使用
./scripts/gh-workflow.sh push -b feat/my-feature
./scripts/gh-workflow.sh pr --title "feat: add X" --body-file .gemini_temp/pr_body.md --reviewer codex-reviewer
./scripts/gh-workflow.sh issue --title "Bug: something wrong" --body-file .gemini_temp/issue_body.md
./scripts/gh-workflow.sh request-review --pr 123 --reviewer codex-reviewer
./scripts/bootstrap.sh
python3 scripts/doctor.py
python3 scripts/validate-config.py --tracked-only
python3 scripts/validate-config.py --check-local
```

## 開発ルール（このリポジトリの設定）

> 以下はこのリポジトリが採用しているルールです。  
> あなたのチームに合わせて自由に変更してください。

- `main` への直接 push はしない
- コミットメッセージと PR タイトルは英語・Conventional Commits 形式を推奨
- PR 本文、コードコメント、運用ドキュメントは日本語でもよい
- テストは `pytest tests/ -v -p no:cacheprovider` を基準にする
- same identity の `COMMENTED` review は正式な approval gate とみなさない
- PR review flow の詳細は `docs/pr-review-flow.md` を source of truth とする
- 暫定運用でも `review-needed` は外し、`approved` は review 結果 OK を示すラベルとして使う
- **このリポジトリのReviewerポリシー**: 🔴必須 1件以上 または 🟡推奨 3件以上で即 NG・PR を即 Close
  - ※ これはこのリポジトリの選択です。別のポリシー（修正ループ許容など）も valid です

## Onboarding

- `./scripts/bootstrap.sh` は非破壊な初期化補助
- `./scripts/bootstrap.sh --init-pmo-config` は optional PMO profile 用の `*.local.yaml` を未存在時だけ生成
- `python3 scripts/doctor.py` は success / warning / failure で環境状態を返す
- onboarding の説明は `docs/onboarding.md` を source of truth とする

## PMO テンプレートの前提

PMO 機能は optional profile であり、外部サービスの接続が前提です。

- Notion MCP
- Atlassian MCP
- Google Calendar MCP
- Slack MCP
- Gmail MCP

`config/notion.yaml` と `config/confluence.yaml` は OSS 配布用テンプレートです。  
`YOUR_*` の値を各自の環境に置き換えず、実値は `*.local.yaml` のような未追跡ファイルに分離してください。

### config の運用方針

- tracked な `config/*.yaml` は public-safe な template として維持する
- `config/*.example.yaml` はコピー元サンプルであり、runtime の優先順位には入れない
- 実運用値は `config/*.local.yaml` に置き、git へ入れない
- 優先順位は `local > tracked template` とする
- config 変更後は `python3 scripts/validate-config.py --tracked-only` または `--check-local` で整合性を確認する

### セットアップ手順

1. core workflow を使う場合は、このセクションを読まずに `README.md` の Quickstart に従う
2. PMO profile を使う場合だけ必要な MCP / CLI を追加する
3. `config/notion.yaml` を直接編集せず、`config/notion.local.yaml` などの未追跡ファイルに実値を置く
4. `config/confluence.yaml` も同様に `config/confluence.local.yaml` へ分離する
5. `python3 scripts/validate-config.py --check-local` で local override を検証する
6. `/pmo/run-tasks --dry-run` で接続確認する
