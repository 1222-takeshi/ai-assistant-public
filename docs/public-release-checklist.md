# Public Release Checklist

## Goal

このリポジトリを private 運用から public テンプレートとして切り出す前に、
作業木と git 履歴の両方に内部情報が残っていないことを確認する。

## Working Tree

1. `pytest tests/ -v -p no:cacheprovider` を実行する
2. `config/` が `YOUR_*` プレースホルダーのままであることを確認する
3. `scripts/gh-workflow.sh` に特定 repo 依存がないことを確認する
4. README / CLAUDE / `.claude/commands/` に社内 URL や個人パスがないことを確認する
5. tracked config を実値で直接編集する導線が残っていないことを確認する

## Git History

shared な private repo で直接履歴改変しない。  
公開用には mirror clone または新規 clone で別作業ディレクトリを用意する。

```bash
git clone --mirror <private-repo-url> ai-assistant-public.git
cd ai-assistant-public.git
```

履歴に残したくない値を洗い出し、`git filter-repo` などで public 用に削除する。  
対象例:

- 実運用の Notion / Confluence page ID
- 社内 Atlassian ドメイン
- 個人ローカル絶対パス
- 固定された private repo slug

履歴改変後は、全履歴を対象に禁止パターン検索を行う。

## Publish Strategy

- 安全なのは「新しい public repo を作る」運用
- 既存 private repo はそのまま保持する
- public 側は sanitized history のみを push する

## Final Gate

- OSS メタデータが揃っている
  - `LICENSE`
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `SECURITY.md`
- config の実値は `*.local.yaml` のような未追跡ファイルに分離されている
- README だけで第三者がセットアップを開始できる
- 現行作業木に内部値が残っていない
- public に出す履歴が private 運用履歴から分離されている
