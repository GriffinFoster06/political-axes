"""Extract verbatim ANES 2024 question wording for every item in the model.

Parses the official questionnaire PDF (converted with `pdftotext -layout`),
matches each question to its release variable, and attaches any display-only
introduction that precedes it in the same question block (same name prefix).
Writes items/anes_wording.csv. Question wording is public documentation and
is reused with citation to ANES.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anes_items import ITEMS, source_vars  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "raw" / "anes"
HEAD = re.compile(r"^([A-Z0-9][A-Z0-9_]+)\s{3,}(PRE|POST)\b")


def clean(lines):
    keep = []
    for l in lines:
        t = l.strip()
        if not t or t == "Survey Question" or re.fullmatch(r"\d{1,3}", t):
            continue
        t = re.sub(r"^Survey Question\s+", "", t)
        t = re.sub(r"\d+\s+(PRE|POST)-?\s?ELECTION SURVEY QUESTIONNAIRE", "", t).strip()
        t = re.sub(r"(PRE|POST)-?\s?ELECTION SURVEY QUESTIONNAIRE\s+\d+", "", t).strip()
        if t:
            keep.append(t)
    s = " ".join(keep)
    s = re.sub(r"\s+", " ", s).replace("ﬀ", "ff").replace("ﬁ", "fi").replace("ﬂ", "fl")
    return s.strip()


def parse():
    txt = DIR / "questionnaire.txt"
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(DIR / "anes_timeseries_2024_questionnaire_20240808.pdf"),
                        str(txt)], check=True)
    L = txt.read_text().split("\n")
    starts = [i for i, l in enumerate(L) if HEAD.match(l)]
    entries = []
    for n, i in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(L)
        block = L[i:end]
        name = HEAD.match(L[i]).group(1)
        rel = next((re.findall(r"V24\d{4}[a-z]?x?", l) for l in block if l.startswith("Release Variable")), [])
        try:
            qs = next(k for k, l in enumerate(block) if l.startswith("Label")) + 1
        except StopIteration:
            continue
        # skip wrapped continuation of the all-caps label
        while qs < len(block) and block[qs].strip() and block[qs].strip().upper() == block[qs].strip() \
                and not re.match(r"^\s+\d+\.", block[qs]) and len(block[qs].strip()) < 60:
            qs += 1
        stop = next((k for k, l in enumerate(block) if k > qs and (
            re.match(r"^\s+(-?\d+)\.\s", l) or l.startswith(("Response Order", "Misc Spec", "Display Spec",
                                                            "Web Spec", "Universe", "Release Variable",
                                                            "Randomization", "Preload", "Help Text"))
        )), len(block))
        q = clean(block[qs:stop])
        opts = [re.sub(r"\s+", " ", m.group(2)).strip() for l in block[stop:]
                if (m := re.match(r"^\s+(\d+)\.\s+(.*\S)", l))]
        intro = any("No response options" in l or "Display Only" in l for l in block)
        entries.append({"name": name, "rel": rel, "q": q, "opts": opts, "intro": intro})
    return entries


def main():
    entries = parse()
    by_var = {}
    last_intro = {}
    for e in entries:
        prefix = e["name"].split("_")[0]
        if e["intro"]:
            last_intro[prefix] = e["q"]
            continue
        for v in e["rel"]:
            by_var.setdefault(v, {**e, "intro_text": last_intro.get(prefix, "")})
    import json
    cb = json.loads((DIR / "codebook_index.json").read_text())
    rows = []
    for iid, spec, dom, hyp, high, summ in ITEMS:
        v = source_vars(spec)[0]
        e = by_var.get(v)
        if e is None and v in cb:
            # summary variable: use the first source question it is built from
            src = re.findall(r"V24\d{4}[a-z]?", cb[v]["block"])
            src = [x for x in src if x != v and x in by_var]
            if src:
                e = by_var[src[0]]
                v = f"{v} (from {src[0]})"
        rows.append({"item_id": iid, "anes_var": v, "intro": (e or {}).get("intro_text", ""),
                     "question": (e or {}).get("q", ""),
                     "options": " | ".join((e or {}).get("opts", [])),
                     "found": e is not None})
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "items" / "anes_wording.csv", index=False)
    print(f"{df.found.sum()} of {len(df)} items matched to verbatim questionnaire text")
    return df


if __name__ == "__main__":
    d = main()
    print(d[~d.found])
