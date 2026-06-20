import argparse
import sys
from .engine import SyncEngine
from .audit import run_audit, random_audit

def main():
    parser = argparse.ArgumentParser(
        prog="synclogai",
        description="SyncLog-AI: Binary-optimized, self-healing context management for AI-assisted development",
    )
    sub = parser.add_subparsers(dest="command")

    for cmd, help_text in [
        ("sync", "Sync work.md to binary snapshot"),
        ("audit", "Check consistency; auto-repair if drift detected"),
        ("random-audit", "Probabilistic audit (4-7%% chance, for CI / agent hooks)"),
    ]:
        p = sub.add_parser(cmd, help=help_text)
        p.add_argument("path", nargs="?", default="work.md", help="Path to work.md (default: ./work.md)")

    args = parser.parse_args()

    if args.command == "sync":
        SyncEngine().sync(args.path)
    elif args.command == "audit":
        sys.exit(0 if run_audit(args.path) else 1)
    elif args.command == "random-audit":
        sys.exit(0 if random_audit(args.path) else 1)
    else:
        parser.print_help()
