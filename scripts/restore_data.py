#!/usr/bin/env python3
"""Pull the `data` branch and rebuild the raw files under data/raw/.

    python3 scripts/restore_data.py            # everything
    python3 scripts/restore_data.py voteview   # only paths starting with voteview/

Verifies SHA256SUMS, joins split parts, and gunzips.
"""
from __future__ import annotations

import gzip
import hashlib
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "-C", str(ROOT), "fetch", "--depth", "1", "origin", "data"], check=True)
        subprocess.run(["git", "-C", str(ROOT), "worktree", "add", "--force", "--detach", tmp, "FETCH_HEAD"],
                       check=True, capture_output=True)
        try:
            src = Path(tmp)
            sums = {}
            for line in (src / "SHA256SUMS").read_text().splitlines():
                h, name = line.split(maxsplit=1)
                sums[name.strip()] = h
            for name, h in sums.items():
                if not name.startswith("raw/" + prefix):
                    continue
                got = hashlib.sha256((src / name).read_bytes()).hexdigest()
                if got != h:
                    raise SystemExit(f"checksum mismatch: {name}")
            groups = defaultdict(list)
            for p in sorted((src / "raw").rglob("*")):
                if p.is_file():
                    rel = p.relative_to(src / "raw").as_posix()
                    if not rel.startswith(prefix):
                        continue
                    base = rel.split(".gz.part")[0] + ".gz" if ".gz.part" in rel else rel
                    groups[base].append(p)
            for base, parts in groups.items():
                dest = OUT / base[:-3]
                dest.parent.mkdir(parents=True, exist_ok=True)
                joined = Path(tmp) / "_joined.gz"
                with open(joined, "wb") as j:
                    for p in sorted(parts):
                        j.write(p.read_bytes())
                with gzip.open(joined, "rb") as g, open(dest, "wb") as f:
                    shutil.copyfileobj(g, f)
                print("restored", dest.relative_to(ROOT))
        finally:
            subprocess.run(["git", "-C", str(ROOT), "worktree", "remove", "--force", tmp],
                           capture_output=True)


if __name__ == "__main__":
    main()
