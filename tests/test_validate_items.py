"""The item validator must reject items that break the writing standard."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_items import check  # noqa: E402

GOOD = {
    "id": "ok", "format": "position", "stem": "What should the federal minimum wage be?",
    "scope": "This is the national floor.", "high_pole": "lower",
    "options": ["$15 an hour", "$10 an hour", "$7.25 an hour"], "links": {}, "definitions": [],
}


def run(items, tmp_path):
    p = tmp_path / "x.json"
    p.write_text(json.dumps({"items": items}))
    return check(p)


def test_drafts_pass():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_items.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_good_item(tmp_path):
    errs, _, _ = run([GOOD], tmp_path)
    assert errs == []


def test_catches_violations(tmp_path):
    bad = [
        {**GOOD, "id": "party", "stem": "Should Republicans raise the minimum wage?"},
        {**GOOD, "id": "blank_middle", "options": ["Raise it", "Neutral", "Lower it"]},
        {**GOOD, "id": "two_opts", "options": ["Yes", "No"]},
        {**GOOD, "id": "long", "stem": " ".join(["word"] * 40) + "?"},
        {**GOOD, "id": "agree_no_pair", "format": "agree_defined",
         "options": ["Agree", "Torn", "Disagree"], "point_meanings": ["a", "b", "c"]},
        {**GOOD, "id": "bad_def", "definitions": [{"term": "viability", "text": "x", "source": "y"}]},
        {**GOOD, "id": "stale", "facts": [{"claim": "c", "source": "s", "checked": "2020-01-01"}]},
    ]
    errs, _, _ = run(bad, tmp_path)
    text = "\n".join(errs)
    for iid in ["party", "blank_middle", "two_opts", "long", "agree_no_pair", "bad_def", "stale"]:
        assert f"{iid}:" in text, f"validator missed {iid}"


TRADE = {**GOOD, "id": "tr", "format": "tradeoff", "stem": "Which matters more?",
         "options": ["Clearly A", "Lean A", "Lean B", "Clearly B"],
         "sides": [{"label": "Jobs", "text": "Protect jobs, even if prices rise"},
                   {"label": "Prices", "text": "Keep prices low, even if some jobs are lost"}]}


def test_tradeoff_and_frequency(tmp_path):
    errs, _, _ = run([TRADE], tmp_path)
    assert errs == []
    bad = [{**TRADE, "id": "one_side", "sides": TRADE["sides"][:1]},
           {**TRADE, "id": "free_opts", "options": ["Yes", "Mostly", "Rarely", "No"]},
           {**GOOD, "id": "freq", "format": "frequency", "options": ["Often", "Sometimes", "Rarely"]},
           {**GOOD, "id": "badsub", "subtopic": "Not a real subtopic"}]
    text = "\n".join(run(bad, tmp_path)[0])
    for iid in ["one_side", "free_opts", "freq", "badsub"]:
        assert f"{iid}:" in text, f"validator missed {iid}"


def test_duplicate_ids_across_files(tmp_path):
    from validate_items import collect_ids
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    a.write_text(json.dumps({"items": [GOOD]}))
    b.write_text(json.dumps({"items": [GOOD]}))
    _, dups = collect_ids([a, b])
    assert dups
