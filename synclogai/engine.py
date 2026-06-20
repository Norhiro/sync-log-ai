import hashlib
import msgpack
from pathlib import Path
from .utils import load_config

class SyncEngine:
    def __init__(self, context_dir=None):
        config = load_config()
        self.context_dir = Path(context_dir or config["system"]["context_dir"])
        self.context_dir.mkdir(exist_ok=True)
        self.bin_path = self.context_dir / "memory.bin"

    def _hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def sync(self, md_path: str):
        md_file = Path(md_path)
        if not md_file.exists():
            print(f"Error: {md_path} not found.")
            return
        content = md_file.read_text(encoding="utf-8")
        data = {"task_file": md_path, "content": content, "hash": self._hash(content)}
        with open(self.bin_path, "wb") as f:
            f.write(msgpack.packb(data))
        print(f"Sync complete: {md_path} -> {self.bin_path}")

    def verify(self, md_path: str) -> bool:
        if not self.bin_path.exists():
            return False
        with open(self.bin_path, "rb") as f:
            stored = msgpack.unpackb(f.read())
        current = Path(md_path).read_text(encoding="utf-8")
        return self._hash(current) == stored["hash"]
