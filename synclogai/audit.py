import random
import sys
from .engine import SyncEngine

def run_audit(md_path: str = "work.md") -> bool:
    print(f"--- 監査開始: {md_path} ---")
    engine = SyncEngine()
    if engine.verify(md_path):
        print("ステータス: [PASS] 整合性は正常です。")
        return True
    print("ステータス: [ALERT] 乖離が検出されました！")
    print("アクション: バイナリログを修復します...")
    engine.sync(md_path)
    print("修復完了。")
    return False

def random_audit(md_path: str = "work.md") -> bool:
    probability = 1 / random.randint(15, 25)
    if random.random() < probability:
        print(">>> [抜き打ち監査発動] 整合性チェックを開始します...")
        return run_audit(md_path)
    print(">>> [通常モード] 監査はスキップされました。")
    return True
