#!/usr/bin/env python3
"""Planned-missing design for the pilots (docs/question-bank-plan.md section 9).

Every pilot taker answers:
  * the LINK block (strong general-factor questions, everyone), and
  * 3 of 9 balanced blocks, chosen as one of the 12 lines of the affine plane
    AG(2,3), so every pair of blocks is seen together by exactly 1/12 of
    people. With n takers, each block question gets about n/3 answers and each
    cross-block pair about n/12.

Questions that must be seen together stay together: a rule question and its
exceptions follow-up, and the two halves of each agree/disagree pair.

    python3 scripts/make_pilot_design.py      # writes items/pilot_design.json
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N_BLOCKS = 9

# Strong general-factor questions across many domains: the common thread that
# puts every block on one scale. Picked for content breadth, from domains where
# ANES/GSS showed the strongest left-right loadings.
LINK = [
    "abortion_rule", "health_coverage", "min_wage", "status_policy", "climate_action",
    "handgun_purchase", "college_admissions_race", "trans_school_sports", "top_income_tax",
    "legal_immigration_level", "police_spending", "same_sex_marriage", "cash_aid_level",
    "coverage_guarantee", "school_choice", "reparations", "regulation_tradeoff",
    "voter_id", "drilling_public_lands", "federal_size",
]
SECONDS = {"position": 15, "belief": 15, "frequency": 10, "tradeoff": 15, "agree_defined": 10}


def seconds(it):
    return 5 * len(it["cases"]) if it["format"] == "exceptions" else SECONDS[it["format"]]


def load():
    items = {}
    for p in sorted((ROOT / "items" / "drafts").glob("*.json")):
        d = json.loads(p.read_text())
        for it in d["items"]:
            it["_domain"] = d.get("domain_id", "core")
            items[it["id"]] = it
    return items


def bundles(items):
    """Union-find over follow-up, show_if and pair links."""
    parent = {i: i for i in items}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for i, it in items.items():
        for ref in [it.get("followup"), it.get("pair"), *it.get("show_if", {})]:
            if ref:
                union(i, ref)
    groups = defaultdict(list)
    for i in items:
        groups[find(i)].append(i)
    return [sorted(g, key=lambda x: list(items).index(x)) for g in groups.values()]


def ag23_lines():
    pts = [(x, y) for x in range(3) for y in range(3)]
    idx = {p: k for k, p in enumerate(pts)}
    lines = set()
    for (x1, y1) in pts:
        for (x2, y2) in pts:
            if (x1, y1) >= (x2, y2):
                continue
            dx, dy = (x2 - x1) % 3, (y2 - y1) % 3
            line = frozenset(idx[((x1 + t * dx) % 3, (y1 + t * dy) % 3)] for t in range(3))
            lines.add(line)
    lines = sorted(sorted(l) for l in lines)
    assert len(lines) == 12
    pairs = Counter((a, b) for l in lines for a in l for b in l if a < b)
    assert set(pairs.values()) == {1} and len(pairs) == 36
    return lines


def main():
    items = load()
    groups = bundles(items)
    link_set = set(LINK)
    missing = link_set - set(items)
    assert not missing, missing
    link, rest = [], []
    for g in groups:
        (link if link_set & set(g) else rest).append(g)
    # greedy balance: by primary axis, then by time
    rest.sort(key=lambda g: (items[g[0]]["axis"][0], -sum(seconds(items[i]) for i in g), g[0]))
    blocks = [[] for _ in range(N_BLOCKS)]
    axis_count = [Counter() for _ in range(N_BLOCKS)]
    dom_count = [Counter() for _ in range(N_BLOCKS)]
    time = [0] * N_BLOCKS
    for g in rest:
        ax, dom = items[g[0]]["axis"][0], items[g[0]]["_domain"]
        b = min(range(N_BLOCKS), key=lambda k: (axis_count[k][ax], dom_count[k][dom], time[k], k))
        blocks[b] += g
        axis_count[b][ax] += 1
        dom_count[b][dom] += 1
        time[b] += sum(seconds(items[i]) for i in g)
    link_ids = [i for g in link for i in g]
    link_time = sum(seconds(items[i]) for i in link_ids)
    lines = ag23_lines()
    forms = [link_time + sum(time[b] for b in l) for l in lines]
    out = {
        "design": "planned-missing, link block + 3 of 9 blocks per person (AG(2,3) lines)",
        "generated_by": "scripts/make_pilot_design.py",
        "seconds_per_unit": {**SECONDS, "exception_case": 5},
        "link": link_ids,
        "blocks": blocks,
        "forms": lines,
        "est_minutes": {
            "link": round(link_time / 60, 1),
            "per_block": [round(t / 60, 1) for t in time],
            "per_form_min": round(min(forms) / 60, 1),
            "per_form_max": round(max(forms) / 60, 1),
            "note": "Question time only. Add ~3 min priorities, ~2 min about-you, ~1 min checks, ~2 min intro.",
        },
        "expected_answers_per_question": "link: n; block questions: n/3; pairs of questions in different blocks: n/12",
    }
    (ROOT / "items" / "pilot_design.json").write_text(json.dumps(out, indent=1) + "\n")
    all_ids = set(link_ids) | {i for b in blocks for i in b}
    assert all_ids == set(items), set(items) ^ all_ids
    print(f"link: {len(link_ids)} items, {link_time/60:.1f} min")
    for k, b in enumerate(blocks):
        print(f"block {k}: {len(b):3d} items, {time[k]/60:4.1f} min, axes {len(axis_count[k])}")
    print(f"form length {min(forms)/60:.1f}-{max(forms)/60:.1f} min of questions")
    axes = {it['axis'][0] for it in items.values()}
    thin = [(k, sorted(axes - set(axis_count[k]) - {items[i]['axis'][0] for i in link_ids})) for k in range(N_BLOCKS)]
    print("axes missing from a block (and not in link):", [t for t in thin if t[1]])


if __name__ == "__main__":
    main()
