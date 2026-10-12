"""Load the GSS subset and apply the item crosswalk (recodes + keying)."""
from __future__ import annotations

import ast
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
YEARS = (2016, 2018, 2021, 2022, 2024)


def load_crosswalk() -> pd.DataFrame:
    cw = pd.read_csv(ROOT / "items" / "gss_crosswalk.csv")
    cw["recode_map"] = cw["recode"].apply(lambda s: {float(k): v for k, v in ast.literal_eval(s).items()})
    cw["ncat"] = cw["recode_map"].apply(lambda m: max(m.values()) + 1)
    return cw


def load_gss(years=YEARS, min_n: int = 500):
    raw = pd.read_parquet(ROOT / "data" / "raw" / "gss_subset.parquet")
    raw = raw[raw["year"].isin(years)].reset_index(drop=True)
    cw = load_crosswalk()
    X = pd.DataFrame(index=raw.index)
    for _, row in cw.iterrows():
        X[row.item_id] = raw[row.gss_var].map(row.recode_map)
    keep = [c for c in X.columns if X[c].notna().sum() >= min_n]
    dropped = [c for c in X.columns if c not in keep]
    X = X[keep]
    cw = cw.set_index("item_id").loc[keep].reset_index()
    # weights: post-stratification weight, normalized to mean 1 within each year,
    # then each year scaled to equal total so big years don't dominate
    w = raw["wtssps"].astype(float).fillna(1.0)
    w = w / raw.groupby("year")["wtssps"].transform("mean")
    w = w / raw.groupby("year")["year"].transform("count") * len(raw) / len(years)
    outcomes = raw[["year", "polviews", "partyid", "pres16", "pres20", "age", "sex",
                    "race", "degree", "region", "attend", "relig"]].copy()
    return X, w.to_numpy(), cw, outcomes, dropped
