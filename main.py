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

# Gate limits from the competition rules, in one place: the entry must be
# a PNG, at most 1 MiB, exactly 1024x1024. The checks below use these
# constants instead of repeating the literals, so a limit can never be
# mistyped in one check and right in another.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
CANVAS = (1024, 1024)


def validate_output(path):
    """Check the copied entry against the gate: PNG, <= 1 MiB, 1024x1024.

    Reads the PNG signature and the IHDR chunk with the standard library
    only — this file must not import PIL, because the grader's Pillow
    cannot be relied on for anything beyond what the gate needs.
    """
    import struct
    if os.path.getsize(path) > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB")
    with open(path, "rb") as f:
        head = f.read(8)
        ihdr = f.read(25)
    if head != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if len(ihdr) < 25 or ihdr[4:8] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", ihdr[8:16])
    if (width, height) != CANVAS:
        raise SystemExit("entry.png is not 1024x1024")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    # Guard: the copied file must be a whole PNG within the gate's limits.
    with open(dest, "rb") as f:
        head = f.read(8)
    if head != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if os.path.getsize(dest) > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB")
    validate_output(dest)


if __name__ == "__main__":
    main()
