"""Helpers for writing items/statements/Dxx.json.

Each answer's statement is {"t": headline, "yes": [...], "no": [...], "means": [...]}:
the concrete things that answer means you'd support, oppose, or believe. The topic
scripts in scripts/revisions/statements/ call these helpers and write one file each.

Run all of them: python3 scripts/revisions/statements/run_all.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def S(t, yes=None, no=None, means=None, lean=None):
    out = {"t": t}
    if lean:
        out["lean"] = lean
    if yes:
        out["yes"] = list(yes)
    if no:
        out["no"] = list(no)
    if means:
        out["means"] = list(means)
    return out


PROPER = {"US", "I", "Americans", "American", "Congress", "Washington", "States", "Federal"}


def _lower_first(t):
    w = t.split(" ", 1)[0]
    return t if w in PROPER or w.isupper() else t[0].lower() + t[1:]


def agree(options, agree_side, disagree_side, torn):
    """agree_defined: five points. agree_side/disagree_side are S(...) for the view itself;
    the strong and moderate points share the same lists and differ in the headline."""
    out = []
    for o in options:
        low = o.lower()
        if low == "torn":
            out.append(torn)
            continue
        side = disagree_side if "disagree" in low else agree_side
        strong = low.startswith("strongly")
        tail = " You'd say this holds in nearly every case." if strong else " You'd say this holds most of the time, with some real exceptions."
        d = dict(side)
        d["t"] = side["t"] + tail
        out.append(d)
    return out


def trade(a, b, torn):
    """tradeoff: Clearly A, Lean A, Lean B, Clearly B, plus the torn statement."""
    def lean(s):
        d = dict(s)
        d["t"] = s.get("lean") or "On balance, " + _lower_first(s["t"])
        d.pop("lean", None)
        return d
    a2, b2 = dict(a), dict(b)
    a2.pop("lean", None); b2.pop("lean", None)
    return {"s": [a2, lean(a), lean(b), b2], "torn": torn}


def write(dom, statements):
    p = ROOT / "items" / "statements" / f"{dom}.json"
    p.write_text(json.dumps(statements, indent=1, ensure_ascii=False) + "\n")


def write_clarity(dom, edits):
    p = ROOT / "scripts" / "revisions" / "clarity" / f"{dom}.json"
    p.write_text(json.dumps(edits, indent=1, ensure_ascii=False) + "\n")


_ITEMS = None


def item(iid):
    global _ITEMS
    if _ITEMS is None:
        _ITEMS = {}
        for p in (ROOT / "items" / "drafts").glob("*.json"):
            for it in json.loads(p.read_text())["items"]:
                _ITEMS[it["id"]] = it
    return _ITEMS[iid]


def agree_item(iid, agree_side, disagree_side, torn):
    return agree(item(iid)["options"], agree_side, disagree_side, torn)


def existing(dom, iid):
    """An exceptions template list kept as written in the current statements file."""
    p = ROOT / "items" / "statements" / f"{dom}.json"
    v = json.loads(p.read_text())[iid]
    assert all(isinstance(x, str) and "{case}" in x for x in v), iid
    return v


FREQ = {
    "Almost always": ("almost always", "9 or more"),
    "Most of the time": ("most of the time", "about 7"),
    "About half the time": ("about half the time", "about 5"),
    "Sometimes": ("sometimes", "about 3"),
    "Rarely": ("rarely", "1 or fewer"),
}


def freq(iid, t, means):
    """frequency items: t and means are templates with {f} (how often, in words) and {n}
    (how many out of 10)."""
    out = []
    for o in item(iid)["options"]:
        key = next(k for k in FREQ if o.startswith(k))
        f, n = FREQ[key]
        out.append(S(t.format(f=f, n=n), means=[m.format(f=f, n=n) for m in means]))
    return out
