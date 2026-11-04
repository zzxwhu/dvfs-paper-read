"""Restore the large, unchanged Quartz emoji asset from the pinned upstream.

This keeps repository uploads small without changing Quartz's rendering data.
The official Git blob hash is verified before the downloaded JSON is used.
"""
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "quartz/util/emojimap.json"
SOURCE = "https://raw.githubusercontent.com/Futuresxy/paper_read/1281313ed734c72d5c7ae523dbe84974f9997fb0/quartz/util/emojimap.json"
EXPECTED_BLOB = "a9a8e3977f4275c93a6bac80300a9e31bd029475"

def main():
    if TARGET.exists():
        print("Quartz emoji data already present.")
        return
    with urllib.request.urlopen(SOURCE, timeout=60) as response:
        data = response.read()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if digest != EXPECTED_BLOB:
        raise SystemExit("Upstream emoji asset hash mismatch; refusing to use it.")
    json.loads(data)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(data)
    print("Restored verified Quartz emoji data.")

if __name__ == "__main__":
    main()
