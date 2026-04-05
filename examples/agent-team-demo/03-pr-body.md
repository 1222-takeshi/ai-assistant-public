# [Demo] PR #54: feat: add hello command (v2)

> ⚠️ **フィクションです。架空の PR 本文です。**  
> PR #53 は NG により即時 close されました。このPRは新ブランチで再作成したものです。

---

**Branch**: `feat/add-hello-command-v2`  
**Base**: `main`  
**Labels**: `review-needed`  
**Author**: @impl-1

---

## 変更内容

Issue #52 `requirements: add hello command` の実装。

### 追加ファイル

| ファイル | 内容 |
|---------|------|
| `scripts/hello.sh` | 引数なしで `Hello, world!` を出力するシェルスクリプト |
| `tests/test_hello.py` | UT-001（出力確認）・UT-002（実行権限確認） |

### 変更ファイル

| ファイル | 変更内容 |
|---------|---------|
| `README.md` | Scripts セクションに `hello.sh` の説明を追記 |

---

## 実装詳細

```bash
# scripts/hello.sh
#!/usr/bin/env bash
set -euo pipefail
echo "Hello, world!"
```

```python
# tests/test_hello.py (抜粋)
import os, subprocess
from pathlib import Path

HELLO_SH = Path(__file__).parent.parent / "scripts" / "hello.sh"

def test_hello_output():
    result = subprocess.run([str(HELLO_SH)], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Hello, world!" in result.stdout

def test_hello_executable():
    assert os.access(HELLO_SH, os.X_OK)
```

---

## v2 での修正点（PR #53 NG からの変更）

PR #53 は以下の理由で NG となり即時 close されました:

> 🔴 **必須**: `scripts/hello.sh` に実行権限が付与されていない（`chmod +x` 漏れ）

v2 では以下を対応:
- `git add --chmod=+x scripts/hello.sh` で実行権限を付与
- UT-002 を追加してテストで権限を検証するよう強化

---

## テスト結果

```
pytest tests/test_hello.py -v
test_hello_output PASSED
test_hello_executable PASSED
2 passed in 0.12s
```

全体: `pytest tests/ -q -p no:cacheprovider` → `316 passed, 35 skipped`

---

## 受け入れ条件チェック

- [x] `scripts/hello.sh` が存在し、`chmod +x` されている
- [x] 引数なし実行で標準出力に `Hello, world!` が含まれる
- [x] `pytest tests/test_hello.py -v` が全 pass
- [x] `README.md` の Scripts セクションに `hello.sh` の説明が追加されている
- [x] スクリプト内にハードコードされたパス・ユーザー名がない

## レビュー依頼

@reviewer レビューをお願いします。
