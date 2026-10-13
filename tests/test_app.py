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


def wait_moved(page, pos):
    page.wait_for_function(f"(() => {{ const S = window.__wys.state(); return S.pos !== {pos} || S.phase !== 'quiz'; }})()", timeout=5000)


def walk(page, rng, mode):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.click(f'[data-mode="{mode}"]')     # home: pick length
    page.click("#go")                       # start
    page.click("#go")                       # how to answer -> begin
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
        pos = page.evaluate("window.__wys.state().pos")
        cases = page.query_selector_all(".case")
        if cases:
            for c in cases:
                chips = c.query_selector_all("[data-code]")
                (c.query_selector(".esc") if rng.random() < 0.05 else rng.choice(chips)).click()
            assert not page.is_disabled("#next")
            page.click("#next")
            continue
        r = rng.random()
        if not page.query_selector('[data-esc="1"]'):
            r = 1.0  # attention-check screens have no escape options
        if r < 0.04:
            page.click('[data-esc="1"]')
            page.fill("#nftext", "my own view")
            page.click("#next")
        elif r < 0.07:
            page.click('[data-esc="2"]')         # "I don't know" moves on by itself
            wait_moved(page, pos)
        elif r < 0.09:
            page.click("#skip")
        else:
            rng.choice(page.query_selector_all(".opt[data-code], .opt[data-torn]")).click()
            wait_moved(page, pos)
    # priorities: one screen, pick up to five
    assert page.evaluate("window.__wys.state().phase") == "pri"
    pris = page.query_selector_all(".pri")
    for b in rng.sample(pris, 6):
        if not b.is_disabled():
            b.click()
    page.click("#next")
    assert page.evaluate("window.__wys.state().phase") == "aboutyou"
    page.check('input[name="age_bracket"][value="3"]')
    page.check('input[name="party_id"][value="2"]')
    page.check('input[name="party_lean"][value="1"]')
    page.select_option("#in-state", "15")
    page.click("#go")
    page.click('[data-k="0"]')
    page.click("#go")
    page.wait_for_selector("#panel .block")
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
        # every report tab renders without errors
        for tab in ("matches", "map", "axes", "topics", "answers", "summary"):
            page.click(f'[data-tab="{tab}"]')
            assert page.query_selector("#panel .block, #panel .topic-card"), tab
        page.click('[data-tab="matches"]')
        n_profiles = len(page.query_selector_all(".profiles li"))
        page.click('[data-tab="axes"]')
        n_axes = len(page.query_selector_all(".axis-card"))
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
    assert len(S["pri"]["top"]) == 5 and len(set(S["pri"]["top"])) == 5
    assert S["about"]["party_lean"] == 1 and S["about"]["state"] == 15
    # one display direction per person, repeats included
    assert len({a["d"] for a in S["ans"].values() if a.get("d") is not None}) == 1
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
        first = page.evaluate("window.__wys.state().queue[0].id")
        if not page.query_selector(".case"):
            page.query_selector_all(".opt[data-code]")[0].click()
            wait_moved(page, 0)
        page.reload()
        page.click("#cont")
        assert page.evaluate("window.__wys.state().queue[0].id") == first
        assert page.evaluate("window.__wys.state().phase") == "quiz"
        assert page.evaluate("window.__wys.state().ans")
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
            page.evaluate("window.__wys.render()")
            assert bool(page.query_selector("[data-torn]")) == torn
            if torn:
                k = page.evaluate("window.__wys.state().queue[window.__wys.state().pos].id")
                page.click("[data-torn]")
                a = page.evaluate(f"window.__wys.state().ans['{k}']")
                assert a["t"] == 1 and a.get("c") is None
        page.evaluate("""(() => { const S = window.__wys.state(), B = window.__wys.bank;
            S.pos = S.queue.findIndex(e => e.k === 'item' && B.items[e.id].context && !B.items[e.id].show_if); })()""")
        page.evaluate("window.__wys.render()")
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
        # axis cards open to bands, the group strip and the answers that moved it
        page.click('[data-tab="axes"]')
        page.click(".axis-card summary")
        assert page.query_selector(".axis-card[open] .drill li")
        assert page.query_selector(".axis-card[open] .ladder li.here")
        assert page.query_selector(".axis-card[open] .strip .tick")
        # matches open to a head-to-head comparison
        page.click('[data-tab="matches"]')
        page.click(".profiles details summary")
        assert len(page.query_selector_all(".profiles details[open] .h2h li")) >= 6
        # the map can plot any two axes
        page.click('[data-tab="map"]')
        avail = page.eval_on_selector_all("#mapx option:not([disabled])", "os => os.map(o => o.value).filter(v => v.length > 4)")
        page.select_option("#mapx", avail[0]); page.select_option("#mapy", avail[1])
        names = page.evaluate(f"[window.__wys.bank.axes.families.flatMap(f => f.axes).find(a => a.id === '{avail[0]}').name]")
        assert names[0] in page.inner_text(".map-notes")
        page.click('[data-tab="summary"]')
        # compare with a made-up friend
        friend = {k: {"v": -v["v"], "n": 3} for k, v in sc.items()}
        fcode = page.evaluate(f"window.__wys.encode({json.dumps(friend)})")
        page.fill("#cmpin", "https://example.com/?r=" + fcode)
        page.click("#cmpgo")
        assert page.query_selector(".dot.other")
        page.fill("#cmpin", "garbage") if page.query_selector("#cmpin") else None
        # explore: a group page and an axis page
        page.click("#nav-explore")
        page.click('[data-ex-group="pres_fdr"]')
        assert "Roosevelt" in page.inner_text("h1")
        page.click('[data-ex="axes"]'); page.click('[data-ex-axis="IMMIG"]')
        assert "Immigration" in page.inner_text("h1")
        assert len(page.query_selector_all(".axis-rank li")) > 50
        page.click("#ex-back")
        assert page.query_selector(".res-head")
        # about page
        page.click("#nav-about")
        assert "How it works" in page.inner_text("h1")
        page.click("#back")
        assert page.query_selector(".res-head")
        # theme toggle sets an explicit theme
        page.click("#nav-theme")
        assert page.evaluate("document.documentElement.getAttribute('data-theme')") in ("dark", "light")
        # shared view through a ?r= link (same origin, so it can compare with the saved result)
        page.goto(built + "?r=" + fcode)
        assert "Their closest match" in page.inner_text("h1")
        page.click("#cmp")
        assert page.query_selector(".dot.other")
        page.click("#home")
        assert page.query_selector(".res-head") or page.query_selector(".hero")
        browser.close()
    assert errors == []
