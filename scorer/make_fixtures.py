"""Generate scorer/fixtures.json: response patterns + the Python reference scores.

The TypeScript test (scorer.test.ts) checks it reproduces these to 1e-6.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))
from grm import Item, score_eap  # noqa: E402

params = json.loads((ROOT / "model" / "params.json").read_text())
items = [Item(i["id"], i["dim"], i["a"], np.array(i["d"]), i["ncat"]) for i in params["items"]]
dims = [d["id"] for d in params["dimensions"]]
S = np.array(params["sigma"])
sc = params["scoring"]

rng = np.random.default_rng(7)
cases = [{"name": "no answers", "responses": {}}]
cases.append({"name": "all lowest", "responses": {it.item_id: 0 for it in items}})
cases.append({"name": "all highest", "responses": {it.item_id: it.ncat - 1 for it in items}})
cases.append({"name": "one item", "responses": {items[0].item_id: items[0].ncat - 1}})
for k in range(26):
    frac = [0.1, 0.3, 0.6, 1.0][k % 4]
    resp = {it.item_id: int(rng.integers(0, it.ncat)) for it in items if rng.random() < frac}
    cases.append({"name": f"random {k} ({int(frac * 100)}% answered)", "responses": resp})

for c in cases:
    out = score_eap(c["responses"], items, dims, S, n_draws=sc["draws"], seed=sc["seed"],
                    inflate=sc["inflate"])
    c["expected"] = {"mean": out["mean"].tolist(), "sd": out["sd"].tolist(),
                     "map": out["map"].tolist(), "ess": out["ess"]}

(Path(__file__).parent / "fixtures.json").write_text(json.dumps(cases))
print("wrote", len(cases), "cases")
