"""Rebuild modern comparison groups from simulated members (fixes 6 and 7 of the
simulation report).

Groups made of politicians in the simulation roster (sim/roster.py) are placed at
the average score of their members, computed with the quiz's own scoring from
each member's full set of simulated answers. Three past presidents are placed
from record-in-office answer sets (sim/records.py) rather than their views
today. Every other group (Pew voter types, historical parties before 2000,
ideologies, parties abroad, and modern groups with no politicians in the
roster) keeps its hand placement; those get hand-set positions on the two new
axes (PUBHEALTH, CHINA) where the group has a clear view.

Run after rev_2026_10_13_profiles.py and rev_2026_10_14_sim_fixes.py, and after
building the app (the scoring reads app/dist/bank.js):
    python3 scripts/build_app.py && python3 scripts/revisions/rev_2026_10_14_sim_profiles.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sim"))
import evaluate as E  # noqa: E402
from load import load_all, load_records  # noqa: E402
from roster import R  # noqa: E402

P = ROOT / "items" / "modules" / "profiles.json"

MEMBERS = {
    "dem_progressive": "sanders aoc omar tlaib pressley jayapal khanna warren crockett",
    "dem_mainstream": " ".join(i for i, g in E.GROUP.items() if g == "DM"),
    "blue_dog": "manchin sinema tester golden cuellar mgp gottheimer",
    "dem_socialist": "mamdani tlaib sanders cornel_west",
    "green": "stein nader cornel_west",
    "libertarian": "gjohnson amash chase_oliver rpaul_sr",
    "never_trump": "romney lcheney kinzinger hutchinson christie kasich",
    "gop_current": "thune kemp youngkin tscott burgum rubio haley cassidy mccarthy graham cotton mjohnson",
    "maga": "trump vance stefanik noem hsanders hegseth lake tuberville gaetz mtg bannon",
    "freedom_caucus": "jordan roy donalds boebert mlee cruz",
    "natcon": "hawley vance bannon",
    "religious_right": "pence huckabee santorum mjohnson carson",
    "gop_establishment": "gwbush_rec dcheney mccain romney ryan jeb mcconnell",
    "pres_trump": "trump",
    "pres_biden": "biden",
    "pres_obama": "obama_rec",
    "pres_clinton": "bclinton_rec",
    "pres_bush43": "gwbush_rec",
}

# groups the simulation showed were missing: moderate Republicans' closest group
# was Moderate Democrats, because no group sat where they do
NEW_PROFILES = [
    {"id": "gop_moderate", "name": "Moderate Republicans", "short": "Moderate GOP", "era": "2020s", "cat": "today",
     "about": "Northeastern governors and swing-state senators: fiscally conservative, socially moderate to liberal, "
              "pro-institution and pro-trade, often at odds with the national party."},
]
MEMBERS["gop_moderate"] = "collins murkowski pscott hogan sununu cox kasich schwarzenegger"

# hand placements on the new axes for groups that keep hand placement
NEW_AXES = {
    "pew_progressive": (.5, -.1), "pew_estlib": (.5, .2), "pew_mainstays": (.4, .2), "pew_outsider": (.3, -.1),
    "pew_sideliners": (0, .2), "pew_ambivalent": (-.2, .3), "pew_populist": (-.6, .5), "pew_committed": (-.4, .6),
    "pew_faithflag": (-.6, .6),
    "abundance": (.3, .2), "civil_libertarian": (-.1, -.2), "centrist": (.1, .3), "mises": (-.9, -.4),
    "tech_right": (-.5, .7), "postliberal": (.4, .6),
    "ancap": (-1, -.6), "classical_liberal": (-.6, -.3), "neoliberal": (.1, -.2), "social_democracy": (.5, 0),
    "ecosocialism": (.6, -.4), "communism": (.8, -.8), "left_anarchism": (-.6, -.7), "christian_democracy": (.4, .2),
    "neoconservatism": (0, .8), "paleoconservatism": (-.3, .3),
    "uk_labour": (.6, .1), "uk_conservatives": (.3, .3), "reform_uk": (-.4, .5), "ca_liberals": (.6, .1),
    "ca_conservatives": (-.1, .5), "nordic_sd": (.6, .1), "de_cdu": (.4, .2), "de_greens": (.6, .4),
    "fr_rn": (.1, .2), "fr_renaissance": (.5, .1),
}


def member_scores():
    people, _ = load_all()
    sets = dict(people)
    sets.update(load_records(people))
    return {pid: E.scores(E.visible_answers(a)) for pid, a in sets.items()}


def place(SC, ids):
    pos = {}
    for ax in E.AXES:
        vs = [SC[i][ax]["v"] for i in ids if E.ok(SC[i], ax)]
        if len(vs) * 2 >= len(ids) and vs:
            pos[ax] = round(sum(vs) / len(vs), 2)
    return pos


def main():
    data = json.loads(P.read_text())
    have = {p["id"] for p in data["profiles"]}
    for np_ in NEW_PROFILES:
        if np_["id"] not in have:
            i = max(k for k, p in enumerate(data["profiles"]) if p["cat"] == np_["cat"])
            data["profiles"].insert(i + 1, dict(np_, pos={}))
    SC = member_scores()
    names = {r["id"]: r["name"] for r in R}
    from records import RECORDS
    for rid, rec in RECORDS.items():
        names[rid] = f"{names[rec['base']]} (record in office, {rec['years']})"
    seen = set()
    for p in data["profiles"]:
        if p["id"] in MEMBERS:
            ids = MEMBERS[p["id"]].split()
            old = p.get("hand_pos") or p["pos"]
            if old:
                p["hand_pos"] = old
            p["pos"] = place(SC, ids)
            p["basis"] = {"kind": "sim", "members": [names[i] for i in ids], "ids": ids}
            seen.add(p["id"])
        else:
            p.pop("basis", None)
            if p["id"] in NEW_AXES:
                ph, ch = NEW_AXES[p["id"]]
                p["pos"]["PUBHEALTH"], p["pos"]["CHINA"] = ph, ch
    missing = set(MEMBERS) - seen
    assert not missing, missing
    P.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    for pid in MEMBERS:
        p = next(x for x in data["profiles"] if x["id"] == pid)
        gaps = {ax: round(p["pos"][ax] - v, 2) for ax, v in p.get("hand_pos", {}).items() if ax in p["pos"] and abs(p["pos"][ax] - v) >= 0.35}
        print(f"{pid:18} G {p['pos'].get('G')}  big moves from hand placement: {gaps}")


if __name__ == "__main__":
    main()
