"""Small helper for scripted edits to the draft bank (used for review revisions).

    from bankedit import Bank
    b = Bank(); it = b["min_wage"]; it["stem"] = "..."; b.save()
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "items" / "drafts"


class Bank:
    def __init__(self):
        self.files = {p: json.loads(p.read_text()) for p in sorted(DRAFTS.glob("*.json"))}

    def _find(self, iid):
        for p, d in self.files.items():
            for k, it in enumerate(d["items"]):
                if it["id"] == iid:
                    return p, d, k
        raise KeyError(iid)

    def __getitem__(self, iid):
        p, d, k = self._find(iid)
        return d["items"][k]

    def __contains__(self, iid):
        try:
            self._find(iid)
            return True
        except KeyError:
            return False

    def remove(self, iid):
        p, d, k = self._find(iid)
        return d["items"].pop(k)

    def replace(self, iid, *new_items):
        """Replace one item with one or more items, in the same place."""
        p, d, k = self._find(iid)
        d["items"][k:k + 1] = list(new_items)

    def insert_after(self, iid, *new_items):
        p, d, k = self._find(iid)
        d["items"][k + 1:k + 1] = list(new_items)

    def append(self, domain_file, *new_items):
        p = DRAFTS / domain_file
        self.files[p]["items"].extend(new_items)

    def save(self):
        for p, d in self.files.items():
            p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def item(iid, subtopic, axis, fmt, stem, scope, options, high_pole, **kw):
    out = {"id": iid, "subtopic": subtopic, "axis": axis, "format": fmt, "stem": stem, "scope": scope}
    if "context" in kw:
        out["context"] = kw.pop("context")
    out["options"] = options
    out["high_pole"] = high_pole
    out.update(kw)
    return out


FREQ = ["Almost always (9 or more times in 10)", "Most of the time (about 7 in 10)", "About half the time",
        "Sometimes (about 3 in 10)", "Rarely (1 in 10 or less)"]
FREQ_REV = list(reversed(FREQ))
TRADE = ["Clearly A", "Lean A", "Lean B", "Clearly B"]
AGREE = ["Strongly disagree", "Disagree", "Torn", "Agree", "Strongly agree"]
MEAN = ["False in nearly every case I can think of", "False in most cases, with some real exceptions",
        "I can see it both ways about equally", "True in most cases, with some real exceptions",
        "True in nearly every case I can think of"]
