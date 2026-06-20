import yaml
from pathlib import Path

_DEFAULT_CONFIG = {
    "system": {
        "context_dir": ".ai_context",
        "monitor_file": "work.md",
    },
    "audit": {
        "random_range": [15, 25],
        "log_file": ".ai_context/audit_history.log",
        "auto_repair": True,
    },
}

def load_config():
    config_path = Path.cwd() / "rules.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return _DEFAULT_CONFIG
