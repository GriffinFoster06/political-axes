/* Where You Stand: pilot quiz app.
 * Plain browser JavaScript, no build step or dependencies. Reads window.BANK
 * (scripts/build_app.py) and window.QUIZ_CONFIG (config.js).
 * Answer codes always follow the bank's code order; only the on-screen order
 * is randomized, and it is recorded with every answer.
 */
(function () {
  "use strict";
  var B = window.BANK;
  var CFG = window.QUIZ_CONFIG || {};
  var KEY = "wys_pilot_v1";
  var BREAK_MS = 12 * 60 * 1000;
  var SCREEN_CAP_MS = 5 * 60 * 1000;
  var screen = document.getElementById("screen");
  var metaEl = document.getElementById("meta");
  var progEl = document.getElementById("progress");
  var S = null;
  var t0 = 0;

  // ---------- utilities ----------
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hash(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function shuffle(arr, rnd) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function randId(n) {
    var abc = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789", out = "", buf = new Uint32Array(n);
    try { crypto.getRandomValues(buf); } catch (e) { for (var k = 0; k < n; k++) buf[k] = Math.floor(Math.random() * 4294967296); }
    for (var i = 0; i < n; i++) out += abc[buf[i] % abc.length];
    return out;
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage unavailable: keep going in memory */ } }
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; } }
  function clearSaved() { try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ } }
  function el(html) { var d = document.createElement("div"); d.innerHTML = html; return d; }
  function show(html) {
    screen.innerHTML = html;
    window.scrollTo(0, 0);
    try { screen.focus({ preventScroll: true }); } catch (e) { screen.focus(); }
    t0 = performance.now();
  }
  function spend() {
    var dt = Math.min(performance.now() - t0, SCREEN_CAP_MS);
    S.activeMs += dt;
    t0 = performance.now();
    return Math.round(dt);
  }
  function domainName(id) {
    for (var i = 0; i < B.domains.length; i++) if (B.domains[i].id === id) return B.domains[i].name;
    return "";
  }

  // ---------- state ----------
  function newState() {
    return {
      v: 1, bank: B.version, rid: randId(12), code: randId(8), started: new Date().toISOString().slice(0, 10),
      phase: "intro", introStep: 0, mode: null, form: null, queue: [], pos: 0,
      ans: {}, qc: {}, pri: {}, priOrder: [], priPos: 0, about: {}, honesty: null,
      activeMs: 0, lastBreak: 0, consent: false, minor: false, done: false, submitted: null,
    };
  }

  function buildQueue() {
    var rnd = mulberry32(hash(S.rid + "order"));
    var ids = {};
    if (S.mode === "pilot") {
      var d = B.design;
      S.form = d.forms[Math.floor(rnd() * d.forms.length)];
      d.link.forEach(function (i) { ids[i] = 1; });
      S.form.forEach(function (b) { d.blocks[b].forEach(function (i) { ids[i] = 1; }); });
    } else {
      Object.keys(B.items).forEach(function (i) { ids[i] = 1; });
    }
    var q = [];
    shuffle(B.domains.map(function (x) { return x.id; }), rnd).forEach(function (dom) {
      var seen = {}, late = [];
      B.order[dom].forEach(function (i) {
        if (!ids[i]) return;
        var it = B.items[i];
        if (it.pair && seen[it.pair]) late.push(i); else q.push({ k: "item", id: i, d: dom });
        seen[i] = 1;
      });
      late.forEach(function (i) { q.push({ k: "item", id: i, d: dom }); });
    });
    // attention checks in the middle third, never between a question and its follow-up
    var n = q.length;
    var qcs = B.quality.instructed_responses.items.slice();
    var spots = qcs.map(function () { return Math.floor(n / 3 + rnd() * (n / 3)); }).sort(function (a, b) { return b - a; });
    spots.forEach(function (idx, k) {
      while (idx < q.length && isFollowup(q, idx)) idx++;
      q.splice(idx, 0, { k: "qc", id: qcs[k].id });
    });
    B.quality.repeated_items.ids.forEach(function (i) { if (ids[i]) q.push({ k: "repeat", id: i }); });
    S.queue = q;
    S.pos = 0;
    S.priOrder = shuffle(B.priorities.sets.map(function (_, k) { return k; }), rnd);
  }
  function isFollowup(q, idx) {
    var e = q[idx];
    if (!e || e.k !== "item") return false;
    var it = B.items[e.id];
    if (it.show_if) return true;
    var prev = q[idx - 1];
    return !!(prev && prev.k === "item" && B.items[prev.id].followup === e.id);
  }
  var PARENT = {};
  Object.keys(B.items).forEach(function (i) { var f = B.items[i].followup; if (f) PARENT[f] = i; });
  function visible(e) {
    if (e.k === "repeat") { var a = S.ans[e.id]; return !!(a && a.c != null); }
    if (e.k !== "item") return true;
    var it = B.items[e.id];
    if (!it.show_if) {
      // a follow-up that refers back to an earlier answer needs that answer
      var par = PARENT[e.id];
      return !par || !!(S.ans[par] && S.ans[par].c != null);
    }
    var parent = Object.keys(it.show_if)[0];
    var pa = S.ans[parent];
    return !!(pa && pa.c != null && it.show_if[parent].indexOf(pa.c) >= 0);
  }

  // ---------- navigation ----------
  function render() {
    updateMeta();
    if (S.phase === "intro") return renderIntro();
    if (S.phase === "quiz") {
      while (S.pos < S.queue.length && !visible(S.queue[S.pos])) S.pos++;
      if (S.pos >= S.queue.length) { S.phase = "pri"; S.priPos = 0; save(); return render(); }
      var e = S.queue[S.pos];
      return e.k === "qc" ? renderQC(e) : renderItem(e);
    }
    if (S.phase === "break") return renderBreak();
    if (S.phase === "pri") return renderPriorities();
    if (S.phase === "about") return renderAbout();
    if (S.phase === "honesty") return renderHonesty();
    if (S.phase === "done") return renderResults();
  }
  function next() {
    S.pos++;
    while (S.pos < S.queue.length && !visible(S.queue[S.pos])) S.pos++;
    if (S.pos < S.queue.length && S.activeMs - S.lastBreak > BREAK_MS) { S.lastBreak = S.activeMs; S.phase = "break"; }
    save(); render();
  }
  function back() {
    var p = S.pos - 1;
    while (p >= 0 && !visible(S.queue[p])) p--;
    if (p >= 0) { S.pos = p; save(); render(); }
  }
  function updateMeta() {
    var frac = 0, label = "";
    if (S.phase === "quiz" || S.phase === "break") {
      frac = 0.04 + 0.82 * (S.pos / Math.max(1, S.queue.length));
      var answered = Object.keys(S.ans).length;
      label = Math.round(100 * S.pos / Math.max(1, S.queue.length)) + "% · " + answered + " answers";
    } else if (S.phase === "pri") { frac = 0.86 + 0.08 * (S.priPos / B.priorities.sets.length); label = "Priorities " + (S.priPos + 1) + " of " + B.priorities.sets.length; }
    else if (S.phase === "about" || S.phase === "honesty") { frac = 0.96; label = "Almost done"; }
    else if (S.phase === "done") { frac = 1; label = "Finished"; }
    else { frac = 0.01 + 0.03 * S.introStep / 4; }
    progEl.style.width = (100 * frac).toFixed(1) + "%";
    metaEl.textContent = label;
  }

  // ---------- intro ----------
  function introScreen(id) {
    var s = B.intro.screens.filter(function (x) { return x.id === id; })[0];
    return s || {};
  }
  function renderIntro() {
    var step = S.introStep;
    if (step === 0) {
      var w = introScreen("welcome");
      show('<div class="eyebrow"><span>US politics</span><span>25 topics</span><span>No party labels</span></div>' +
        "<h1>" + esc(w.title) + "</h1>" +
        '<p class="lede">' + esc(w.text) + "</p>" +
        '<div class="nav"><span></span><button class="btn" id="go">Start</button></div>');
      return bind("#go", function () { S.introStep = 1; save(); render(); });
    }
    if (step === 1) {
      var p = introScreen("privacy");
      show("<h2>" + esc(p.title) + "</h2><p>" + esc(p.text) + "</p>" +
        '<label class="radio"><input type="checkbox" id="consent"' + (S.consent ? " checked" : "") + "> <span>" + esc(p.consent) + "</span></label>" +
        '<div class="nav"><button class="link" id="bk">Back</button><button class="btn" id="go"' + (S.consent ? "" : " disabled") + ">Continue</button></div>");
      document.getElementById("consent").addEventListener("change", function (ev) {
        S.consent = ev.target.checked; document.getElementById("go").disabled = !S.consent;
      });
      bind("#bk", function () { S.introStep = 0; render(); });
      return bind("#go", function () { S.introStep = 2; save(); render(); });
    }
    if (step === 2) {
      var opts = [
        { id: "pilot", title: "Pilot version", time: "about 45 minutes", text: "A balanced share of the questions. Everyone gets a different share, so together the answers cover every question. This is the version for the pilot study." },
      ];
      if (CFG.allowFullMode !== false) opts.push({ id: "full", title: "Full map", time: "about 75 minutes", text: "Every question in every topic. You can stop and come back any time on this device." });
      var html = '<h2>Choose a length</h2><div class="mode">';
      opts.forEach(function (o) {
        html += '<button class="opt" data-mode="' + o.id + '" aria-pressed="' + (S.mode === o.id) + '"><b>' + esc(o.title) + "</b> <span class=\"mono\">" + esc(o.time) + "</span><small>" + esc(o.text) + "</small></button>";
      });
      html += '<div class="opt" aria-disabled="true" style="opacity:.55;cursor:default"><b>Precision mode</b> <span class="mono">about 30–45 minutes</span><small>Picks the most informative questions for you. Available once the pilot has calibrated the questions.</small></div>';
      html += '</div><div class="nav"><button class="link" id="bk">Back</button><button class="btn" id="go"' + (S.mode ? "" : " disabled") + ">Continue</button></div>";
      show(html);
      screen.querySelectorAll("[data-mode]").forEach(function (b) {
        b.addEventListener("click", function () {
          S.mode = b.getAttribute("data-mode");
          screen.querySelectorAll("[data-mode]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
          document.getElementById("go").disabled = false;
        });
      });
      bind("#bk", function () { S.introStep = 1; render(); });
      return bind("#go", function () { S.introStep = 3; save(); render(); });
    }
    if (step === 3) {
      var how = introScreen("how_answers_work"), tr = introScreen("tradeoff_example"), br = introScreen("breaks");
      show("<h2>" + esc(how.title) + "</h2><p>" + esc(how.text) + "</p><h2>" + esc(tr.title) + "</h2><p>" + esc(tr.text) + "</p><p>" + esc(br.text) + "</p>" +
        '<div class="notice">Your code is <span class="code">' + esc(S.code) + "</span><br>Write it down if you want to come back on another device later or take the quiz again for the follow-up study. It isn't linked to your name.</div>" +
        '<div class="nav"><button class="link" id="bk">Back</button><button class="btn" id="go">Begin</button></div>');
      bind("#bk", function () { S.introStep = 2; render(); });
      return bind("#go", function () {
        if (!S.queue.length || S.queueMode !== S.mode) { buildQueue(); S.queueMode = S.mode; }
        S.phase = "quiz"; spend(); S.lastBreak = S.activeMs; save(); render();
      });
    }
  }
  function bind(sel, fn) { var b = screen.querySelector(sel); if (b) b.addEventListener("click", fn); }

  // ---------- question text with tappable definitions ----------
  function richFactory(it) {
    var defs = (it.definitions || []).slice(), used = {};
    return function (text) {
      var out = esc(text);
      defs.forEach(function (d, k) {
        if (used[k]) return;
        var t = esc(d.term), i = out.toLowerCase().indexOf(t.toLowerCase());
        if (i < 0) return;
        used[k] = 1;
        out = out.slice(0, i) + '<button type="button" class="term" data-def="' + k + '">' + out.slice(i, i + t.length) + "</button>" + out.slice(i + t.length);
      });
      return out;
    };
  }
  function wireDefs(it, a) {
    var box = screen.querySelector("#defs");
    screen.querySelectorAll(".term").forEach(function (b) {
      b.addEventListener("click", function (ev) {
        ev.stopPropagation();
        var k = +b.getAttribute("data-def"), d = it.definitions[k];
        var id = "def-" + k, ex = document.getElementById(id);
        if (ex) { ex.remove(); return; }
        var div = el('<div class="def" id="' + id + '"><b>' + esc(d.term) + "</b>" + esc(d.text) + "</div>").firstChild;
        box.appendChild(div);
        a.df = a.df || [];
        if (a.df.indexOf(d.term) < 0) a.df.push(d.term);
        save();
      });
    });
  }

  // ---------- one question ----------
  var FIRMNESS = ["Firm", "Fairly firm", "It really depends on the details"];
  var ESCAPES = [null, "None of these fit my view", "I don't know enough about this to say"];

  function displayDir(it, isRepeat) {
    var d = hash(S.rid + "|" + it.id) % 2;
    if (isRepeat) { var first = S.ans[it.id]; d = 1 - (first && first.d != null ? first.d : d); }
    return d;
  }

  function header(it, extra) {
    var dom = it.domain ? domainName(it.domain) : "";
    return '<div class="eyebrow"><span>' + esc(dom) + "</span>" + (extra ? "<span>" + esc(extra) + "</span>" : "") + "</div>";
  }

  function renderItem(e) {
    var it = B.items[e.id], isRep = e.k === "repeat";
    var key = isRep ? e.id + "#r" : e.id;
    var a = S.ans[key] || (S.ans[key] = {});
    var dir = displayDir(it, isRep);
    a.d = dir;
    var rich = richFactory(it);
    var html = header(it, isRep ? "One more look" : "");
    if (isRep) html += '<p class="scope">You saw this question earlier. Please answer it again as you see it now.</p>';
    if (it.context) html += '<div class="context">' + rich(it.context) + "</div>";
    html += '<p class="stem">' + rich(it.stem) + "</p>";
    html += '<p class="scope">' + rich(it.scope) + "</p>";
    html += '<div id="defs"></div>';
    if (it.format === "exceptions") html += casesHtml(it, dir, rich);
    else if (it.format === "tradeoff") html += tradeoffHtml(it, dir, rich);
    else html += optionsHtml(it, dir, rich);
    if (it.format !== "exceptions") {
      html += '<div class="escapes">' + ESCAPES.slice(1).map(function (t, k) {
        return '<button type="button" class="esc" data-esc="' + (k + 1) + '" aria-pressed="' + (a.e === k + 1) + '">' + esc(t) + "</button>";
      }).join("") + "</div>";
      html += '<div id="nf" ' + (a.e === 1 ? "" : "hidden") + '><label for="nftext" class="scope">Optional: what would your answer be?</label><textarea id="nftext" maxlength="500">' + esc(a.x || "") + "</textarea></div>";
      if (it.format === "position" || it.format === "tradeoff") {
        html += '<div class="firm" id="firm" ' + (a.c != null ? "" : "hidden") + "><span>How settled is this view?</span>" +
          FIRMNESS.map(function (f, k) { return '<button type="button" class="chip" data-firm="' + k + '" aria-pressed="' + (a.f === k) + '">' + esc(f) + "</button>"; }).join("") + "</div>";
      }
    }
    html += navHtml(answered(it, a));
    show(html);
    wireDefs(it, a);
    if (it.format === "exceptions") wireCases(it);
    else wireOptions(it, a);
    wireNav(function () { a.ms = (a.ms || 0) + spend(); });
  }

  function optionsHtml(it, dir, rich) {
    var a = S.ans[it.id] || {};
    var codes = it.options.map(function (_, k) { return k; });
    if (dir) codes.reverse();
    return '<div class="options" role="group">' + codes.map(function (c, p) {
      var meaning = it.point_meanings ? "<small>" + esc(it.point_meanings[c]) + "</small>" : "";
      return '<button type="button" class="opt" data-code="' + c + '" data-pos="' + p + '">' + rich(it.options[c]) + meaning + "</button>";
    }).join("") + "</div>";
  }
  function tradeoffHtml(it, swap, rich) {
    var A = it.sides[0], Bs = it.sides[1];
    var left = swap ? Bs : A, right = swap ? A : Bs;
    var codes = swap ? [3, 2, 1, 0] : [0, 1, 2, 3];
    var labels = ["Clearly " + left.label, "Lean " + left.label, "Lean " + right.label, "Clearly " + right.label];
    return '<div class="sides"><div class="side"><b>' + esc(left.label) + "</b><span>" + rich(left.text) + '</span></div><div class="side"><b>' + esc(right.label) + "</b><span>" + rich(right.text) + "</span></div></div>" +
      '<div class="scale options" role="group">' + codes.map(function (c, p) {
        return '<button type="button" class="opt" data-code="' + c + '" data-pos="' + p + '">' + esc(labels[p]) + "</button>";
      }).join("") + "</div>";
  }
  function wireOptions(it, a) {
    var key = Object.keys(S.ans).filter(function (k) { return S.ans[k] === a; })[0];
    function paint() {
      screen.querySelectorAll(".opt[data-code]").forEach(function (b) { b.setAttribute("aria-pressed", String(a.c != null && +b.getAttribute("data-code") === a.c)); });
      screen.querySelectorAll(".esc").forEach(function (b) { b.setAttribute("aria-pressed", String(a.e === +b.getAttribute("data-esc"))); });
      var nf = document.getElementById("nf"); if (nf) nf.hidden = a.e !== 1;
      var fm = document.getElementById("firm"); if (fm) fm.hidden = a.c == null;
      screen.querySelectorAll("[data-firm]").forEach(function (b) { b.setAttribute("aria-pressed", String(a.f === +b.getAttribute("data-firm"))); });
      var nx = document.getElementById("next"); if (nx) nx.disabled = !answered(it, a);
    }
    paint();
    screen.querySelectorAll(".opt[data-code]").forEach(function (b) {
      b.addEventListener("click", function () {
        a.c = +b.getAttribute("data-code"); a.p = +b.getAttribute("data-pos"); a.e = null;
        if (it.format === "tradeoff") a.s = a.d;
        save(); paint();
      });
    });
    screen.querySelectorAll(".esc").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = +b.getAttribute("data-esc");
        a.e = a.e === v ? null : v; a.c = null; a.p = null; a.f = null;
        save(); paint();
      });
    });
    screen.querySelectorAll("[data-firm]").forEach(function (b) {
      b.addEventListener("click", function () { var v = +b.getAttribute("data-firm"); a.f = a.f === v ? null : v; save(); paint(); });
    });
    var ta = document.getElementById("nftext");
    if (ta) ta.addEventListener("input", function () { a.x = ta.value.slice(0, 500); save(); });
    return key;
  }

  function casesHtml(it, dir, rich) {
    var codes = it.options.map(function (_, k) { return k; });
    if (dir) codes.reverse();
    return '<div class="cases">' + it.cases.map(function (c) {
      return '<div class="case" data-case="' + esc(c.id) + '"><div class="case-text">' + rich(c.text) + '</div><div class="case-opts">' +
        codes.map(function (code, p) { return '<button type="button" class="chip" data-code="' + code + '" data-pos="' + p + '">' + esc(it.options[code]) + "</button>"; }).join("") +
        '<button type="button" class="esc" data-esc="2">Don\'t know</button></div></div>';
    }).join("") + "</div>";
  }
  function wireCases(it) {
    var dir = displayDir(it, false);
    function paint() {
      screen.querySelectorAll(".case").forEach(function (row) {
        var ca = S.ans[row.getAttribute("data-case")] || {};
        row.querySelectorAll("[data-code]").forEach(function (b) { b.setAttribute("aria-pressed", String(ca.c != null && +b.getAttribute("data-code") === ca.c)); });
        row.querySelectorAll(".esc").forEach(function (b) { b.setAttribute("aria-pressed", String(ca.e === 2)); });
      });
      var nx = document.getElementById("next"); if (nx) nx.disabled = !answered(it, null);
    }
    screen.querySelectorAll(".case").forEach(function (row) {
      var cid = row.getAttribute("data-case");
      row.querySelectorAll("[data-code]").forEach(function (b) {
        b.addEventListener("click", function () {
          var ca = S.ans[cid] || (S.ans[cid] = {});
          ca.c = +b.getAttribute("data-code"); ca.p = +b.getAttribute("data-pos"); ca.e = null; ca.d = dir;
          save(); paint();
        });
      });
      row.querySelector(".esc").addEventListener("click", function () {
        var ca = S.ans[cid] || (S.ans[cid] = {});
        ca.e = ca.e === 2 ? null : 2; ca.c = null; ca.p = null; ca.d = dir;
        save(); paint();
      });
    });
    paint();
  }
  function answered(it, a) {
    if (it.format === "exceptions") {
      return it.cases.every(function (c) { var ca = S.ans[c.id]; return ca && (ca.c != null || ca.e); });
    }
    return !!(a && (a.c != null || a.e));
  }
  function navHtml(ok) {
    return '<div class="nav"><button class="link" id="bk"' + (S.pos === 0 ? " hidden" : "") + '>Back</button>' +
      '<span><button class="link" id="skip">Skip</button> &nbsp; <button class="btn" id="next"' + (ok ? "" : " disabled") + ">Next</button></span></div>";
  }
  function wireNav(onLeave) {
    bind("#next", function () { onLeave(); next(); });
    bind("#skip", function () { onLeave(); next(); });
    bind("#bk", function () { onLeave(); back(); });
  }

  // ---------- attention checks ----------
  function renderQC(e) {
    var q = B.quality.instructed_responses.items.filter(function (x) { return x.id === e.id; })[0];
    var rec = S.qc[q.id] || (S.qc[q.id] = {});
    var fake = { id: q.id, format: q.format, options: q.options, sides: q.sides, stem: q.stem, scope: q.scope, domain: S.queue[Math.max(0, S.pos - 1)].d };
    var dir = displayDir(fake, false);
    var html = header(fake, "") + '<p class="stem">' + esc(q.stem) + '</p><p class="scope">' + esc(q.scope) + "</p>" +
      (q.format === "tradeoff" ? tradeoffHtml(fake, dir, esc) : optionsHtml(fake, dir, esc)) +
      navHtml(rec.c != null);
    show(html);
    screen.querySelectorAll(".opt[data-code]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(rec.c != null && +b.getAttribute("data-code") === rec.c));
      b.addEventListener("click", function () {
        rec.c = +b.getAttribute("data-code"); rec.ok = rec.c === q.correct;
        screen.querySelectorAll(".opt[data-code]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        document.getElementById("next").disabled = false; save();
      });
    });
    wireNav(function () { rec.ms = (rec.ms || 0) + spend(); });
  }

  // ---------- break ----------
  function renderBreak() {
    var pct = Math.round(100 * S.pos / Math.max(1, S.queue.length));
    var mins = Math.round(S.activeMs / 60000);
    show('<div class="eyebrow"><span>Short break</span></div><h2>You\'re about ' + pct + "% of the way through the questions.</h2>" +
      "<p>You've spent about " + mins + " minutes so far. Stretch, grab a drink, or keep going. Your answers are saved on this device, so you can also close the page and come back later.</p>" +
      '<div class="nav"><span></span><button class="btn" id="go">Keep going</button></div>');
    bind("#go", function () { spend(); S.phase = "quiz"; save(); render(); });
  }

  // ---------- priorities (best-worst) ----------
  function renderPriorities() {
    var P = B.priorities, k = S.priOrder[S.priPos], set = P.sets[k];
    var rec = S.pri[k] || (S.pri[k] = {});
    if (!rec.o) rec.o = shuffle(set, mulberry32(hash(S.rid + "pri" + k)));
    var html = '<div class="eyebrow"><span>What matters most to you</span><span class="mono">' + (S.priPos + 1) + " of " + P.sets.length + "</span></div>" +
      '<p class="stem">' + esc(P.stem) + '</p><p class="scope">' + esc(P.scope) + "</p>" +
      '<table class="pmat"><thead><tr><th class="c">Most</th><th></th><th class="c">Least</th></tr></thead><tbody>' +
      rec.o.map(function (d) {
        return '<tr><td class="c"><input type="radio" name="best" id="b-' + d + '" value="' + d + '"' + (rec.b === d ? " checked" : "") + ' aria-label="Most: ' + esc(P.labels[d]) + '"></td>' +
          '<td class="topic"><label for="b-' + d + '">' + esc(P.labels[d]) + "</label></td>" +
          '<td class="c"><input type="radio" name="worst" id="w-' + d + '" value="' + d + '"' + (rec.w === d ? " checked" : "") + ' aria-label="Least: ' + esc(P.labels[d]) + '"></td></tr>';
      }).join("") + "</tbody></table>" +
      '<div class="nav"><button class="link" id="bk"' + (S.priPos === 0 ? " hidden" : "") + '>Back</button><span><button class="link" id="skip">Skip</button> &nbsp; <button class="btn" id="next"' + (rec.b && rec.w ? "" : " disabled") + ">Next</button></span></div>";
    show(html);
    function upd(name, val) {
      if (name === "best") { rec.b = val; if (rec.w === val) { rec.w = null; document.getElementById("w-" + val).checked = false; } }
      else { rec.w = val; if (rec.b === val) { rec.b = null; document.getElementById("b-" + val).checked = false; } }
      document.getElementById("next").disabled = !(rec.b && rec.w);
      save();
    }
    screen.querySelectorAll("input[type=radio]").forEach(function (r) { r.addEventListener("change", function () { upd(r.name, r.value); }); });
    function leave() { rec.ms = (rec.ms || 0) + spend(); }
    function adv() {
      leave(); S.priPos++;
      if (S.priPos >= P.sets.length) S.phase = "about";
      save(); render();
    }
    bind("#next", adv); bind("#skip", adv);
    bind("#bk", function () { leave(); S.priPos = Math.max(0, S.priPos - 1); save(); render(); });
  }

  // ---------- about you ----------
  var STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "A US territory", "I live outside the US"];

  function aboutItems() {
    var out = [];
    B.about.items.forEach(function (q) {
      if (q.placement) return; // asked on the results page
      out.push(q);
      if (q.followups) Object.keys(q.followups).forEach(function (fid) {
        var f = q.followups[fid];
        out.push({ id: fid, stem: f.stem, options: f.options, show_if: f.show_if });
      });
    });
    return out;
  }
  function aboutVisible(q) {
    if (!q.show_if) return true;
    var p = Object.keys(q.show_if)[0], v = S.about[p];
    return typeof v === "number" && q.show_if[p].indexOf(v) >= 0;
  }
  function renderAbout() {
    var qs = aboutItems();
    var html = '<div class="eyebrow"><span>About you</span><span>Optional</span></div><h2>A few questions about you</h2><p>' + esc(B.about.intro_text) + "</p><div class=\"form\">";
    qs.forEach(function (q) {
      html += '<fieldset id="fs-' + q.id + '"' + (aboutVisible(q) ? "" : " hidden") + "><legend>" + esc(q.stem) + "</legend>";
      if (q.id === "state") {
        html += '<select id="in-state"><option value="">Choose…</option>' + STATES.map(function (s, k) { return '<option value="' + k + '"' + (S.about.state === k ? " selected" : "") + ">" + esc(s) + "</option>"; }).join("") + "</select>";
      } else {
        var type = q.multi_select ? "checkbox" : "radio";
        q.options.forEach(function (o, k) {
          var v = S.about[q.id];
          var checked = q.multi_select ? (Array.isArray(v) && v.indexOf(k) >= 0) : v === k;
          html += '<label class="radio"><input type="' + type + '" name="' + q.id + '" value="' + k + '"' + (checked ? " checked" : "") + "> <span>" + esc(o) + "</span></label>";
        });
      }
      html += "</fieldset>";
    });
    html += '</div><div class="nav"><span></span><button class="btn" id="go">Continue</button></div>';
    show(html);
    function refresh() { qs.forEach(function (q) { var fs = document.getElementById("fs-" + q.id); if (fs) fs.hidden = !aboutVisible(q); }); }
    screen.querySelectorAll("fieldset input").forEach(function (inp) {
      inp.addEventListener("change", function () {
        var id = inp.name, k = +inp.value;
        if (inp.type === "checkbox") {
          var arr = Array.isArray(S.about[id]) ? S.about[id] : [];
          if (inp.checked) { if (arr.indexOf(k) < 0) arr.push(k); } else arr = arr.filter(function (x) { return x !== k; });
          S.about[id] = arr;
        } else S.about[id] = k;
        refresh(); save();
      });
    });
    var st = document.getElementById("in-state");
    if (st) st.addEventListener("change", function () { S.about.state = st.value === "" ? null : +st.value; save(); });
    bind("#go", function () {
      spend();
      var ageQ = B.about.items.filter(function (q) { return q.id === "age_bracket"; })[0];
      S.minor = S.about.age_bracket === 0 && ageQ.options[0] === "Under 18";
      S.phase = "honesty"; save(); render();
    });
  }

  function renderHonesty() {
    var q = B.quality.self_report;
    show('<div class="eyebrow"><span>Last question</span></div><p class="stem">' + esc(q.stem) + '</p><p class="scope">' + esc(q.scope) + '</p><div class="options">' +
      q.options.map(function (o, k) { return '<button type="button" class="opt" data-k="' + k + '" aria-pressed="' + (S.honesty === k) + '">' + esc(o) + "</button>"; }).join("") +
      '</div><div class="nav"><span></span><button class="btn" id="go"' + (S.honesty == null ? " disabled" : "") + ">Finish</button></div>");
    screen.querySelectorAll("[data-k]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.honesty = +b.getAttribute("data-k");
        screen.querySelectorAll("[data-k]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        document.getElementById("go").disabled = false; save();
      });
    });
    bind("#go", function () { spend(); finish(); });
  }

  // ---------- finish and submit ----------
  function payload() {
    return {
      v: S.v, bank: S.bank, rid: S.rid, code: S.code, mode: S.mode, form: S.form, started: S.started,
      active_s: Math.round(S.activeMs / 1000),
      order: S.queue.map(function (e) { return e.k === "qc" ? "qc:" + e.id : e.k === "repeat" ? e.id + "#r" : e.id; }),
      ans: S.ans, qc: S.qc, pri: S.pri, about: S.about, honesty: S.honesty,
      result_fit: S.resultFit == null ? null : S.resultFit, result_fit_text: S.resultFitText || null,
    };
  }
  function submit() {
    if (S.minor) { S.submitted = "minor"; save(); return Promise.resolve(); }
    if (!CFG.submitUrl) { S.submitted = "local"; save(); return Promise.resolve(); }
    S.submitted = "sending";
    return fetch(CFG.submitUrl, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(payload()) })
      .then(function () { S.submitted = "sent"; save(); })
      .catch(function () { S.submitted = "failed"; save(); });
  }
  function finish() {
    S.phase = "done"; S.done = true; save();
    render();
    submit().then(function () { if (S.phase === "done") render(); });
  }

  // ---------- results ----------
  function answerText(it, a) {
    if (!a) return null;
    if (a.e === 1) return "None of these fit my view" + (a.x ? ': "' + a.x + '"' : "");
    if (a.e === 2) return "I don't know enough to say";
    if (a.c == null) return null;
    if (it.format === "tradeoff") {
      var side = a.c <= 1 ? it.sides[0] : it.sides[1];
      return (a.c === 0 || a.c === 3 ? "Clearly: " : "Leaning: ") + side.label + ". " + side.text;
    }
    return it.options[a.c];
  }
  function priorityRanking() {
    var score = {};
    Object.keys(S.pri).forEach(function (k) {
      var r = S.pri[k];
      if (r.b) score[r.b] = (score[r.b] || 0) + 1;
      if (r.w) score[r.w] = (score[r.w] || 0) - 1;
    });
    return Object.keys(score).sort(function (a, b) { return score[b] - score[a]; }).map(function (d) { return { d: d, s: score[d] }; });
  }
  function renderResults() {
    var status = {
      sent: "Your anonymous answers were sent to the study. Thank you.",
      sending: "Sending your answers…",
      failed: "Your answers couldn't be sent (no connection?). They're still saved on this device; reload this page later to try again, or copy them below.",
      local: "This copy of the quiz isn't connected to a study, so your answers stay on this device. You can copy them below.",
      minor: "Thanks for taking it. Because you're under 18, your answers were not stored for research.",
    }[S.submitted] || "";
    var html = '<div class="eyebrow"><span>Finished</span><span class="mono">code ' + esc(S.code) + "</span></div><h1>Your issue map</h1>" +
      '<p class="lede">These are your positions, topic by topic, in your own answers. Scores on each axis, with comparisons to the country, need the pilot data to calibrate the questions first. Keep your code to look them up once they\'re ready.</p>' +
      '<div class="notice' + (S.submitted === "failed" ? " warn" : "") + '">' + esc(status) + (S.submitted === "failed" ? ' <button class="link" id="retry">Try sending again</button>' : "") + "</div>";
    var rank = priorityRanking();
    if (rank.length) {
      html += "<h2>What matters most to you</h2><ol class=\"rank\">" + rank.slice(0, 5).map(function (r) { return "<li>" + esc(B.priorities.labels[r.d]) + "</li>"; }).join("") + "</ol>";
    }
    html += '<div class="map">';
    B.domains.forEach(function (dm) {
      var rows = "";
      B.order[dm.id].forEach(function (id) {
        var it = B.items[id];
        if (it.format === "exceptions") {
          var parts = it.cases.map(function (c) {
            var ca = S.ans[c.id]; if (!ca || (ca.c == null && !ca.e)) return null;
            return esc(c.text) + ": <b>" + esc(ca.c != null ? it.options[ca.c] : "don't know") + "</b>";
          }).filter(Boolean);
          if (parts.length) rows += "<dt>" + esc(it.stem) + "</dt><dd>" + parts.join("<br>") + "</dd>";
          return;
        }
        var a = S.ans[id], txt = answerText(it, a);
        if (!txt) return;
        rows += "<dt>" + esc(it.stem) + "</dt><dd>" + esc(txt) + (a.f != null ? '<span class="firmtag">' + esc(FIRMNESS[a.f]) + "</span>" : "") + "</dd>";
      });
      if (rows) html += "<section><h3>" + esc(dm.name) + "</h3><dl>" + rows + "</dl></section>";
    });
    html += "</div>";
    var fit = B.about.items.filter(function (q) { return q.id === "result_fit"; })[0];
    if (fit) {
      html += "<h2>" + esc(fit.stem) + '</h2><div class="escapes">' + fit.options.map(function (o, k) {
        return '<button type="button" class="chip" data-fit="' + k + '" aria-pressed="' + (S.resultFit === k) + '">' + esc(o) + "</button>";
      }).join("") + '</div><label for="fittext" class="scope">' + esc(fit.free_text) + '</label><textarea id="fittext" maxlength="800">' + esc(S.resultFitText || "") + "</textarea>";
    }
    html += '<h2>Your answers</h2><p class="scope">A copy of everything you answered, without anything that identifies you.</p>' +
      '<div class="nav" style="justify-content:flex-start"><button class="btn ghost" id="copy">Copy my answers</button>' + (window.claude ? "" : '<button class="btn ghost" id="dl">Download</button>') + '</div>' +
      '<textarea id="raw" readonly hidden></textarea>' +
      '<div class="nav"><span></span><button class="link" id="restart">Start over</button></div><div id="confirm"></div>';
    show(html);
    screen.querySelectorAll("[data-fit]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.resultFit = +b.getAttribute("data-fit");
        screen.querySelectorAll("[data-fit]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        save(); if (S.submitted === "sent" || S.submitted === "failed") sendFeedback();
      });
    });
    var ft = document.getElementById("fittext");
    if (ft) { ft.addEventListener("input", function () { S.resultFitText = ft.value.slice(0, 800); save(); }); ft.addEventListener("change", function () { if (S.submitted === "sent") sendFeedback(); }); }
    bind("#retry", function () { submit().then(render); });
    bind("#copy", function () {
      var txt = JSON.stringify(payload(), null, 1), raw = document.getElementById("raw");
      function fallback() { raw.hidden = false; raw.value = txt; raw.focus(); raw.select(); }
      try {
        navigator.clipboard.writeText(txt).then(function () { document.getElementById("copy").textContent = "Copied"; }, fallback);
      } catch (e) { fallback(); }
    });
    bind("#dl", function () {
      var blob = new Blob([JSON.stringify(payload(), null, 1)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "where-you-stand-" + S.code + ".json";
      document.body.appendChild(a); a.click(); a.remove();
    });
    bind("#restart", function () {
      var box = document.getElementById("confirm");
      box.innerHTML = '<div class="notice">Start over? This clears your answers from this device. <button class="link" id="yes">Yes, start over</button> <button class="link" id="no">Cancel</button></div>';
      bind("#yes", function () { clearSaved(); S = newState(); save(); render(); });
      bind("#no", function () { box.innerHTML = ""; });
    });
  }
  var fbTimer = null;
  function sendFeedback() {
    if (!CFG.submitUrl || S.minor) return;
    clearTimeout(fbTimer);
    fbTimer = setTimeout(function () {
      fetch(CFG.submitUrl, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify({ v: S.v, rid: S.rid, feedback: true, result_fit: S.resultFit, result_fit_text: S.resultFitText || null }) }).catch(function () {});
    }, 1500);
  }

  // ---------- start ----------
  function resumeScreen(saved) {
    show('<div class="eyebrow"><span>Welcome back</span></div><h2>Pick up where you left off?</h2>' +
      "<p>Your answers from earlier are saved on this device (code <span class=\"mono\">" + esc(saved.code) + "</span>).</p>" +
      '<div class="nav" style="justify-content:flex-start"><button class="btn" id="cont">Continue</button><button class="btn ghost" id="fresh">Start over</button></div>');
    bind("#cont", function () { S = saved; render(); });
    bind("#fresh", function () { clearSaved(); S = newState(); save(); render(); });
  }
  function start() {
    if (!B) { screen.innerHTML = '<p class="lede">The question bank didn\'t load. Rebuild with scripts/build_app.py.</p>'; return; }
    var saved = load();
    if (saved && saved.v === 1 && saved.bank === B.version && saved.phase !== "intro") {
      if (saved.done) { S = saved; if (S.submitted === "sending") S.submitted = "failed"; render(); return; }
      return resumeScreen(saved);
    }
    S = newState(); save(); render();
  }
  window.__wys = { state: function () { return S; }, bank: B, payload: function () { return payload(); } };
  start();
})();
