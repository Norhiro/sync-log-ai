import os
import sys
from sync_engine import SyncEngine
from utils import load_config
from pathlib import Path

def run_audit(md_path="work.md"):
    print(f"--- 監査開始: {md_path} ---")

    # 修正箇所: self. を削除してローカル変数に
    config = load_config()
    context_dir = Path(config['system']['context_dir'])

    engine = SyncEngine()
    
    # 整合性チェック
    if engine.verify(md_path):
        print("ステータス: [PASS] 整合性は正常です。")
        return True
    else:
        print("ステータス: [ALERT] 乖離が検出されました！")
        print("推論: Markdownの内容が変更されていますが、バイナリログと一致していません。")
        print("アクション: 自動的に sync_engine.py を再実行して同期を修復します...")
        
        # 自動修復機能
        engine.sync(md_path)
        print("修復完了: バイナリログを最新のMarkdownに合わせて更新しました。")
        return False

if __name__ == "__main__":
    # 監査を実行
    is_safe = run_audit()
    if not is_safe:
        sys.exit(1)