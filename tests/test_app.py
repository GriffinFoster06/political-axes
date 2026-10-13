"""End-to-end test of the pilot quiz app in a headless browser.

Clicks through intro, every question, priorities, about-you and the finish,
answering pseudo-randomly, then checks what was recorded.
"""
import json
import random
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
pw = pytest.importorskip("playwright.sync_api")


@pytest.fixture(scope="module")
def built():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_app.py")], check=True, capture_output=True)
    return (ROOT / "app" / "dist" / "index.html").as_uri()


def walk(page, rng, mode):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.click(f'[data-mode="{mode}"]')     # home: pick length
    page.click("#go")                       # start
    page.click("#go")                       # instructions -> begin
    screens = 0
    while True:
        st = page.evaluate("window.__wys.state().phase")
        if st != "quiz" and st != "break":
            break
        screens += 1
        assert screens < 900, "stuck in the quiz loop"
        if st == "break":
            page.click("#go")
            continue
        cases = page.query_selector_all(".case")
        if cases:
            for c in cases:
                chips = c.query_selector_all("[data-code]")
                (c.query_selector(".esc") if rng.random() < 0.05 else rng.choice(chips)).click()
        else:
            r = rng.random()
            if not page.query_selector('[data-esc="1"]'):
                r = 1.0  # attention-check screens have no escape options
            if r < 0.04:
                page.click('[data-esc="1"]')
                page.fill("#nftext", "my own view")
            elif r < 0.07:
                page.click('[data-esc="2"]')
            elif r < 0.09:
                page.click("#skip")
                continue
            else:
                rng.choice(page.query_selector_all(".opt[data-code]")).click()
                firm = page.query_selector_all("[data-firm]")
                if firm and rng.random() < 0.5:
                    rng.choice(firm).click()
        assert not page.is_disabled("#next")
        page.click("#next")
    # priorities
    for _ in range(15):
        assert page.evaluate("window.__wys.state().phase") == "pri"
        rows = page.query_selector_all('input[name="best"]')
        b, w = rng.sample(range(len(rows)), 2)
        rows[b].check()
        page.query_selector_all('input[name="worst"]')[w].check()
        page.click("#next")
    assert page.evaluate("window.__wys.state().phase") == "aboutyou"
    page.check('input[name="age_bracket"][value="3"]')
    page.check('input[name="party_id"][value="2"]')
    page.check('input[name="party_lean"][value="1"]')
    page.select_option("#in-state", "15")
    page.click("#go")
    page.click('[data-k="0"]')
    page.click("#go")
    page.wait_for_selector(".map", state="attached")
    return errors


@pytest.mark.parametrize("mode,seed", [("quick", 4), ("pilot", 1), ("pilot", 2), ("full", 3)])
def test_click_through(built, mode, seed):
    with pw.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.route("**/fonts.g*/**", lambda r: r.abort())
        page.goto(built)
        errors = walk(page, random.Random(seed), mode)
        S = page.evaluate("window.__wys.state()")
        bank = page.evaluate("window.__wys.bank")
        payload = page.evaluate("window.__wys.payload()")
        n_axes = len(page.query_selector_all(".axis"))
        n_profiles = len(page.query_selector_all(".profiles li"))
        scores = page.evaluate("window.__wys.scores()")
        browser.close()
    assert errors == []
    assert S["done"] and S["submitted"] == "local"
    items = bank["items"]
    shown = {e["id"] for e in S["queue"] if e["k"] == "item"}
    # results page: overall bar plus axis bars and closest groups
    assert n_axes >= 10 and n_profiles >= 3
    assert all(-1.0001 <= v["v"] <= 1.0001 for v in scores.values())
    if mode == "quick":
        assert shown == set(bank["quick"])
    elif mode == "pilot":
        d = bank["design"]
        expect = set(d["link"]) | {i for b in S["form"] for i in d["blocks"][b]}
        assert shown == expect
        assert S["form"] in d["forms"]
    else:
        assert shown == set(items)
    # every recorded answer uses a valid code and records display direction
    for k, a in S["ans"].items():
        base = k.split("#")[0]
        it = items.get(base)
        if it is None:  # an exception case
            parent = next(i for i in items.values() if any(c["id"] == base for c in i.get("cases", [])))
            k_opts = len(parent["options"])
        else:
            k_opts = len(it["options"])
        if a.get("c") is not None:
            assert 0 <= a["c"] < k_opts
            assert a["d"] in (0, 1)
    # follow-ups only answered when their condition held
    for i, it in items.items():
        if it.get("show_if") and it["format"] == "exceptions":
            parent, codes = next(iter(it["show_if"].items()))
            pa = S["ans"].get(parent, {})
            if any(c["id"] in S["ans"] for c in it["cases"]):
                assert pa.get("c") in codes
    assert len(S["qc"]) == 3
    assert sum(1 for r in S["pri"].values() if r.get("b") and r.get("w")) == 15
    assert S["about"]["party_lean"] == 1 and S["about"]["state"] == 15
    # repeats asked in the opposite display direction
    for k, a in S["ans"].items():
        if k.endswith("#r"):
            assert a["d"] == 1 - S["ans"][k[:-2]]["d"]
    assert S["activeMs"] > 0
    # the analysis script reads the payload and applies the exclusion rule
    import os, csv as _csv, tempfile
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "r.json"
        f.write_text(json.dumps(payload))
        env = {**os.environ, "PILOT_OUT": tmp}
        subprocess.run([sys.executable, str(ROOT / "scripts" / "pilot_responses.py"), str(f)], check=True, env=env)
        people = list(_csv.DictReader(open(Path(tmp) / "respondents.csv")))
        rows = list(_csv.DictReader(open(Path(tmp) / "answers_long.csv")))
    assert len(people) == 1 and float(people[0]["complete"]) > 0.8
    assert len(rows) == len(S["ans"])
    assert people[0]["qc_failed"] in {"0", "1", "2", "3"}


def test_resume(built):
    with pw.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.route("**/fonts.g*/**", lambda r: r.abort())
        page.goto(built)
        page.click('[data-mode="pilot"]'); page.click("#go"); page.click("#go")
        page.query_selector_all(".opt[data-code]")[0].click() if not page.query_selector(".case") else None
        first = page.evaluate("window.__wys.state().queue[0].id")
        page.reload()
        page.click("#cont")
        assert page.evaluate("window.__wys.state().queue[0].id") == first
        assert page.evaluate("window.__wys.state().phase") == "quiz"
        browser.close()


def test_payload_is_compact(built):
    # a full-mode payload must fit in one Google Sheets cell chunking scheme (< 200 KB)
    bank = json.loads((ROOT / "app" / "dist" / "bank.js").read_text()[len("window.BANK = "):-2])
    n = len(bank["items"]) + sum(len(i.get("cases", [])) for i in bank["items"].values())
    assert n * 80 < 200_000


def test_experiments(built):
    """Torn option appears only in the torn arm, is recorded, and context visibility is recorded."""
    with pw.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.route("**/fonts.g*/**", lambda r: r.abort())
        page.goto(built)
        page.click('[data-mode="full"]'); page.click("#go"); page.click("#go")
        for torn in (True, False):
            page.evaluate(f"""(() => {{ const S = window.__wys.state(), B = window.__wys.bank;
                S.exp.torn = {str(torn).lower()};
                S.pos = S.queue.findIndex(e => e.k === 'item' && B.items[e.id].format === 'tradeoff'); }})()""")
            page.click("#skip"); page.click("#bk")
            assert bool(page.query_selector("[data-torn]")) == torn
            if torn:
                page.click("[data-torn]")
                assert not page.is_disabled("#next")
                a = page.evaluate("(() => { const S = window.__wys.state(); return S.ans[S.queue[S.pos].id]; })()")
                assert a["t"] == 1 and a.get("c") is None
        page.evaluate("""(() => { const S = window.__wys.state(), B = window.__wys.bank;
            S.pos = S.queue.findIndex(e => e.k === 'item' && B.items[e.id].context && !B.items[e.id].show_if); })()""")
        page.click("#skip"); page.click("#bk")
        a = page.evaluate("(() => { const S = window.__wys.state(); return S.ans[S.queue[S.pos].id]; })()")
        assert a["cx"] in (0, 1)
        assert bool(page.query_selector(".context")) == bool(a["cx"])
        browser.close()


def test_share_compare_and_about(built):
    """Share code round-trips, a shared link renders, comparing works, About opens and closes."""
    with pw.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.route("**/fonts.g*/**", lambda r: r.abort())
        page.goto(built)
        errors = walk(page, random.Random(11), "quick")
        sc = page.evaluate("window.__wys.scores()")
        code = page.evaluate("window.__wys.encode(window.__wys.scores())")
        back = page.evaluate(f"window.__wys.decode('{code}')")
        for ax, v in back.items():
            assert abs(v["v"] - sc[ax]["v"]) <= 0.006
        # drill-down opens and lists answers
        page.click("details.axis summary")
        assert page.query_selector("details.axis[open] .drill li")
        # compare with a made-up friend
        friend = {k: {"v": -v["v"], "n": 3} for k, v in sc.items()}
        fcode = page.evaluate(f"window.__wys.encode({json.dumps(friend)})")
        page.fill("#cmpin", "https://example.com/?r=" + fcode)
        page.click("#cmpgo")
        assert page.query_selector(".dot.other")
        page.fill("#cmpin", "garbage") if page.query_selector("#cmpin") else None
        # about page
        page.click("#nav-about")
        assert "How this quiz works" in page.inner_text("h1")
        page.click("#back")
        assert page.query_selector(".hero-result")
        # theme toggle sets an explicit theme
        page.click("#nav-theme")
        assert page.evaluate("document.documentElement.getAttribute('data-theme')") in ("dark", "light")
        # shared view through a ?r= link (same origin, so it can compare with the saved result)
        page.goto(built + "?r=" + fcode)
        assert "Where they stand" in page.inner_text("h1")
        page.click("#cmp")
        assert page.query_selector(".dot.other")
        page.click("#home")
        assert page.query_selector(".hero-result") or page.query_selector(".hero")
        browser.close()
    assert errors == []
