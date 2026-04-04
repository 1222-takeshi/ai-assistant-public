# Security Policy

## Supported Versions

このリポジトリはテンプレートであり、`main` の最新状態のみをサポート対象とします。

## Reporting a Vulnerability

- トークン、内部 ID、社内 URL などの露出を見つけた場合は公開 Issue に書かない
- まず再現手順、影響範囲、該当ファイルを整理する
- maintainer に非公開チャネルで連絡し、公開修正後に必要なら disclosure する

## Secrets and Internal Data

- `config/` には public-safe なプレースホルダーのみを残す
- 実運用の設定値はローカル管理し、公開ブランチへ含めない
- 履歴に混入した場合は公開前に履歴ごと除去する
