import random
import sys
from auditor import run_audit

def random_audit(md_path="work.md"):
    # 15回〜25回に一度の確率で監査を実行 (4%〜6.6%の確率)
    probability = 1 / random.randint(15, 25)
    
    if random.random() < probability:
        print(">>> [抜き打ち監査発動] 整合性チェックを開始します...")
        return run_audit(md_path)
    else:
        print(">>> [通常モード] 監査はスキップされました。")
        return True

if __name__ == "__main__":
    # AIやCI環境からこれを呼ぶようにする
    if not random_audit():
        sys.exit(1)