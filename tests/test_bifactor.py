"""Simulation check for the bifactor estimator and multidimensional scorer."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from bifactor import fit_bifactor, simulate_bifactor  # noqa: E402
from grm import Item, score_eap  # noqa: E402

SPECS = ["S1", "S2", "S3"]


def make_items(rng):
    items = []
    for s in SPECS:
        for j in range(8):
            K = [2, 3, 5, 7][j % 4]
            ag, as_ = rng.uniform(0.6, 2.0), rng.uniform(0.4, 1.6)
            d = np.sort(rng.uniform(-2, 2, K - 1))[::-1]
            items.append(Item(f"{s}_{j}", s, ag, d, K, {"G": ag, s: as_}))
    for j in range(3):
        ag = rng.uniform(1.0, 2.0)
        items.append(Item(f"G_{j}", "G", ag, np.array([0.5, -0.5]), 3, {"G": ag}))
    return items


def test_bifactor_recovery():
    rng = np.random.default_rng(11)
    items = make_items(rng)
    th, X = simulate_bifactor(items, SPECS, 3000, rng)
    X[rng.random(X.shape) < 0.3] = np.nan
    groups = [None if it.dim == "G" else it.dim for it in items]
    fitted, specs, ll, iters, conv = fit_bifactor(
        X, np.ones(len(X)), [it.ncat for it in items], [it.item_id for it in items],
        groups, verbose=False)
    assert conv
    tg = np.array([it.slopes["G"] for it in items])
    eg = np.array([it.slopes["G"] for it in fitted])
    assert np.corrcoef(tg, eg)[0, 1] > 0.93
    assert np.mean(np.abs(tg - eg)) < 0.2
    spec_items = [k for k, it in enumerate(items) if it.dim != "G"]
    ts = np.array([items[k].slopes[items[k].dim] for k in spec_items])
    es = np.array([fitted[k].slopes[fitted[k].dim] for k in spec_items])
    assert np.corrcoef(ts, es)[0, 1] > 0.85
    assert np.mean(np.abs(ts - es)) < 0.25

    dims = ["G"] + SPECS
    S = np.eye(4)
    idx = rng.choice(len(X), 300, replace=False)
    est, ora = [], []
    for i in idx:
        r_fit = {it.item_id: int(X[i, j]) for j, it in enumerate(fitted) if not np.isnan(X[i, j])}
        est.append(score_eap(r_fit, fitted, dims, S)["mean"])
        ora.append(score_eap(r_fit, items, dims, S)["mean"])
    est, ora = np.array(est), np.array(ora)
    for k in range(4):
        r_est = np.corrcoef(est[:, k], th[idx, k])[0, 1]
        r_ora = np.corrcoef(ora[:, k], th[idx, k])[0, 1]
        assert r_est > r_ora - 0.03, (dims[k], r_est, r_ora)
