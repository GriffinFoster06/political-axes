"""Step 3: dimensionality of ANES 2024 attitude items (141 items).

Same method as step 1 on GSS: weighted pairwise polychoric correlations,
parallel analysis, minres EFA with oblimin rotation for k = 1..16.
Raw ANES data stays local (data/raw/anes, git-ignored); only aggregate
outputs are written to reports/anes/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anes_items import build, crosswalk  # noqa: E402
from efa import efa  # noqa: E402
from polychoric import nearest_pd, polychoric_matrix  # noqa: E402
from prep import ROOT  # noqa: E402

OUT = ROOT / "reports" / "anes"
OUT.mkdir(parents=True, exist_ok=True)
RAW = ROOT / "data" / "raw" / "anes" / "anes_timeseries_2024_csv_20260519.csv"


def load():
    raw = pd.read_csv(RAW, low_memory=False)
    return build(raw)


def main(kmax=16):
    X, ncats, w, out = load()
    cw = crosswalk().set_index("item_id")
    cw.reset_index().to_csv(ROOT / "items" / "anes_crosswalk.csv", index=False)
    p = OUT / "polychoric.csv"
    if p.exists():
        R = pd.read_csv(p, index_col=0)
        N = pd.read_csv(OUT / "polychoric_n.csv", index_col=0)
    else:
        Rm, Nm = polychoric_matrix(X.to_numpy(), w, [ncats[c] for c in X.columns])
        R = pd.DataFrame(Rm, index=X.columns, columns=X.columns)
        N = pd.DataFrame(Nm, index=X.columns, columns=X.columns)
        R.round(5).to_csv(p)
        N.to_csv(OUT / "polychoric_n.csv")
    items = list(R.columns)
    while R.loc[items, items].isna().to_numpy().any():
        items.remove(R.loc[items, items].isna().sum().idxmax())
    print("excluded from EFA:", [c for c in R.columns if c not in items])
    Rc = nearest_pd(R.loc[items, items].to_numpy())
    n_eff = int(np.median(N.loc[items, items].to_numpy()[np.triu_indices(len(items), 1)]))
    rng = np.random.default_rng(1)
    obs = np.sort(np.linalg.eigvalsh(Rc))[::-1]
    sims = np.array([np.sort(np.linalg.eigvalsh(np.corrcoef(rng.standard_normal((n_eff, len(items))),
                                                            rowvar=False)))[::-1] for _ in range(50)])
    pa = pd.DataFrame({"observed": obs, "random_95": np.percentile(sims, 95, axis=0)},
                      index=np.arange(1, len(obs) + 1))
    pa.to_csv(OUT / "parallel_analysis.csv")
    print("items", len(items), "median pairwise n", n_eff,
          "| parallel analysis retains", int((pa.observed > pa.random_95).cumprod().sum()))
    print("first eigenvalues:", obs[:16].round(2))
    rows = []
    for k in range(1, kmax + 1):
        L, Phi, rmsr = efa(Rc, k, items)
        L["hyp"] = cw.loc[items, "hyp_dimension"].values
        L.round(3).to_csv(OUT / f"efa_loadings_k{k}.csv")
        if k > 1:
            Phi.round(3).to_csv(OUT / f"efa_phi_k{k}.csv")
        rows.append({"k": k, "rmsr": rmsr, "weak_items": int((L.max_abs < .30).sum()),
                     "smallest_factor_items": int(L.primary.value_counts().min()),
                     "max_factor_corr": float(np.abs(Phi.to_numpy() - np.eye(k)).max())})
    s = pd.DataFrame(rows)
    s.to_csv(OUT / "efa_summary.csv", index=False)
    print(s.to_string(index=False))


if __name__ == "__main__":
    main()
