#!/usr/bin/env python3
"""Entry for make.fun news-image-20261125.

Writes the bundled one-page summary of Wednesday 25 November 2026 world
news to /output/entry.png.

Deterministic: the output bytes are exactly the bundled image bytes on
every run. No network, no randomness, stdlib only. The image itself was
drawn programmatically (see draw_image_v5.py) from 35 headlines verified
against Reuters, AP, AFP, Al Jazeera, WSJ, CMSA/Xinhua and UN summaries
of 25 November 2026.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry-v5.png")
DST = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")


def main():
    if not os.path.exists(SRC):
        print("missing bundled image: %s" % SRC, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote %s (%d bytes)" % (DST, os.path.getsize(DST)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
