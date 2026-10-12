"""Exploratory factor analysis helper (minres + oblimin) with correct fit stats.

factor_analyzer 0.5.1 returns a wrong `phi_` (factor correlation matrix) for
oblique rotations with about 4 or more factors: Lambda @ phi_ @ Lambda.T does
not reproduce the model's own fitted matrix. The rotated loadings themselves
are fine. So:
- fit statistics come from the unrotated solution (rotation does not change fit)
- factor correlations are recovered exactly from the rotation: since
  Lambda_unrot = Lambda_rot @ T, Phi = T @ T.T
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer


def efa(Rc: np.ndarray, k: int, items: list[str]):
    un = FactorAnalyzer(n_factors=k, rotation=None, method="minres", is_corr_matrix=True)
    un.fit(Rc)
    Lu = un.loadings_
    iu = np.triu_indices(len(Rc), 1)
    rmsr = float(np.sqrt(np.mean((Rc - Lu @ Lu.T)[iu] ** 2)))
    cols = [f"F{i+1}" for i in range(k)]
    if k == 1:
        L, Phi = Lu, np.eye(1)
    else:
        ob = FactorAnalyzer(n_factors=k, rotation="oblimin", method="minres", is_corr_matrix=True)
        ob.fit(Rc)
        L = ob.loadings_
        T = np.linalg.lstsq(L, Lu, rcond=None)[0]
        Phi = T @ T.T
        d = np.sqrt(np.diag(Phi))
        Phi = Phi / np.outer(d, d)
        L = L * d          # keep Lambda Phi Lambda' invariant after normalizing
        # orient each factor so its largest loadings are positive
        s = np.sign(L[np.argmax(np.abs(L), axis=0), np.arange(k)])
        L = L * s
        Phi = Phi * np.outer(s, s)
    Ldf = pd.DataFrame(L, index=items, columns=cols)
    Ldf["primary"] = Ldf[cols].abs().idxmax(axis=1)
    Ldf["max_abs"] = Ldf[cols].abs().max(axis=1)
    return Ldf, pd.DataFrame(Phi, index=cols, columns=cols), rmsr
