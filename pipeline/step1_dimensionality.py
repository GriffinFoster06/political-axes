"""Step 1: how many dimensions does the GSS item pool support?

Outputs (in reports/):
- polychoric.csv, polychoric_n.csv: weighted pairwise polychoric matrix and pair counts
- parallel_analysis.csv: observed vs random eigenvalues
- efa_loadings_k{k}.csv for k = 1..7 (oblimin), efa_summary.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from polychoric import nearest_pd, polychoric_matrix  # noqa: E402
from prep import ROOT, load_gss  # noqa: E402

OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)


def main():
    X, w, cw, outcomes, dropped = load_gss()
    print("items kept:", X.shape[1], "dropped (<500 obs):", dropped)
    poly_path = OUT / "polychoric.csv"
    if poly_path.exists():
        R = pd.read_csv(poly_path, index_col=0)
        N = pd.read_csv(OUT / "polychoric_n.csv", index_col=0)
    else:
        Rm, Nm = polychoric_matrix(X.to_numpy(), w, cw["ncat"].tolist())
        R = pd.DataFrame(Rm, index=X.columns, columns=X.columns)
        N = pd.DataFrame(Nm, index=X.columns, columns=X.columns)
        R.to_csv(poly_path)
        N.to_csv(OUT / "polychoric_n.csv")

    # EFA needs every pair observed; drop split-ballot alternates / single-year items
    # greedily until the matrix is complete.
    items = list(R.columns)
    while R.loc[items, items].isna().to_numpy().any():
        miss = R.loc[items, items].isna().sum()
        items.remove(miss.idxmax())
    excluded = [c for c in R.columns if c not in items]
    print("excluded from EFA (never co-observed with others):", excluded)
    Rc = nearest_pd(R.loc[items, items].to_numpy())
    n_eff = int(np.median(N.loc[items, items].to_numpy()[np.triu_indices(len(items), 1)]))
    print("EFA items:", len(items), "median pairwise n:", n_eff)

    # Parallel analysis (Horn): eigenvalues of random normal data, same n and p
    rng = np.random.default_rng(1)
    obs_eig = np.sort(np.linalg.eigvalsh(Rc))[::-1]
    sims = []
    for _ in range(100):
        Z = rng.standard_normal((n_eff, len(items)))
        sims.append(np.sort(np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False)))[::-1])
    sims = np.array(sims)
    pa = pd.DataFrame({"observed": obs_eig, "random_mean": sims.mean(0),
                       "random_95": np.percentile(sims, 95, axis=0)})
    pa.index = np.arange(1, len(pa) + 1)
    pa.to_csv(OUT / "parallel_analysis.csv")
    n_pa = int((pa["observed"] > pa["random_95"]).cumprod().sum())
    print("parallel analysis retains:", n_pa)
    print(pa.head(12).round(3).to_string())

    rows = []
    for k in range(1, 9):
        fa = FactorAnalyzer(n_factors=k, rotation="oblimin" if k > 1 else None,
                            method="minres", is_corr_matrix=True)
        fa.fit(Rc)
        L = pd.DataFrame(fa.loadings_, index=items, columns=[f"F{i+1}" for i in range(k)])
        resid = Rc - L.to_numpy() @ (fa.phi_ if k > 1 and fa.phi_ is not None else np.eye(k)) @ L.to_numpy().T
        off = resid[np.triu_indices(len(items), 1)]
        rmsr = float(np.sqrt(np.mean(off ** 2)))
        L["primary"] = L.abs().idxmax(axis=1)
        L["max_abs"] = L[[f"F{i+1}" for i in range(k)]].abs().max(axis=1)
        L["hyp_dim"] = cw.set_index("item_id").loc[items, "hyp_dimension"].values
        L.round(3).to_csv(OUT / f"efa_loadings_k{k}.csv")
        if k > 1 and fa.phi_ is not None:
            pd.DataFrame(fa.phi_, index=L.columns[:k], columns=L.columns[:k]).round(3) \
                .to_csv(OUT / f"efa_phi_k{k}.csv")
        weak = int((L["max_abs"] < 0.30).sum())
        rows.append({"k": k, "rmsr": rmsr, "items_max_loading_lt_.30": weak,
                     "var_explained": float(fa.get_factor_variance()[2][-1])})
    summ = pd.DataFrame(rows)
    summ.to_csv(OUT / "efa_summary.csv", index=False)
    print(summ.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
