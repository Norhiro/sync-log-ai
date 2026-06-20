import argparse
import sys
from pathlib import Path
from .engine import SyncEngine
from .audit import run_audit, random_audit

_WORK_MD_TEMPLATE = """\
# Work Log

## Current Task


## Progress


## Notes

"""

_RULES_YAML_TEMPLATE = """\
# AI-Agent Operational Rules (SyncLog-AI)
system:
  context_dir: ".ai_context"
  monitor_file: "work.md"

audit:
  random_range: [15, 25]
  log_file: ".ai_context/audit_history.log"
  auto_repair: true

ai_directives:
  persona: "You are an expert engineer. Keep the work log consistent."
  critical_rules:
    - "Always verify hash before starting new task."
    - "If audit fails, stop and wait for manual intervention."
"""

def cmd_init():
    work_md = Path("work.md")
    rules_yaml = Path("rules.yaml")
    created = []

    if not work_md.exists():
        work_md.write_text(_WORK_MD_TEMPLATE, encoding="utf-8")
        created.append("work.md")
    else:
        print("work.md already exists, skipping.")

    if not rules_yaml.exists():
        rules_yaml.write_text(_RULES_YAML_TEMPLATE, encoding="utf-8")
        created.append("rules.yaml")
    else:
        print("rules.yaml already exists, skipping.")

    if created:
        print(f"Initialized: {', '.join(created)}")
        print("Run `synclogai sync` to create the first snapshot.")

def main():
    parser = argparse.ArgumentParser(
        prog="synclogai",
        description="SyncLog-AI: Binary-optimized, self-healing context management for AI-assisted development",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Create work.md and rules.yaml in the current directory")

    for cmd, help_text in [
        ("sync", "Sync work.md to binary snapshot"),
        ("audit", "Check consistency; auto-repair if drift detected"),
        ("random-audit", "Probabilistic audit (4-7%% chance, for CI / agent hooks)"),
    ]:
        p = sub.add_parser(cmd, help=help_text)
        p.add_argument("path", nargs="?", default="work.md", help="Path to work.md (default: ./work.md)")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "sync":
        SyncEngine().sync(args.path)
    elif args.command == "audit":
        sys.exit(0 if run_audit(args.path) else 1)
    elif args.command == "random-audit":
        sys.exit(0 if random_audit(args.path) else 1)
    else:
        parser.print_help()
