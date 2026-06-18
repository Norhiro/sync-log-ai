import hashlib
import msgpack
import os
from pathlib import Path
from utils import load_config

class SyncEngine:
    def __init__(self, context_dir=".ai_context"):
        self.config = load_config()
        self.context_dir = Path(self.config['system']['context_dir'])

        self.context_dir = Path(context_dir)
        self.context_dir.mkdir(exist_ok=True)
        self.bin_path = self.context_dir / "memory.bin"

    def _calculate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def sync(self, md_path: str):
        """Markdownを読み込み、バイナリとして保存する"""
        md_file = Path(md_path)
        if not md_file.exists():
            print(f"Error: {md_path} not found.")
            return

        content = md_file.read_text(encoding='utf-8')
        data = {
            "task_file": md_path,
            "content": content,
            "hash": self._calculate_hash(content)
        }

        with open(self.bin_path, "wb") as f:
            f.write(msgpack.packb(data))
        
        print(f"Sync complete: {md_path} -> {self.bin_path}")


    def verify(self, md_path: str) -> bool:
        """MDとバイナリのハッシュを照合して乖離をチェック"""
        if not self.bin_path.exists():
            return False
            
        with open(self.bin_path, "rb") as f:
            # 修正：unpack(f) ではなく unpackb(f.read()) に変更
            stored_data = msgpack.unpackb(f.read())
            
        current_content = Path(md_path).read_text(encoding='utf-8')
        return self._calculate_hash(current_content) == stored_data['hash']


# 使用例
if __name__ == "__main__":
    engine = SyncEngine()
    # 対象のMDファイルを同期
    engine.sync("work.md")
    
    # 整合性チェック
    if engine.verify("work.md"):
        print("整合性OK: MDとバイナリは同期されています。")
    else:
        print("警告: 乖離が検出されました！")