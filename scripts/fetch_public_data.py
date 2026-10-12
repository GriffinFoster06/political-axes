#!/usr/bin/env python3
"""Download the public, no-login datasets this project uses.

Runs inside the GitHub Action (.github/workflows/fetch-data.yml) or on your Mac:

    python3 scripts/fetch_public_data.py --out data/staging

Sources (all free; cite them, see DATA.md):
- GSS 1972-2024 cumulative file, as packaged by gssr (MIT-licensed R package)
- Voteview: all members and roll calls since 1789, plus individual votes for
  the most recent Congresses
- Cooperative Election Study (CES): 2024 Common Content and the 2006-2024
  cumulative file, via the Harvard Dataverse API

Not included because they need a login or API key: ANES, Pew microdata,
Manifesto Project. Use scripts/push_local_data.sh for those.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = {"User-Agent": "political-axes-data-fetch/0.1 (personal research project)"}

GSS = [("gss/gss_all.rda", "https://github.com/kjhealy/gssr/raw/main/data/gss_all.rda")]

VOTEVIEW_BASE = "https://voteview.com/static/data/out"
VOTEVIEW = [
    ("voteview/HSall_members.csv", f"{VOTEVIEW_BASE}/members/HSall_members.csv"),
    ("voteview/HSall_rollcalls.csv", f"{VOTEVIEW_BASE}/rollcalls/HSall_rollcalls.csv"),
    ("voteview/HSall_parties.csv", f"{VOTEVIEW_BASE}/parties/HSall_parties.csv"),
]
VOTE_CONGRESSES = range(110, 120)  # 2007-2026

DATAVERSE = "https://dataverse.harvard.edu"
CES = {
    "ces2024": "doi:10.7910/DVN/X11EP6",
    "ces_cumulative": "doi:10.7910/DVN/II2DB6",
}
CES_KEEP_EXT = (".csv", ".feather", ".pdf")  # one format per file; .dta/.rds duplicate these


def get(url: str, dest: Path, retries: int = 3) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            h = hashlib.sha256()
            n = 0
            with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
                    h.update(chunk)
                    n += len(chunk)
            return {"url": url, "bytes": n, "sha256": h.hexdigest()}
        except Exception as e:  # noqa: BLE001
            print(f"  attempt {attempt + 1} failed for {url}: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"giving up on {url}")


def dataverse_files(doi: str) -> list[dict]:
    url = f"{DATAVERSE}/api/datasets/:persistentId/?persistentId={doi}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        meta = json.load(r)
    files = meta["data"]["latestVersion"]["files"]
    out = []
    for f in files:
        df = f["dataFile"]
        name = df.get("originalFileName") or df["filename"]
        out.append({"id": df["id"], "name": name, "size": df.get("originalFileSize") or df.get("filesize"),
                    "restricted": f.get("restricted", False)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/staging")
    ap.add_argument("--skip", nargs="*", default=[], help="gss voteview ces")
    args = ap.parse_args()
    out = Path(args.out)
    manifest = {"fetched_at": datetime.now(timezone.utc).isoformat(), "files": {}}
    failures = []

    def fetch(rel, url):
        print("->", rel)
        try:
            manifest["files"][rel] = get(url, out / rel)
        except RuntimeError as e:
            failures.append(str(e))

    if "gss" not in args.skip:
        for rel, url in GSS:
            fetch(rel, url)
    if "voteview" not in args.skip:
        for rel, url in VOTEVIEW:
            fetch(rel, url)
        for c in VOTE_CONGRESSES:
            for ch in ("H", "S"):
                fetch(f"voteview/votes/{ch}{c}_votes.csv", f"{VOTEVIEW_BASE}/votes/{ch}{c}_votes.csv")
    if "ces" not in args.skip:
        for key, doi in CES.items():
            try:
                files = dataverse_files(doi)
            except Exception as e:  # noqa: BLE001
                failures.append(f"{key}: could not list files ({e})")
                continue
            for f in files:
                if f["restricted"] or not f["name"].lower().endswith(CES_KEEP_EXT):
                    continue
                fetch(f"ces/{key}/{f['name']}",
                      f"{DATAVERSE}/api/access/datafile/{f['id']}?format=original")

    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=1))
    print(f"\nfetched {len(manifest['files'])} files")
    if failures:
        print("FAILURES:\n  " + "\n  ".join(failures))
        (out / "FAILURES.txt").write_text("\n".join(failures))


if __name__ == "__main__":
    main()
