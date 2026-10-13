#!/usr/bin/env python3
"""Build the pilot quiz app from the question bank.

    python3 scripts/build_app.py

Reads items/drafts/*.json, items/modules/*.json, items/pilot_design.json and
app/src/*, and writes:

  app/dist/index.html   standalone site (open locally or host on GitHub Pages)
  app/dist/bank.js      the bank as `window.BANK = {...}`
  app/dist/app.js, app/dist/style.css, app/dist/config.js (copied from app/src)
  app/dist/quiz.html    a single self-contained fragment (everything inline),
                        used for previews
"""
from __future__ import annotations

import csv
import json
import os
import shutil
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC, DIST = ROOT / "app" / "src", ROOT / "app" / "dist"


def bank():
    bp, dom_names = [], {}
    with open(ROOT / "items" / "blueprint.csv", newline="") as f:
        for r in csv.DictReader(f):
            bp.append((r["domain_id"], r["subtopic"]))
            dom_names[r["domain_id"]] = r["domain"]
    sub_dom = {s: d for d, s in bp}
    sub_idx = {s: k for k, (_, s) in enumerate(bp)}
    items = {}
    for p in sorted((ROOT / "items" / "drafts").glob("*.json")):
        for it in json.loads(p.read_text())["items"]:
            it = {k: v for k, v in it.items() if k not in ("links", "notes", "dimension_hint")}
            it["domain"] = sub_dom[it["subtopic"]]
            items[it["id"]] = it
    order = {d: [] for d in dom_names}
    file_pos = {i: k for k, i in enumerate(items)}
    for i in sorted(items, key=lambda i: (sub_idx[items[i]["subtopic"]], file_pos[i])):
        order[items[i]["domain"]].append(i)
    mods = {p.stem: json.loads(p.read_text()) for p in (ROOT / "items" / "modules").glob("*.json")}
    # Version = hash of the question content, so saved progress survives app-only redeploys
    # but is reset if any question changes.
    ver = hashlib.sha1(json.dumps(items, sort_keys=True).encode()).hexdigest()[:10]
    return {
        "version": ver,
        "domains": [{"id": d, "name": n, "label": mods["priorities"]["labels"][d]} for d, n in dom_names.items()],
        "order": order,
        "items": items,
        "design": json.loads((ROOT / "items" / "pilot_design.json").read_text()),
        "intro": mods["intro"], "priorities": mods["priorities"], "quality": mods["quality"],
        "about": mods["about_you"],
        "axes": mods["axes"], "profiles": [{k: v for k, v in p.items() if k != "hand_pos"} for p in mods["profiles"]["profiles"]], "profileCats": mods["profiles"]["categories"], "quick": mods["quick"]["ids"],
        "keying": keying(items, mods["axes"]),
    }


def keying(items, axes):
    """Parse items/keying.txt -> {id: {"G": sign, AXIS: sign}} and check it covers the bank."""
    valid = {a["id"] for f in axes["families"] for a in f["axes"]}
    case_ids = {c["id"] for it in items.values() for c in it.get("cases", [])}
    out = {}
    for n, line in enumerate((ROOT / "items" / "keying.txt").read_text().splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        iid, g = parts[0], parts[1]
        if iid not in items and iid not in case_ids:
            raise SystemExit(f"keying.txt line {n}: unknown id {iid}")
        k = {"G": {"+": 1, "-": -1, "0": 0}[g]}
        for tok in parts[2:]:
            ax, sign = tok[:-1], tok[-1]
            if ax not in valid or sign not in "+-":
                raise SystemExit(f"keying.txt line {n}: bad axis token {tok}")
            k[ax] = 1 if sign == "+" else -1
        out[iid] = k
    missing = [i for i, it in items.items() if i not in out and not it.get("issue_map_only")]
    if missing:
        raise SystemExit(f"keying.txt is missing: {missing}")
    return out


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    b = bank()
    bank_js = "window.BANK = " + json.dumps(b, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (DIST / "bank.js").write_text(bank_js)
    for f in ("app.js", "style.css", "config.js"):
        shutil.copy(SRC / f, DIST / f)
    for f in (SRC / "static").glob("*"):
        shutil.copy(f, DIST / f.name)
    body = (SRC / "body.html").read_text()
    site = os.environ.get("URL", "").rstrip("/")  # Netlify sets URL at build time
    desc = ("A deeper map of your US politics: real positions on 25 topics, up to 31 dimensions, "
            "and the parties past and present you're closest to.")
    head = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, '
            'viewport-fit=cover">\n'
            f'<meta name="description" content="{desc}">\n'
            '<meta name="theme-color" content="#eceef2">\n'
            '<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="Where You Stand">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{site}/og.png">\n'
            '<meta name="twitter:card" content="summary_large_image">\n')
    fonts = (SRC / "fonts.html").read_text()  # Google Fonts, for the single-file preview
    fonts_local = (SRC / "fonts-local.html").read_text()  # self-hosted copies for the real site (no third-party requests)
    (DIST / "index.html").write_text(
        "<!doctype html>\n<html lang=\"en\">\n<head>\n" + head + "<title>Where You Stand</title>\n" + fonts_local
        + '<link rel="stylesheet" href="style.css">\n</head>\n<body>\n' + body
        + '<script src="config.js"></script>\n<script src="bank.js"></script>\n<script src="app.js"></script>\n'
        + "</body>\n</html>\n")
    css = (SRC / "style.css").read_text()
    js = (SRC / "app.js").read_text()
    cfg = (SRC / "config.js").read_text()
    (DIST / "quiz.html").write_text(
        "<title>Where You Stand</title>\n" + fonts + "<style>\n" + css + "</style>\n" + body
        + "<script>\n" + cfg + "</script>\n<script>\n" + bank_js + "</script>\n<script>\n" + js + "</script>\n")
    n = len(b["items"])
    print(f"built app/dist: {n} items, bank {len(bank_js)//1024} KB, version {b['version']}")


if __name__ == "__main__":
    main()
