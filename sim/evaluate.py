"""Score the simulated politicians with the quiz's own scoring and check the
pre-registered expectations in sim/roster.py.

Writes sim/out/scores.csv, sim/out/summary.json and prints a readable summary.
Run: python3 sim/evaluate.py
"""
import csv, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sim"))
from load import load_all, BANK  # noqa: E402
from roster import R, ORDER  # noqa: E402
from archetypes import G as GROUP  # noqa: E402

OUT = ROOT / "sim" / "out"
OUT.mkdir(exist_ok=True)
ITEMS, KEY = BANK["items"], BANK["keying"]
AX_META = {"G": BANK["axes"]["overall"]}
for f in BANK["axes"]["families"]:
    for a in f["axes"]:
        AX_META[a["id"]] = a
AXES = list(AX_META)
PROFILES = BANK["profiles"]
MIN_N = 3
ECON = ["REDIS", "REG", "SOCINS"]
CULT = ["MORAL", "GENDERID", "RELIGION", "FAMILY", "EQUITY", "IMMIG", "NATION"]
LR_AXES = ["REDIS", "REG", "SOCINS", "ENV", "MORAL", "GENDERID", "RELIGION", "FAMILY", "EQUITY", "IMMIG", "NATION", "ORDER", "GUNS", "EDUC", "VOTING", "VALUES"]
PARENT = {it["followup"]: i for i, it in ITEMS.items() if it.get("followup")}


# ---------------- what the app would actually have shown ----------------
def visible_answers(ans):
    """Drop answers to follow-ups the app would have hidden (same rules as app.js visible())."""
    out = dict(ans)
    for i, it in ITEMS.items():
        show = True
        if it.get("show_if"):
            p, codes = next(iter(it["show_if"].items()))
            pa = ans.get(p)
            show = bool(pa and pa.get("c") is not None and pa["c"] in codes)
        elif i in PARENT:
            pa = ans.get(PARENT[i])
            show = bool(pa and pa.get("c") is not None)
        if not show:
            out.pop(i, None)
            for c in it.get("cases", []):
                out.pop(c["id"], None)
    return out


# ---------------- scoring: a line-for-line port of computeScores() in app.js ----------------
def item_values(ans):
    """(item id, case id or None, x in [-1, 1], weight) for every scored answer."""
    vals = []
    for i, it in ITEMS.items():
        if it.get("issue_map_only"):
            continue
        if it["format"] == "exceptions":
            K = len(it["options"])
            for c in it["cases"]:
                a = ans.get(c["id"])
                if a and a.get("c") is not None:
                    vals.append((i, c["id"], 2 * a["c"] / (K - 1) - 1, 0.5))
            continue
        a = ans.get(i)
        if not a:
            continue
        if a.get("t"):
            x = 0.0
        elif a.get("c") is not None:
            x = 2 * a["c"] / (len(it["options"]) - 1) - 1
        else:
            continue
        vals.append((i, None, x, 1.0))
    return vals


def scores(ans):
    acc = defaultdict(lambda: [0.0, 0.0, 0])
    for i, cid, x, w in item_values(ans):
        k = KEY.get(cid) if cid and cid in KEY else KEY.get(i)
        if not k:
            continue
        for ax, s in k.items():
            if not s:
                continue
            o = acc[ax]
            o[0] += s * x * w; o[1] += w; o[2] += 1
    return {ax: {"v": s / w, "n": n} for ax, (s, w, n) in acc.items()}


def ok(sc, ax):
    return ax in sc and sc[ax]["n"] >= MIN_N


def match_one(sc, pos):
    s = w = 0.0
    diffs = []
    for ax, v in pos.items():
        if not ok(sc, ax):
            continue
        k = 2 if ax == "G" else 1
        d = abs(sc[ax]["v"] - v)
        s += k * d * d; w += k
        if ax != "G":
            diffs.append(d)
    if len(diffs) < 6:
        return None
    rms = math.sqrt((s + 0.25) / (w + 1))
    return max(0, round(100 * (1 - rms / 2)))


def matches(sc):
    out = []
    for p in PROFILES:
        m = match_one(sc, p["pos"])
        if m is not None:
            out.append((m, p["id"]))
    return [pid for m, pid in sorted(out, key=lambda t: -t[0])], dict((pid, m) for m, pid in out)


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def userpos(sc, axes):
    return mean(sc[a]["v"] for a in axes if ok(sc, a))


def archetype(sc):
    e, c = userpos(sc, ECON), userpos(sc, CULT)
    if e is None or c is None:
        return None
    E = 0 if e < -0.2 else 2 if e > 0.2 else 1
    C = 0 if c < -0.2 else 2 if c > 0.2 else 1
    core = [["Progressive", "Economic progressive", "Communitarian"], ["Liberal", "Moderate", "Traditionalist"], ["Libertarian", "Free-market moderate", "Conservative"]][E][C]
    return core


def consistency(sc):
    L = R_ = M = 0
    for ax in LR_AXES:
        if not ok(sc, ax):
            continue
        v = sc[ax]["v"]
        if v < -0.1: L += 1
        elif v > 0.1: R_ += 1
        else: M += 1
    n = L + R_
    share = min(L, R_) / n if n else 0
    return "Consistent" if share < 0.12 else "Mostly consistent" if share < 0.3 else "Cross-pressured"


def corr(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(sxx * syy)


def auc(neg, pos):
    """P(random pos > random neg)."""
    wins = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    return wins / (len(pos) * len(neg))


def main():
    people, done = load_all()
    assert len(done) == 25, done
    roster = {r["id"]: r for r in R}
    SC, VIS = {}, {}
    for pid, ans in people.items():
        VIS[pid] = visible_answers(ans)
        SC[pid] = scores(VIS[pid])

    # ---------- per-politician table ----------
    rows, topm = [], {}
    for r in R:
        sc = SC[r["id"]]
        order, mm = matches(sc)
        topm[r["id"]] = (order, mm)
        row = {"id": r["id"], "name": r["name"], "party": r["party"], "group": GROUP[r["id"]],
               "archetype": archetype(sc), "consistency": consistency(sc),
               "econ": round(userpos(sc, ECON), 3), "cult": round(userpos(sc, CULT), 3),
               "top1": order[0], "top1_match": mm[order[0]], "top2": order[1], "top3": order[2],
               "answers": len(VIS[r["id"]])}
        for ax in AXES:
            row[ax] = round(sc[ax]["v"], 3) if ok(sc, ax) else ""
        rows.append(row)
    with open(OUT / "scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    res = {"n": len(R), "topics": len(done)}

    # ---------- H1: party separation on the overall score ----------
    G = {r["id"]: SC[r["id"]]["G"]["v"] for r in R}
    dem = [G[r["id"]] for r in R if r["party"] == "D"]
    rep = [G[r["id"]] for r in R if r["party"] == "R"]
    res["party_auc"] = round(auc(dem, rep), 4)
    res["party_G"] = {"D_min": round(min(dem), 3), "D_max": round(max(dem), 3), "R_min": round(min(rep), 3), "R_max": round(max(rep), 3),
                      "D_mean": round(mean(dem), 3), "R_mean": round(mean(rep), 3)}
    overlap = [(r["name"], r["party"], round(G[r["id"]], 3)) for r in R
               if (r["party"] == "D" and G[r["id"]] > min(rep)) or (r["party"] == "R" and G[r["id"]] < max(dem))]
    res["party_overlap"] = overlap

    # ---------- H2: pre-registered within-party orderings ----------
    ok_pairs = [(a, b, round(G[a], 3), round(G[b], 3), G[a] < G[b]) for a, b in ORDER]
    res["order_hits"] = sum(x[4] for x in ok_pairs); res["order_total"] = len(ok_pairs)
    res["order_misses"] = [(roster[a]["name"], roster[b]["name"], ga, gb) for a, b, ga, gb, hit in ok_pairs if not hit]

    # ---------- H3: pre-registered axis signatures ----------
    sig_rows = []
    for r in R:
        sc = SC[r["id"]]
        for tok in r["sig"]:
            ax, want = tok[:-1], tok[-1]
            if not ok(sc, ax):
                sig_rows.append((r["id"], ax, want, None, None)); continue
            v = sc[ax]["v"]
            hit = v > 0.2 if want == "+" else v < -0.2 if want == "-" else abs(v) <= 0.35
            sig_rows.append((r["id"], ax, want, round(v, 3), hit))
    scored = [s for s in sig_rows if s[4] is not None]
    res["sig_hits"] = sum(s[4] for s in scored); res["sig_total"] = len(scored); res["sig_unscored"] = len(sig_rows) - len(scored)
    by_ax = defaultdict(lambda: [0, 0])
    for s in scored:
        by_ax[s[1]][0] += s[4]; by_ax[s[1]][1] += 1
    res["sig_by_axis"] = {ax: f"{h}/{t}" for ax, (h, t) in sorted(by_ax.items(), key=lambda kv: kv[1][0] / kv[1][1])}
    g_sig = [s for s in scored if s[1] != "G"]
    res["sig_hits_nonG"] = sum(s[4] for s in g_sig); res["sig_total_nonG"] = len(g_sig)
    res["sig_misses"] = [(roster[i]["name"], ax, want, v) for i, ax, want, v, hit in scored if not hit]

    # ---------- H4: expected comparison-group matches ----------
    hit1 = hit3 = hit5 = 0
    miss5 = []
    for r in R:
        order = topm[r["id"]][0]
        e = set(r["expect_match"])
        if order[0] in e: hit1 += 1
        if e & set(order[:3]): hit3 += 1
        if e & set(order[:5]): hit5 += 1
        else: miss5.append((r["name"], order[:3]))
    res["match_top1"], res["match_top3"], res["match_top5"] = hit1, hit3, hit5
    res["match_miss5"] = miss5
    # the five presidents and VPs with their own profile
    selfp = {"biden": "pres_biden", "obama": "pres_obama", "trump": "pres_trump", "gwbush": "pres_bush43", "bclinton": "pres_clinton"}
    res["president_self_rank"] = {k: topm[k][0].index(v) + 1 for k, v in selfp.items()}
    # does the top match come from the politician's own side?
    side = {"dem_progressive": "L", "dem_mainstream": "L", "blue_dog": "L", "abundance": "L", "dem_socialist": "L", "green": "L", "civil_libertarian": "L",
            "pew_progressive": "L", "pew_estlib": "L", "pew_mainstays": "L", "pew_outsider": "L"}
    for p in PROFILES:
        if p["id"] not in side:
            gp = p["pos"].get("G")
            side[p["id"]] = None if gp is None else ("L" if gp < -0.15 else "R" if gp > 0.15 else "C")
    same = cross = 0
    for r in R:
        if r["party"] not in ("D", "R"):
            continue
        s = side.get(topm[r["id"]][0][0])
        want = "L" if r["party"] == "D" else "R"
        if s == want: same += 1
        elif s and s != "C": cross += 1
    res["top_match_same_side"], res["top_match_cross_side"] = same, cross

    # ---------- labels ----------
    res["archetypes_by_group"] = {g: dict(Counter(archetype(SC[r["id"]]) for r in R if GROUP[r["id"]] == g)) for g in sorted(set(GROUP.values()))}
    res["consistency_by_group"] = {g: dict(Counter(consistency(SC[r["id"]]) for r in R if GROUP[r["id"]] == g)) for g in sorted(set(GROUP.values()))}

    # ---------- reliability: Cronbach's alpha per axis across politicians ----------
    # item score = key sign x answer value, missing = skipped; case answers grouped by parent item
    def keyed_matrix(ax):
        cols = {}
        for pid in SC:
            for i, cid, x, w in item_values(VIS[pid]):
                k = KEY.get(cid) if cid and cid in KEY else KEY.get(i)
                if not k or not k.get(ax):
                    continue
                col = cid or i
                cols.setdefault(col, {})[pid] = k[ax] * x
        return cols
    rel, bad_items, flat_items = {}, [], []
    pids = list(SC)
    for ax in AXES:
        cols = keyed_matrix(ax)
        cols = {c: v for c, v in cols.items() if len(v) >= 0.6 * len(pids)}
        if len(cols) < 3:
            continue
        use = [p for p in pids if all(p in v for v in cols.values())]
        if len(use) < 30:
            # fall back to pairwise-complete with mean imputation
            use = pids
        M = {c: [v.get(p, mean(v.values())) for p in use] for c, v in cols.items()}
        k = len(M)
        var = lambda xs: sum((x - mean(xs)) ** 2 for x in xs) / (len(xs) - 1)
        tot = [sum(M[c][j] for c in M) for j in range(len(use))]
        iv = sum(var(M[c]) for c in M)
        tv = var(tot)
        alpha = k / (k - 1) * (1 - iv / tv) if tv > 0 else None
        rel[ax] = {"items": k, "alpha": round(alpha, 3) if alpha is not None else None}
        for c in M:
            if var(M[c]) < 0.01:
                flat_items.append((ax, c))
                continue
            rest = [tot[j] - M[c][j] for j in range(len(use))]
            r_ = corr(M[c], rest)
            if r_ is not None and r_ < 0.1:
                bad_items.append((ax, c, round(r_, 3)))
    res["reliability"] = rel
    res["low_item_rest"] = sorted(bad_items, key=lambda t: t[2])
    res["flat_items"] = flat_items

    # ---------- item spread: questions everyone answered the same way ----------
    same_answer = []
    for i, it in ITEMS.items():
        if it["format"] == "exceptions":
            continue
        codes = [VIS[p][i]["c"] for p in pids if i in VIS[p] and VIS[p][i].get("c") is not None]
        if len(codes) > 50:
            top = Counter(codes).most_common(1)[0][1] / len(codes)
            if top >= 0.85:
                same_answer.append((i, round(top, 2)))
    res["near_unanimous_items"] = sorted(same_answer, key=lambda t: -t[1])

    # ---------- party gap per item: which questions split D and R most ----------
    gaps = []
    for i, it in ITEMS.items():
        if it["format"] == "exceptions" or it.get("issue_map_only"):
            continue
        K = len(it["options"])
        d = [2 * VIS[r["id"]][i]["c"] / (K - 1) - 1 for r in R if r["party"] == "D" and i in VIS[r["id"]] and VIS[r["id"]][i].get("c") is not None]
        rr = [2 * VIS[r["id"]][i]["c"] / (K - 1) - 1 for r in R if r["party"] == "R" and i in VIS[r["id"]] and VIS[r["id"]][i].get("c") is not None]
        if len(d) > 20 and len(rr) > 20:
            gaps.append((i, round(abs(mean(d) - mean(rr)), 3)))
    gaps.sort(key=lambda t: -t[1])
    res["top_partisan_items"] = gaps[:15]
    res["least_partisan_items"] = gaps[-15:]

    # ---------- axis correlations and dimensionality ----------
    axes_ok = [ax for ax in AXES if sum(ok(SC[p], ax) for p in pids) >= 0.9 * len(pids)]
    vec = {ax: [SC[p][ax]["v"] if ok(SC[p], ax) else 0 for p in pids] for ax in axes_ok}
    cm = {a: {b: corr(vec[a], vec[b]) for b in axes_ok} for a in axes_ok}
    res["corr_with_G"] = {ax: round(cm[ax]["G"], 3) for ax in axes_ok if ax != "G"}
    pairs = [(a, b, round(cm[a][b], 3)) for i, a in enumerate(axes_ok) for b in axes_ok[i + 1:] if a != "G" and b != "G"]
    res["most_correlated_pairs"] = sorted(pairs, key=lambda t: -abs(t[2]))[:12]
    # eigenvalues of the axis correlation matrix (power iteration with deflation)
    names = [a for a in axes_ok if a != "G"]
    C = [[cm[a][b] for b in names] for a in names]
    eig = []
    Mx = [row[:] for row in C]
    for _ in range(5):
        v = [1.0] * len(names)
        for _ in range(500):
            w_ = [sum(Mx[i][j] * v[j] for j in range(len(v))) for i in range(len(v))]
            nrm = math.sqrt(sum(x * x for x in w_)) or 1
            v = [x / nrm for x in w_]
        lam = sum(v[i] * sum(Mx[i][j] * v[j] for j in range(len(v))) for i in range(len(v)))
        eig.append(lam)
        Mx = [[Mx[i][j] - lam * v[i] * v[j] for j in range(len(v))] for i in range(len(v))]
    res["eigen_share"] = [round(e / len(names), 3) for e in eig]

    # ---------- spread: are politicians using the scale? ----------
    spread = {}
    for ax in AXES:
        vs = [SC[p][ax]["v"] for p in pids if ok(SC[p], ax)]
        if vs:
            spread[ax] = {"min": round(min(vs), 2), "max": round(max(vs), 2), "sd": round(math.sqrt(sum((x - mean(vs)) ** 2 for x in vs) / len(vs)), 3)}
    res["spread"] = spread

    # ---------- calibration: hand-placed profiles vs the politicians who belong to them ----------
    calib = {}
    fam = {"maga": ["trump", "vance", "stefanik", "noem", "hsanders", "hegseth", "lake", "tuberville", "gaetz", "mtg"],
           "dem_mainstream": ["biden", "harris", "schumer", "pelosi", "jeffries", "klobuchar", "whitmer", "walz", "kaine", "ossoff"],
           "dem_progressive": ["aoc", "omar", "tlaib", "pressley", "jayapal", "crockett", "warren"],
           "freedom_caucus": ["jordan", "roy", "donalds", "boebert", "mlee", "cruz"],
           "libertarian": ["gjohnson", "amash", "chase_oliver", "rpaul", "massie"],
           "gop_establishment": ["romney", "mccain", "jeb", "ryan", "haley", "mcconnell"],
           "blue_dog": ["manchin", "golden", "cuellar", "mgp", "gottheimer", "tester"]}
    for prof, members in fam.items():
        p = next(x for x in PROFILES if x["id"] == prof)
        diffs = {}
        for ax, v in p["pos"].items():
            vs = [SC[m][ax]["v"] for m in members if ok(SC[m], ax)]
            if vs:
                diffs[ax] = round(mean(vs) - v, 2)
        big = {ax: d for ax, d in diffs.items() if abs(d) >= 0.35}
        calib[prof] = {"mean_abs_gap": round(mean(abs(d) for d in diffs.values()), 3), "big_gaps": big}
    res["profile_calibration"] = calib

    # ---------- missing axes ----------
    res["axes_missing"] = {ax: sum(not ok(SC[p], ax) for p in pids) for ax in AXES if sum(not ok(SC[p], ax) for p in pids)}

    (OUT / "summary.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    return res, rows


if __name__ == "__main__":
    res, rows = main()
    p = lambda *a: print(*a)
    p(f"{res['n']} politicians, {res['topics']} topics")
    p("party AUC on G:", res["party_auc"], res["party_G"])
    p("overlap:", res["party_overlap"])
    p(f"orderings: {res['order_hits']}/{res['order_total']}", res["order_misses"])
    p(f"signatures: {res['sig_hits']}/{res['sig_total']} (non-G {res['sig_hits_nonG']}/{res['sig_total_nonG']}), unscored {res['sig_unscored']}")
    p("by axis:", res["sig_by_axis"])
    p("misses:"); [p("  ", m) for m in res["sig_misses"]]
    p(f"expected match top1 {res['match_top1']} top3 {res['match_top3']} top5 {res['match_top5']} of {res['n']}")
    p("miss top5:"); [p("  ", m) for m in res["match_miss5"]]
    p("president self rank:", res["president_self_rank"], "same/cross side:", res["top_match_same_side"], res["top_match_cross_side"])
    p("archetypes:", json.dumps(res["archetypes_by_group"]))
    p("consistency:", json.dumps(res["consistency_by_group"]))
    p("reliability:", json.dumps(res["reliability"]))
    p("low item-rest:", res["low_item_rest"][:40])
    p("flat items:", len(res["flat_items"]))
    p("near-unanimous:", res["near_unanimous_items"][:30])
    p("corr with G:", res["corr_with_G"])
    p("most correlated:", res["most_correlated_pairs"])
    p("eigen share:", res["eigen_share"])
    p("spread:", res["spread"])
    p("calibration:", json.dumps(res["profile_calibration"], indent=0))
    p("missing axes:", res["axes_missing"])
