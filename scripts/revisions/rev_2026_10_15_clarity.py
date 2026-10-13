"""Clarity pass: rewrite wording that could be read more than one way.

Each edit names an item and the fields to replace (stem, scope, context, an option by
its code, a tradeoff side, or a case). Edits never add, remove or reorder options, so
answer codes, scoring keys and the simulated answers keep their meaning. The edits are
listed in clarity_edits.json, one entry per item, with the reason.

Run: python3 scripts/revisions/rev_2026_10_15_clarity.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITS = json.loads((Path(__file__).with_name("clarity_edits.json")).read_text())


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
