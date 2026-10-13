"""Scoring fixes from the 135-politician simulation (sim/README.md, report 2026-10-13).

1. Free speech and federalism are scored as consistency. Each question on these
   axes is tagged with the side whose speech (or whose state policies) the
   protective answer helps. The score weights the left-coded and right-coded
   questions equally, so protecting only your own side's speech no longer reads
   as "protect all speech". The gap between the two halves is reported
   separately as lopsidedness. The employer-firing and platform-moderation
   questions come off free speech: they are about private companies, and they
   split people by party rather than by how much they protect speech.
2. Personal freedom is split. LIBERTY keeps drugs, gambling, sex work and
   end-of-life choices. A new PUBHEALTH axis takes health and safety rules
   (vaccines, helmets, vapes, sugary-drink taxes, raw milk, insurance mandates).
   The two pulled in opposite partisan directions and cancelled out.
3. China gets its own axis (CHINA). China trade, ownership, chip exports, the AI
   race and overall posture come off HAWK, which keeps military force and
   spending. Israel aid, arms sales and trust in military leaders also come off
   HAWK, as does required national service: they measure alliances, trust and
   civic duty, not readiness to use force.
4. Four questions come off the overall score, because in the simulation they
   ran against it: conscience_vs_law, nato, ukraine_support, data_centers.
   marijuana_records leaves personal freedom (it is a criminal-justice question).

Run: python3 scripts/revisions/rev_2026_10_14_sim_fixes.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEY = ROOT / "items" / "keying.txt"
AXES = ROOT / "items" / "modules" / "axes.json"

# full replacement lines for keying.txt (id -> rest of line)
NEW_KEYS = {
    # fix 4: off the overall score
    "conscience_vs_law": "0 VALUES+",
    "nato": "0 GLOBAL+",
    "ukraine_support": "0 GLOBAL+ HAWK-",
    "data_centers": "0 TECH+ ENV+",
    # fix 3: China axis; HAWK keeps force and spending
    "china_trade": "0 TRADE+ CHINA+",
    "china_ownership": "0 TRADE+ CHINA+",
    "export_controls": "0 CHINA+ TRADE+",
    "ai_china_race": "0 TECH+ CHINA+",
    "china_posture": "0 CHINA+",
    "taiwan_defense": "0 CHINA+ HAWK+",
    "israel_military_aid": "-",
    "arms_sales": "0",
    "trust_military": "- TRUST+",
    "national_service": "0",  # required service is civic, not readiness to use force
    # fix 1: speech questions about private companies leave SPEECH
    "employer_speech": "0 REG+",
    "employer_speech_cases": "0",
    "fire_racist_joke": "-",
    "fire_praise_attack": "+",
    "moderation_false": "+ TECH+",
    "moderation_offensive": "+",
    "moderation_law": "+ TECH-",
    # fix 2: health and safety rules move to PUBHEALTH
    "school_vaccines": "+ PUBHEALTH-",
    "vaccine_exemptions": "+ PUBHEALTH-",
    "outbreak_gov_mandate": "+ PUBHEALTH-",
    "outbreak_employer": "+",
    "insurance_mandate": "+ SOCINS+ PUBHEALTH-",
    "sin_taxes": "- PUBHEALTH+",
    "helmet_law": "- PUBHEALTH+",
    "drinking_age": "0 PUBHEALTH+",
    "vape_flavors": "- PUBHEALTH+",
    "raw_milk": "- PUBHEALTH+",
    "right_to_try": "- PUBHEALTH+",
    "involuntary_treatment": "0 PUBHEALTH+",
    "aid_form": "+",
    "plastic_bags": "+ ENV+",
    "social_media_min_age": "0 TECH-",
    "ai_companions_minors": "0 TECH+",
    "marijuana_records": "+ ORDER+",
}

# fix 1: which side the protective answer helps. FED tags are by hand (most
# federalism questions have no overall-score key); SPEECH tags follow from the
# keys: the protective end of a question is right-coded when its high end is
# left and limits speech, and so on.
FED_SIDES = {
    "L": ["gc_immigration", "gc_sports_allow", "gc_police_cuts", "sr_immigration", "sr_marijuana",
          "ai_state_laws", "state_preemption", "grant_conditions", "state_refusal"],
    "R": ["gc_abortion", "gc_sports_ban", "sr_guns", "sd_guns", "sd_min_wage", "sd_voting", "sd_marriage",
          "abortion_who_decides", "education_department", "federal_size", "sell_public_land",
          "closer_government_tradeoff"],
}

LIB_BANDS = [
    "Adults should be free to use drugs, gamble, sell sex or end their lives as they choose.",
    "Mostly legal and regulated, with limits on the riskiest choices.",
    "Mixed: legal for some choices, prohibited for others.",
    "Mostly prohibited, with room for medical use and narrow exceptions.",
    "Drugs, gambling, sex work and assisted dying should stay illegal and be enforced.",
]
PH_BANDS = [
    "Adults and parents decide about vaccines, helmets, raw milk and other health risks; no mandates.",
    "Mostly individual choice, with a few rules like school vaccines.",
    "Mixed: some health and safety mandates make sense, others go too far.",
    "Health and safety rules are usually worth it, from school vaccines to vape limits.",
    "Strong public-health rules: mandates, bans and taxes that steer people away from health risks.",
]
CHINA_BANDS = [
    "Treat China like any other country: trade freely and cooperate on shared problems.",
    "Engage China, with limits on sensitive technology.",
    "Compete with China and protect key industries, but keep talking and trading.",
    "Treat China as a serious rival: limit trade, ownership and technology sales.",
    "China is the main adversary: cut ties, block investment and confront it on every front.",
]


def keys():
    lines = KEY.read_text().splitlines()
    seen = set()
    out = []
    for ln in lines:
        s = ln.split("#", 1)[0].strip()
        iid = s.split()[0] if s else None
        if iid in NEW_KEYS:
            out.append(f"{iid} {NEW_KEYS[iid]}")
            seen.add(iid)
        else:
            out.append(ln)
    missing = set(NEW_KEYS) - seen
    case_lines = [i for i in missing if i in ("fire_racist_joke", "fire_praise_attack")]
    assert set(missing) <= set(case_lines), missing
    KEY.write_text("\n".join(out) + "\n")


def parse_keys():
    k = {}
    for ln in KEY.read_text().splitlines():
        s = ln.split("#", 1)[0].strip()
        if not s:
            continue
        p = s.split()
        d = {"G": {"+": 1, "-": -1, "0": 0}[p[1]]}
        for t in p[2:]:
            d[t[:-1]] = 1 if t[-1] == "+" else -1
        k[p[0]] = d
    return k


def axes():
    a = json.loads(AXES.read_text())
    fams = a["families"]
    order_fam = next(f for f in fams if any(x["id"] == "LIBERTY" for x in f["axes"]))
    world = next(f for f in fams if any(x["id"] == "HAWK" for x in f["axes"]))
    lib = next(x for x in order_fam["axes"] if x["id"] == "LIBERTY")
    lib.update({"name": "Drugs and vice laws", "minus": "Legalize; adults choose", "plus": "Prohibit",
                "about": "Whether drugs, gambling, sex work and assisted dying should be legal for adults or prohibited.",
                "bands": LIB_BANDS})
    if not any(x["id"] == "PUBHEALTH" for x in order_fam["axes"]):
        i = order_fam["axes"].index(lib)
        order_fam["axes"].insert(i + 1, {"id": "PUBHEALTH", "name": "Health and safety rules", "minus": "Individual choice",
                                         "plus": "Public-health rules",
                                         "about": "Whether government should require or discourage things for health and safety: vaccines, helmets, vapes, sugary drinks.",
                                         "bands": PH_BANDS})
    hawk = next(x for x in world["axes"] if x["id"] == "HAWK")
    hawk["about"] = "How readily to use military force abroad and how big a military to keep."
    if not any(x["id"] == "CHINA" for x in world["axes"]):
        i = world["axes"].index(hawk)
        world["axes"].insert(i + 1, {"id": "CHINA", "name": "China", "minus": "Engage", "plus": "Confront",
                                     "about": "How hard to compete with and confront China: trade, ownership, technology and Taiwan.",
                                     "bands": CHINA_BANDS})
    speech = next(x for x in order_fam["axes"] if x["id"] == "SPEECH")
    speech["about"] = ("How far to protect offensive, false or hateful speech, counted evenly across speech the left "
                       "dislikes and speech the right dislikes.")
    fed = next(x for f in fams for x in f["axes"] if x["id"] == "FED")
    fed["about"] = ("Whether big decisions should be made nationally or left to states and cities, counted evenly across "
                    "cases where state power helps the left and where it helps the right.")
    AXES.write_text(json.dumps(a, indent=1, ensure_ascii=False) + "\n")  # so the bank builds with the new axes
    # side tags
    k = parse_keys()
    cases = {}
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from build_app import bank as _bank  # noqa: E402
    items = _bank()["items"]
    for iid, it in items.items():
        for c in it.get("cases", []):
            cases[c["id"]] = iid
    sp = {}
    for iid in list(items) + list(cases):
        kk = k.get(iid) or (k.get(cases[iid]) if iid in cases else None)
        if iid in cases and iid not in k:
            kk = k.get(cases[iid])
        if not kk or not kk.get("SPEECH") or items.get(cases.get(iid, iid), {}).get("issue_map_only"):
            continue
        if iid in items and items[iid]["format"] == "exceptions":
            continue  # the cases carry the tags
        g = kk.get("G", 0)
        sp[iid] = "N" if not g else ("R" if -g * kk["SPEECH"] > 0 else "L")
    fed_sides = {i: s for s, ids in FED_SIDES.items() for i in ids}
    a["balanced"] = {
        "SPEECH": {"sides": sp, "protect": -1,
                   "note_L": "speech the right objects to", "note_R": "speech the left objects to"},
        "FED": {"sides": fed_sides, "protect": 1,
                "note_L": "states and cities pursuing left-leaning policies", "note_R": "states pursuing right-leaning policies"},
    }
    a["note"] = ("Display names and poles for the scores. Scores run from -100 (minus pole) to +100 (plus pole). "
                 "'balanced' axes weight left-coded and right-coded questions equally; see "
                 "scripts/revisions/rev_2026_10_14_sim_fixes.py.")
    AXES.write_text(json.dumps(a, indent=1, ensure_ascii=False) + "\n")
    n = sum(len(f["axes"]) for f in fams)
    print("axes:", n, "speech sides:", {s: sum(v == s for v in sp.values()) for s in "LRN"},
          "fed sides:", {s: sum(v == s for v in fed_sides.values()) for s in "LR"})


if __name__ == "__main__":
    keys()
    axes()
