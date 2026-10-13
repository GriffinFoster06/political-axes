"""Clarity pass: rewrite wording that could be read more than one way.

Each edit names an item and the fields to replace (stem, scope, context, an option by
its code, a tradeoff side, or a case). Edits never add, remove or reorder options, so
answer codes, scoring keys and the simulated answers keep their meaning. The edits are
listed in clarity_edits.json and clarity/Dxx.json (one file per topic), one entry per
item, with the reason. "definitions" adds or replaces dotted-term definitions by term;
"point_meanings" replaces the meaning shown under each agree/disagree point.

Run: python3 scripts/revisions/rev_2026_10_15_clarity.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
EDITS = json.loads((HERE / "clarity_edits.json").read_text())
for _p in sorted((HERE / "clarity").glob("*.json")):
    for _k, _v in json.loads(_p.read_text()).items():
        assert _k not in EDITS, f"{_p.name}: {_k} edited twice"
        EDITS[_k] = _v


def main():
    done = set()
    for p in sorted((ROOT / "items" / "drafts").glob("*.json")):
        data = json.loads(p.read_text())
        changed = False
        for it in data["items"]:
            e = EDITS.get(it["id"])
            if not e:
                continue
            for f in ("stem", "scope", "context"):
                if f in e:
                    it[f] = e[f]
            if "point_meanings" in e:
                assert len(e["point_meanings"]) == len(it["options"]), it["id"]
                it["point_meanings"] = e["point_meanings"]
            for d in e.get("definitions", []):
                defs = it.setdefault("definitions", []) or []
                it["definitions"] = defs
                old = next((x for x in defs if x["term"].lower() == d["term"].lower()), None)
                new = {"term": d["term"], "text": d["text"], "source": d.get("source", "descriptive"), "verify": False}
                if old:
                    old.update(new)
                else:
                    defs.append(new)
            for k, v in e.get("options", {}).items():
                assert 0 <= int(k) < len(it["options"]), (it["id"], k)
                it["options"][int(k)] = v
            for k, v in e.get("sides", {}).items():
                it["sides"][int(k)].update(v)
            for cid, v in e.get("cases", {}).items():
                c = next(c for c in it["cases"] if c["id"] == cid)
                c["text"] = v
            done.add(it["id"])
            changed = True
        if changed:
            p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    missing = set(EDITS) - done - {k for k in EDITS if k.startswith("_")}
    assert not missing, missing
    print(f"applied clarity edits to {len(done)} items")


if __name__ == "__main__":
    main()
