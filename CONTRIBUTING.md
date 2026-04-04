# Contributing

## Scope

このリポジトリは Claude Code / Codex 向けの運用テンプレートです。  
社内固有の設定や接続先を含む変更ではなく、再利用可能な改善を歓迎します。

## Setup

```bash
python3 -m pip install -r requirements-dev.txt
pytest tests/ -v -p no:cacheprovider
python3 scripts/validate-config.py --tracked-only
```

## Development Rules

- 変更は小さく保つ
- 実運用値や内部 URL、ID、トークンはコミットしない
- `config/*.yaml` の tracked ファイルは public-safe template として維持する
- `config/*.example.yaml` はコピー元サンプル、`config/*.local.yaml` は ignored な local override として扱う
- 実運用値は `config/*.local.yaml` などの未追跡ファイルに分離する
- 優先順位は `local > tracked template` とし、`example` は runtime に含めない
- config を変更したら `python3 scripts/validate-config.py --tracked-only` で template 状態を確認する
- スクリプトは特定 repo やローカル絶対パスに依存させない

## Pull Requests

- コミットメッセージは Conventional Commits を推奨
- PR には背景、変更内容、テスト結果、ロールバック方針を記載する
- 破壊的変更やテンプレートの契約変更は README / CLAUDE / tests を合わせて更新する
