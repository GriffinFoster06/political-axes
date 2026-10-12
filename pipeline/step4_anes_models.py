"""Step 4: which structure predicts Americans' answers best? (ANES 2024)

Competitors, all judged on the same hidden answers (15% of each person's
answers, for 1,500 random respondents):
  baselines: average American; liberal-conservative self-label; party ID;
             self-label x party ID
  1 dimension (single left-right)
  2 dimensions, compass-style (economic/role-of-government vs everything else)
  9 correlated dimensions (between-item, from the 9-factor EFA)
  bifactor: one general left-right factor + 9 specific factors

Then fits the winner on everyone, reports reliability, known groups and 2024
vote prediction, and writes model/params_anes.json. ANES microdata stays
local; only aggregate results are written.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anes_items import build, crosswalk  # noqa: E402
from bifactor import fit_bifactor  # noqa: E402
from general_factor import schmid_leiman  # noqa: E402
from grm import score_eap  # noqa: E402
from prep import ROOT  # noqa: E402
from step2_fit_and_validate import (conditional_baseline, fit_model,  # noqa: E402
                                    predictive_logloss)

REP = ROOT / "reports" / "anes"
RAW = ROOT / "data" / "raw" / "anes" / "anes_timeseries_2024_csv_20260519.csv"
K_EFA = 9
EFA_TO_DIM = {"F1": "GOV", "F2": "EQUITY", "F3": "CULT", "F4": "NORMS", "F5": "GENDER",
              "F6": "ESTAB", "F7": "TRUST", "F8": "THREAT", "F9": "FOREIGN"}
DIM_LABELS = {
    "G": "General left-right",
    "GOV": "Role of government (economy, environment, guns)",
    "EQUITY": "Perceived discrimination & group equity",
    "CULT": "Moral traditionalism & authority in child-rearing",
    "NORMS": "Indifference to democratic checks & a free press",
    "GENDER": "Resentment of women's equality claims",
    "ESTAB": "Distrust of mainstream media, elections & experts",
    "TRUST": "Distrust of government institutions (Congress, courts, parties)",
    "THREAT": "Foreign threat perception",
    "FOREIGN": "Support for Israel & foreign engagement",
}
# Content overrides: keep balanced (pro/con keyed) batteries on one dimension
# instead of letting agreement bias split them.
OVERRIDES = {
    "rr_try_harder": "EQUITY", "rr_no_favors": "EQUITY",
    "egal_worry_less": "GOV", "egal_not_big_problem": "GOV",
}
SPEC_MIN = 0.20     # below this specific loading, the item measures only G
DROP_MAX = 0.25     # items below this on both G and specific are dropped
N_EVAL = 1500
MASK = 0.15
DRAWS_EVAL = 800


def structure(items):
    L = pd.read_csv(REP / f"efa_loadings_k{K_EFA}.csv", index_col=0)
    Phi = pd.read_csv(REP / f"efa_phi_k{K_EFA}.csv", index_col=0).to_numpy()
    cols = [c for c in L.columns if c.startswith("F") and c[1:].isdigit()]
    Lm = L[cols].to_numpy()
    g, spec, _ = schmid_leiman(Lm, Phi)
    prim = L["primary"].map(EFA_TO_DIM)
    for k, v in OVERRIDES.items():
        prim[k] = v
    dim_to_col = {v: int(k[1:]) - 1 for k, v in EFA_TO_DIM.items()}
    rows = []
    for i, it in enumerate(L.index):
        d = prim[it]
        s_load = spec[i, dim_to_col[d]]
        sign = np.sign(Lm[i, dim_to_col[d]]) or 1.0
        rows.append({"item": it, "primary": d, "g_loading": g[i] * sign,
                     "spec_loading": s_load * sign})
    S = pd.DataFrame(rows).set_index("item")
    S["group"] = np.where(S.spec_loading.abs() >= SPEC_MIN, S.primary, None)
    S["drop"] = (S.g_loading.abs() < DROP_MAX) & (S.spec_loading.abs() < DROP_MAX)
    return S.loc[[c for c in items if c in S.index]]


def start_slopes(S):
    h2 = np.clip(S.g_loading ** 2 + S.spec_loading ** 2, 0, 0.9)
    k = 1.702 / np.sqrt(1 - h2)
    return np.column_stack([S.g_loading * k, S.spec_loading * k])


def score(Xdf, items, dims, Sigma, rows, draws=DRAWS_EVAL, keep=True):
    cols = [it.item_id for it in items]
    Xv = Xdf[cols].to_numpy()
    out = []
    for i in rows:
        resp = {cols[j]: int(Xv[i, j]) for j in range(len(cols)) if not np.isnan(Xv[i, j])}
        out.append(score_eap(resp, items, dims, Sigma, n_draws=draws, return_draws=keep))
    return out


def fit_bif(Xdf, w, ncats, S):
    cols = list(S.index)
    groups = [g if isinstance(g, str) else None for g in S.group]
    items, specs, ll, iters, conv = fit_bifactor(
        Xdf[cols].to_numpy(), w, [ncats[c] for c in cols], cols, groups,
        start_a=start_slopes(S), verbose=False)
    print(f"  bifactor: {iters} EM iterations, converged {conv}")
    dims = ["G"] + specs
    return items, dims, np.eye(len(dims))


def main():
    t0 = time.time()
    raw = pd.read_csv(RAW, low_memory=False)
    X, ncats, w, out = build(raw)
    S = structure(list(X.columns))
    dropped = list(S.index[S["drop"]])
    S = S[~S["drop"]]
    X = X[list(S.index)]
    print("items:", X.shape[1], "dropped:", dropped)
    print("general-only items:", list(S.index[S.group.isna()]))
    S.round(3).to_csv(REP / "item_structure.csv")

    rng = np.random.default_rng(2024)
    nobs = X.notna().sum(axis=1).to_numpy()
    rows = rng.choice(np.where(nobs >= 40)[0], size=N_EVAL, replace=False)
    Xtr = X.copy()
    masked = []
    for pos, i in enumerate(rows):
        obs_items = X.columns[X.iloc[i].notna()].tolist()
        for iid in rng.choice(obs_items, size=max(1, round(MASK * len(obs_items))), replace=False):
            masked.append((pos, iid, int(X.iloc[i][iid])))
            Xtr.iat[i, Xtr.columns.get_loc(iid)] = np.nan
    print("hidden answers:", len(masked))

    res = {}
    res["Average American (marginal)"] = conditional_baseline(Xtr, w, np.zeros(len(X)), masked, rows, ncats)
    pv, pid = out.polviews.to_numpy(), out.pid7.to_numpy()
    res["Liberal-conservative self-label"] = conditional_baseline(Xtr, w, pv, masked, rows, ncats)
    res["Party ID (7-point)"] = conditional_baseline(Xtr, w, pid, masked, rows, ncats)
    combo = np.where(np.isnan(pv) | np.isnan(pid), np.nan, pv * 10 + pid)
    res["Self-label x party ID"] = conditional_baseline(Xtr, w, combo, masked, rows, ncats)

    prim = S.primary.to_dict()
    structs = {
        "1 dimension (single left-right)": {c: "LR" for c in X.columns},
        "2 dimensions (compass-style)": {c: ("ECO" if prim[c] == "GOV" else "SOC") for c in X.columns},
        "9 correlated dimensions": prim,
    }
    for name, st in structs.items():
        dims = list(dict.fromkeys(st[c] for c in X.columns))
        print("fitting", name)
        items, Sig, _ = fit_model(Xtr, w, ncats, st, dims)
        res[name] = predictive_logloss(items, dims, score(Xtr, items, dims, Sig, rows), masked)
        print(f"  done {time.time() - t0:.0f}s")
    print("fitting bifactor (general + 9 specific)")
    items, dims, Sig = fit_bif(Xtr, w, ncats, S)
    res["Bifactor: general + 9 specific"] = predictive_logloss(items, dims, score(Xtr, items, dims, Sig, rows), masked)
    print(f"  done {time.time() - t0:.0f}s")

    base = res["Average American (marginal)"][0].mean()
    tab = pd.DataFrame([{"model": k, "log_loss": v[0].mean(), "accuracy": np.nanmean(v[1]),
                         "improvement_vs_marginal_%": 100 * (1 - v[0].mean() / base)}
                        for k, v in res.items()])
    tab.to_csv(REP / "holdout_prediction.csv", index=False)
    print(tab.round(4).to_string(index=False))
    # paired bootstrap: bifactor vs 9 correlated
    a = res["Bifactor: general + 9 specific"][0]
    b = res["9 correlated dimensions"][0]
    c2 = res["2 dimensions (compass-style)"][0]
    by_person = pd.DataFrame({"p": [m[0] for m in masked], "bif": a, "cor": b, "two": c2}).groupby("p").sum()
    bs = []
    for _ in range(2000):
        s = by_person.sample(len(by_person), replace=True, random_state=rng.integers(1e9))
        bs.append(((s.cor - s.bif).sum() / len(masked), (s.two - s.bif).sum() / len(masked)))
    bs = np.array(bs)
    ci = {"bifactor_minus_9corr_logloss_95ci": np.percentile(-bs[:, 0], [2.5, 97.5]).round(4).tolist(),
          "bifactor_minus_2axis_logloss_95ci": np.percentile(-bs[:, 1], [2.5, 97.5]).round(4).tolist()}
    print(ci)
    (REP / "holdout_bootstrap.json").write_text(json.dumps(ci, indent=1))

    # ------------- final bifactor model on everyone
    print("final bifactor fit on all respondents")
    items, dims, Sig = fit_bif(X, w, ncats, S)
    allrows = np.arange(len(X))
    sc = score(X, items, dims, Sig, allrows, draws=1000, keep=False)
    M = np.array([s["mean"] for s in sc])
    SD = np.array([s["sd"] for s in sc])
    scores = pd.DataFrame(M, columns=dims)
    for j, d in enumerate(dims):
        scores[d + "_sd"] = SD[:, j]
    scores = pd.concat([scores, out.reset_index(drop=True)], axis=1)
    scores["weight"] = w
    scores.to_parquet(ROOT / "data" / "derived_anes_scores.parquet")   # git-ignored

    rel = []
    for j, d in enumerate(dims):
        v = np.cov(M[:, j], aweights=w)
        e = np.average(SD[:, j] ** 2, weights=w)
        n_it = sum(1 for it in items if d in (it.slopes or {}))
        rel.append({"dimension": d, "label": DIM_LABELS[d], "items": n_it,
                    "empirical_reliability": v / (v + e),
                    "corr_with_self_label": scores[[d, "polviews"]].dropna().corr().iloc[0, 1]})
    rel = pd.DataFrame(rel)
    rel.to_csv(REP / "reliability.csv", index=False)
    print(rel.round(3).to_string(index=False))

    kg = scores.dropna(subset=["polviews"]).groupby("polviews").apply(
        lambda g: pd.Series({d: np.average(g[d], weights=g["weight"]) for d in dims}))
    kg.round(3).to_csv(REP / "known_groups_polviews.csv")
    print(kg.round(2))

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    v = scores[scores.vote2024.isin([1, 2])].copy()
    v["trump"] = (v.vote2024 == 2).astype(int)
    feats = {"Self-label only": ["polviews"], "General factor only": ["G"],
             "General + 9 specific": dims, "General + 9 specific + self-label": dims + ["polviews"],
             "Party ID only (reference; never an input)": ["pid7"]}
    auc = []
    for name, f in feats.items():
        vv = v.dropna(subset=f)
        s = cross_val_score(LogisticRegression(max_iter=3000), vv[f], vv.trump, cv=5, scoring="roc_auc")
        auc.append({"predictors": name, "n": len(vv), "cv_auc": s.mean()})
    auc = pd.DataFrame(auc)
    auc.to_csv(REP / "vote2024_auc.csv", index=False)
    print(auc.round(3).to_string(index=False))

    norms = {}
    for j, d in enumerate(dims):
        o = np.argsort(M[:, j])
        cw_ = np.cumsum(w[o]) / w.sum()
        norms[d] = [float(np.interp(q, cw_, M[o, j])) for q in np.linspace(0.01, 0.99, 99)]
    cwk = crosswalk().set_index("item_id")
    params = {
        "version": "0.2.0-anes-bifactor",
        "source": "ANES 2024 Time Series (release 2026-05-19), weight V240107a",
        "model": "bifactor graded response model: general factor G + specific factors, all independent N(0,1)",
        "dimensions": [{"id": d, "label": DIM_LABELS[d]} for d in dims],
        "sigma": np.eye(len(dims)).tolist(),
        "scoring": {"method": "EAP, Laplace-centered importance sampling, antithetic draws",
                    "prng": "mulberry32", "seed": 20261012, "draws": 2000, "inflate": 1.3},
        "items": [{"id": it.item_id, "dim": it.dim, "a": round(it.a, 6),
                   "slopes": {k: round(v, 6) for k, v in it.slopes.items()},
                   "d": [round(x, 6) for x in it.d], "ncat": it.ncat,
                   "source_var": cwk.loc[it.item_id, "anes_vars"],
                   "source_label": cwk.loc[it.item_id, "question_summary"],
                   "high_pole": cwk.loc[it.item_id, "high_pole"]} for it in items],
        "norms_percentiles_1_to_99": norms,
        "dropped_items": dropped,
        "overrides": OVERRIDES,
    }
    (ROOT / "model" / "params_anes.json").write_text(json.dumps(params, indent=1))
    print(f"wrote model/params_anes.json ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
