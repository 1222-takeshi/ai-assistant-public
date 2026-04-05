# Dev Workflow — ソフトウェア開発チーム（参考実装）

> ⚠️ **これは参考実装です。** このリポジトリが採用している一例であり、強要するものではありません。
> あなたのチームに合わせて自由に変更・置き換えてください。

---

## このワークフローの構成

```
Orchestrator (1)
  ├── Researcher x2  ─── 技術調査
  ├── Requirements Analyst ─── 要件定義
  ├── Implementer x2 ─── 実装 (git worktree 並列)
  └── Reviewer (ultra-strict) ─── コードレビュー
```

**Reviewer ポリシー（このリポジトリの設定）**:
🔴必須 ≥ 1 または 🟡推奨 ≥ 3 → NG（PR 即時 close）  
→ ポリシーは自由に変更できます。詳細は `commands/dev/review.md` を参照してください。

## ファイル構成

```
examples/dev-workflow/
├── README.md              # このファイル
├── team-topology.yaml     # チーム構成定義（参考）
└── commands/
    └── dev/
        ├── start-team.md
        ├── status.md
        ├── orchestrate.md
        ├── research.md
        ├── define-requirements.md
        ├── implement.md
        └── review.md
```

## セットアップ手順

```bash
# 1. topology を自分のリポジトリにコピー
cp examples/dev-workflow/team-topology.yaml .claude/team-topology.yaml

# 2. コマンドをコピー
cp -r examples/dev-workflow/commands/dev/ .claude/commands/dev/

# 3. topology / コマンドをチームに合わせて編集する

# 4. ラベルをセットアップ
./scripts/setup-labels.sh
```

## このワークフローを変える場合

- ロール名を変えたい → `team-topology.yaml` の `id:` と `role:` を変更
- レビューポリシーを変えたい → `commands/dev/review.md` の閾値を変更
- Researcher を 1 人にしたい → topology の lanes から 1 つ削除
- Implementer を 3 人に増やしたい → lanes に `impl-3` を追加し worktree を作成

詳細は [docs/customization.md](../../docs/customization.md) を参照してください。
