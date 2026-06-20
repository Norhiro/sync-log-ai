from synclogai.audit import run_audit
import sys

if __name__ == "__main__":
    if not run_audit():
        sys.exit(1)
