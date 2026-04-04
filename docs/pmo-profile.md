# PMO Profile

このリポジトリの PMO 機能は optional profile です。  
core の開発フローを使うだけであれば、PMO の設定や外部 SaaS 接続は不要です。

## What This Profile Adds

- `/pmo/run-tasks`
- `/pmo/write-minutes`
- `/pmo/daily-routine`
- `config/notion.yaml` と `config/confluence.yaml` を使った PMO 向けテンプレート設定

## Prerequisites

PMO profile を使う場合のみ、以下を準備します。

- Notion MCP
- Atlassian MCP
- Google Calendar MCP
- Slack MCP
- Gmail MCP
- `config/*.local.yaml` のローカル設定

## Setup

1. `config/notion.example.yaml` を参考に `config/notion.local.yaml` を作成する
2. `config/confluence.example.yaml` を参考に `config/confluence.local.yaml` を作成する
3. 各 `YOUR_*` をローカル設定側で置き換える
4. 必要な MCP / CLI を接続する
5. `/pmo/run-tasks --dry-run` のような安全な確認から始める

## Boundaries

- PMO profile は core Quickstart に含めない
- PMO profile は GitHub-only happy path の必須条件ではない
- PMO profile の設定値は tracked file に書き戻さない
