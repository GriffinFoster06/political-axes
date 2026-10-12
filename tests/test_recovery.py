"""Simulation check: does the pipeline recover known truth?

Generates data from a known 3-dimension graded response model with 30% of
responses missing at random, fits it, and checks:
- item slopes and intercepts are recovered
- latent correlations are recovered
- multidimensional EAP scores track the true positions
- 80% intervals cover the truth about 80% of the time
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from grm import Item, fit_unidim, loglik_grid, estimate_corr, score_eap, simulate  # noqa: E402

DIMS = ["ECON", "CULT", "IMM"]
SIGMA = np.array([[1.0, 0.55, 0.40], [0.55, 1.0, 0.50], [0.40, 0.50, 1.0]])


def make_items(rng):
    items = []
    for d in DIMS:
        for j in range(8):
            K = [2, 3, 4, 5][j % 4]
            a = rng.uniform(0.8, 2.4)
            d_ = np.sort(rng.uniform(-2.0, 2.0, K - 1))[::-1]
            items.append(Item(f"{d}_{j}", d, a, d_, K))
    return items


def test_recovery():
    rng = np.random.default_rng(42)
    items = make_items(rng)
    theta, X = simulate(items, DIMS, SIGMA, n=3000, rng=rng, missing=0.3)
    w = np.ones(len(X))

    fitted = []
    for d in DIMS:
        cols = [j for j, it in enumerate(items) if it.dim == d]
        fit = fit_unidim(X[:, cols], w, [items[j].ncat for j in cols],
                         [items[j].item_id for j in cols], d)
        assert fit.converged
        fitted += fit.items

    true_a = np.array([it.a for it in items])
    est_a = np.array([it.a for it in fitted])
    assert np.corrcoef(true_a, est_a)[0, 1] > 0.95
    assert np.mean(np.abs(true_a - est_a)) < 0.15

    true_d = np.concatenate([it.d for it in items])
    est_d = np.concatenate([it.d for it in fitted])
    assert np.corrcoef(true_d, est_d)[0, 1] > 0.98

    L = {}
    for d in DIMS:
        cols = [j for j, it in enumerate(items) if it.dim == d]
        L[d] = loglik_grid(X[:, cols], [fitted[j] for j in cols])
    S = np.eye(3)
    for i in range(3):
        for k in range(i + 1, 3):
            S[i, k] = S[k, i] = estimate_corr(L[DIMS[i]], L[DIMS[k]], w)
    assert np.max(np.abs(S - SIGMA)) < 0.06, S

    # score a subsample with the full multidimensional scorer
    idx = rng.choice(len(X), 400, replace=False)
    means, sds = [], []
    for i in idx:
        resp = {it.item_id: int(X[i, j]) for j, it in enumerate(fitted) if not np.isnan(X[i, j])}
        out = score_eap(resp, fitted, DIMS, S)
        means.append(out["mean"])
        sds.append(out["sd"])
    means, sds = np.array(means), np.array(sds)
    # Oracle: same scorer with the TRUE item parameters and correlations.
    # The fitted pipeline should lose almost nothing relative to it.
    oracle = []
    for i in idx:
        resp = {it.item_id: int(X[i, j]) for j, it in enumerate(items) if not np.isnan(X[i, j])}
        oracle.append(score_eap(resp, items, DIMS, SIGMA)["mean"])
    oracle = np.array(oracle)
    for k in range(3):
        r = np.corrcoef(means[:, k], theta[idx, k])[0, 1]
        r_oracle = np.corrcoef(oracle[:, k], theta[idx, k])[0, 1]
        r_expected = np.sqrt(1 - np.mean(sds[:, k] ** 2))
        assert r > r_oracle - 0.02, (DIMS[k], r, r_oracle)
        assert abs(r - r_expected) < 0.04, (DIMS[k], r, r_expected)
    z = np.abs(means - theta[idx]) / sds
    coverage = np.mean(z < 1.2816)
    assert 0.74 < coverage < 0.86, coverage
