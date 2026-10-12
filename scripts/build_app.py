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
    }


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    b = bank()
    bank_js = "window.BANK = " + json.dumps(b, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (DIST / "bank.js").write_text(bank_js)
    for f in ("app.js", "style.css", "config.js"):
        shutil.copy(SRC / f, DIST / f)
    body = (SRC / "body.html").read_text()
    head = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, '
            'viewport-fit=cover">\n')
    fonts = (SRC / "fonts.html").read_text()
    (DIST / "index.html").write_text(
        "<!doctype html>\n<html lang=\"en\">\n<head>\n" + head + "<title>Where You Stand</title>\n" + fonts
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
