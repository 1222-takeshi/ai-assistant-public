# [Demo] Requirements Issue #52: add `hello` command

> ⚠️ **フィクションです。架空の Issue です。**

---

**Title**: requirements: add `hello` command to scripts/

**Labels**: `requirements`  
**Author**: @req-analyst  
**Created**: (fictional date)

---

## 概要 (Summary)

`scripts/hello.sh` を新規追加し、引数なしで `Hello, world!` を出力する最小コマンドを提供する。
チームの「開発 → レビュー → merge」フローをエンドツーエンドで確認するためのサンプル実装として使用する。

## 背景 (Background)

- @researcher-1 の調査 Issue #51 より、フローを示す具体的な実装サンプルが必要と判明
- 既存の `examples/github-only-flow.md` はコマンド手順だが、実際に動くコードが存在しない
- 最小限のシェルスクリプトを題材にすることで、全エージェントの役割を実演できる

## スコープ (Scope)

### In Scope

- `scripts/hello.sh` の新規作成（実行権限付き）
- `tests/test_hello.py` の新規作成（UT-001〜002）
- `README.md` の Scripts セクションへの記載追加

### Out of Scope

- 引数パース・国際化対応
- CI への専用ジョブ追加（既存 `test.yml` で `pytest` が通れば十分）

## 受け入れ条件 (Acceptance Criteria)

- [ ] `scripts/hello.sh` が存在し、`chmod +x` されている
- [ ] 引数なし実行で標準出力に `Hello, world!` が含まれる
- [ ] `pytest tests/test_hello.py -v` が全 pass
- [ ] `README.md` の Scripts セクションに `hello.sh` の説明が 1 行以上追加されている
- [ ] スクリプト内にハードコードされたパス・ユーザー名がない

## テスト仕様 (Test Spec)

| ID | テスト種別 | 内容 | 期待結果 |
|----|-----------|------|---------|
| UT-001 | Unit | `scripts/hello.sh` を subprocess で実行 | stdout に `Hello, world!` を含む、exit code 0 |
| UT-002 | Unit | ファイルが実行権限を持つ | `os.access(path, os.X_OK)` が True |

## 参考 (References)

- Issue #51: research findings (fictional)
- [examples/github-only-flow.md](../github-only-flow.md)

## 実装依頼への移行条件

この Issue が `approved` ラベルを受け取ったら、
Implementer が `implementation` ラベル付き Issue を作成して着手すること。
