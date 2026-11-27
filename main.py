#!/usr/bin/env python3
"""Entry program for news-image-20261127.

Copies the repository's news-v5.png (rendered by build27-v5.py from the verified
27 November 2026 stories) to $MAKEFUN_OUTPUT_DIR/entry.png.
Standard library only, no network, deterministic: the same bytes every run.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news-v5.png")
    if not os.path.isfile(src):
        print(f"missing image: {src}", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
