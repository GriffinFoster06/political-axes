"""Regression test from the 135-politician simulation (sim/).

The simulated answers are fixed, so these numbers only move when the scoring,
the keys or the comparison groups change. The thresholds sit a little below the
results at the time of the October 2026 fixes; if a change pushes one under,
look at sim/out/evaluation.txt before loosening it.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def ev():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_app.py")], check=True, capture_output=True)
    sys.path.insert(0, str(ROOT / "sim"))
    import evaluate
    res, rows = evaluate.main()
    return evaluate, res, rows


def test_party_and_order(ev):
    _, res, _ = ev
    assert res["party_auc"] >= 0.99
    assert res["order_hits"] >= res["order_total"] - 1
    assert res["sig_hits"] / res["sig_total"] >= 0.85


def test_matches(ev):
    _, res, _ = ev
    assert res["match_top3"] >= 120 and res["match_top5"] >= 128
    assert res["top_match_cross_side"] == 0


def test_reliability(ev):
    _, res, _ = ev
    # balanced axes measure consistency across sides, so internal consistency across items is not the target
    low = {ax: r["alpha"] for ax, r in res["reliability"].items() if r["alpha"] is not None and r["alpha"] < 0.7 and ax not in ("SPEECH", "FED")}
    assert not low, low
    assert res["reliability"]["SPEECH"]["alpha"] > 0.4


def test_labels(ev):
    _, res, _ = ev
    a = res["archetypes_by_group"]
    assert a["DL"] == {"Progressive": sum(a["DL"].values())}
    assert a["DM"].get("Liberal", 0) >= 0.8 * sum(a["DM"].values())
    assert a["LB"] == {"Libertarian": sum(a["LB"].values())}
    assert a["RF"] == {"Very conservative": sum(a["RF"].values())}


def test_map_dimension_is_cross_cutting(ev):
    _, res, _ = ev
    assert abs(res["map_dim_corr_with_G"]["auth"]) < 0.5
    assert res["map_dim_corr_with_G"]["econ"] > 0.9  # why econ x culture is no longer the default


pw = pytest.importorskip("playwright.sync_api")


def test_js_matches_python(ev):
    """The Python port in sim/evaluate.py must score exactly like app.js."""
    E, _, _ = ev
    from load import load_all
    people, _ = load_all()
    ids = ["sanders", "biden", "manchin", "romney", "trump", "gjohnson", "rfk", "pence"]
    with pw.sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.goto((ROOT / "app" / "dist" / "index.html").as_uri())
        for pid in ids:
            vis = E.visible_answers(people[pid])
            py = E.scores(vis)
            js = page.evaluate("a => { const s = window.__wys.score(a); const o = {}; for (const k in s) o[k] = [s[k].v, s[k].n]; o.__label = window.__wys.archetype(s).label; return o; }", vis)
            assert set(js) - {"__label"} == set(py), pid
            for ax in py:
                v, n = js[ax]
                assert abs(v - py[ax]["v"]) < 1e-9 and n == py[ax]["n"], (pid, ax, v, py[ax])
            assert js["__label"].lower().endswith(E.archetype(py).lower()), (pid, js["__label"], E.archetype(py))
        b.close()
