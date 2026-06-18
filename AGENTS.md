# Project Sync-log-ai Instructions for Codex

Codex reads repository-level `AGENTS.md` files before starting work. This file provides the Codex-facing instructions for this project.

Codex は作業開始前にリポジトリ単位の `AGENTS.md` を読み込みます。このファイルは、本プロジェクトにおける Codex 向けの指示です。

## Repository Purpose

SyncLog-AI is a memory synchronization protocol for AI-assisted development. It synchronizes the human-readable `work.md` file with `.ai_context/memory.bin` and verifies consistency with a hash.

SyncLog-AI は、AI 支援開発向けのメモリ同期プロトコルです。人間が読む `work.md` と `.ai_context/memory.bin` を同期し、ハッシュで整合性を確認します。

## Codex Working Rules

- Keep documentation bilingual in English and Japanese when editing user-facing Markdown files.
- Preserve `work.md` as an empty starter file for the public repository unless the user explicitly asks to record local work there.
- Do not commit or expose local runtime artifacts such as `.ai_context/memory.bin`, audit logs, `venv/`, or `__pycache__/`.
- Prefer small, focused edits that match the existing project structure.
- When changing Python behavior, run a syntax check before finishing:

```bash
python -m py_compile sync_engine.py auditor.py random_auditor.py utils.py
```

- If the system Python does not have dependencies installed, use the project virtual environment when available:

```bash
venv\Scripts\python.exe -m py_compile sync_engine.py auditor.py random_auditor.py utils.py
```

## Memory Synchronization Protocol

- Before starting a task, check `work.md` and `.ai_context/memory.bin` when they exist.
- After changing project files, verify the relevant files and Git status.
- After local work that should be synchronized, run:

```bash
python sync_engine.py
```

- Run the audit when checking consistency:

```bash
python auditor.py
```

## Project Files

- `README.md`: Public project documentation.
- `CLAUDE.md`: Claude-facing project instructions.
- `AGENTS.md`: Codex-facing project instructions.
- `work.md`: Empty public starter file for human-readable work logs.
- `sync_engine.py`: Markdown-to-MessagePack synchronization and hash verification.
- `auditor.py`: Drift detection and automatic repair.
- `random_auditor.py`: Occasional audit entry point.
- `rules.yaml`: Protocol configuration.
- `requirements.txt`: Python dependencies.

