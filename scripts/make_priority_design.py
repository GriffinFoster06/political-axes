#!/usr/bin/env python3
"""Build the best-worst design for the priorities module.

25 topic areas are points (x, y) of the affine plane over Z5. Lines of slope
0, 1 and 2 (three parallel classes) give 15 sets of 5 topics. Every topic
appears in exactly 3 sets and no two topics share more than one set, so
each topic is compared against 12 different others with equal exposure.

    python3 scripts/make_priority_design.py   # writes items/modules/priorities.json
"""
import csv
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Plain-language labels shown to people (no party or ideology cues).
LABELS = {
    "D01": "Taxes and help for low-income families",
    "D02": "Wages, unions and rules for business",
    "D03": "Health care, Social Security and Medicare",
    "D04": "Housing costs and homelessness",
    "D05": "Climate, energy and the environment",
    "D06": "Trade, tariffs and American manufacturing",
    "D07": "Technology, AI and social media",
    "D08": "Privacy and government surveillance",
    "D09": "Abortion and reproductive issues",
    "D10": "Sexual orientation and gender identity",
    "D11": "Religion in public life",
    "D12": "Family, marriage and children",
    "D13": "Race and discrimination",
    "D14": "Immigration and national identity",
    "D15": "Crime, policing and prisons",
    "D16": "Guns",
    "D17": "Drugs and personal freedom",
    "D18": "Free speech",
    "D19": "Limits on presidential power",
    "D20": "Voting and elections",
    "D21": "Honesty and competence of government and institutions",
    "D22": "Foreign policy and the military",
    "D23": "Schools and college costs",
    "D24": "Federal versus state power",
    "D25": "Moral values in society",
}


def main():
    domains = []
    with open(ROOT / "items" / "blueprint.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["domain_id"] not in domains:
                domains.append(r["domain_id"])
    assert len(domains) == 25 and set(domains) == set(LABELS)
    point = {(i // 5, i % 5): d for i, d in enumerate(sorted(domains))}
    sets = []
    for m in range(3):
        for b in range(5):
            sets.append([point[(x, (m * x + b) % 5)] for x in range(5)])
    count = Counter(d for s in sets for d in s)
    assert set(count.values()) == {3}
    pairs = Counter(p for s in sets for p in itertools.combinations(sorted(s), 2))
    assert max(pairs.values()) == 1
    out = {
        "module": "priorities",
        "status": "DRAFT v0.1",
        "method": "Best-worst scaling (MaxDiff). 15 sets of 5 topics from three parallel classes of the affine plane AG(2,5): each topic shown 3 times, no pair of topics shown together more than once. Set order and topic order within sets are randomized per person. Scored as importance weights (count best minus count worst, then a multinomial logit on pilot data). Never used to compute axis positions; used to weight the issue map and the 'what you care about most' summary.",
        "stem": "Of these five topics, which matters MOST to you when you think about politics, and which matters LEAST?",
        "scope": "There are no right answers. Pick one of each, even if it's a close call.",
        "labels": LABELS,
        "sets": sets,
    }
    p = ROOT / "items" / "modules" / "priorities.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {p.relative_to(ROOT)}: {len(sets)} sets, each topic {set(count.values())} times")


if __name__ == "__main__":
    main()
