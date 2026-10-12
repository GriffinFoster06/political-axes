#!/usr/bin/env python3
"""Turn collected pilot responses into analysis-ready files with quality flags.

    python3 scripts/pilot_responses.py data/pilot/responses.csv [more.csv | answers.json ...]

Inputs: CSV exports of the Google Sheet (server/README.md) and/or JSON files
people downloaded from the results page. Writes to data/pilot/ (git-ignored):

  answers_long.csv   one row per answer: rid, item, case, code, escape,
                     firmness, ms, screen_pos, display_dir, side_swap,
                     defs_opened, repeat, torn (tradeoff middle, scored as
                     the midpoint), context_shown (experiment), order_index
  respondents.csv    one row per person: mode, form, time, counts, quality
                     flags and the exclusion decision (docs/preregistration.md
                     section 3)
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import os
OUT = Path(os.environ.get("PILOT_OUT", ROOT / "data" / "pilot"))
csv.field_size_limit(10**9)


def load_bank():
    items, case_parent = {}, {}
    for p in sorted((ROOT / "items" / "drafts").glob("*.json")):
        for it in json.loads(p.read_text())["items"]:
            items[it["id"]] = it
            for c in it.get("cases", []):
                case_parent[c["id"]] = it["id"]
    return items, case_parent


def read_payloads(paths):
    out = []
    for p in map(Path, paths):
        if p.suffix == ".json":
            out.append(json.loads(p.read_text()))
            continue
        with open(p, newline="") as f:
            for r in csv.DictReader(f):
                n = int(r.get("chunks") or 0)
                body = "".join(r.get(f"payload_{k}", "") for k in range(1, n + 1))
                if body:
                    out.append(json.loads(body))
    return out


def longest_run(seq):
    best = run = 0
    prev = object()
    for x in seq:
        run = run + 1 if x == prev and x is not None else 1
        prev = x
        best = max(best, run if x is not None else 0)
    return best


def main(paths):
    items, case_parent = load_bank()
    design = json.loads((ROOT / "items" / "pilot_design.json").read_text())
    rq = json.loads((ROOT / "items" / "modules" / "quality.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    payloads = [p for p in read_payloads(paths) if not p.get("feedback")]
    seen_codes = {}
    long_rows, people = [], []
    for P in payloads:
        rid, ans, order = P["rid"], P.get("ans", {}), P.get("order", [])
        pos_in_order = {k: i for i, k in enumerate(order)}
        for key, a in ans.items():
            rep = key.endswith("#r")
            base = key[:-2] if rep else key
            item = case_parent.get(base, base)
            long_rows.append({
                "rid": rid, "item": item, "case": base if base in case_parent else "",
                "code": a.get("c"), "escape": {1: "none_fit", 2: "dont_know"}.get(a.get("e"), ""),
                "none_fit_text": a.get("x", ""), "firmness": a.get("f"), "ms": a.get("ms"),
                "screen_pos": a.get("p"), "display_dir": a.get("d"), "side_swap": a.get("s"),
                "defs_opened": "|".join(a.get("df", [])), "repeat": int(rep),
                "torn": int(bool(a.get("t"))), "context_shown": a.get("cx", ""),
                "order_index": pos_in_order.get(item if base in case_parent else key),
            })
        # assigned questions
        if P.get("mode") == "pilot" and P.get("form") is not None:
            assigned = set(design["link"]) | {i for b in P["form"] for i in design["blocks"][b]}
        else:
            assigned = set(items)
        units, answered = 0, 0
        fast = timed = 0
        for i in assigned:
            it = items[i]
            if it["format"] == "exceptions":
                keys = [c["id"] for c in it["cases"]]
            else:
                keys = [i]
            if it.get("show_if"):
                parent, codes = next(iter(it["show_if"].items()))
                if (ans.get(parent) or {}).get("c") not in codes:
                    continue
            units += len(keys)
            done = [k for k in keys if (ans.get(k) or {}).get("c") is not None or (ans.get(k) or {}).get("e") or (ans.get(k) or {}).get("t")]
            answered += len(done)
            ms = (ans.get(i) or {}).get("ms")
            if it["format"] == "exceptions":
                # case timing is recorded on the item screen; use the per-case average
                first = next((ans.get(k) for k in keys if ans.get(k)), None)
                ms = (ans.get(i) or {}).get("ms") or (first or {}).get("ms")
                if ms:
                    timed += 1
                    fast += ms / max(1, len(keys)) < 1000
            elif ms and done:
                timed += 1
                fast += ms < 2000
        # straightlining: same on-screen position across consecutive multi-option questions
        positions = []
        for k in order:
            if k.startswith("qc:") or k.endswith("#r"):
                continue
            it = items.get(k)
            if not it or it["format"] == "exceptions" or len(it["options"]) < 3:
                continue
            positions.append((ans.get(k) or {}).get("p"))
        run = longest_run(positions)
        qc = P.get("qc", {})
        qc_fail = sum(1 for q in rq["instructed_responses"]["items"] if not (qc.get(q["id"]) or {}).get("ok"))
        speed_flag = timed > 0 and fast / timed > 0.30
        straight_flag = run >= 12
        honesty = P.get("honesty")
        complete = answered / units if units else 0
        dup = P.get("code") in seen_codes
        seen_codes.setdefault(P.get("code"), rid)
        reasons = []
        if qc_fail >= 2:
            reasons.append("failed_checks")
        if speed_flag and straight_flag:
            reasons.append("speed_and_straightline")
        if honesty == 2:
            reasons.append("self_report_careless")
        if complete < 0.60:
            reasons.append("under_60pct_answered")
        if dup:
            reasons.append("duplicate_code")
        about = P.get("about", {})
        if about.get("age_bracket") == 0:
            reasons.append("under_18")
        # within-session repeat agreement
        rep_diff = []
        for i in rq["repeated_items"]["ids"]:
            a1, a2 = ans.get(i) or {}, ans.get(i + "#r") or {}
            if a1.get("c") is not None and a2.get("c") is not None:
                k = len(items[i]["options"]) - 1
                rep_diff.append(abs(a1["c"] - a2["c"]) / max(1, k))
        people.append({
            "rid": rid, "code": P.get("code"), "bank": P.get("bank"), "mode": P.get("mode"),
            "form": "-".join(map(str, P.get("form") or [])), "active_min": round(P.get("active_s", 0) / 60, 1),
            "assigned_units": units, "answered_units": answered, "complete": round(complete, 3),
            "qc_failed": qc_fail, "fast_share": round(fast / timed, 3) if timed else "",
            "longest_same_position": run, "honesty": honesty,
            "repeat_mean_diff": round(sum(rep_diff) / len(rep_diff), 3) if rep_diff else "",
            "repeat_flag": int(sum(d >= 0.5 for d in rep_diff) >= 4),
            "exclude": int(bool(reasons)), "exclude_reasons": "|".join(reasons),
            "exp_torn": int(bool((P.get("exp") or {}).get("torn"))), "exp_top_tax_swap": int(bool((P.get("exp") or {}).get("topTaxSwap"))),
            **{f"about_{k}": (json.dumps(v) if isinstance(v, list) else v) for k, v in about.items()},
        })
    with open(OUT / "answers_long.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(long_rows[0]) if long_rows else ["rid"])
        w.writeheader()
        w.writerows(long_rows)
    cols = sorted({k for p in people for k in p}, key=lambda k: (k.startswith("about_"), list(people[0]).index(k) if k in people[0] else 99, k)) if people else ["rid"]
    with open(OUT / "respondents.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(people)
    n_ex = sum(p["exclude"] for p in people)
    print(f"{len(people)} responses, {len(long_rows)} answers; {n_ex} excluded by the pre-registered rule")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
