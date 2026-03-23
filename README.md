# ai-assistant

Claude Code を中心に、開発エージェントと PMO エージェントを運用する実験用リポジトリです。

## Development team entrypoints

- `/dev/start-team` — `CLAUDE.md` と `.claude/team-topology.yaml` を確認して、開発チームを起動する
- `/dev/status` — Researcher / Requirements Analyst / Implementer / Reviewer の稼働状況を確認する
- `/dev/orchestrate` — 優先度判断、着手判断、最終マージ判断を行う

## Development team topology

開発チームの source of truth は `.claude/team-topology.yaml` です。  
このファイルに以下を明示しています。

- ロールとコマンドの対応
- 各レーンの capacity
- worktree の割り当て
- GitHub label の意味
- handoff の流れ

## Worktree safety

worktree 作成前は `scripts/worktree-cleanup.sh` で stale metadata を prune し、
`scripts/setup-worktree.sh` から安全に `.claude/worktrees/` 配下へ追加します。
