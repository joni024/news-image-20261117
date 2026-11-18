#!/usr/bin/env python3
"""Entry for make.fun competition news-image-20261117.

Writes the pre-rendered news infographic (1024x1024, drawn by
draw_news.py from the verified events of Tuesday 17 November 2026) to the
output directory. The image ships in the repository as base64 text
(image_b64.txt), so the entry holds no binary file; this program decodes
it and writes entry.png. Standard library only; no network;
deterministic: every run writes the same bytes.
"""
import base64
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
B64 = HERE / "image_b64.txt"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    data = base64.b64decode(B64.read_text(encoding="ascii").strip())
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("image_b64.txt did not decode to a PNG file")
    (out_dir / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
