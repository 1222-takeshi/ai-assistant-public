# PR Review Flow

このドキュメントは、Codex を使った GitHub PR review flow の source of truth です。

## Identity Model

- `author identity`: PR を作成する主体
- `reviewer identity`: requested reviewer として review を返す主体

重要:

- `author identity` と `reviewer identity` は分離する
- same identity の `COMMENTED` review は正式な approval gate とみなさない
- required approving reviews を使う場合、`APPROVED` は reviewer identity から返る必要がある

## Review States

1. PR 作成
2. reviewer request
3. review 実施
4. `APPROVE` / `REQUEST_CHANGES` / `COMMENT`
5. 指摘対応
6. 再 reviewer request
7. merge または close and recreate PR

## Meaning

- `APPROVE`
  - merge gate を開ける review
  - CI green と blocking 指摘なしが前提
- `REQUEST_CHANGES`
  - blocking review
  - 修正または合理的な reject が必要
- `COMMENT`
  - 参考意見または暫定レビュー
  - 単体では merge gate を開かない

## Response Contract

implementer は各 review 指摘に対して、次のいずれかで応答する。

- 修正して push する
- 根拠付きで reject する
- 別 Issue に切り出す
- close and recreate PR を提案する

## Close And Recreate PR

次の条件では、既存 PR を close して新規 PR を作る。

- 差分が元の requirements / implementation Issue の境界を超えた
- review 対応で別の大きな設計変更が必要になった
- reviewer identity / branch protection 前提を満たせず、現行 PR で正式 gate を構成できない
- review thread と差分の対応が崩れ、既存 PR で品質の高い review を維持できない

close 時は、元 PR・新 PR・関連 Issue を相互リンクする。

## Branch Protection Assumptions

この flow は次を前提にする。

- required approving reviews
- requested reviewer が設定できること
- stale approval dismissal または latest push approval requirement のいずれか

これらが未設定の場合は暫定運用とする。

暫定運用:

- review comment を残す
- `review-needed` を外し、`approved` ラベルで状態管理する
- ただし正式な GitHub approval gate を満たしたとは主張しない

ラベルの意味:

- `review-needed`: reviewer の判断待ち
- `approved`: reviewer の判断としては OK
- ただし same identity fallback で付いた `approved` は GitHub の formal `APPROVED` review と同義ではない

## Helper Usage

PR 作成時に reviewer を request する:

```bash
./scripts/gh-workflow.sh pr \
  --title "feat: add X" \
  --body-file .gemini_temp/pr_body.md \
  --label "review-needed" \
  --reviewer codex-reviewer
```

再レビューを request する:

```bash
./scripts/gh-workflow.sh request-review \
  --pr 123 \
  --reviewer codex-reviewer
```

`--reviewer` には、author identity と分離された reviewer identity を指定する。
