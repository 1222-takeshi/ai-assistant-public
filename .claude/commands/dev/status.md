# /dev/status — Development Team Status Dashboard

あなたは **ai-assistant** 開発チームの稼働状況を可視化するオペレータです。  
`.claude/team-topology.yaml` を基準に、GitHub と git worktree の状態を突き合わせ、
Researcher / Requirements Analyst / Implementer / Reviewer の稼働状況、
レビュー滞留、ブロッカーを 1 画面で把握できるようにします。

## 参照元

- `.claude/team-topology.yaml`
- `CLAUDE.md`
- GitHub Issues / PRs
- `git worktree list`

## 実行フロー

以下では必要に応じて `REPO="${GH_REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"` を事前に設定する。

### 1. レポジトリ状態の確認

```bash
gh issue list --repo "$REPO" --state open
gh issue list --repo "$REPO" --label "blocked" --state open
gh issue list --repo "$REPO" --label "review-needed" --state open
gh issue list --repo "$REPO" --label "implementation" --state open
gh issue list --repo "$REPO" --label "research" --state open
gh pr list --repo "$REPO" --state open
git worktree list
```

### 2. ロール別の見立て

- **Researcher**: `research` Issue の件数と重複テーマの有無
- **Requirements Analyst**: `requirements` / `review-needed` Issue の滞留
- **Implementer**: `implementation` Issue と対応ブランチ・worktree の存在
- **Reviewer**: `review-needed` requirements / PR の滞留状況
- **ブロッカー**: `blocked` ラベルの有無と、誰が次に受けるべきか

### 3. 判定ルール

- `blocked` が 1 件でもあれば最上段に表示する
- `review-needed` がある場合、Reviewer を busy と見なす
- `approved` requirements がある場合、Implementer の空きレーンへ候補として表示する
- worktree が不足している、または余分に残っている場合は明示する

## 出力フォーマット

```markdown
## Development Team Status

### ブロッカー
- {issue or なし}

### Researchers
- Researcher 1: {assigned theme or idle}
- Researcher 2: {assigned theme or idle}

### Requirements Analyst
- {issue or idle}

### Implementers
- Implementer 1: {branch / issue / idle}
- Implementer 2: {branch / issue / idle}

### Reviewer
- {review target or idle}

### Queue Hints
- Ready for implementation: {approved requirements}
- Ready for review: {review-needed items}
- Needs clarification: {untriaged requests}
```

## 注意事項

- 状態の source of truth は `.claude/team-topology.yaml` と GitHub のラベル
- worktree の状態は `git worktree list` を優先する
- 不整合がある場合は Orchestrator にエスカレーションする
