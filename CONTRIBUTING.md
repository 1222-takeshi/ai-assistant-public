# Contributing

## Scope

このリポジトリは Claude Code / Codex 向けの運用テンプレートです。  
社内固有の設定や接続先を含む変更ではなく、再利用可能な改善を歓迎します。

## Setup

```bash
python -m pip install -r requirements-dev.txt
pytest tests/ -v -p no:cacheprovider
```

## Development Rules

- 変更は小さく保つ
- 実運用値や内部 URL、ID、トークンはコミットしない
- `config/` の tracked ファイルは public-safe テンプレートとして維持する
- 実運用値は `config/*.local.yaml` などの未追跡ファイルに分離する
- `*.example.yaml` を採る場合は、コミット対象は example のみ、実値は ignored の local file にする
- スクリプトは特定 repo やローカル絶対パスに依存させない

## Pull Requests

- コミットメッセージは Conventional Commits を推奨
- PR には背景、変更内容、テスト結果、ロールバック方針を記載する
- 破壊的変更やテンプレートの契約変更は README / CLAUDE / tests を合わせて更新する
