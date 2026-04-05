# ai-assistant

[![CI](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Claude Code / Codex 向けのマルチエージェント運用テンプレートです。  
この OSS の core は、GitHub Issue 駆動の開発チーム workflow と `git worktree` ベースの並列開発です。  
PMO 連携は optional profile として分離し、core Quickstart には含めません。

## What This Repository Provides

### Core Workflow

- 開発チーム用のカスタムコマンド群
  - `/dev/start-team`
  - `/dev/status`
  - `/dev/orchestrate`
  - `/dev/research`
  - `/dev/define-requirements`
  - `/dev/implement`
  - `/dev/review`
- `.claude/team-topology.yaml` による役割・レーン・handoff の定義
- `scripts/setup-worktree.sh` を中心とした worktree 運用補助

### Optional PMO Profile

- Notion / Jira / Confluence / Slack / Gmail 連携を前提にした PMO コマンドテンプレート
- 詳細は [docs/pmo-profile.md](docs/pmo-profile.md)

## Repository Layout

```text
ai-assistant/
├── .claude/
│   ├── commands/
│   │   ├── dev/
│   │   └── pmo/
│   └── team-topology.yaml
├── config/
│   ├── notion.yaml
│   └── confluence.yaml
├── docs/
├── examples/
│   ├── github-only-flow.md   ← GitHub-only happy path walkthrough
│   └── templates/            ← Issue / PR / review サンプル成果物
├── scripts/
├── templates/
└── tests/
```

## Quickstart

1. Python 3.11 以降を用意する
2. `gh` と `git` を使える状態にする
3. 依存を入れる

```bash
python3 -m pip install -r requirements-dev.txt
```

4. テストを実行する

```bash
pytest tests/ -v -p no:cacheprovider
```

5. 非破壊な bootstrap を実行する

```bash
./scripts/bootstrap.sh
```

6. doctor で環境を確認する

```bash
python3 scripts/doctor.py
```

7. tracked config template の状態を確認する

```bash
python3 scripts/validate-config.py --tracked-only
```

8. `.claude/team-topology.yaml` と `/dev/start-team` を source of truth として開発フローを開始する
9. PMO profile が必要な場合だけ [docs/pmo-profile.md](docs/pmo-profile.md) を参照する

## GitHub-Only Happy Path

外部 SaaS なしで開発 workflow を完走したい場合は、**[examples/github-only-flow.md](examples/github-only-flow.md)** を参照してください。

```
Issue 作成 → Requirements Review → 実装 → PR 作成 → PR Review → Merge
```

- `gh` と `git` だけで全ステップを実行できます
- サンプル Issue / PR / review コメントは [examples/templates/](examples/templates/) にあります
- エージェントチームが実際に動く様子は [examples/agent-team-demo/](examples/agent-team-demo/) を参照してください
- Reviewer は超辛口（🔴必須 1件以上または🟡推奨 3件以上で即 NG・PR 即 Close）

## Development Team Workflow

開発チームの source of truth は `.claude/team-topology.yaml` です。  
このファイルに以下を定義しています。

- ロールとコマンドの対応
- 各レーンの capacity
- worktree の割り当て
- GitHub label の意味
- handoff の流れ

worktree 作成前は `scripts/worktree-cleanup.sh` で stale metadata を prune し、
`scripts/setup-worktree.sh` から `.claude/worktrees/` 配下に追加します。

```bash
./scripts/setup-worktree.sh impl-1 feat/my-feature
./scripts/list-worktrees.sh
```

PR review flow の詳細は [docs/pr-review-flow.md](docs/pr-review-flow.md) を参照してください。

## Optional PMO Profile

PMO 関連のコマンドは optional profile です。  
core workflow を使うだけなら設定不要です。使う場合だけ `config/` と外部サービス接続を準備してください。

- `/pmo/run-tasks`
- `/pmo/write-minutes`
- `/pmo/daily-routine`

詳細は [docs/pmo-profile.md](docs/pmo-profile.md) を参照してください。

## Making This Template Your Own

- onboarding は [docs/onboarding.md](docs/onboarding.md) から開始できます
- `./scripts/bootstrap.sh` は非破壊な初期化補助です。`--init-pmo-config` を付けた場合だけ `*.local.yaml` を生成します
- `python3 scripts/doctor.py` は success / warning / failure で環境状態を返します
- `scripts/gh-workflow.sh` は `GH_REPO`、`--repo`、または `origin` remote から対象 repo を決定します
- PR review flow は [docs/pr-review-flow.md](docs/pr-review-flow.md) を source of truth とし、same identity の `COMMENTED` review を正式 approval gate にしません
- reviewer request は `./scripts/gh-workflow.sh pr --reviewer ...` または `./scripts/gh-workflow.sh request-review --pr ... --reviewer ...` で行えます
- 暫定運用では `review-needed` を外して `approved` ラベルで状態管理しますが、これは GitHub の formal `APPROVED` review と同義ではありません
- `config/*.yaml` は tracked template、`config/*.example.yaml` はコピー元サンプル、`config/*.local.yaml` は ignored な local override です
- 実行時の優先順位は `local > tracked template` です。`example` は runtime に入りません
- 実運用値は tracked file に書かず、`*.local.yaml` に分離してください
- 変更後は `python3 scripts/validate-config.py --check-local` で local override を検証してください
- `.claude/team-topology.yaml` の role / lane / worktree 名はそのままでも、チーム運用に合わせて変更しても構いません
- PMO を使わない利用者は `docs/pmo-profile.md` を無視して構いません

## OSS Metadata

- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Code of Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Security: [SECURITY.md](SECURITY.md)
- Release Checklist: [docs/public-release-checklist.md](docs/public-release-checklist.md)
- Onboarding: [docs/onboarding.md](docs/onboarding.md)
- PR Review Flow: [docs/pr-review-flow.md](docs/pr-review-flow.md)
- PMO Profile: [docs/pmo-profile.md](docs/pmo-profile.md)
