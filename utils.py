import yaml
from pathlib import Path

def load_config():
    # プロジェクトルートにある rules.yaml を常に読み込む
    config_path = Path(__file__).parent / "rules.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)