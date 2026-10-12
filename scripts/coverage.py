#!/usr/bin/env python3
"""Compare the written question bank with the plan in items/blueprint.csv.

    python3 scripts/coverage.py            # summary by domain + any gaps
    python3 scripts/coverage.py --write    # also writes items/coverage.csv

A scored unit is one position / tradeoff / frequency / belief / agree item,
or one case of an exceptions item (each case is scored on its own).
Exit code 1 if any subtopic has fewer units than planned or an item has no
subtopic.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def units(it):
    return len(it["cases"]) if it["format"] == "exceptions" else 1


def main(write=False):
    plan = list(csv.DictReader(open(ROOT / "items" / "blueprint.csv", newline="")))
    got, fmts, axes = Counter(), Counter(), Counter()
    by_sub = defaultdict(list)
    missing_sub = []
    for p in sorted((ROOT / "items" / "drafts").glob("*.json")):
        for it in json.loads(p.read_text())["items"]:
            if "subtopic" not in it:
                missing_sub.append(it["id"])
                continue
            n = units(it)
            got[it["subtopic"]] += n
            fmts[it["format"]] += n
            for ax in it.get("axis", [])[:1]:
                axes[ax] += n
            by_sub[it["subtopic"]].append(it["id"])
    rows, gaps = [], []
    dom = defaultdict(lambda: [0, 0, 0])
    for r in plan:
        g = got[r["subtopic"]]
        want = int(r["draft_items"])
        rows.append({**{k: r[k] for k in ("domain_id", "domain", "subtopic", "axis_hypothesis")},
                     "planned": want, "written": g, "items": " ".join(by_sub[r["subtopic"]])})
        d = dom[(r["domain_id"], r["domain"])]
        d[0] += want
        d[1] += g
        d[2] += 1
        if g < want:
            gaps.append(f"{r['domain_id']} {r['subtopic']}: {g}/{want}")
    print(f"{'domain':40s} planned written")
    for (did, name), (w, g, _) in sorted(dom.items()):
        print(f"{did} {name:36s} {w:7d} {g:7d}")
    tp, tw = sum(v[0] for v in dom.values()), sum(v[1] for v in dom.values())
    print(f"{'TOTAL':40s} {tp:7d} {tw:7d}")
    print("\nformats (scored units):", dict(fmts.most_common()))
    print("primary axis (scored units):", dict(sorted(axes.items())))
    thin = [a for a, n in axes.items() if a not in ("G",) and n < 10]
    if thin:
        print("axes under 10 units:", thin)
    if gaps:
        print(f"\n{len(gaps)} subtopics below plan:")
        for g in gaps:
            print("  ", g)
    if missing_sub:
        print("\nitems without a subtopic:", missing_sub)
    if write:
        with open(ROOT / "items" / "coverage.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return 1 if gaps or missing_sub else 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
