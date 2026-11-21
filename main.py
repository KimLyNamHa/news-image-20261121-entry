#!/usr/bin/env python3
"""news-image-20261121 entry (Python 3.13, standard library only).

The image is the entry.png beside this file, drawn by draw_poster.py from
the world news of Saturday 21 November 2026. The program copies it to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png); it needs no network
and always copies the same bytes. No font is loaded anywhere in this file.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    # Guard: the copied file must be a whole PNG within the gate's limits.
    with open(dest, "rb") as f:
        head = f.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if os.path.getsize(dest) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")


if __name__ == "__main__":
    main()
