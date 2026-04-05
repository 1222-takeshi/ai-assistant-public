# Onboarding

このリポジトリには、OSS 利用者向けの非破壊な onboarding 導線があります。

## Bootstrap

`bootstrap` は安全な初期化補助です。既存ファイルを上書きしません。

```bash
./scripts/bootstrap.sh
```

optional PMO profile を使う場合だけ、example config から local override を生成します。

```bash
./scripts/bootstrap.sh --init-pmo-config
```

## GitHub Labels のセットアップ

開発 workflow に必要な GitHub Labels（`research`, `requirements`, `implementation`, `review-needed`, `approved`, `blocked`）を作成します。

```bash
# bootstrap と同時に実行
./scripts/bootstrap.sh --setup-labels

# または単独で実行
./scripts/setup-labels.sh
```

`gh` 認証済みであることが前提です（`gh auth login`）。すでに同名ラベルが存在する場合はスキップされます。

## Doctor

`doctor` は環境診断です。既存ファイルを変更しません。

```bash
python3 scripts/doctor.py
```

確認内容:

- `gh` の存在
- `gh auth status`
- Python からの pytest 実行可否
- `git worktree` 前提のドキュメント整合性
- tracked config template の validation
- optional PMO profile の local config 状態

## Status Meaning

- `success`: 必須条件を満たしている
- `warning`: core workflow は使えるが、optional PMO profile は未設定
- `failure`: 必須依存または config が壊れており、修正が必要

## First Setup

```bash
python3 -m pip install -r requirements-dev.txt
./scripts/bootstrap.sh --setup-labels
python3 scripts/doctor.py
```
