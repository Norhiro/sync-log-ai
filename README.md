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

## Comparison with Headroom / Headroom との比較

> Netflix のエンジニアが、AI のトークンを最大 95% カットする OSS を公開した。
>
> しかも精度は落ちない。元に戻せる「可逆圧縮」だから。
>
> Claude や Cursor を使っていると、地味にきついのがトークン消費。
> 長いログ、RAG で取得したテキスト、複数ファイルの読み込み。
> AI に渡すたびにトークンが溶けていく。
>
> その問題を、AI に渡す前に解決するのが「Headroom」。

[Headroom](https://github.com/chopratejas/headroom) is a local-first context compression layer built on a Rust core with Python bindings. It compresses tool outputs, logs, RAG chunks, and files before they reach the LLM — reversibly (CCR: Cached Compressed Retrieval), with 60–95% token reduction. Benchmarks on GSM8K, TruthfulQA, and SQuAD v2 show accuracy is maintained or improved.

SyncLog-AI addresses a different problem: **work-state consistency across sessions**. It does not reduce what you send to the AI; instead it keeps a hash-verified MessagePack snapshot of `work.md` so agents can resume from a consistent point without re-reading the full Markdown history.

| | SyncLog-AI | Headroom |
|---|---|---|
| **Goal** | Session state consistency | Token reduction per API call |
| **Core language** | Python | Rust + Python bindings |
| **Mechanism** | Markdown → MessagePack + SHA-256 | 6 compression algorithms (SmartCrusher, CodeCompressor, etc.) |
| **Token savings** | None (different purpose) | 60–95% (benchmark-verified) |
| **Integration** | CLAUDE.md / AGENTS.md protocol | Library, proxy, MCP server, agent wrapper |
| **Cross-agent memory** | Via shared `work.md` | Built-in (Claude, Codex, Gemini) |

Headroom also ships a `.claude-plugin` for direct Claude Code integration and an MCP server mode, making it a deeper fit for agent workflows than a simple compression utility.

The two tools address complementary problems and can be used together.

Headroom は Rust コアと Python バインディングで構成されたローカルファーストのコンテキスト圧縮レイヤーです。ツール出力・ログ・RAG チャンク・ファイルを LLM に届く前に可逆圧縮し（CCR）、トークンを 60〜95% 削減します。精度はベンチマーク上で維持または改善されています。

SyncLog-AI が解決するのは別の問題、**セッション間の作業状態の一貫性**です。AI への入力を圧縮するのではなく、`work.md` のハッシュ検証済みスナップショットを保持し、AI が前回の続きから矛盾なく再開できるようにします。Headroom はクロスエージェントのメモリ共有機能も持ち、概念的に重なる部分がありますが、アプローチは異なります。両者は補完的に組み合わせて使えます。

## Features

- **Binary-text sync / バイナリとテキストの同期**: Stores `work.md` in `.ai_context/memory.bin` as MessagePack.
- **Hash verification / ハッシュ検証**: Compares the current Markdown content with the hash stored in the binary snapshot.
- **Self-repair audit / 自動修復監査**: Detects drift and regenerates the binary snapshot from `work.md`.
- **Random audit hook / 抜き打ち監査**: Runs audits probabilistically for agent or CI workflows.
- **Config file / 設定ファイル**: `rules.yaml` defines paths and operational rules (optional; built-in defaults are used if absent).

## Requirements

- Python 3.10 or later.

## Installation

```bash
pip install git+https://github.com/Norhiro/sync-log-ai.git
```

Dependencies (`msgpack`, `PyYAML`) are installed automatically.

依存パッケージ（`msgpack`、`PyYAML`）は自動的にインストールされます。

## Quick Start

1. Initialize a new directory:

```bash
synclogai init
```

This creates `work.md` and `rules.yaml` in the current directory. Skips files that already exist.

カレントディレクトリに `work.md` と `rules.yaml` を生成します。既存ファイルはスキップします。

2. Write your current work state in `work.md`.

3. Synchronize:

```bash
synclogai sync
```

This creates or updates `.ai_context/memory.bin` in the current directory.

4. Audit:

```bash
synclogai audit
```

If `work.md` and `.ai_context/memory.bin` differ, the snapshot is repaired automatically. Exit code `1` is returned after repair so CI or agents can detect drift.

5. Probabilistic audit (for CI / agent hooks):

```bash
synclogai random-audit
```

All commands accept an optional path argument to target a specific file:

```bash
synclogai sync path/to/work.md
```

## Using with Headroom / Headroom との併用

```bash
headroom wrap claude   # compress context before it reaches the LLM
synclogai sync         # save work state after each session
synclogai audit        # verify consistency before resuming
```

Headroom reduces tokens sent to the AI. SyncLog-AI ensures the agent resumes from a consistent state. The two tools are complementary.

Headroom が AI に渡すトークンを削減し、SyncLog-AI がセッション間の作業状態の一貫性を保証します。

## File Overview

- `synclogai/`: Python package — `engine.py`, `audit.py`, `cli.py`, `utils.py`.
- `work.md`: Human-readable work log.
- `rules.yaml`: Operational settings (optional).
- `pyproject.toml`: Package definition and CLI entry point.
- `CLAUDE.md`: Agent-facing operating rules, written in Japanese and English.
- `AGENTS.md`: Codex-facing operating rules, written in Japanese and English.

### Legacy scripts (for direct execution without install)

- `sync_engine.py`, `auditor.py`, `random_auditor.py`: thin wrappers around the `synclogai` package.

## Notes for Public Repositories

Do not commit local runtime artifacts such as virtual environments, Python caches, or `.ai_context/memory.bin`. The included `.gitignore` excludes these files.

このモジュールを利用し公開される場合、ローカル実行で生成される `venv/`、`__pycache__/`、`.ai_context/memory.bin` などは公開リポジトリに含めないでください。このリポジトリの `.gitignore` では、それらを除外しています。

## License

This project is licensed under the MIT License. See `LICENSE` for details.

このプロジェクトは MIT License の下で公開されています。詳細は `LICENSE` を参照してください。
