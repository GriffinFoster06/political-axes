"""Graded response model (Samejima) with marginal maximum likelihood / EM.

Design choices:
- Slope-intercept form: P(Y >= k | theta) = logistic(a * theta + d_k), k = 1..K-1,
  with d_1 > d_2 > ... enforced by reparameterization.
- Missing responses are simply skipped in the likelihood, so split-ballot and
  adaptive (CAT) designs are handled without imputation.
- Survey weights enter every sum over persons.
- Weak priors on a and d (MAP) keep sparse items from running off to infinity.
- Multidimensional model is "between-item": every item measures exactly one
  dimension. Item parameters are calibrated per dimension; the latent
  correlation matrix is then estimated by 2-D quadrature for each pair.
- Scoring: EAP with the correlated prior via Laplace-centered importance
  sampling, using a fixed shared PRNG so the TypeScript scorer can reproduce
  results exactly.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import expit

NODES = np.linspace(-6, 6, 61)
PRIOR_A_MEAN, PRIOR_A_SD = 1.0, 2.0
PRIOR_D_SD = 6.0


# ---------------------------------------------------------------- item model
def cat_probs(a: float, d: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """Category probabilities, shape (len(theta), K)."""
    z = np.outer(theta, np.atleast_1d(a)).ravel()[:, None] + d[None, :]
    ps = expit(z)
    ones = np.ones((len(theta), 1))
    zeros = np.zeros((len(theta), 1))
    star = np.hstack([ones, ps, zeros])
    P = star[:, :-1] - star[:, 1:]
    return np.clip(P, 1e-12, 1.0)


def _unpack(v: np.ndarray):
    a = v[0]
    d1 = v[1]
    deltas = np.exp(v[2:])
    d = d1 - np.concatenate([[0.0], np.cumsum(deltas)])
    return a, d


def _pack(a: float, d: np.ndarray) -> np.ndarray:
    diffs = -np.diff(d)
    diffs = np.clip(diffs, 1e-3, None)
    return np.concatenate([[a, d[0]], np.log(diffs)])


def _item_negloglik(v, r, theta):
    """r: expected counts (Q, K) at nodes theta. Returns (nll, grad)."""
    a, d = _unpack(v)
    K = len(d) + 1
    ps = expit(a * theta[:, None] + d[None, :])           # (Q, K-1)
    star = np.hstack([np.ones((len(theta), 1)), ps, np.zeros((len(theta), 1))])
    P = np.clip(star[:, :-1] - star[:, 1:], 1e-12, 1.0)   # (Q, K)
    W = star * (1.0 - star)                               # (Q, K+1); 0 at ends
    ll = (r * np.log(P)).sum()
    ratio = r / P                                          # (Q, K)
    # gradient wrt d_j (j = 1..K-1 -> star index j)
    g_d = np.zeros(K - 1)
    for j in range(1, K):
        g_d[j - 1] = (ratio[:, j] * W[:, j] - ratio[:, j - 1] * W[:, j]).sum()
    g_a = (ratio * theta[:, None] * (W[:, :-1] - W[:, 1:])).sum()
    # priors
    ll += -0.5 * ((a - PRIOR_A_MEAN) / PRIOR_A_SD) ** 2 - 0.5 * (d ** 2).sum() / PRIOR_D_SD ** 2
    g_a += -(a - PRIOR_A_MEAN) / PRIOR_A_SD ** 2
    g_d += -d / PRIOR_D_SD ** 2
    # chain rule to (a, d1, log deltas)
    deltas = np.exp(v[2:])
    g = np.empty_like(v)
    g[0] = g_a
    g[1] = g_d.sum()
    suffix = np.cumsum(g_d[::-1])[::-1]                    # sum_{k>=j} g_d[k]
    g[2:] = -deltas * suffix[1:]
    return -ll, -g


@dataclass
class Item:
    """One item. `dim`/`a` give its primary dimension and slope; `slopes`
    (optional) gives slopes on several dimensions for within-item models
    such as the bifactor model (then `a` is the primary slope)."""
    item_id: str
    dim: str
    a: float
    d: np.ndarray
    ncat: int
    slopes: dict | None = None

    def avec(self, dim_idx: dict, D: int) -> np.ndarray:
        v = np.zeros(D)
        if self.slopes:
            for k, a in self.slopes.items():
                v[dim_idx[k]] = a
        else:
            v[dim_idx[self.dim]] = self.a
        return v


@dataclass
class DimFit:
    items: list[Item]
    loglik: float
    iters: int
    converged: bool


def _start_values(x: np.ndarray, w: np.ndarray, K: int):
    ok = ~np.isnan(x)
    counts = np.bincount(x[ok].astype(int), weights=w[ok], minlength=K) + 0.5
    cum = np.cumsum(counts[::-1])[::-1][1:] / counts.sum()      # P(Y>=k), k=1..K-1
    d = np.log(cum / (1 - cum))
    for j in range(1, len(d)):
        if d[j] >= d[j - 1] - 0.05:
            d[j] = d[j - 1] - 0.05
    return 1.0, d


def fit_unidim(X: np.ndarray, w: np.ndarray, ncats: list[int], item_ids: list[str],
               dim: str, start_signs: np.ndarray | None = None,
               max_iter: int = 300, tol: float = 1e-5) -> DimFit:
    """EM for a unidimensional GRM. X codes 0..K-1 with nan for missing."""
    n, p = X.shape
    theta = NODES
    logprior = -0.5 * theta ** 2
    logprior -= np.log(np.exp(logprior).sum())
    params = []
    for j in range(p):
        a, d = _start_values(X[:, j], w, ncats[j])
        if start_signs is not None:
            a *= start_signs[j]
        params.append(_pack(a, d))
    obs = [~np.isnan(X[:, j]) for j in range(p)]
    codes = [X[obs[j], j].astype(int) for j in range(p)]
    prev = -np.inf
    converged = False
    for it in range(max_iter):
        # E-step
        logL = np.zeros((n, len(theta)))
        for j in range(p):
            a, d = _unpack(params[j])
            lp = np.log(cat_probs(a, d, theta))           # (Q, K)
            logL[obs[j]] += lp[:, codes[j]].T
        lj = logL + logprior[None, :]
        mx = lj.max(axis=1, keepdims=True)
        post = np.exp(lj - mx)
        marg = post.sum(axis=1, keepdims=True)
        post /= marg
        ll = float((w * (np.log(marg[:, 0]) + mx[:, 0])).sum())
        wpost = post * w[:, None]
        # M-step
        for j in range(p):
            K = ncats[j]
            r = np.zeros((len(theta), K))
            for k in range(K):
                sel = codes[j] == k
                if sel.any():
                    r[:, k] = wpost[obs[j]][sel].sum(axis=0)
            res = minimize(_item_negloglik, params[j], args=(r, theta), jac=True,
                           method="L-BFGS-B")
            params[j] = res.x
        if abs(ll - prev) < tol * abs(ll):
            converged = True
            break
        prev = ll
    items = []
    for j in range(p):
        a, d = _unpack(params[j])
        items.append(Item(item_ids[j], dim, float(a), d, ncats[j]))
    return DimFit(items, ll, it + 1, converged)


# ------------------------------------------------------------ likelihoods
def loglik_grid(X: np.ndarray, items: list[Item], theta: np.ndarray = NODES) -> np.ndarray:
    """Per-person log-likelihood on a grid, shape (n, Q). Missing items skipped."""
    n = X.shape[0]
    out = np.zeros((n, len(theta)))
    for j, it in enumerate(items):
        ok = ~np.isnan(X[:, j])
        if not ok.any():
            continue
        lp = np.log(cat_probs(it.a, it.d, theta))
        out[ok] += lp[:, X[ok, j].astype(int)].T
    return out


def estimate_corr(L1: np.ndarray, L2: np.ndarray, w: np.ndarray,
                  theta: np.ndarray = NODES) -> float:
    """ML latent correlation between two dims given per-person grid log-likelihoods."""
    has = (L1.max(axis=1) - L1.min(axis=1) > 1e-9) & (L2.max(axis=1) - L2.min(axis=1) > 1e-9)
    A = np.exp(L1[has] - L1[has].max(axis=1, keepdims=True))
    B = np.exp(L2[has] - L2[has].max(axis=1, keepdims=True))
    ww = w[has]
    T1, T2 = np.meshgrid(theta, theta, indexing="ij")

    def nll(rho):
        s = 1 - rho ** 2
        logphi = -(T1 ** 2 - 2 * rho * T1 * T2 + T2 ** 2) / (2 * s)
        phi = np.exp(logphi)
        phi /= phi.sum()
        m = np.einsum("iq,qr,ir->i", A, phi, B)
        return -(ww * np.log(np.clip(m, 1e-300, None))).sum()

    res = minimize_scalar(nll, bounds=(-0.99, 0.99), method="bounded",
                          options={"xatol": 1e-4})
    return float(res.x)


# ----------------------------------------------------------------- scoring
class Mulberry32:
    """Tiny deterministic PRNG shared with the TypeScript scorer."""

    def __init__(self, seed: int):
        self.s = seed & 0xFFFFFFFF

    def next(self) -> float:
        self.s = (self.s + 0x6D2B79F5) & 0xFFFFFFFF
        t = self.s
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t &= 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0


def std_normals(n: int, D: int, seed: int = 20261012) -> np.ndarray:
    rng = Mulberry32(seed)
    out = np.empty(n * D)
    i = 0
    while i < n * D:
        u1 = rng.next()
        u2 = rng.next()
        u1 = max(u1, 1e-12)
        r = np.sqrt(-2.0 * np.log(u1))
        out[i] = r * np.cos(2 * np.pi * u2)
        if i + 1 < n * D:
            out[i + 1] = r * np.sin(2 * np.pi * u2)
        i += 2
    return out.reshape(n, D)


def _item_ll_and_derivs(theta_d: float, a: float, d: np.ndarray, k: int):
    """log P(Y=k|theta) and its first/second derivative wrt theta."""
    z = a * theta_d + d
    ps = expit(z)
    star = np.concatenate([[1.0], ps, [0.0]])
    W = star * (1 - star)
    Wp = W * (1 - 2 * star)  # derivative of W wrt z
    P = max(star[k] - star[k + 1], 1e-12)
    dP = a * (W[k] - W[k + 1])
    d2P = a * a * (Wp[k] - Wp[k + 1])
    return np.log(P), dP / P, d2P / P - (dP / P) ** 2


def score_eap(responses: dict[str, int], items: list[Item], dims: list[str],
              Sigma: np.ndarray, n_draws: int = 2000, seed: int = 20261012,
              inflate: float = 1.3, return_draws: bool = False) -> dict:
    """EAP + posterior SD for one respondent under the correlated MVN prior."""
    D = len(dims)
    dim_idx = {d: i for i, d in enumerate(dims)}
    used = [(it.avec(dim_idx, D), it, responses[it.item_id]) for it in items
            if it.item_id in responses and responses[it.item_id] is not None]
    Sinv = np.linalg.inv(Sigma)

    def logpost_grad_hess(t):
        lp = -0.5 * t @ Sinv @ t
        g = -Sinv @ t
        H = -Sinv.copy()
        for av, it, k in used:
            l, g1, h1 = _item_ll_and_derivs(float(av @ t), 1.0, it.d, k)
            lp += l
            g += av * g1
            H += np.outer(av, av) * h1
        return lp, g, H

    # Newton for the posterior mode
    t = np.zeros(D)
    for _ in range(50):
        lp, g, H = logpost_grad_hess(t)
        step = np.linalg.solve(H, g)
        t_new = t - step
        # backtracking
        lam = 1.0
        while logpost_grad_hess(t_new)[0] < lp - 1e-12 and lam > 1e-4:
            lam /= 2
            t_new = t - lam * step
        if np.max(np.abs(t_new - t)) < 1e-8:
            t = t_new
            break
        t = t_new
    _, _, H = logpost_grad_hess(t)
    cov = np.linalg.inv(-H)
    cov = 0.5 * (cov + cov.T)
    Lc = np.linalg.cholesky(cov * inflate ** 2)
    # antithetic pairs (z, -z): removes odd-moment Monte Carlo error
    Zh = std_normals(n_draws // 2, D, seed)
    Z = np.vstack([Zh, -Zh])
    draws = t + Z @ Lc.T
    # log proposal (up to the same constant for every draw)
    logq = -0.5 * (Z ** 2).sum(axis=1)
    logp = -0.5 * np.einsum("nd,de,ne->n", draws, Sinv, draws)
    for av, it, k in used:
        logp += np.log(cat_probs(1.0, it.d, draws @ av)[:, k])
    lw = logp - logq
    lw -= lw.max()
    wgt = np.exp(lw)
    wgt /= wgt.sum()
    mean = wgt @ draws
    dev = draws - mean
    pcov = (dev * wgt[:, None]).T @ dev
    ess = 1.0 / (wgt ** 2).sum()
    out = {"mean": mean, "sd": np.sqrt(np.diag(pcov)), "cov": pcov,
           "map": t, "ess": float(ess), "n_items": len(used)}
    if return_draws:
        out["draws"] = draws
        out["weights"] = wgt
    return out


def eap_unidim(L: np.ndarray, theta: np.ndarray = NODES):
    """EAP and SD from grid log-likelihoods with a N(0,1) prior."""
    lj = L - 0.5 * theta[None, :] ** 2
    lj -= lj.max(axis=1, keepdims=True)
    p = np.exp(lj)
    p /= p.sum(axis=1, keepdims=True)
    m = p @ theta
    sd = np.sqrt(np.clip(p @ theta ** 2 - m ** 2, 0, None))
    return m, sd


# --------------------------------------------------------------- simulation
def simulate(items: list[Item], dims: list[str], Sigma: np.ndarray, n: int,
             rng: np.random.Generator, missing: float = 0.0):
    D = len(dims)
    th = rng.multivariate_normal(np.zeros(D), Sigma, size=n)
    dim_idx = {d: i for i, d in enumerate(dims)}
    X = np.full((n, len(items)), np.nan)
    for j, it in enumerate(items):
        P = cat_probs(it.a, it.d, th[:, dim_idx[it.dim]])
        u = rng.random(n)[:, None]
        X[:, j] = (u > np.cumsum(P, axis=1)).sum(axis=1)
    if missing > 0:
        X[rng.random(X.shape) < missing] = np.nan
    return th, X
