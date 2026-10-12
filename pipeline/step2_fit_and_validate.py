"""Step 2: fit the multidimensional GRM on GSS 2016-2024 and validate it.

1. Assign items to dimensions (primary loading in the 7-factor EFA, plus
   documented overrides), fit a between-item multidimensional GRM.
2. Out-of-sample test: hide 15% of answers for 4,000 random respondents,
   refit, and predict the hidden answers. Compared against:
   - marginal (everyone answers like the average American)
   - liberal-conservative self-label (polviews)
   - party ID
   - self-label x party ID combined
   - 1 dimension (single left-right)
   - 2 dimensions, compass-style (economic vs everything else)
   - the 7-dimension model
3. Reliability, latent correlations, known-groups, 2020 vote prediction.
4. Writes model/params.json (the scorer's input) and reports/step2_*.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grm import (cat_probs, estimate_corr, fit_unidim, loglik_grid,  # noqa: E402
                 score_eap)
from polychoric import nearest_pd  # noqa: E402
from prep import ROOT, load_gss  # noqa: E402

REPORTS = ROOT / "reports"
MODEL = ROOT / "model"
MODEL.mkdir(exist_ok=True)

DIM_LABELS = {
    "ECON": "Redistribution & role of government",
    "SPEND": "Domestic spending priorities",
    "CULT": "Moral traditionalism (abortion, sexuality, end of life)",
    "GENDER": "Traditional gender roles",
    "GROUP": "Race, immigration & law-and-order",
    "TOLER": "Civil-liberties tolerance (reversed: high = less tolerant)",
    "TRUST": "Institutional confidence (reversed: high = less confident)",
}
EFA_TO_DIM = {"F1": "CULT", "F2": "TOLER", "F3": "TRUST", "F4": "GROUP",
              "F5": "SPEND", "F6": "GENDER", "F7": "ECON"}
# Documented hand overrides of the primary-loading rule (k = 7 EFA):
OVERRIDES = {
    "divorce_law": "CULT",        # loaded .33 on ECON factor; conceptually moral traditionalism
    "affirm_action": "GROUP",     # .36 on ECON; it is a race-policy item
    "women_pref_hiring": "GENDER",  # .45 on ECON; gender-policy item
    "sex_ed": "CULT",             # .34 on GENDER; moral-traditionalism item
    "spend_poor": "SPEND",        # split-ballot twin of spend_welfare (not in EFA)
    "spend_race_b": "SPEND",      # split-ballot twin of spend_race
    "immig_level_b": "GROUP",     # 2024 twin of immig_level
}
DROP = {
    "spend_space": "max loading < .30",
    "spend_roads": "loads negatively on economic factor; not ideological",
    "spend_foreignaid": "max loading < .30",
    "spend_othercountries": "twin of a dropped item",
    "gun_permit": "max loading < .30 (only .24, on institutional confidence)",
    "getahead_luck": "max loading < .30",
    "race_inborn": "very low endorsement; loads with gender items, ambiguous meaning",
}
EVAL_PERSONS = 4000
MASK_FRAC = 0.15
N_DRAWS_EVAL = 1000


def assign_dims(items):
    L = pd.read_csv(REPORTS / "efa_loadings_k7.csv", index_col=0)
    dims = {}
    for it in items:
        if it in DROP:
            continue
        if it in OVERRIDES:
            dims[it] = OVERRIDES[it]
        elif it in L.index:
            dims[it] = EFA_TO_DIM[L.loc[it, "primary"]]
    return dims


def fit_model(X, w, ncats, item_dims, dims):
    """Fit per-dimension GRMs and the latent correlation matrix."""
    items_by_dim, fitted = {}, {}
    for d in dims:
        cols = [c for c in X.columns if item_dims.get(c) == d]
        fit = fit_unidim(X[cols].to_numpy(), w, [ncats[c] for c in cols], cols, d)
        for it in fit.items:
            fitted[it.item_id] = it
        items_by_dim[d] = cols
        print(f"  {d}: {len(cols)} items, EM iters {fit.iters}, converged {fit.converged}")
    L = {d: loglik_grid(X[items_by_dim[d]].to_numpy(), [fitted[c] for c in items_by_dim[d]])
         for d in dims}
    S = np.eye(len(dims))
    for i in range(len(dims)):
        for k in range(i + 1, len(dims)):
            S[i, k] = S[k, i] = estimate_corr(L[dims[i]], L[dims[k]], w)
    S = nearest_pd(S, 1e-3)
    order = [c for c in X.columns if c in item_dims]
    return [fitted[c] for c in order], S, L


def score_people(X, items, dims, S, rows, n_draws=N_DRAWS_EVAL, keep_draws=False):
    cols = [it.item_id for it in items]
    Xv = X[cols].to_numpy()
    out = []
    for i in rows:
        resp = {cols[j]: int(Xv[i, j]) for j in range(len(cols)) if not np.isnan(Xv[i, j])}
        out.append(score_eap(resp, items, dims, S, n_draws=n_draws, return_draws=keep_draws))
    return out


def predictive_logloss(items, dims, scores, masked):
    """masked: list of (row_position, item_id, true_code)."""
    by_id = {it.item_id: it for it in items}
    dim_idx = {d: i for i, d in enumerate(dims)}
    ll, hit = [], []
    for pos, item_id, y in masked:
        it = by_id.get(item_id)
        if it is None:
            ll.append(np.nan); hit.append(np.nan)
            continue
        s = scores[pos]
        av = it.avec(dim_idx, len(dims))
        P = cat_probs(1.0, it.d, s["draws"] @ av)                     # (draws, K)
        p = s["weights"] @ P
        ll.append(-np.log(max(p[y], 1e-12)))
        hit.append(float(np.argmax(p) == y))
    return np.array(ll), np.array(hit)


def conditional_baseline(Xtrain, w, group, masked, rows, ncats, alpha=1.0):
    """Predict each hidden answer from the answer distribution of people in the same group."""
    ll, hit = [], []
    cache = {}
    for pos, item_id, y in masked:
        g = group[rows[pos]]
        key = (item_id, g)
        if key not in cache:
            x = Xtrain[item_id].to_numpy()
            K = ncats[item_id]
            sel = ~np.isnan(x) & ((group == g) if not pd.isna(g) else np.ones(len(x), bool))
            cnt = np.bincount(x[sel].astype(int), weights=w[sel], minlength=K) + alpha
            cache[key] = cnt / cnt.sum()
        p = cache[key]
        ll.append(-np.log(p[y]))
        hit.append(float(np.argmax(p) == y))
    return np.array(ll), np.array(hit)


def main():
    t0 = time.time()
    X, w, cw, outcomes, _ = load_gss()
    ncats = dict(zip(cw.item_id, cw.ncat))
    item_dims = assign_dims(list(X.columns))
    dims7 = list(DIM_LABELS)
    X = X[[c for c in X.columns if c in item_dims]]
    print("model items:", X.shape[1], {d: sum(v == d for v in item_dims.values()) for d in dims7})

    # ---------------- out-of-sample evaluation
    rng = np.random.default_rng(2026)
    nobs = X.notna().sum(axis=1).to_numpy()
    eligible = np.where(nobs >= 10)[0]
    rows = rng.choice(eligible, size=min(EVAL_PERSONS, len(eligible)), replace=False)
    Xtrain = X.copy()
    masked = []
    for pos, i in enumerate(rows):
        obs_items = X.columns[X.iloc[i].notna()].tolist()
        m = max(1, int(round(MASK_FRAC * len(obs_items))))
        for item_id in rng.choice(obs_items, size=m, replace=False):
            masked.append((pos, item_id, int(X.iloc[i][item_id])))
            Xtrain.iat[i, Xtrain.columns.get_loc(item_id)] = np.nan
    print("hidden answers:", len(masked), "from", len(rows), "people")

    results = {}
    results["Marginal (average American)"] = conditional_baseline(
        Xtrain, w, np.zeros(len(X)), masked, rows, ncats)
    pv = outcomes["polviews"].to_numpy()
    pid = outcomes["partyid"].to_numpy()
    results["Liberal-conservative self-label"] = conditional_baseline(Xtrain, w, pv, masked, rows, ncats)
    results["Party ID"] = conditional_baseline(Xtrain, w, pid, masked, rows, ncats)
    combo = np.where(np.isnan(pv) | np.isnan(pid), np.nan, pv * 10 + pid)
    results["Self-label x party ID"] = conditional_baseline(Xtrain, w, combo, masked, rows, ncats)

    structures = {
        "1 dimension (single left-right)": {c: "LR" for c in item_dims},
        "2 dimensions (compass-style econ vs social)":
            {c: ("ECO" if d in ("ECON", "SPEND") else "SOC") for c, d in item_dims.items()},
        "7 dimensions (data-driven)": item_dims,
    }
    for name, struct in structures.items():
        dims = list(dict.fromkeys(struct[c] for c in X.columns))
        print("fitting", name)
        items, S, _ = fit_model(Xtrain, w, ncats, struct, dims)
        scores = score_people(Xtrain, items, dims, S, rows, keep_draws=True)
        results[name] = predictive_logloss(items, dims, scores, masked)
        print(f"  done ({time.time() - t0:.0f}s)")

    base = results["Marginal (average American)"][0].mean()
    tab = pd.DataFrame([{"model": k, "log_loss": v[0].mean(), "accuracy": np.nanmean(v[1]),
                         "improvement_vs_marginal_%": 100 * (1 - v[0].mean() / base)}
                        for k, v in results.items()])
    tab.to_csv(REPORTS / "step2_holdout_prediction.csv", index=False)
    print(tab.round(4).to_string(index=False))
    # per-dimension breakdown for the main competitors
    item_dim_of = {iid: item_dims[iid] for _, iid, _ in masked}
    breakdown = []
    for k in ["Self-label x party ID", "2 dimensions (compass-style econ vs social)",
              "7 dimensions (data-driven)"]:
        ll = results[k][0]
        for d in dims7:
            sel = np.array([item_dim_of[iid] == d for _, iid, _ in masked])
            breakdown.append({"model": k, "dimension": d, "log_loss": ll[sel].mean(), "n": int(sel.sum())})
    pd.DataFrame(breakdown).pivot(index="dimension", columns="model", values="log_loss") \
        .to_csv(REPORTS / "step2_holdout_by_dimension.csv")

    # ---------------- final model on all data
    print("fitting final 7-dimension model on all data")
    items, S, L = fit_model(X, w, ncats, item_dims, dims7)
    allrows = np.arange(len(X))
    scores = score_people(X, items, dims7, S, allrows, n_draws=1000)
    M = np.array([s["mean"] for s in scores])
    SD = np.array([s["sd"] for s in scores])
    ESS = np.array([s["ess"] for s in scores])
    sc = pd.DataFrame(M, columns=dims7)
    for j, d in enumerate(dims7):
        sc[d + "_sd"] = SD[:, j]
    sc = pd.concat([sc, outcomes.reset_index(drop=True)], axis=1)
    sc["weight"] = w
    sc["n_items"] = [s["n_items"] for s in scores]
    sc["ess"] = ESS
    sc.to_parquet(ROOT / "data" / "derived_gss_scores.parquet")

    # reliability per dimension (people with >=3 items on that dimension)
    rel = []
    for j, d in enumerate(dims7):
        cols = [it.item_id for it in items if it.dim == d]
        n_d = X[cols].notna().sum(axis=1).to_numpy()
        sel = n_d >= 3
        v = np.cov(M[sel, j], aweights=w[sel])
        e = np.average(SD[sel, j] ** 2, weights=w[sel])
        rel.append({"dimension": d, "label": DIM_LABELS[d], "items": len(cols),
                    "respondents_with_3plus": int(sel.sum()),
                    "empirical_reliability": v / (v + e),
                    "median_items_answered": float(np.median(n_d[sel]))})
    rel = pd.DataFrame(rel)
    rel.to_csv(REPORTS / "step2_reliability.csv", index=False)
    print(rel.round(3).to_string(index=False))
    pd.DataFrame(S, index=dims7, columns=dims7).round(3).to_csv(REPORTS / "step2_latent_correlations.csv")
    print(pd.DataFrame(S, index=dims7, columns=dims7).round(2))

    # known groups: weighted mean score by self-label
    kg = sc.dropna(subset=["polviews"]).groupby("polviews").apply(
        lambda g: pd.Series({d: np.average(g[d], weights=g["weight"]) for d in dims7}))
    kg.round(3).to_csv(REPORTS / "step2_known_groups_polviews.csv")
    print(kg.round(2))

    # 2020 vote (asked in 2022 and 2024 surveys)
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    v = sc[sc["pres20"].isin([1, 2])].copy()
    v["trump"] = (v["pres20"] == 2).astype(int)
    v["econ_social_ECO"] = v[["ECON", "SPEND"]].mean(axis=1)
    v["econ_social_SOC"] = v[["CULT", "GENDER", "GROUP", "TOLER", "TRUST"]].mean(axis=1)
    feats = {
        "Self-label only": ["polviews"],
        "2 axes (avg of econ dims, avg of social dims)": ["econ_social_ECO", "econ_social_SOC"],
        "7 dimensions": dims7,
        "7 dimensions + self-label": dims7 + ["polviews"],
    }
    auc = []
    for name, f in feats.items():
        vv = v.dropna(subset=f)
        s = cross_val_score(LogisticRegression(max_iter=2000), vv[f], vv["trump"],
                            cv=5, scoring="roc_auc")
        auc.append({"predictors": name, "n": len(vv), "cv_auc": s.mean()})
    auc = pd.DataFrame(auc)
    auc.to_csv(REPORTS / "step2_vote2020_auc.csv", index=False)
    print(auc.round(3).to_string(index=False))

    # national norms (weighted percentiles of EAP scores)
    norms = {}
    for d in dims7:
        order = np.argsort(M[:, list(dims7).index(d)])
        vals = M[order, list(dims7).index(d)]
        cw_ = np.cumsum(w[order]) / w.sum()
        norms[d] = [float(np.interp(q, cw_, vals)) for q in np.linspace(0.01, 0.99, 99)]

    meta = cw.set_index("item_id")
    params = {
        "version": "0.1.0-gss",
        "source": "GSS 1972-2024 cumulative file (Release 3), years 2016-2024, weight wtssps",
        "dimensions": [{"id": d, "label": DIM_LABELS[d]} for d in dims7],
        "sigma": S.round(6).tolist(),
        "scoring": {"method": "EAP, Laplace-centered importance sampling",
                    "prng": "mulberry32", "seed": 20261012, "draws": 2000, "inflate": 1.3},
        "items": [{
            "id": it.item_id, "dim": it.dim, "a": round(it.a, 6),
            "d": [round(x, 6) for x in it.d], "ncat": it.ncat,
            "source_var": meta.loc[it.item_id, "gss_var"],
            "source_label": meta.loc[it.item_id, "gss_label"],
            "high_pole": meta.loc[it.item_id, "high_pole"],
        } for it in items],
        "norms_percentiles_1_to_99": norms,
        "dropped_items": DROP,
        "overrides": OVERRIDES,
    }
    (MODEL / "params.json").write_text(json.dumps(params, indent=1))
    print(f"wrote model/params.json; total {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
