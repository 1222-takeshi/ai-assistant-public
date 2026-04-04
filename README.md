# ai-assistant

Claude Code / Codex 向けのマルチエージェント運用テンプレートです。  
開発チームの役割分担、`git worktree` ベースの並列開発、PMO 連携コマンドのたたき台を含みます。

## What This Repository Provides

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
- Notion / Jira / Confluence / Slack / Gmail 連携を前提にした PMO コマンドテンプレート

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
├── scripts/
├── templates/
└── tests/
```

## Quickstart

1. Python 3.11 以降を用意する
2. 依存を入れる

```bash
python -m pip install -r requirements-dev.txt
```

3. テストを実行する

```bash
pytest tests/ -v -p no:cacheprovider
```

4. `config/*.yaml` は public-safe なテンプレートとして扱い、実値は `config/*.local.yaml` のような未追跡ファイルに置く
5. もし config を分離運用するなら、`config/notion.example.yaml` と `config/confluence.example.yaml` をコピー元にする
6. 利用する MCP / CLI を接続する
   - `gh`
   - Notion MCP
   - Atlassian MCP
   - Google Calendar MCP
   - Slack MCP
   - Gmail MCP

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

## PMO Commands

PMO 関連のコマンドはそのままでは動きません。  
`config/` の設定と外部サービス接続を行った上で、自身のワークフローに合わせて調整してください。

- `/pmo/run-tasks`
- `/pmo/write-minutes`
- `/pmo/daily-routine`

## Making This Template Your Own

- `scripts/gh-workflow.sh` は `GH_REPO`、`--repo`、または `origin` remote から対象 repo を決定します
- `config/` の YAML は配布用テンプレートです。実運用値は `*.local.yaml` などの未追跡ファイルに分離してください
- `example` と `local override` の2段構えにするなら、`*.example.yaml` をコミット対象、`*.local.yaml` を ignored にするのが安全です
- `.claude/team-topology.yaml` の role / lane / worktree 名はそのままでも、チーム運用に合わせて変更しても構いません

## OSS Metadata

- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Code of Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Security: [SECURITY.md](SECURITY.md)
- Release Checklist: [docs/public-release-checklist.md](docs/public-release-checklist.md)
