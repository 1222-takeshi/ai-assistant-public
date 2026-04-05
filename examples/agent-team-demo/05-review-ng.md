# [Demo] Code Review Comment — PR #53 (NG → immediate close)

> ⚠️ **フィクションです。架空のレビューコメントです。**

---

**Author**: @reviewer  
**Target**: PR #53 feat: add hello command

---

## レビュー結果: ❌ NG — PR を即時 close します

**判定**: ❌ NG — 🔴必須 1件（閾値: 🔴≥1 → NG）

### 確認項目

| 項目 | 評価 |
|------|------|
| `scripts/hello.sh` が存在する | ✅ |
| 出力が `Hello, world!` を含む | ✅ |
| **`scripts/hello.sh` に実行権限がある** | 🔴 |
| `README.md` に説明追記 | ✅ |
| ハードコードされたパス・ユーザー名なし | ✅ |

### 🔴 必須（NG 判定）

> **`scripts/hello.sh` に実行権限が付与されていません。**
>
> ```
> $ ls -la scripts/hello.sh
> -rw-r--r-- 1 user group 42 Apr  5 10:00 scripts/hello.sh
> ```
>
> 受け入れ条件「`chmod +x` されている」を満たしていません。
> UT-002 も追加されておらず、テストでも検出できない状態です。

---

## 対応方針

このポリシーにより、**PR は即時 close します。Fix commit による再オープンは禁止です。**

```bash
gh pr close 53 --comment "NG: 実行権限未付与 (受け入れ条件未達)"
```

@impl-1 は以下の手順で対応してください:

1. `feat/add-hello-command` ブランチを削除
2. `main` から **新ブランチ** `feat/add-hello-command-v2` を作成
3. 以下を修正して新しい PR を作成:
   - `git add --chmod=+x scripts/hello.sh`
   - `tests/test_hello.py` に UT-002（実行権限確認）を追加
4. `gh pr create --label review-needed` で新 PR を提出

> 🚫 PR #53 を reopen しないこと。
