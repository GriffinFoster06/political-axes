"""Weighted pairwise polychoric correlations (two-step ML).

Two-step method (Olsson 1979): thresholds come from each item's own weighted
marginal distribution, then for each item pair the latent correlation rho is
chosen to maximize the weighted multinomial likelihood of the observed
contingency table. Pairwise-complete data, so split-ballot designs work.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import ndtr, owens_t, ndtri


def bvn_cdf(h: np.ndarray, k: np.ndarray, rho: float) -> np.ndarray:
    """P(X <= h, Y <= k) for standard bivariate normal with correlation rho.

    Uses Owen's T representation. Handles +/- inf limits.
    """
    h = np.asarray(h, dtype=float)
    k = np.asarray(k, dtype=float)
    h, k = np.broadcast_arrays(h, k)
    out = np.zeros(h.shape)
    neg = np.isneginf(h) | np.isneginf(k)
    hinf = np.isposinf(h)
    kinf = np.isposinf(k)
    out[~neg & hinf & kinf] = 1.0
    m = ~neg & hinf & ~kinf
    out[m] = ndtr(k[m])
    m = ~neg & kinf & ~hinf
    out[m] = ndtr(h[m])
    m = ~neg & ~hinf & ~kinf
    if np.any(m):
        hh = h[m].copy()
        kk = k[m].copy()
        hh[hh == 0] = 1e-10
        kk[kk == 0] = 1e-10
        s = np.sqrt(1.0 - rho * rho)
        ah = (kk - rho * hh) / (hh * s)
        ak = (hh - rho * kk) / (kk * s)
        corr = ((hh * kk) < 0).astype(float) * 0.5
        out[m] = 0.5 * (ndtr(hh) + ndtr(kk)) - owens_t(hh, ah) - owens_t(kk, ak) - corr
    return np.clip(out, 0.0, 1.0)


def thresholds(x: np.ndarray, w: np.ndarray, ncat: int) -> np.ndarray:
    ok = ~np.isnan(x)
    counts = np.bincount(x[ok].astype(int), weights=w[ok], minlength=ncat)
    p = np.cumsum(counts)[:-1] / counts.sum()
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.concatenate([[-np.inf], ndtri(p), [np.inf]])


def _pair(x, y, w, tx, ty, nx, ny):
    ok = ~np.isnan(x) & ~np.isnan(y)
    if ok.sum() < 30:
        return np.nan, int(ok.sum())
    table = np.zeros((nx, ny))
    np.add.at(table, (x[ok].astype(int), y[ok].astype(int)), w[ok])
    # effective counts: rescale weights so the table sums to the raw n
    table *= ok.sum() / table.sum()
    H, K = np.meshgrid(tx, ty, indexing="ij")

    def nll(rho):
        F = bvn_cdf(H, K, rho)
        P = F[1:, 1:] - F[:-1, 1:] - F[1:, :-1] + F[:-1, :-1]
        P = np.clip(P, 1e-12, None)
        return -(table * np.log(P)).sum()

    res = minimize_scalar(nll, bounds=(-0.995, 0.995), method="bounded",
                          options={"xatol": 1e-5})
    return float(res.x), int(ok.sum())


def polychoric_matrix(X: np.ndarray, w: np.ndarray, ncats: list[int]):
    """X: n x p with integer codes 0..ncat-1 or nan. Returns (R, Npair)."""
    n, p = X.shape
    th = [thresholds(X[:, j], w, ncats[j]) for j in range(p)]
    R = np.eye(p)
    N = np.zeros((p, p), dtype=int)
    for j in range(p):
        N[j, j] = int((~np.isnan(X[:, j])).sum())
        for k in range(j + 1, p):
            r, m = _pair(X[:, j], X[:, k], w, th[j], th[k], ncats[j], ncats[k])
            R[j, k] = R[k, j] = r
            N[j, k] = N[k, j] = m
    return R, N


def nearest_pd(R: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Smooth a pairwise matrix to the nearest positive-definite correlation matrix."""
    vals, vecs = np.linalg.eigh(R)
    vals = np.clip(vals, eps, None)
    S = vecs @ np.diag(vals) @ vecs.T
    d = np.sqrt(np.diag(S))
    S = S / np.outer(d, d)
    np.fill_diagonal(S, 1.0)
    return S
