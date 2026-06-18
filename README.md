# SyncLog-AI: Binary-Optimized, Self-Healing Context Management

> Status: Prototype
>
> SyncLog-AI is currently an experimental prototype. It demonstrates Markdown-to-MessagePack synchronization and hash-based consistency checks, but it is not yet a production-ready logging framework.
>
> SyncLog-AI は現在、実験的なプロトタイプです。Markdown と MessagePack の同期、およびハッシュによる整合性確認を検証する段階であり、まだ本番利用向けのログ管理基盤ではありません。

SyncLog-AI is a lightweight memory synchronization experiment for AI-assisted development. It keeps a human-readable Markdown work log and a compact MessagePack binary snapshot in sync, then verifies the two with a SHA-256 hash.

SyncLog-AI は、AI エージェントとの共同作業向けの軽量なメモリ同期実験プロジェクトです。人間が読める Markdown の作業ログと、AI や自動処理が扱いやすい MessagePack バイナリスナップショットを同期し、SHA-256 ハッシュで整合性を確認します。

## Why SyncLog-AI?

Large AI-assisted projects often accumulate long Markdown histories. Reading the whole history every time can be slow, expensive, and error-prone. SyncLog-AI explores whether separating the human log from the machine snapshot can help agents resume work from a more consistent state.

大規模な AI 共同作業では、Markdown の履歴が長くなりがちです。毎回すべての履歴を読み込むと、遅く、高コストで、整合性も崩れやすくなります。SyncLog-AI は人間向けログと機械向けスナップショットを分けることで、AI がより一貫した状態から作業を再開できるかを検証します。

## Features

- **Binary-text sync / バイナリとテキストの同期**: Stores `work.md` in `.ai_context/memory.bin` as MessagePack.
- **Hash verification / ハッシュ検証**: Compares the current Markdown content with the hash stored in the binary snapshot.
- **Self-repair audit / 自動修復監査**: `auditor.py` detects drift and regenerates the binary snapshot from `work.md`.
- **Random audit hook / 抜き打ち監査**: `random_auditor.py` runs the audit occasionally for agent or CI workflows.
- **Config file / 設定ファイル**: `rules.yaml` defines paths and operational rules.

## Requirements

- Python 3.10 or later is recommended.
- Required Python packages:
  - `msgpack`: serializes the memory snapshot to MessagePack.
  - `PyYAML`: reads `rules.yaml`.

`watchdog` is not required by the current codebase. Add it only if you later implement file watching.

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

1. Write your current work state in `work.md`.

2. Synchronize the Markdown log to the binary memory file:

```bash
python sync_engine.py
```

This creates or updates `.ai_context/memory.bin`.

3. Run the audit:

```bash
python auditor.py
```

If `work.md` and `.ai_context/memory.bin` differ, the audit regenerates the binary file from `work.md`. In that case, `auditor.py` exits with code `1` after repair so CI or agents can notice that drift occurred.

4. Optionally run a random audit:

```bash
python random_auditor.py
```

## File Overview

- `work.md`: Human-readable work log.
- `sync_engine.py`: Converts `work.md` into `.ai_context/memory.bin` and verifies hashes.
- `auditor.py`: Checks consistency and repairs binary memory when drift is detected.
- `random_auditor.py`: Runs audits occasionally.
- `rules.yaml`: Operational settings for the protocol.
- `CLAUDE.md`: Agent-facing operating rules, written in Japanese and English.
- `AGENTS.md`: Codex-facing operating rules, written in Japanese and English.
- `requirements.txt`: Python package dependencies.

## Notes for Public Repositories

Do not commit local runtime artifacts such as virtual environments, Python caches, or `.ai_context/memory.bin`. The included `.gitignore` excludes these files.

ローカル実行で生成される `venv/`、`__pycache__/`、`.ai_context/memory.bin` などは公開リポジトリに含めないでください。このリポジトリの `.gitignore` では、それらを除外しています。

## License

This project is licensed under the MIT License. See `LICENSE` for details.

このプロジェクトは MIT License の下で公開されています。詳細は `LICENSE` を参照してください。
