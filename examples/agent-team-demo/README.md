# Agent Team Demo

> ⚠️ **このデモはフィクションです。**  
> 登場するユーザー名・Issue 番号・PR 番号・コードはすべて架空のものです。  
> 実際のリポジトリや人物とは関係ありません。

---

## デモ概要

**題材**: `hello` コマンド（`scripts/hello.sh`）を新規追加する feature  
**目的**: エージェントチームが実際にどう動くか、成果物がどう見えるかを示す

## 登場エージェント

| エージェント | ロール |
|------------|--------|
| @orchestrator | Orchestrator — sprint 起動・merge 判断 |
| @researcher-1 | Researcher — 技術調査 |
| @req-analyst | Requirements Analyst — 要件定義 |
| @impl-1 | Implementer 1 — 実装・PR 作成 |
| @reviewer | Reviewer (ultra-strict) |

## ファイル構成

| ファイル | 内容 |
|---------|------|
| [01-requirements-issue.md](01-requirements-issue.md) | requirements Issue の完成例 |
| [02-requirements-review-ok.md](02-requirements-review-ok.md) | requirements レビュー OK コメント例 |
| [03-pr-body.md](03-pr-body.md) | 実装 PR 本文例 |
| [04-review-ok.md](04-review-ok.md) | コードレビュー OK コメント例 |
| [05-review-ng.md](05-review-ng.md) | コードレビュー NG コメント例（即時 close） |

## フロー

```
@orchestrator: /dev/start-team
  → @researcher-1: /dev/research → Issue #51 (調査結果)
  → @req-analyst: /dev/define-requirements → Issue #52 (requirements)
  → @reviewer: /dev/review (requirements) → approved
  → @impl-1: /dev/implement → feat/add-hello-command → PR #53
  → @reviewer: /dev/review (PR) → NG → PR close
  → @impl-1: 新ブランチ feat/add-hello-command-v2 → PR #54
  → @reviewer: /dev/review (PR) → OK → merge
  → @orchestrator: Issue #52 close
```

## 関連ドキュメント

- [examples/github-only-flow.md](../github-only-flow.md) — コマンドベースの手順
- [docs/architecture.md](../../docs/architecture.md) — システム構成図
- [.claude/commands/dev/](../../.claude/commands/dev/) — 各エージェントのコマンド定義
