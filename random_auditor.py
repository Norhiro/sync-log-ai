from synclogai.audit import random_audit
import sys

if __name__ == "__main__":
    if not random_audit():
        sys.exit(1)
