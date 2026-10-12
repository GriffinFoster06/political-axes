"""Bifactor graded response model, fitted by EM with dimension reduction.

Every item loads on a general factor G and on at most one specific factor.
All factors are independent N(0, 1). Following Gibbons & Hedeker (1992) and
Cai, Yang & Hansen (2011), the likelihood only ever needs 2-D integrals
(G x one specific), so the cost grows linearly in the number of specific
factors instead of exponentially.

    P(Y >= k | g, s) = logistic(a_g * g + a_s * s + d_k)

Missing responses are skipped; survey weights enter every sum over people.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logsumexp

from grm import Item

Q_NODES = np.linspace(-5, 5, 21)
LOGW = -0.5 * Q_NODES ** 2
LOGW -= logsumexp(LOGW)
PRIOR_SD = 2.0


def _unpack(v, D):
    a = v[:D]
    d1 = v[D]
    d = d1 - np.concatenate([[0.0], np.cumsum(np.exp(v[D + 1:]))])
    return a, d


def _pack(a, d):
    diffs = np.clip(-np.diff(d), 1e-3, None)
    return np.concatenate([np.atleast_1d(a), [d[0]], np.log(diffs)])


def logp_grid(a, d, T):
    """log P(Y=k) at node rows T (M x D) -> (M, K)."""
    z = T @ a
    ps = expit(z[:, None] + d[None, :])
    star = np.hstack([np.ones((len(T), 1)), ps, np.zeros((len(T), 1))])
    return np.log(np.clip(star[:, :-1] - star[:, 1:], 1e-12, 1.0))


def _nll(v, r, T, prior_mean):
    D = T.shape[1]
    a, d = _unpack(v, D)
    K = len(d) + 1
    z = T @ a
    ps = expit(z[:, None] + d[None, :])
    star = np.hstack([np.ones((len(T), 1)), ps, np.zeros((len(T), 1))])
    P = np.clip(star[:, :-1] - star[:, 1:], 1e-12, 1.0)
    W = star * (1 - star)
    ll = (r * np.log(P)).sum()
    ratio = r / P
    g_d = np.array([(ratio[:, j] * W[:, j] - ratio[:, j - 1] * W[:, j]).sum() for j in range(1, K)])
    dz = (ratio * (W[:, :-1] - W[:, 1:])).sum(axis=1)       # d ll / d z per node
    g_a = T.T @ dz
    ll += -0.5 * (((a - prior_mean) / PRIOR_SD) ** 2).sum() - 0.5 * (d ** 2).sum() / 36.0
    g_a += -(a - prior_mean) / PRIOR_SD ** 2
    g_d += -d / 36.0
    deltas = np.exp(v[D + 1:])
    g = np.empty_like(v)
    g[:D] = g_a
    g[D] = g_d.sum()
    suffix = np.cumsum(g_d[::-1])[::-1]
    g[D + 1:] = -deltas * suffix[1:]
    return -ll, -g


def fit_bifactor(X: np.ndarray, w: np.ndarray, ncats: list[int], item_ids: list[str],
                 groups: list[str | None], start_a: np.ndarray | None = None,
                 max_iter: int = 200, tol: float = 1e-6, verbose: bool = True):
    """groups[j] = name of item j's specific factor, or None (general only).

    start_a: optional (p, 2) array of starting (a_general, a_specific).
    Returns (items, specific_names, loglik, iters, converged).
    """
    n, p = X.shape
    Q = len(Q_NODES)
    specs = sorted({g for g in groups if g is not None})
    members = {s: [j for j in range(p) if groups[j] == s] for s in specs}
    general_only = [j for j in range(p) if groups[j] is None]
    obs = [~np.isnan(X[:, j]) for j in range(p)]
    codes = [X[obs[j], j].astype(int) for j in range(p)]
    G2, S2 = np.meshgrid(Q_NODES, Q_NODES, indexing="ij")
    T2 = np.column_stack([G2.ravel(), S2.ravel()])          # (Q*Q, 2): rows q*Q + r
    T1 = Q_NODES[:, None]

    params = []
    for j in range(p):
        x = X[obs[j], j]
        cnt = np.bincount(x.astype(int), weights=w[obs[j]], minlength=ncats[j]) + 0.5
        cum = np.cumsum(cnt[::-1])[::-1][1:] / cnt.sum()
        d = np.log(cum / (1 - cum))
        for k in range(1, len(d)):
            d[k] = min(d[k], d[k - 1] - 0.05)
        if groups[j] is None:
            a = np.array([start_a[j, 0] if start_a is not None else 1.0])
        else:
            a = np.array(start_a[j] if start_a is not None else [1.0, 0.5])
        params.append(_pack(a, d))

    prev = -np.inf
    converged = False
    for it in range(max_iter):
        # ---------------- E-step
        logL = np.zeros((n, Q))
        S = {}
        Lk = {}
        for s in specs:
            Ss = np.zeros((n, Q, Q))
            for j in members[s]:
                a, d = _unpack(params[j], 2)
                lp = logp_grid(a, d, T2).reshape(Q, Q, -1)
                Ss[obs[j]] += np.moveaxis(lp[:, :, codes[j]], 2, 0)
            S[s] = Ss
            Lk[s] = logsumexp(Ss + LOGW[None, None, :], axis=2)
            logL += Lk[s]
        for j in general_only:
            a, d = _unpack(params[j], 1)
            lp = logp_grid(a, d, T1)
            logL[obs[j]] += lp[:, codes[j]].T
        lj = logL + LOGW[None, :]
        marg = logsumexp(lj, axis=1)
        ll = float((w * marg).sum())
        # ---------------- M-step
        for s in specs:
            rest = logL - Lk[s]                                # (n, Q)
            logpost = (S[s] + LOGW[None, None, :] + (LOGW[None, :] + rest - marg[:, None])[:, :, None])
            post = np.exp(logpost) * w[:, None, None]           # (n, Q, Q)
            for j in members[s]:
                K = ncats[j]
                pj = post[obs[j]]
                r = np.zeros((Q * Q, K))
                for c in range(K):
                    sel = codes[j] == c
                    if sel.any():
                        r[:, c] = pj[sel].sum(axis=0).ravel()
                res = minimize(_nll, params[j], args=(r, T2, np.array([1.0, 0.5])),
                               jac=True, method="L-BFGS-B")
                params[j] = res.x
        if general_only:
            post0 = np.exp(lj - marg[:, None]) * w[:, None]
            for j in general_only:
                K = ncats[j]
                pj = post0[obs[j]]
                r = np.zeros((Q, K))
                for c in range(K):
                    sel = codes[j] == c
                    if sel.any():
                        r[:, c] = pj[sel].sum(axis=0)
                res = minimize(_nll, params[j], args=(r, T1, np.array([1.0])),
                               jac=True, method="L-BFGS-B")
                params[j] = res.x
        if verbose and it % 5 == 0:
            print(f"    EM {it}: loglik {ll:.2f}")
        if abs(ll - prev) < tol * abs(ll):
            converged = True
            break
        prev = ll

    items = []
    for j in range(p):
        if groups[j] is None:
            a, d = _unpack(params[j], 1)
            slopes = {"G": float(a[0])}
        else:
            a, d = _unpack(params[j], 2)
            slopes = {"G": float(a[0]), groups[j]: float(a[1])}
        items.append(Item(item_ids[j], groups[j] or "G", float(a[0]), d, ncats[j], slopes))
    return items, specs, ll, it + 1, converged


def simulate_bifactor(items: list[Item], specs: list[str], n: int, rng):
    dims = ["G"] + specs
    idx = {d: i for i, d in enumerate(dims)}
    th = rng.standard_normal((n, len(dims)))
    X = np.full((n, len(items)), np.nan)
    for j, it in enumerate(items):
        z = th @ it.avec(idx, len(dims))
        ps = expit(z[:, None] + it.d[None, :])
        star = np.hstack([np.ones((n, 1)), ps, np.zeros((n, 1))])
        P = star[:, :-1] - star[:, 1:]
        X[:, j] = (rng.random(n)[:, None] > np.cumsum(P, axis=1)).sum(axis=1)
    return th, X
