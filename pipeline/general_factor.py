"""How much of the item pool is one general left-right factor?

Schmid-Leiman transformation of an oblique EFA solution: fit one
second-order factor to the factor correlation matrix, split every item's
loading into a general part and a factor-specific part, then compute
- omega total: reliable share of variance of the unit-weighted total score
- omega hierarchical: share due to the general factor alone
- ECV: explained common variance due to the general factor
- per factor: omega-hierarchical-subscale (variance unique to that factor)

Items are oriented so a high score is the named pole of each item, and items
whose primary loading is negative are reversed before summing.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer

ROOT = Path(__file__).resolve().parents[1]


def schmid_leiman(L: np.ndarray, Phi: np.ndarray):
    fa2 = FactorAnalyzer(n_factors=1, rotation=None, method="minres", is_corr_matrix=True)
    fa2.fit(Phi)
    gam = fa2.loadings_[:, 0]
    if gam.sum() < 0:
        gam = -gam
    g = L @ gam
    spec = L * np.sqrt(np.clip(1 - gam ** 2, 0, None))
    return g, spec, gam


def omegas(L: np.ndarray, Phi: np.ndarray, primary: np.ndarray):
    g, spec, gam = schmid_leiman(L, Phi)
    sign = np.sign(L[np.arange(len(L)), primary])
    g, spec = g * sign, spec * sign[:, None]
    uniq = 1 - (g ** 2 + (spec ** 2).sum(axis=1))
    tot = g.sum() ** 2 + sum(spec[:, j].sum() ** 2 for j in range(spec.shape[1])) + uniq.sum()
    omega_t = (tot - uniq.sum()) / tot
    omega_h = g.sum() ** 2 / tot
    ecv = (g ** 2).sum() / ((g ** 2).sum() + (spec ** 2).sum())
    sub = []
    for j in range(spec.shape[1]):
        m = primary == j
        gs, ss = g[m].sum(), spec[m, j].sum()
        other = sum(spec[m, k].sum() ** 2 for k in range(spec.shape[1]) if k != j)
        var = gs ** 2 + ss ** 2 + other + uniq[m].sum()
        sub.append({"factor": f"F{j+1}", "items": int(m.sum()), "second_order_loading": gam[j],
                    "omega_subscale": (gs ** 2 + ss ** 2) / var,
                    "omega_h_subscale": ss ** 2 / var,
                    "share_of_subscale_reliable_variance_that_is_general": gs ** 2 / (gs ** 2 + ss ** 2)})
    return {"omega_total": omega_t, "omega_h": omega_h, "ecv": ecv}, pd.DataFrame(sub), g


def run(report_dir: Path, k: int, label: str):
    L = pd.read_csv(report_dir / f"efa_loadings_k{k}.csv", index_col=0)
    Phi = pd.read_csv(report_dir / f"efa_phi_k{k}.csv", index_col=0).to_numpy()
    cols = [c for c in L.columns if c.startswith("F") and c[1:].isdigit()]
    prim = L["primary"].str[1:].astype(int).to_numpy() - 1
    summ, sub, g = omegas(L[cols].to_numpy(), Phi, prim)
    print(f"== {label} (k={k}): omega_total {summ['omega_total']:.3f}  "
          f"omega_h {summ['omega_h']:.3f}  ECV {summ['ecv']:.3f}")
    print(sub.round(3).to_string(index=False))
    out = pd.Series(g, index=L.index, name="general_loading")
    sub.round(4).to_csv(report_dir / f"general_factor_k{k}.csv", index=False)
    pd.Series(summ).round(4).to_csv(report_dir / f"general_factor_summary_k{k}.csv")
    return summ, sub, out


if __name__ == "__main__":
    run(ROOT / "reports", 7, "GSS 2016-2024")
    run(ROOT / "reports" / "anes", int(sys.argv[1]) if len(sys.argv) > 1 else 9, "ANES 2024")
