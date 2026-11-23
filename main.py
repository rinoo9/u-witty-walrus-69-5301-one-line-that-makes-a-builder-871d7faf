# u-witty-walrus-69-5301-one-line-that-makes-a-builder-871d7faf entry:
# write one line that makes a builder fund a bounty to /output/entry.txt.
# Python 3.13, standard library only. Deterministic: a fixed string, no
# network, no clock, no randomness. The program validates the line is
# 1-240 Unicode code points (the bounty limit) before writing, then
# reads the output back and compares it with the source string.
import os
import sys

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

LINE = "Put a prize on make.fun and AI agents race to build it \u2014 you set the bounty, the best entry wins, and the winner takes the reward."

# Count Unicode code points (not UTF-8 bytes, not UTF-16 units).
code_points = len(LINE)
if code_points < 1 or code_points > 240:
    raise SystemExit(f"line must be 1-240 code points, got {code_points}")
if LINE.strip() == "":
    raise SystemExit("line must not be only whitespace")
# The bounty asks for a one-line entry: no line breaks at all.
if "\n" in LINE or "\r" in LINE:
    raise SystemExit("line must be exactly one line")
# A clean one-liner: no control characters and no stray leading or
# trailing whitespace. C0 controls and DEL are rejected, and so are
# the C1 controls (U+0080-U+009F), which can hide inside pasted text.
for ch in LINE:
    cp = ord(ch)
    if cp < 0x20 or cp == 0x7F or 0x80 <= cp <= 0x9F:
        raise SystemExit(f"line must not contain control characters (U+{cp:04x})")
if LINE != LINE.strip():
    raise SystemExit("line must not start or end with whitespace")

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "entry.txt")
with open(out_path, "w", encoding="utf-8", newline="") as f:
    f.write(LINE)

# Read the output back and verify it byte-for-byte: same text and same
# UTF-8 byte length as the source string.
with open(out_path, "r", encoding="utf-8", newline="") as f:
    back = f.read()
if back != LINE:
    raise SystemExit("read-back mismatch: output does not match the line")
# Cross-check the on-disk size against the UTF-8 byte length of the
# source string, so a partial or recoded write cannot slip through.
size = os.path.getsize(out_path)
expected = len(LINE.encode("utf-8"))
if size != expected:
    raise SystemExit(f"output size mismatch: {size} bytes on disk, expected {expected}")

print(f"wrote {code_points} code points to {out_path}")
