"""Step 0: pull only the needed columns out of the GSS cumulative file.

Reads data/raw/gss/gss_all.rda (from scripts/restore_data.py) and writes
data/raw/gss_subset.parquet + gss_subset_meta.json (variable and value labels).
Streams the file, so it works with a few hundred MB of RAM.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rda_stream import column_names, read_columns  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
EXTRA = ["year", "id", "ballot", "wtssps", "wtssall", "wtssnrps", "vpsu", "vstrat",
         "polviews", "partyid", "pres16", "pres20", "age", "sex", "race", "educ",
         "degree", "region", "relig", "attend", "income16", "realinc",
         "trust", "fair", "helpful", "owngun", "tax", "xmarsex"]


def main():
    src = next((p for p in [RAW / "gss" / "gss_all.rda", RAW / "gss_all.rda"] if p.exists()), None)
    if src is None:
        raise SystemExit("GSS file not found. Run: python3 scripts/restore_data.py gss")
    names = column_names(str(src))
    (RAW / "gss_columns.json").write_text(json.dumps(names))
    cw = pd.read_csv(ROOT / "items" / "gss_crosswalk.csv")
    cols = list(dict.fromkeys(EXTRA + cw["gss_var"].tolist()))
    missing = [c for c in cols if c not in names]
    if missing:
        print("not in this GSS release, skipped:", missing)
    cols = [c for c in cols if c in names]
    df, meta = read_columns(str(src), cols, names)
    df.to_parquet(RAW / "gss_subset.parquet")
    (RAW / "gss_subset_meta.json").write_text(json.dumps(meta, indent=1))
    print(f"wrote {df.shape[0]} rows x {df.shape[1]} columns from {src.name}")


if __name__ == "__main__":
    main()
