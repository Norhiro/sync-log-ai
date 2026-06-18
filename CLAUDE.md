# Project Sync-log-ai Configuration

This project uses a memory synchronization protocol for AI-agent collaboration. AI agents must follow the rules below.

本プロジェクトは、AI エージェントとの協調作業におけるメモリ同期プロトコルを採用しています。AI は以下のルールを厳守してください。

## Memory Synchronization Protocol

- **Before starting work / 作業開始前**: Check the current state of `work.md` and, when available, `.ai_context/memory.bin`.
- **After finishing work / 作業終了時**: Run `python sync_engine.py` to synchronize the current work state into `.ai_context/memory.bin`.
- **When resuming work / 作業再開時**: Read the previous state saved in `.ai_context/memory.bin` when available, then continue from the last recorded point.
- **Consistency / 整合性担保**: The audit flow compares `work.md` with the binary memory hash. Keep both in sync.
- **Saving files / 保存の徹底**: Save every new or modified file before running synchronization.
- **Verification after edits / 保存後の検証**: After creating or modifying files, verify that the target files exist and that timestamps or Git status reflect the change.
- **Work log updates / 作業記録の更新**: When creating or editing files, update `work.md` with what changed and why.
- **Sync trigger / 同期のトリガー**: After file edits and `work.md` updates are complete, run `python sync_engine.py`.

## Commands

```bash
python sync_engine.py
python auditor.py
python random_auditor.py
```

## Directory Structure

- `.ai_context/`: System memory directory for binary memory and audit logs.
- `work.md`: Human-readable work log.
- `rules.yaml`: Protocol configuration.

## Public Repository Notes

Do not commit local runtime artifacts such as `.ai_context/memory.bin`, audit logs, virtual environments, or Python cache files.

`.ai_context/memory.bin`、監査ログ、仮想環境、Python キャッシュなどのローカル生成物はコミットしないでください。

