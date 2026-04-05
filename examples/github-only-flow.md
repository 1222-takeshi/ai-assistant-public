# GitHub-Only Happy Path

外部 SaaS（Notion / Jira / Confluence）なしで、このテンプレートの開発 workflow を  
**GitHub だけ**で完走する最小シナリオです。

## 前提条件

- `git` と `gh` が使える状態になっていること（`gh auth login` 済み）
- Python 3.11 以降（テスト実行時のみ）
- このリポジトリを fork またはテンプレートから作成済みであること

```bash
# 依存インストール（テスト実行時のみ必要）
python3 -m pip install -r requirements-dev.txt

# 環境確認
python3 scripts/doctor.py
./scripts/bootstrap.sh
```

---

## フロー概要

```text
[1] Issue 作成（Orchestrator / 誰でも可）
      ↓
[2] Requirements Review（Requirements Analyst → Reviewer）
      ↓ approved ラベル付与
[3] Implementation（Implementer）
      ↓ PR 作成 + review-needed ラベル
[4] PR Review（Reviewer）
      ↓ OK → approved ラベル / NG → PR 即 Close
[5] Merge（Orchestrator）
```

---

## ステップ詳細

### Step 1 — Issue 作成

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# requirements Issue を作成する
gh issue create \
  --repo "$REPO" \
  --title "requirements: add greeting feature" \
  --label "requirements" \
  --body-file examples/templates/issue-body.md
```

> サンプル: [examples/templates/issue-body.md](templates/issue-body.md)

---

### Step 2 — Requirements Review

Requirements Analyst がテスト仕様を含む要件 Issue を整理したら、Reviewer にレビューを依頼します。

```bash
ISSUE_NUMBER=<作成した Issue 番号>

# review-needed ラベルを付ける
gh issue edit "$ISSUE_NUMBER" \
  --repo "$REPO" \
  --add-label "review-needed"
```

**Reviewer の判定（超辛口）**:
- 🔴必須 0件 かつ 🟡推奨 2件以下 → ✅ OK
- 🔴必須 1件以上 または 🟡推奨 3件以上 → ❌ NG（再修正）

```bash
# OK の場合: ラベル切り替え
gh issue edit "$ISSUE_NUMBER" \
  --repo "$REPO" \
  --remove-label "review-needed" \
  --add-label "approved"
```

> サンプルコメント: [examples/templates/review-ok.md](templates/review-ok.md) / [review-ng.md](templates/review-ng.md)

---

### Step 3 — 実装 & PR 作成

要件 Issue に `approved` が付いたら実装を開始します。

```bash
# worktree を作成
./scripts/setup-worktree.sh impl-1 feat/greeting-feature
cd .claude/worktrees/impl-1

# 実装後にコミット
git add <変更ファイル>
git commit -m "feat: add greeting feature"

# push して PR 作成
./scripts/gh-workflow.sh push -b feat/greeting-feature
./scripts/gh-workflow.sh pr \
  --title "feat: add greeting feature" \
  --body-file examples/templates/pr-body.md \
  --label "review-needed"
```

> PR 本文サンプル: [examples/templates/pr-body.md](templates/pr-body.md)

---

### Step 4 — PR Review

```bash
PR_NUMBER=<作成した PR 番号>

# Reviewer が diff を確認
gh pr view "$PR_NUMBER" --repo "$REPO"
gh pr diff "$PR_NUMBER" --repo "$REPO"
gh pr checks "$PR_NUMBER" --repo "$REPO"
```

**OK の場合**:

```bash
gh pr review "$PR_NUMBER" --repo "$REPO" --comment \
  --body "$(cat examples/templates/review-ok.md)"

gh pr edit "$PR_NUMBER" \
  --repo "$REPO" \
  --remove-label "review-needed" \
  --add-label "approved"
```

**NG の場合（即 Close）**:

```bash
gh pr review "$PR_NUMBER" --repo "$REPO" --comment \
  --body "$(cat examples/templates/review-ng.md)"

gh pr close "$PR_NUMBER" \
  --repo "$REPO" \
  --comment "レビュー NG のため Close します。指摘事項を修正の上、新規ブランチ・新規 PR で再挑戦してください。"

gh pr edit "$PR_NUMBER" \
  --repo "$REPO" \
  --remove-label "review-needed"
```

NG の場合、実装者は Close された PR を再オープンせず、**新規ブランチ**で再実装します:

```bash
cd <repo-root>
git worktree remove .claude/worktrees/impl-1
git branch -D feat/greeting-feature

./scripts/setup-worktree.sh impl-1 feat/greeting-feature-v2
cd .claude/worktrees/impl-1
# 再実装 → Step 3 へ戻る
```

---

### Step 5 — Merge（Orchestrator）

```bash
# CI が pass しており approved ラベルが付いていることを確認
gh pr checks "$PR_NUMBER" --repo "$REPO"

gh pr merge "$PR_NUMBER" \
  --repo "$REPO" \
  --squash

# worktree クリーンアップ
cd <repo-root>
git worktree remove .claude/worktrees/impl-1
git branch -d feat/greeting-feature
```

---

## 自動化と手作業の境界

| ステップ | 自動化 | 手作業 |
|---------|--------|--------|
| Issue 作成 | `gh issue create` でコマンド化可能 | タイトル・内容の記述 |
| requirements review ラベル操作 | `gh issue edit` | レビュー判断・コメント記述 |
| worktree 作成 | `./scripts/setup-worktree.sh` | 実装コード作成 |
| push / PR 作成 | `./scripts/gh-workflow.sh` | PR 本文の記述 |
| review コメント | `gh pr review` | 判定・コメント内容の記述 |
| PR Close（NG 時） | `gh pr close` | レビュー判断 |
| Merge | `gh pr merge` | マージ判断 |

---

## dry-run 確認

実際に Issue / PR を作らずにコマンド構文だけ確認したい場合:

```bash
# gh コマンドのヘルプ確認
gh issue create --help
gh pr create --help

# scripts の dry-run 相当（実行はされない）
bash -n scripts/gh-workflow.sh
bash -n scripts/setup-worktree.sh
```

シナリオ全体の静的検証は以下で実行できます:

```bash
pytest tests/test_github_only_flow.py -v -p no:cacheprovider
```
