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
    page.click("#go")                       # welcome
    page.check("#consent")
    page.click("#go")                       # privacy
    page.click(f'[data-mode="{mode}"]')
    page.click("#go")                       # mode
    page.click("#go")                       # how answers work -> begin
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
    assert page.evaluate("window.__wys.state().phase") == "about"
    page.check('input[name="age_bracket"][value="3"]')
    page.check('input[name="party_id"][value="2"]')
    page.check('input[name="party_lean"][value="1"]')
    page.select_option("#in-state", "15")
    page.click("#go")
    page.click('[data-k="0"]')
    page.click("#go")
    page.wait_for_selector(".map")
    return errors


@pytest.mark.parametrize("mode,seed", [("pilot", 1), ("pilot", 2), ("full", 3)])
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
        browser.close()
    assert errors == []
    assert S["done"] and S["submitted"] == "local"
    items = bank["items"]
    shown = {e["id"] for e in S["queue"] if e["k"] == "item"}
    if mode == "pilot":
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
        page.click("#go"); page.check("#consent"); page.click("#go")
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
