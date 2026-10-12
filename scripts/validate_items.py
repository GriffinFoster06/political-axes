#!/usr/bin/env python3
"""Check quiz item files against docs/item-writing-standard.md.

    python3 scripts/validate_items.py                 # all items/drafts/*.json
    python3 scripts/validate_items.py path/to/file.json

Errors (exit code 1) are rule violations. Warnings are things a person must
check: facts flagged for verification, reading level, long text.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATS = {"position", "exceptions", "frequency", "agree_defined"}
REQUIRED = ["id", "format", "stem", "scope", "options", "high_pole", "links"]
MAX_STEM, MAX_OPT, MAX_SCOPE = 35, 30, 40
GRADE_WARN = 9.0
BANNED = [
    # party and ideology cues (Rule 4)
    r"democrats?", r"republicans?", r"gop", r"liberals?", r"conservatives?", r"progressives?",
    r"maga", r"woke", r"socialis[mt]s?", r"leftists?", r"right-wing", r"left-wing", r"far[- ]right",
    r"far[- ]left", r"trump", r"biden", r"harris", r"obama",
    # loaded terms on either side
    r"illegal aliens?", r"illegals", r"undocumented", r"pro-life", r"pro-choice", r"baby killing",
    r"radical", r"extremists?", r"common[- ]sense", r"gun nuts?", r"assault weapons?",
    # blank middles are added automatically, never written as positions (Rule 5)
    r"neutral", r"neither agree nor disagree", r"no opinion", r"not sure",
]
BANNED_RE = re.compile(r"\b(" + "|".join(BANNED) + r")\b", re.I)


def words(s: str) -> int:
    return len(re.findall(r"[A-Za-z0-9$%'’-]+", s))


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def fk_grade(text: str) -> float:
    sents = max(1, len(re.findall(r"[.!?]", text)) or 1)
    ws = re.findall(r"[A-Za-z]+", text)
    if not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return 0.39 * len(ws) / sents + 11.8 * syl / len(ws) - 15.59


def all_text(it: dict) -> list[tuple[str, str]]:
    out = [("stem", it.get("stem", "")), ("scope", it.get("scope", "")), ("context", it.get("context", ""))]
    out += [(f"option {k}", o) for k, o in enumerate(it.get("options", []))]
    out += [(f"case {c['id']}", c["text"]) for c in it.get("cases", [])]
    return out


def check(path: Path):
    data = json.loads(path.read_text())
    items = data["items"]
    errs, warns = [], []
    ids = {}
    for it in items:
        for c in [it] + it.get("cases", []):
            if c["id"] in ids:
                errs.append(f"{c['id']}: duplicate id")
            ids[c["id"]] = it
    today = date.today()
    for it in items:
        iid = it.get("id", "?")
        for f in REQUIRED:
            if f not in it:
                errs.append(f"{iid}: missing field '{f}'")
        fmt = it.get("format")
        if fmt not in FORMATS:
            errs.append(f"{iid}: unknown format {fmt}")
        opts = it.get("options", [])
        lo, hi = (2, 3) if fmt == "exceptions" else (3, 7)
        if not lo <= len(opts) <= hi:
            errs.append(f"{iid}: {len(opts)} options (allowed {lo}-{hi} for {fmt})")
        if len(set(o.lower() for o in opts)) != len(opts):
            errs.append(f"{iid}: duplicate options")
        if fmt == "exceptions" and not it.get("cases"):
            errs.append(f"{iid}: exceptions item has no cases")
        if fmt == "agree_defined":
            pm = it.get("point_meanings", [])
            if len(pm) != len(opts):
                errs.append(f"{iid}: needs a meaning for every scale point")
            pair = it.get("pair")
            if pair not in ids:
                errs.append(f"{iid}: agree/disagree items need a reverse-keyed pair (Rule 6)")
            elif ids[pair]["options"] != list(reversed(opts)):
                errs.append(f"{iid}: pair {pair} must use the same scale in reverse order")
        if words(it.get("stem", "")) > MAX_STEM:
            errs.append(f"{iid}: stem has {words(it['stem'])} words (max {MAX_STEM})")
        if words(it.get("scope", "")) > MAX_SCOPE:
            errs.append(f"{iid}: scope has {words(it['scope'])} words (max {MAX_SCOPE})")
        for k, o in enumerate(opts):
            if words(o) > MAX_OPT:
                errs.append(f"{iid}: option {k} has {words(o)} words (max {MAX_OPT})")
        for where, text in all_text(it):
            for m in BANNED_RE.finditer(text or ""):
                errs.append(f"{iid}: banned term '{m.group(0)}' in {where} (Rule 4/5)")
        g = fk_grade(it.get("stem", "") + " " + it.get("scope", ""))
        if g > GRADE_WARN:
            warns.append(f"{iid}: stem+scope reading grade {g:.1f} (target 8)")
        blob = " ".join(t for _, t in all_text(it)).lower()
        for d in it.get("definitions", []):
            if d["term"].lower() not in blob:
                errs.append(f"{iid}: definition for '{d['term']}' but the term never appears")
            if not d.get("source"):
                errs.append(f"{iid}: definition '{d['term']}' has no source")
            if d.get("verify"):
                warns.append(f"{iid}: verify definition of '{d['term']}' against {d['source']}")
        for fct in it.get("facts", []):
            age = (today - date.fromisoformat(fct["checked"])).days
            if age > 365:
                errs.append(f"{iid}: fact checked {age} days ago; re-check: {fct['claim']}")
            if fct.get("verify"):
                warns.append(f"{iid}: verify fact: {fct['claim']} ({fct['source']})")
        if it.get("context") and not it.get("facts") and fmt != "agree_defined":
            warns.append(f"{iid}: has context text but no recorded fact source")
        for ref in list(it.get("show_if", {})) + ([it["followup"]] if it.get("followup") else []):
            if ref not in ids:
                errs.append(f"{iid}: refers to unknown item {ref}")
        if " and/or " in it.get("stem", ""):
            errs.append(f"{iid}: 'and/or' in stem usually means two questions (Rule 7)")
    return errs, warns, len(items)


def main(paths):
    paths = [Path(p) for p in paths] or sorted((ROOT / "items" / "drafts").glob("*.json"))
    total_err = 0
    for p in paths:
        errs, warns, n = check(p)
        print(f"{p.relative_to(ROOT) if p.is_absolute() else p}: {n} items, "
              f"{len(errs)} errors, {len(warns)} warnings")
        for e in errs:
            print("  ERROR  ", e)
        for w in warns:
            print("  warning", w)
        total_err += len(errs)
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
