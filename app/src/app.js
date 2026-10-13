/* Where You Stand: quiz app.
 * Plain browser JavaScript, no build step or dependencies. Reads window.BANK
 * (scripts/build_app.py) and window.QUIZ_CONFIG (config.js).
 * Answer codes always follow the bank's code order; only the on-screen order
 * is randomized, and it is recorded with every answer.
 */
(function () {
  "use strict";
  var B = window.BANK;
  var CFG = window.QUIZ_CONFIG || {};
  var KEY = "wys_pilot_v1", HIST = "wys_history_v1", THEME = "wys_theme";
  var BREAK_MS = 12 * 60 * 1000, SCREEN_CAP_MS = 5 * 60 * 1000, MIN_N = 3;
  var SEC_PER_SCREEN = 13;
  var screen = document.getElementById("screen");
  var metaEl = document.getElementById("meta");
  var progEl = document.getElementById("progress");
  var S = null, t0 = 0;
  var view = null;          // overlay page: "about" | "shared" | null
  var sharedCode = null;    // decoded from ?r=
  var compare = null;       // {label, scores} overlaid on results
  var keyHandler = null;
  var advTimer = null;

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
  function lsGet(k, dflt) { try { var v = localStorage.getItem(k); return v == null ? dflt : JSON.parse(v); } catch (e) { return dflt; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
  function lsDel(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } }
  function save() { lsSet(KEY, S); }
  function el(html) { var d = document.createElement("div"); d.innerHTML = html; return d.firstChild; }
  function show(html) {
    keyHandler = null;
    clearTimeout(advTimer);
    screen.classList.remove("leaving");
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
  function bind(sel, fn) { var b = screen.querySelector(sel); if (b) b.addEventListener("click", fn); }
  function domain(id) { for (var i = 0; i < B.domains.length; i++) if (B.domains[i].id === id) return B.domains[i]; return { name: "" }; }
  function plural(n, w) { return n + " " + w + (n === 1 ? "" : "s"); }

  // ---------- axes metadata ----------
  var META = { G: B.axes.overall }, AXES = ["G"];
  B.axes.families.forEach(function (f) { f.axes.forEach(function (a) { META[a.id] = a; AXES.push(a.id); }); });
  var ECON = ["REDIS", "REG", "SOCINS"], CULT = ["MORAL", "GENDERID", "RELIGION", "FAMILY", "EQUITY", "IMMIG", "NATION"];
  // axes whose + pole is the conventionally right-of-center side
  var LR_AXES = ["REDIS", "REG", "SOCINS", "ENV", "MORAL", "GENDERID", "RELIGION", "FAMILY", "EQUITY", "IMMIG", "NATION", "ORDER", "GUNS", "EDUC", "VOTING", "VALUES"];

  // ---------- theme ----------
  function effectiveDark() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function applyTheme(t) {
    if (t) document.documentElement.setAttribute("data-theme", t); else document.documentElement.removeAttribute("data-theme");
    var b = document.getElementById("nav-theme");
    if (b) b.textContent = effectiveDark() ? "Light" : "Dark";
  }

  // ---------- state ----------
  function newState() {
    return {
      v: 1, bank: B.version, rid: randId(12), code: randId(8), started: new Date().toISOString().slice(0, 10),
      phase: "home", mode: CFG.defaultMode || "quick", form: null, queue: [], pos: 0,
      ans: {}, qc: {}, pri: {}, priOrder: [], priPos: 0, about: {}, honesty: null,
      activeMs: 0, lastBreak: 0, minor: false, done: false, submitted: null,
    };
  }
  var PHASE_RENAMES = { intro: "home", about: "aboutyou" };

  function buildQueue() {
    var rnd = mulberry32(hash(S.rid + "order"));
    var ids = {};
    if (S.mode === "quick") {
      B.quick.forEach(function (i) { ids[i] = 1; });
    } else if (S.mode === "pilot") {
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
    var n = q.length;
    var qcs = B.quality.instructed_responses.items.slice();
    var spots = qcs.map(function () { return Math.floor(n / 3 + rnd() * (n / 3)); }).sort(function (a, b) { return b - a; });
    spots.forEach(function (idx, k) {
      while (idx < q.length && isFollowup(q, idx)) idx++;
      q.splice(idx, 0, { k: "qc", id: qcs[k].id, d: (q[Math.max(0, idx - 1)] || {}).d });
    });
    S.exp = CFG.experiments === false ? null : { torn: rnd() < 0.5, topTaxSwap: rnd() < 0.5, context: true };
    if (S.exp && S.exp.topTaxSwap) {
      var i1 = -1, i2 = -1;
      q.forEach(function (e, k) { if (e.id === "top_income_tax") i1 = k; if (e.id === "top_rate_number") i2 = k; });
      if (i1 >= 0 && i2 >= 0) { var tmp = q[i1]; q[i1] = q[i2]; q[i2] = tmp; }
    }
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
    if (view === "about") return renderAboutPage();
    if (view === "shared") return renderShared();
    var ph = S.phase;
    if (ph === "home") return renderHome();
    if (ph === "howto") return renderHowTo();
    if (ph === "quiz") {
      while (S.pos < S.queue.length && !visible(S.queue[S.pos])) S.pos++;
      if (S.pos >= S.queue.length) { S.phase = "pri"; S.priPos = 0; save(); return render(); }
      var e = S.queue[S.pos];
      return e.k === "qc" ? renderQC(e) : renderItem(e);
    }
    if (ph === "break") return renderBreak();
    if (ph === "pri") return renderPriorities();
    if (ph === "aboutyou") return renderAboutYou();
    if (ph === "honesty") return renderHonesty();
    if (ph === "done") return renderResults();
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
  function topicsInQueue() {
    var out = [];
    S.queue.forEach(function (e) { if (e.k === "item" && out.indexOf(e.d) < 0) out.push(e.d); });
    return out;
  }
  function minutesLeft() {
    var left = 0;
    for (var i = S.pos; i < S.queue.length; i++) if (S.queue[i].k !== "repeat") left++;
    return Math.max(1, Math.round((left * SEC_PER_SCREEN + 300) / 60));
  }
  // question counter: visible screens so far / visible screens in total (follow-ups join as they unlock)
  function counter() {
    var n = 0, at = 0;
    for (var i = 0; i < S.queue.length; i++) {
      var e = S.queue[i];
      if (e.k === "repeat" ? i > S.pos && !S.ans[e.id] : !visible(e)) continue;
      n++;
      if (i <= S.pos) at = n;
    }
    return { at: Math.max(1, at), n: n };
  }
  function updateMeta() {
    var frac = 0, label = "";
    if (view) { label = ""; frac = S && S.phase === "done" ? 1 : 0; }
    else if (S.phase === "quiz" || S.phase === "break") {
      var c = counter();
      frac = 0.02 + 0.9 * ((c.at - 1) / Math.max(1, c.n));
      label = S.phase === "break" ? "Break" : c.at + " of " + c.n;
    } else if (S.phase === "pri" || S.phase === "aboutyou" || S.phase === "honesty") { frac = 0.95; label = "Almost done"; }
    else if (S.phase === "done") { frac = 1; label = ""; }
    screen.classList.toggle("wide", !!view || S.phase === "home" || S.phase === "done");
    document.body.classList.toggle("in-quiz", !view && /quiz|break|pri|aboutyou|honesty/.test(S.phase));
    progEl.style.width = (100 * frac).toFixed(1) + "%";
    metaEl.textContent = label;
  }

  // ---------- home and instructions ----------
  var MODES = [
    { id: "quick", title: "Quick", time: "about 25 min", n: function () { return B.quick.length; }, text: "The most telling questions on every topic." },
    { id: "pilot", title: "Standard", time: "about 45 min", n: function () { return B.design.link.length + 3 * Math.round(B.design.blocks.reduce(function (s, b) { return s + b.length; }, 0) / B.design.blocks.length); }, text: "Sharper scores. Everyone gets a different mix of questions." },
    { id: "full", title: "Everything", time: "about 2 hours", n: function () { return Object.keys(B.items).length; }, text: "Every question, in as many sittings as you like." },
  ];
  var HERO_LABELS = {};
  ["dem_mainstream", "gop_current", "libertarian", "dem_socialist", "maga", "centrist", "pres_fdr", "pres_reagan", "pres_obama", "green", "religious_right", "ancap", "abundance", "rockefeller", "postliberal", "fr_rn"].forEach(function (id) { HERO_LABELS[id] = 1; });
  function lastResult() { var h = lsGet(HIST, []); return h.length ? h[h.length - 1] : null; }
  function renderHome() {
    var last = lastResult(), lastSc = last ? decodeScores(last.c) : null;
    var modes = MODES.filter(function (m) { return m.id !== "full" || CFG.allowFullMode !== false; });
    var lastPt = lastSc ? { x: userPos(lastSc, ECON), y: userPos(lastSc, CULT) } : null;
    var html = '<div class="home-grid"><section class="hero">' +
      "<h1>Where do you stand?</h1>" +
      '<p class="lede">Answer real policy questions, one issue at a time. Get your position on 29 dimensions and see which of ' + B.profiles.length + " parties, presidents, movements and ideologies you're closest to.</p>" +
      "</section>" +
      '<section class="field-wrap">' + plotHtml({ cat: "all", hero: true, label: HERO_LABELS, user: lastPt && lastPt.x != null ? lastPt : null, userLabel: "You, last time" }) + "</section>" +
      '<section class="start" aria-labelledby="pick"><h2 id="pick">Pick a length</h2>' +
      '<div class="ballot" role="radiogroup" aria-labelledby="pick">' + modes.map(function (m) {
        return '<button type="button" class="ballot-row" role="radio" data-mode="' + m.id + '" aria-checked="' + (S.mode === m.id) + '">' +
          '<span class="oval" aria-hidden="true"></span><span class="ballot-text"><b>' + esc(m.title) + "</b><span>" + esc(m.text) + "</span></span>" +
          '<span class="ballot-meta">' + "<span>" + m.n() + " questions</span><span>" + esc(m.time) + "</span></span></button>";
      }).join("") + "</div>" +
      '<div class="cta-row"><button class="btn big" id="go">Start the quiz</button>' +
      (last ? '<button class="btn ghost" id="last">Your last results</button>' : "") + "</div>" +
      '<p class="fine">Progress saves on this device, so you can stop and come back. No account, no names or emails. <button type="button" class="link" id="how">How it works</button></p></section></div>' +
      '<section class="pitch"><h2>What makes it different</h2><dl>' +
      "<div><dt>Real positions</dt><dd>Pick the policy you actually want, with real numbers, instead of agreeing with a vague slogan.</dd></div>" +
      "<div><dt>More than left and right</dt><dd>Trust, populism, free speech, presidential power and 25 more get their own scores, because they cut across parties.</dd></div>" +
      "<div><dt>No party cues</dt><dd>Questions never name parties or politicians, so you answer the issue, not the team.</dd></div>" +
      "<div><dt>" + B.profiles.length + " comparisons</dt><dd>From FDR and the Whigs to the tech right, Reform UK and anarcho-capitalists.</dd></div></dl></section>";
    show(html);
    wirePlot();
    screen.querySelectorAll("[data-mode]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.mode = b.getAttribute("data-mode");
        screen.querySelectorAll("[data-mode]").forEach(function (x) { x.setAttribute("aria-checked", String(x === b)); });
        save();
      });
    });
    bind("#go", function () { S.phase = "howto"; save(); render(); });
    bind("#how", function () { openAbout(); });
    bind("#last", function () { sharedCode = last.c; view = "shared"; render(); });
  }
  function renderHowTo() {
    var m = MODES.filter(function (x) { return x.id === S.mode; })[0] || MODES[0];
    show("<h1>How to answer</h1>" +
      '<div class="demo" aria-hidden="true"><div class="opt demo-opt"><span class="oval"></span><span class="otext">Somewhat smaller</span></div><div class="opt demo-opt is-on"><span class="oval"></span><span class="otext">About the same as now</span></div></div>' +
      '<ul class="howto">' +
      "<li><b>Tap the answer closest to your view.</b> The quiz moves on by itself. Go back any time to change it.</li>" +
      "<li><b>Picture the usual case.</b> The grey line under each question says what to think about. Exceptions get their own follow-up.</li>" +
      "<li><b>Some questions are a tug-of-war</b> between two goals. Tap how far you lean toward one side.</li>" +
      "<li><b>Not sure? Say so.</b> “I don't know” and “None of these fit” are under every question, and never count as a middle answer.</li>" +
      "<li><b>Underlined words</b> have a definition. Tap them.</li>" +
      "</ul>" +
      '<p class="scope">' + esc(m.title) + " quiz, " + m.n() + " questions, " + esc(m.time) + ". On a keyboard: number keys answer, ← goes back.</p>" +
      '<div class="nav"><button class="link" id="bk">Back</button><button class="btn big" id="go">Begin</button></div>');
    bind("#bk", function () { S.phase = "home"; save(); render(); });
    bind("#go", function () {
      if (!S.queue.length || S.queueMode !== S.mode) { buildQueue(); S.queueMode = S.mode; }
      S.phase = "quiz"; spend(); S.lastBreak = S.activeMs; save(); render();
    });
  }

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
        box.appendChild(el('<div class="def" id="' + id + '"><b>' + esc(d.term) + "</b>" + esc(d.text) + "</div>"));
        a.df = a.df || [];
        if (a.df.indexOf(d.term) < 0) a.df.push(d.term);
        save();
      });
    });
  }

  // ---------- one question ----------
  var FIRMNESS = ["Firm", "Fairly firm", "It really depends on the details"];
  var ESCAPES = [null, "None of these fit", "I don't know"];
  var ADVANCE_MS = 320;

  // One answer direction per person for the whole quiz (recorded with each answer),
  // so scales never flip between questions.
  function displayDir(it, isRepeat) {
    if (isRepeat) { var first = S.ans[it.id]; if (first && first.d != null) return first.d; }
    return hash(S.rid + "|dir") % 2;
  }
  function firstOfTopic() {
    var e = S.queue[S.pos];
    for (var p = S.pos - 1; p >= 0; p--) {
      var q = S.queue[p];
      if (q.k === "item" && visible(q)) return q.d !== e.d;
    }
    return true;
  }
  function topicLine(e, it, isRep) {
    if (isRep) return '<p class="topic">One more look: you saw this earlier. Answer it as you see it now.</p>';
    var name = domain(e.d || it.domain).name.replace(/\s*\(.*\)$/, "");
    if (e.k === "item" && firstOfTopic()) return '<p class="topic is-new"><span class="tag">New topic</span>' + esc(name) + "</p>";
    return '<p class="topic">' + esc(name) + "</p>";
  }

  function renderItem(e) {
    var it = B.items[e.id], isRep = e.k === "repeat";
    var key = isRep ? e.id + "#r" : e.id;
    var a = S.ans[key] || (S.ans[key] = {});
    var dir = displayDir(it, isRep);
    a.d = dir;
    var rich = richFactory(it);
    var html = '<article class="q q-' + it.format + '">' + topicLine(e, it, isRep);
    html += '<h2 class="stem">' + rich(it.stem) + "</h2>";
    if (it.scope) html += '<p class="scope">' + rich(it.scope) + "</p>";
    if (it.context) {
      if (a.cx == null) a.cx = (S.exp && S.exp.context && !isRep) ? hash(S.rid + "|cx|" + it.id) % 2 : 1;
      if (isRep) a.cx = (S.ans[it.id] && S.ans[it.id].cx != null) ? S.ans[it.id].cx : 1;
      if (a.cx) html += '<p class="context"><b>Background.</b> ' + rich(it.context) + "</p>";
    }
    html += '<div id="defs"></div>';
    if (it.format === "exceptions") html += casesHtml(it, dir, rich);
    else if (it.format === "tradeoff") html += tradeoffHtml(it, dir, rich);
    else html += optionsHtml(it, dir, rich);
    if (it.format !== "exceptions") {
      html += '<div class="outs">' + [2, 1].map(function (k) {
        return '<button type="button" class="esc" data-esc="' + k + '" aria-pressed="' + (a.e === k) + '">' + esc(ESCAPES[k]) + "</button>";
      }).join("") + '<button type="button" class="esc" id="skip">Skip</button></div>';
      html += '<div id="nf" class="nf" ' + (a.e === 1 ? "" : "hidden") + '><label for="nftext">What would your answer be? (optional)</label><textarea id="nftext" maxlength="500" rows="2">' + esc(a.x || "") + "</textarea></div>";
    }
    html += "</article>";
    html += navHtml(answered(it, a), it.format === "exceptions" || a.e === 1);
    if (!isRep) html += '<details class="flag"' + (a.flag ? " open" : "") + '><summary>Report a problem with this question</summary><label for="flagtext">What\'s confusing, slanted or missing?</label><textarea id="flagtext" maxlength="300" rows="2">' + esc(a.flag || "") + "</textarea></details>";
    show(html);
    wireDefs(it, a);
    var fl = document.getElementById("flagtext");
    if (fl) fl.addEventListener("input", function () { a.flag = fl.value.slice(0, 300); save(); });
    var leave = function () { a.ms = (a.ms || 0) + spend(); };
    if (it.format === "exceptions") wireCases(it);
    else wireOptions(it, a, leave);
    wireNav(leave);
    keyHandler = function (ev) {
      if (it.format !== "exceptions" && /^[1-9]$/.test(ev.key)) {
        var b = screen.querySelectorAll(".options .opt")[+ev.key - 1];
        if (b) { b.click(); ev.preventDefault(); }
      }
    };
  }

  function optionsHtml(it, dir, rich) {
    var codes = it.options.map(function (_, k) { return k; });
    if (dir) codes.reverse();
    return '<div class="options" role="radiogroup">' + codes.map(function (c, p) {
      var meaning = it.point_meanings ? "<small>" + esc(it.point_meanings[c]) + "</small>" : "";
      return '<button type="button" class="opt" role="radio" data-code="' + c + '" data-pos="' + p + '"><span class="oval" aria-hidden="true"></span><span class="otext">' + rich(it.options[c]) + meaning + "</span></button>";
    }).join("") + "</div>";
  }
  // Tradeoffs: the two goals side by side, then one row of ovals running from one to the other.
  function tradeoffHtml(it, swap, rich) {
    var A = it.sides[0], Bs = it.sides[1];
    var left = swap ? Bs : A, right = swap ? A : Bs;
    var codes = swap ? [3, 2, 1, 0] : [0, 1, 2, 3];
    var torn = S.exp && S.exp.torn && it.id.indexOf("qc_") !== 0;
    var caps = ["Strongly", "Somewhat", "Somewhat", "Strongly"];
    var cells = codes.map(function (c, p) {
      var side = p < 2 ? left.label : right.label;
      return '<button type="button" class="opt pip" role="radio" data-code="' + c + '" data-pos="' + (torn && p > 1 ? p + 1 : p) + '" aria-label="' + esc(caps[p] + " " + side) + '"><span class="oval" aria-hidden="true"></span><span class="cap">' + caps[p] + "</span></button>";
    });
    if (torn) cells.splice(2, 0, '<button type="button" class="opt pip" role="radio" data-torn="1" data-pos="2" aria-label="Torn between them"><span class="oval" aria-hidden="true"></span><span class="cap">Torn</span></button>');
    return '<div class="sides"><div class="side"><b>' + esc(left.label) + "</b><span>" + rich(left.text) + '</span></div><div class="side"><b>' + esc(right.label) + "</b><span>" + rich(right.text) + "</span></div></div>" +
      '<div class="tug"><div class="tug-ends"><span>← ' + esc(left.label) + "</span><span>" + esc(right.label) + ' →</span></div>' +
      '<div class="options pips' + (torn ? " five" : "") + '" role="radiogroup" aria-label="How far you lean">' + cells.join("") + "</div></div>";
  }
  function wireOptions(it, a, leave) {
    function paint() {
      screen.querySelectorAll(".opt[data-code]").forEach(function (b) { b.setAttribute("aria-checked", String(a.c != null && +b.getAttribute("data-code") === a.c)); });
      screen.querySelectorAll(".opt[data-torn]").forEach(function (b) { b.setAttribute("aria-checked", String(!!a.t)); });
      screen.querySelectorAll(".esc[data-esc]").forEach(function (b) { b.setAttribute("aria-pressed", String(a.e === +b.getAttribute("data-esc"))); });
      var nf = document.getElementById("nf"); if (nf) nf.hidden = a.e !== 1;
      var nx = document.getElementById("next"); if (nx) { nx.disabled = !answered(it, a); nx.hidden = !(a.e === 1 || answered(it, a)); }
    }
    function advance() {
      clearTimeout(advTimer);
      var here = S.pos;
      screen.classList.add("leaving");
      advTimer = setTimeout(function () { screen.classList.remove("leaving"); if (S.phase === "quiz" && S.pos === here && !view) { if (leave) leave(); next(); } }, ADVANCE_MS);
    }
    paint();
    screen.querySelectorAll(".opt[data-code]").forEach(function (b) {
      b.addEventListener("click", function () {
        a.c = +b.getAttribute("data-code"); a.p = +b.getAttribute("data-pos"); a.e = null; a.t = null;
        if (it.format === "tradeoff") a.s = a.d;
        save(); paint();
        if (CFG.autoAdvance !== false) advance();
      });
    });
    screen.querySelectorAll(".opt[data-torn]").forEach(function (b) {
      b.addEventListener("click", function () { a.t = 1; a.c = null; a.p = 2; a.e = null; a.s = a.d; save(); paint(); if (CFG.autoAdvance !== false) advance(); });
    });
    screen.querySelectorAll(".esc[data-esc]").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = +b.getAttribute("data-esc");
        a.e = a.e === v ? null : v; a.c = null; a.p = null; a.f = null; a.t = null;
        save(); paint();
        if (a.e === 2 && CFG.autoAdvance !== false) advance();
        if (a.e === 1) { var ta = document.getElementById("nftext"); if (ta) ta.focus(); }
      });
    });
    var ta = document.getElementById("nftext");
    if (ta) ta.addEventListener("input", function () { a.x = ta.value.slice(0, 500); save(); });
  }

  function casesHtml(it, dir, rich) {
    var codes = it.options.map(function (_, k) { return k; });
    if (dir) codes.reverse();
    return '<p class="hint">Answer each line.</p><div class="cases">' + it.cases.map(function (c) {
      return '<div class="case" data-case="' + esc(c.id) + '"><div class="case-text">' + rich(c.text) + '</div><div class="case-opts" role="radiogroup">' +
        codes.map(function (code, p) { return '<button type="button" class="chip" role="radio" data-code="' + code + '" data-pos="' + p + '"><span class="oval" aria-hidden="true"></span>' + esc(it.options[code]) + "</button>"; }).join("") +
        '<button type="button" class="chip esc" data-esc="2"><span class="oval" aria-hidden="true"></span>Not sure</button></div></div>';
    }).join("") + "</div>";
  }
  function wireCases(it) {
    var dir = displayDir(it, false);
    function paint() {
      screen.querySelectorAll(".case").forEach(function (row) {
        var ca = S.ans[row.getAttribute("data-case")] || {};
        row.querySelectorAll("[data-code]").forEach(function (b) { b.setAttribute("aria-checked", String(ca.c != null && +b.getAttribute("data-code") === ca.c)); });
        row.querySelectorAll(".esc").forEach(function (b) { b.setAttribute("aria-checked", String(ca.e === 2)); });
        row.classList.toggle("done", ca.c != null || ca.e === 2);
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
    return !!(a && (a.c != null || a.e || a.t));
  }
  function navHtml(ok, showNext) {
    return '<div class="nav qnav"><button class="link back" id="bk"' + (S.pos === 0 ? " hidden" : "") + '>← Back</button>' +
      '<button class="btn" id="next"' + (ok ? "" : " disabled") + (ok || showNext ? "" : " hidden") + ">Next</button></div>";
  }
  function wireNav(onLeave) {
    bind("#next", function () { clearTimeout(advTimer); onLeave(); next(); });
    bind("#skip", function () { onLeave(); next(); });
    bind("#bk", function () { clearTimeout(advTimer); onLeave(); back(); });
  }

  // ---------- attention checks ----------
  function renderQC(e) {
    var q = B.quality.instructed_responses.items.filter(function (x) { return x.id === e.id; })[0];
    var rec = S.qc[q.id] || (S.qc[q.id] = {});
    var fake = { id: q.id, format: q.format, options: q.options, sides: q.sides, stem: q.stem, scope: q.scope, domain: e.d };
    var dir = displayDir(fake, false);
    show('<article class="q q-' + q.format + '"><p class="topic">' + esc(domain(e.d).name) + '</p><h2 class="stem">' + esc(q.stem) + '</h2><p class="scope">' + esc(q.scope) + "</p>" +
      (q.format === "tradeoff" ? tradeoffHtml(fake, dir, esc) : optionsHtml(fake, dir, esc)) + "</article>" + navHtml(rec.c != null, false));
    function leave() { rec.ms = (rec.ms || 0) + spend(); }
    screen.querySelectorAll(".opt[data-code]").forEach(function (b) {
      b.setAttribute("aria-checked", String(rec.c != null && +b.getAttribute("data-code") === rec.c));
      b.addEventListener("click", function () {
        rec.c = +b.getAttribute("data-code"); rec.ok = rec.c === q.correct;
        screen.querySelectorAll(".opt[data-code]").forEach(function (x) { x.setAttribute("aria-checked", String(x === b)); });
        var nx = document.getElementById("next"); nx.disabled = false; nx.hidden = false; save();
        if (CFG.autoAdvance !== false) {
          clearTimeout(advTimer); var here = S.pos;
          advTimer = setTimeout(function () { if (S.phase === "quiz" && S.pos === here && !view) { leave(); next(); } }, ADVANCE_MS);
        }
      });
    });
    wireNav(leave);
    keyHandler = function (ev) {
      if (/^[1-9]$/.test(ev.key)) { var b = screen.querySelectorAll(".options .opt")[+ev.key - 1]; if (b) { b.click(); ev.preventDefault(); } }
    };
  }

  // ---------- break ----------
  function renderBreak() {
    var c = counter(), pct = Math.round(100 * (c.at - 1) / Math.max(1, c.n));
    var sc = computeScores(S.ans), preview = "", top = profileMatches(sc)[0];
    if (sc.G && sc.G.n >= MIN_N) preview = '<div class="results-block">' + barHtml(META.G, sc.G, { big: true }) +
      (top ? '<p class="scope">Closest so far: <b>' + esc(top.p.name) + "</b>. It will shift as you answer more.</p>" : "") + "</div>";
    show("<h1>" + pct + "% done. Take a breather.</h1>" +
      "<p>About " + minutesLeft() + " minutes to go. Your answers are saved on this device, so you can also close the page and come back later.</p>" + preview +
      '<div class="nav"><span></span><button class="btn big" id="go">Keep going</button></div>');
    bind("#go", function () { spend(); S.phase = "quiz"; save(); render(); });
  }

  // ---------- priorities: pick up to five topics, in order ----------
  var PRI_MAX = 5;
  function renderPriorities() {
    var P = B.priorities;
    if (!S.pri || !Array.isArray(S.pri.top)) S.pri = { top: [] };
    var top = S.pri.top;
    var labels = Object.keys(P.labels).sort(function (a, b) { return P.labels[a].localeCompare(P.labels[b]); });
    show("<h1>Which issues matter most to you?</h1>" +
      '<p class="scope">Tap up to ' + PRI_MAX + ", most important first. Tap again to remove one.</p>" +
      '<div class="pri-grid">' + labels.map(function (d) {
        var r = top.indexOf(d);
        return '<button type="button" class="pri" data-d="' + esc(d) + '" aria-pressed="' + (r >= 0) + '"><span class="rank" aria-hidden="true">' + (r >= 0 ? r + 1 : "") + "</span>" + esc(P.labels[d]) + "</button>";
      }).join("") + "</div>" +
      '<div class="nav"><span class="scope" id="pricount">' + top.length + " of " + PRI_MAX + ' picked</span><button class="btn" id="next">' + (top.length ? "Continue" : "Skip") + "</button></div>");
    function paint() {
      screen.querySelectorAll(".pri").forEach(function (b) {
        var r = top.indexOf(b.getAttribute("data-d"));
        b.setAttribute("aria-pressed", String(r >= 0)); b.querySelector(".rank").textContent = r >= 0 ? r + 1 : "";
        b.disabled = r < 0 && top.length >= PRI_MAX;
      });
      document.getElementById("pricount").textContent = top.length + " of " + PRI_MAX + " picked";
      document.getElementById("next").textContent = top.length ? "Continue" : "Skip";
    }
    paint();
    screen.querySelectorAll(".pri").forEach(function (b) {
      b.addEventListener("click", function () {
        var d = b.getAttribute("data-d"), r = top.indexOf(d);
        if (r >= 0) top.splice(r, 1); else if (top.length < PRI_MAX) top.push(d);
        save(); paint();
      });
    });
    bind("#next", function () { S.pri.ms = (S.pri.ms || 0) + spend(); S.phase = "aboutyou"; save(); render(); });
  }

  // ---------- about you ----------
  var STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "A US territory", "I live outside the US"];
  function aboutItems() {
    var out = [];
    B.about.items.forEach(function (q) {
      if (q.placement) return;
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
  function renderAboutYou() {
    var qs = aboutItems();
    var html = '<h1>A few questions about you</h1><p class="scope">' + esc(B.about.intro_text) + ' All optional, and they never change your results.</p><div class="form">';
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
    html += '</div><div class="nav"><span></span><button class="btn big" id="go">Continue</button></div>';
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
    show('<article class="q"><p class="topic">Last question</p><h2 class="stem">' + esc(q.stem) + '</h2><p class="scope">' + esc(q.scope) + '</p><div class="options" role="radiogroup">' +
      q.options.map(function (o, k) { return '<button type="button" class="opt" role="radio" data-k="' + k + '" aria-checked="' + (S.honesty === k) + '"><span class="oval" aria-hidden="true"></span><span class="otext">' + esc(o) + "</span></button>"; }).join("") +
      '</div></article><div class="nav"><span></span><button class="btn big" id="go"' + (S.honesty == null ? " disabled" : "") + ">See my results</button></div>");
    screen.querySelectorAll("[data-k]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.honesty = +b.getAttribute("data-k");
        screen.querySelectorAll("[data-k]").forEach(function (x) { x.setAttribute("aria-checked", String(x === b)); });
        document.getElementById("go").disabled = false; save();
      });
    });
    bind("#go", function () { spend(); finish(); });
  }

  // ---------- finish and submit ----------
  function payload() {
    return {
      v: S.v, bank: S.bank, rid: S.rid, code: S.code, mode: S.mode, form: S.form, started: S.started, exp: S.exp || null,
      active_s: Math.round(S.activeMs / 1000),
      order: S.queue.map(function (e) { return e.k === "qc" ? "qc:" + e.id : e.k === "repeat" ? e.id + "#r" : e.id; }),
      ans: S.ans, qc: S.qc, pri: S.pri, about: S.about, honesty: S.honesty,
      result_fit: S.resultFit == null ? null : S.resultFit, result_fit_text: S.resultFitText || null,
    };
  }
  function submitUrl() {
    var u = CFG.submitUrl || "";
    if (u === "auto") return (window.claude || !/^https?:$/.test(location.protocol)) ? "" : "/api/submit";
    return u;
  }
  function post(body) {
    var url = submitUrl(), opts = { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: body };
    if (/^https?:\/\//.test(url)) opts.mode = "no-cors";
    return fetch(url, opts).then(function (res) { if (res.type !== "opaque" && !res.ok) throw new Error("HTTP " + res.status); });
  }
  function submit() {
    if (S.minor) { S.submitted = "minor"; save(); return Promise.resolve(); }
    if (!submitUrl()) { S.submitted = "local"; save(); return Promise.resolve(); }
    S.submitted = "sending";
    return post(JSON.stringify(payload()))
      .then(function () { S.submitted = "sent"; save(); })
      .catch(function () { S.submitted = "failed"; save(); });
  }
  function finish() {
    S.phase = "done"; S.done = true; save();
    var h = lsGet(HIST, []);
    if (!h.some(function (x) { return x.rid === S.rid; })) {
      h.push({ rid: S.rid, d: new Date().toISOString().slice(0, 10), m: S.mode, c: encodeScores(computeScores(S.ans)) });
      lsSet(HIST, h.slice(-10));
    }
    render();
    submit().then(function () { if (S.phase === "done" && !view) render(); });
  }
  var fbTimer = null;
  function sendFeedback() {
    if (!submitUrl() || S.minor) return;
    clearTimeout(fbTimer);
    fbTimer = setTimeout(function () {
      post(JSON.stringify({ v: S.v, rid: S.rid, feedback: true, result_fit: S.resultFit, result_fit_text: S.resultFitText || null })).catch(function () {});
    }, 1500);
  }

  // ---------- scoring ----------
  function computeScores(ans) {
    var acc = {};
    function apply(k, x, w, part) {
      if (!k) return;
      Object.keys(k).forEach(function (ax) {
        if (!k[ax]) return;
        var o = acc[ax] || (acc[ax] = { s: 0, w: 0, n: 0, parts: [] });
        o.s += k[ax] * x * w; o.w += w; o.n++;
        o.parts.push({ id: part.id, cid: part.cid, s: k[ax] * x, w: w });
      });
    }
    Object.keys(B.items).forEach(function (id) {
      var it = B.items[id];
      if (it.issue_map_only) return;
      if (it.format === "exceptions") {
        var K = it.options.length;
        it.cases.forEach(function (c) {
          var ca = ans[c.id];
          if (ca && ca.c != null) apply(B.keying[c.id] || B.keying[id], 2 * ca.c / (K - 1) - 1, 0.5, { id: id, cid: c.id });
        });
        return;
      }
      var a = ans[id], x;
      if (!a) return;
      if (a.t) x = 0; else if (a.c != null) x = 2 * a.c / (it.options.length - 1) - 1; else return;
      apply(B.keying[id], x, 1, { id: id });
    });
    var out = {};
    Object.keys(acc).forEach(function (ax) { out[ax] = { v: acc[ax].s / acc[ax].w, n: acc[ax].n, parts: acc[ax].parts }; });
    return out;
  }
  // share codes: version "1", then one byte per axis in AXES order (0-200 = -1..+1, 255 = no score)
  function encodeScores(sc) {
    var bytes = AXES.map(function (ax) { return sc[ax] && sc[ax].n >= MIN_N ? Math.round((Math.max(-1, Math.min(1, sc[ax].v)) + 1) * 100) : 255; });
    var bin = String.fromCharCode.apply(null, bytes);
    return "1" + btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function decodeScores(code) {
    if (!code || code.charAt(0) !== "1") return null;
    try {
      var b64 = code.slice(1).replace(/-/g, "+").replace(/_/g, "/");
      while (b64.length % 4) b64 += "=";
      var bin = atob(b64), out = {};
      AXES.forEach(function (ax, i) {
        var c = bin.charCodeAt(i);
        if (!isNaN(c) && c <= 200) out[ax] = { v: c / 100 - 1, n: MIN_N, parts: [] };
      });
      return Object.keys(out).length ? out : null;
    } catch (e) { return null; }
  }
  function codeFromInput(s) {
    s = String(s || "").trim();
    var m = s.match(/[?&]r=([A-Za-z0-9_-]+)/);
    return m ? m[1] : s;
  }
  function shareLink(code) {
    if (window.claude || !/^https?:$/.test(location.protocol)) return "";
    return location.origin + location.pathname + "?r=" + code;
  }

  // ---------- result components ----------
  function leanText(v, meta) {
    var p = Math.abs(v), side = v < 0 ? meta.minus : meta.plus;
    if (p < 0.1) return "Near the center";
    var word = p < 0.3 ? "Leans" : p < 0.6 ? "Moderately" : p < 0.85 ? "Strongly" : "Very strongly";
    return word + (word === "Leans" ? " " : ": ") + side;
  }
  function pct(v) { return ((Math.max(-1, Math.min(1, v)) + 1) * 50).toFixed(1); }
  function signed(v) { var n = Math.round(100 * v); return (n > 0 ? "+" : "") + n; }
  function barHtml(meta, sc, opt) {
    opt = opt || {};
    var v = Math.max(-1, Math.min(1, sc.v));
    var other = opt.other && opt.other.v != null ? '<span class="dot other" style="left:' + pct(opt.other.v) + '%" title="' + esc(opt.otherLabel || "") + '"></span>' : "";
    var prev = opt.prev != null ? '<span class="dot prev" style="left:' + pct(opt.prev) + '%"></span>' : "";
    var inner = '<div class="axis-head"><span class="axis-name">' + esc(meta.name) + "</span>" +
      '<span class="axis-val">' + esc(leanText(v, meta)) + ' <span class="num">' + signed(v) + "</span></span></div>" +
      '<div class="track" role="img" aria-label="' + esc(meta.name + ": " + leanText(v, meta)) + '"><span class="mid"></span>' + prev + other + '<span class="dot" style="left:' + pct(v) + '%"></span></div>' +
      '<div class="poles"><span>' + esc(meta.minus) + "</span><span>" + esc(meta.plus) + "</span></div>";
    if (opt.drill && sc.parts && sc.parts.length) {
      return '<details class="axis' + (opt.big ? " big" : "") + '"><summary>' + inner + '<span class="axis-n">' + "Which answers moved this? (" + sc.n + ")</span></summary>" + drillHtml(meta, sc) + "</details>";
    }
    return '<div class="axis' + (opt.big ? " big" : "") + '">' + inner + "</div>";
  }
  function partText(p) {
    var it = B.items[p.id];
    if (p.cid) {
      var c = it.cases.filter(function (x) { return x.id === p.cid; })[0], ca = S && S.ans[p.cid];
      return { q: it.stem + " — " + c.text, a: ca && ca.c != null ? it.options[ca.c] : "" };
    }
    return { q: it.stem, a: S ? answerText(it, S.ans[p.id]) : "" };
  }
  function drillHtml(meta, sc) {
    var parts = sc.parts.slice().sort(function (a, b) { return Math.abs(b.s * b.w) - Math.abs(a.s * a.w); });
    return '<div class="drill"><p class="scope">' + esc(meta.about || "") + ' The answers below moved this score, strongest first.</p><ul>' +
      parts.slice(0, 12).map(function (p) {
        var t = partText(p), toward = p.s > 0.05 ? meta.plus : p.s < -0.05 ? meta.minus : "the center";
        return "<li><span class=\"dq\">" + esc(t.q) + "</span><span class=\"da\">" + esc(t.a) + '</span><span class="dt">→ ' + esc(toward) + "</span></li>";
      }).join("") + "</ul>" + (parts.length > 12 ? '<p class="scope">…and ' + (parts.length - 12) + " more.</p>" : "") + "</div>";
  }
  function profilePos(p, axes) {
    var vals = axes.filter(function (a) { return p.pos[a] != null; }).map(function (a) { return p.pos[a]; });
    return vals.length ? vals.reduce(function (s, x) { return s + x; }, 0) / vals.length : null;
  }
  function userPos(sc, axes) {
    var vals = axes.filter(function (a) { return sc[a] && sc[a].n >= MIN_N; }).map(function (a) { return sc[a].v; });
    return vals.length ? vals.reduce(function (s, x) { return s + x; }, 0) / vals.length : null;
  }
  var CATS = B.profileCats || [];
  function catName(id) { var c = CATS.filter(function (x) { return x.id === id; })[0]; return c ? c.name : "All"; }
  function profileMeta(p) {
    if (p.cat === "typology") return "Pew voter type";
    if (p.cat === "ideology") return "Ideology";
    if (p.cat === "president") return "President, " + p.era;
    if (p.cat === "world") return p.era + ", outside the US";
    return "US, " + p.era;
  }
  var PROFILE = {}; B.profiles.forEach(function (p) { PROFILE[p.id] = p; });

  // The field: every comparison group on the economic (across) and cultural (up) summary axes.
  // o: {cat, label: {id:1} or null for all, user:{x,y}, userLabel, other:{x,y}, otherLabel, hero, match:{id:%}}
  function textW(t) { var w = 2; for (var i = 0; i < t.length; i++) w += /[A-Z]/.test(t[i]) ? 6.4 : /[ .il']/.test(t[i]) ? 2.8 : 5; return w; }
  function plotHtml(o) {
    var W = 360, P = 30, R = W - 2 * P;
    function X(v) { return +(P + (v + 1) / 2 * R).toFixed(1); }
    function Y(v) { return +(P + (1 - (v + 1) / 2) * R).toFixed(1); }
    var placed = [];
    if (o.user) {
      var ux0 = X(o.user.x), uy0 = Y(o.user.y), uw = 7.5 * (o.userLabel || "You").length / 2 + 5;
      placed.push({ x0: ux0 - uw, x1: ux0 + uw, y: uy0 - 17 }, { x0: ux0 - 13, x1: ux0 + 13, y: uy0 - 3 }, { x0: ux0 - 13, x1: ux0 + 13, y: uy0 + 7 });
    }
    var pts = B.profiles.map(function (p) {
      var x = profilePos(p, ECON), y = profilePos(p, CULT);
      if (x == null || y == null) return null;
      var inCat = o.cat === "all" || p.cat === o.cat;
      return { p: p, cx: X(x), cy: Y(y), right: x > 0.4, on: inCat, lab: inCat && (!o.label || o.label[p.id]) };
    }).filter(Boolean).sort(function (a, b) { return (a.lab - b.lab) || (a.cy - b.cy); });
    pts.forEach(function (q) { if (q.on) placed.push({ x0: q.cx - 3.5, x1: q.cx + 3.5, y: q.cy + 3.5, dot: 1 }); });
    function free(x0, w, ty) { return !placed.some(function (b) { return x0 < b.x1 && x0 + w > b.x0 && Math.abs(ty - b.y) < (b.dot ? 7 : 10); }); }
    var dots = pts.map(function (q) {
      var label = "";
      if (q.lab) {
        var w = textW(q.p.short), ty = q.cy + 3.5, x0 = null, right = q.right;
        // try both sides at the dot's height, then step up and down
        for (var g = 0; g < 15 && x0 == null; g++) {
          var dy = g === 0 ? 0 : (g % 2 ? 1 : -1) * 10 * Math.ceil(g / 2);
          var sides = [right, !right];
          for (var k = 0; k < 2; k++) {
            var cand = sides[k] ? q.cx - 6 - w : q.cx + 6;
            if (cand < 2 || cand + w > W - 2) continue;
            if (free(cand, w, q.cy + 3.5 + dy)) { x0 = cand; ty = q.cy + 3.5 + dy; right = sides[k]; break; }
          }
        }
        if (x0 == null) { x0 = right ? q.cx - 6 - w : q.cx + 6; }
        placed.push({ x0: x0, x1: x0 + w, y: ty });
        var lead = Math.abs(ty - q.cy - 3.5) > 1 ? '<line x1="' + q.cx + '" y1="' + q.cy + '" x2="' + (right ? x0 + w : x0).toFixed(1) + '" y2="' + (ty - 3).toFixed(1) + '"/>' : "";
        label = lead + '<text x="' + x0.toFixed(1) + '" y="' + ty.toFixed(1) + '">' + esc(q.p.short) + "</text>";
      }
      return '<g class="pdot' + (q.on ? "" : " off") + (q.lab ? " lab" : "") + '" data-pid="' + q.p.id + '" tabindex="' + (q.on ? 0 : -1) + '" role="button" aria-label="' + esc(q.p.name) + '"><title>' + esc(q.p.name + " (" + q.p.era + ")") + '</title><circle class="hit" cx="' + q.cx + '" cy="' + q.cy + '" r="9"/><circle cx="' + q.cx + '" cy="' + q.cy + '" r="' + (q.lab ? 3.6 : 3) + '"/>' + label + "</g>";
    }).join("");
    var odot = o.other ? '<g class="odot"><circle cx="' + X(o.other.x) + '" cy="' + Y(o.other.y) + '" r="7.5"/><text x="' + X(o.other.x) + '" y="' + (Y(o.other.y) + 20) + '" text-anchor="middle">' + esc(o.otherLabel || "Them") + "</text></g>" : "";
    var udot = o.user ? '<g class="udot"><circle class="ring" cx="' + X(o.user.x) + '" cy="' + Y(o.user.y) + '" r="13"/><circle cx="' + X(o.user.x) + '" cy="' + Y(o.user.y) + '" r="8"/><text x="' + X(o.user.x) + '" y="' + (Y(o.user.y) - 17) + '" text-anchor="middle">' + esc(o.userLabel || "You") + "</text></g>" : "";
    var M = W / 2;
    return '<figure class="plot' + (o.hero ? " hero-plot" : "") + '"><svg viewBox="0 0 ' + W + " " + W + '" role="group" aria-label="Map of parties, presidents, movements and ideologies: economics across, culture up and down">' +
      '<rect class="field" x="' + P + '" y="' + P + '" width="' + R + '" height="' + R + '"/>' +
      '<line class="axisline" x1="' + M + '" y1="' + P + '" x2="' + M + '" y2="' + (W - P) + '"/><line class="axisline" x1="' + P + '" y1="' + M + '" x2="' + (W - P) + '" y2="' + M + '"/>' +
      '<text class="axlabel" x="' + M + '" y="' + (P - 9) + '" text-anchor="middle">Tradition</text>' +
      '<text class="axlabel" x="' + M + '" y="' + (W - P + 18) + '" text-anchor="middle">Change</text>' +
      '<text class="axlabel" x="' + (P - 9) + '" y="' + M + '" text-anchor="middle" transform="rotate(-90 ' + (P - 9) + " " + M + ')">Public economy</text>' +
      '<text class="axlabel" x="' + (W - P + 9) + '" y="' + M + '" text-anchor="middle" transform="rotate(90 ' + (W - P + 9) + " " + M + ')">Market economy</text>' +
      dots + odot + udot + "</svg>" +
      '<figcaption class="plotcap" aria-live="polite">' + (o.hero ? "Each dot is a party, president, movement or ideology. Tap one to see who it is." : "Tap any dot to see who it is.") + "</figcaption></figure>";
  }
  var plotMatch = null; // id -> match %, for captions on the results page
  function wirePlot() {
    screen.querySelectorAll(".plot").forEach(function (fig) {
      var cap = fig.querySelector(".plotcap");
      function pick(g) {
        fig.querySelectorAll(".pdot.sel").forEach(function (x) { x.classList.remove("sel"); });
        g.classList.add("sel");
        var p = PROFILE[g.getAttribute("data-pid")];
        cap.innerHTML = "<b>" + esc(p.name) + "</b> <span class=\"era\">" + esc(profileMeta(p)) + (plotMatch && plotMatch[p.id] != null ? ", " + plotMatch[p.id] + "% match" : "") + "</span><br>" + esc(p.about);
      }
      fig.querySelectorAll(".pdot").forEach(function (g) {
        g.addEventListener("click", function () { pick(g); });
        g.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); pick(g); } });
      });
    });
  }
  function profileMatches(sc) {
    return B.profiles.map(function (p) {
      var sum = 0, wsum = 0, diffs = [];
      Object.keys(p.pos).forEach(function (ax) {
        if (!sc[ax] || sc[ax].n < MIN_N) return;
        var w = ax === "G" ? 2 : 1, d = Math.abs(sc[ax].v - p.pos[ax]);
        sum += w * d * d; wsum += w;
        if (ax !== "G") diffs.push({ ax: ax, d: d });
      });
      if (diffs.length < 6) return null;
      // a small prior keeps groups placed on only a few axes from matching too easily
      var rms = Math.sqrt((sum + 0.25) / (wsum + 1));
      diffs.sort(function (a, b) { return a.d - b.d; });
      return { p: p, match: Math.max(0, Math.round(100 * (1 - rms / 2))), agree: diffs.slice(0, 3), differ: diffs.slice(-3).reverse(), n: diffs.length };
    }).filter(Boolean).sort(function (a, b) { return b.match - a.match; });
  }
  function axisList(arr) {
    var names = arr.map(function (x) { return META[x.ax || x].name.toLowerCase(); });
    return names.length > 1 ? names.slice(0, -1).join(", ") + " and " + names[names.length - 1] : names[0] || "";
  }
  function summarySentence(sc) {
    if (!sc.G || sc.G.n < MIN_N) return "";
    var g = sc.G.v, lean = Math.abs(g) < 0.1 ? "near the center overall" : leanText(g, META.G).toLowerCase().replace(":", "") + " overall";
    lean = lean.replace(/^leans /, "leaning ");
    var shown = AXES.filter(function (ax) { return ax !== "G" && sc[ax] && sc[ax].n >= MIN_N; });
    var breaks = shown.filter(function (ax) { return LR_AXES.indexOf(ax) >= 0 && Math.abs(g) > 0.15 && sc[ax].v * g < 0 && Math.abs(sc[ax].v) > 0.2; });
    return "You're " + lean + (breaks.length ? ", but you break from that lean on " + axisList(breaks) + "." : ".");
  }

  var resCat = "all", showAll = false, lastCmp = null;
  function afterResults() { if (lastCmp) wireCompare(lastCmp.sc, lastCmp.matches, lastCmp.o); }
  function matchListHtml(matches, cat) {
    var list = cat === "all" ? matches : matches.filter(function (m) { return m.p.cat === cat; });
    var lim = showAll ? list.length : cat === "all" ? 8 : 6;
    return '<ol class="profiles">' + list.slice(0, lim).map(function (m, k) {
      return '<li><details><summary><span class="prof-rank">' + (k + 1) + '</span><span class="prof-main"><span class="prof-head"><b>' + esc(m.p.name) + '</b><span class="era">' + esc(profileMeta(m.p)) + '</span></span><span class="matchbar"><span style="width:' + m.match + '%"></span></span></span><span class="match">' + m.match + "%</span></summary>" +
        '<div class="prof-body"><p>' + esc(m.p.about) + "</p><p><b>Closest on</b> " + esc(axisList(m.agree)) + ".<br><b>Furthest on</b> " + esc(axisList(m.differ)) + ".</p></div></details></li>";
    }).join("") + "</ol>" +
      (list.length > lim ? '<button type="button" class="link" id="showall">Show all ' + list.length + "</button>" : "") +
      (showAll && list.length > 8 ? '<button type="button" class="link" id="showless">Show fewer</button>' : "");
  }
  function chipsHtml() {
    return '<div class="chips" role="tablist" aria-label="Filter comparisons">' + [{ id: "all", name: "All" }].concat(CATS).map(function (c) {
      return '<button type="button" class="chip" role="tab" data-cat="' + c.id + '" aria-selected="' + (resCat === c.id) + '">' + esc(c.name) + "</button>";
    }).join("") + "</div>";
  }
  function compareBlockHtml(sc, matches, o) {
    var top = {}; matches.slice(0, 5).forEach(function (m) { top[m.p.id] = 1; });
    var ux = userPos(sc, ECON), uy = userPos(sc, CULT);
    var ox = o.other ? userPos(o.other, ECON) : null, oy = o.other ? userPos(o.other, CULT) : null;
    var catAbout = resCat === "all" ? "Everyone on the map; the five closest to " + (o.they ? "them" : "you") + " are labeled." : (CATS.filter(function (c) { return c.id === resCat; })[0] || {}).about || "";
    return chipsHtml() + '<p class="scope cat-about">' + esc(catAbout) + "</p>" +
      '<div class="compare-grid"><div>' + (ux != null && uy != null ? plotHtml({ cat: resCat, label: resCat === "all" ? top : null, user: { x: ux, y: uy }, userLabel: o.they ? "Them" : "You", other: ox != null && oy != null ? { x: ox, y: oy } : null, otherLabel: o.otherLabel }) : "") + "</div>" +
      "<div>" + matchListHtml(matches, resCat) + "</div></div>";
  }
  function wireCompare(sc, matches, o) {
    var box = screen.querySelector("#compare-box");
    if (!box) return;
    plotMatch = {}; matches.forEach(function (m) { plotMatch[m.p.id] = m.match; });
    function rerender() { box.innerHTML = compareBlockHtml(sc, matches, o); wireCompare(sc, matches, o); }
    box.querySelectorAll("[data-cat]").forEach(function (b) {
      b.addEventListener("click", function () { resCat = b.getAttribute("data-cat"); showAll = false; rerender(); });
    });
    var sa = box.querySelector("#showall"); if (sa) sa.addEventListener("click", function () { showAll = true; rerender(); });
    var sl = box.querySelector("#showless"); if (sl) sl.addEventListener("click", function () { showAll = false; rerender(); });
    wirePlot();
  }

  function resultsSections(sc, opt) {
    opt = opt || {};
    var other = opt.other, otherLabel = opt.otherLabel || "Them", prev = opt.prev, html = "";
    var g = sc.G, matches = profileMatches(sc), top = matches[0];
    lastCmp = { sc: sc, matches: matches, o: { other: other, otherLabel: otherLabel, they: opt.they } };
    html += '<header class="res-head">' + (opt.kicker ? '<p class="topic">' + esc(opt.kicker) + "</p>" : "") +
      (top ? "<h1>" + (opt.they ? "Their" : "Your") + " closest match is " + esc(top.p.name) + "</h1>" : "<h1>" + (opt.they ? "Where they stand" : "Where you stand") + "</h1>") +
      (top ? '<p class="res-sub"><b>' + top.match + "% match.</b> " + esc(profileMeta(top.p)) + ". " + esc(top.p.about) + "</p>" : "") +
      (g && g.n >= MIN_N ? '<p class="summary">' + esc(opt.they ? summarySentence(sc).replace(/^You're/, "They're").replace(/you break/, "they break") : summarySentence(sc)) + "</p>" + barHtml(META.G, g, { big: true, other: other && other.G, otherLabel: otherLabel, prev: prev && prev.G ? prev.G.v : null }) : "") +
      "</header>";
    if (matches.length) {
      html += '<section class="results-block"><h2>' + (opt.they ? "Who they're" : "Who you're") + " closest to</h2>" +
        '<div id="compare-box">' + compareBlockHtml(sc, matches, { other: other, otherLabel: otherLabel, they: opt.they }) + "</div>" +
        '<p class="scope">The map squeezes everything into two summary dimensions (economics across, culture up and down). The match percentages use every axis you have a score on, so they can disagree with the map.</p></section>';
    }
    var shown = AXES.filter(function (ax) { return ax !== "G" && sc[ax] && sc[ax].n >= MIN_N; });
    var strongest = shown.slice().sort(function (a, b) { return Math.abs(sc[b].v) - Math.abs(sc[a].v); }).slice(0, 4);
    if (strongest.length) {
      html += '<section class="results-block"><h2>Strongest views</h2><div class="standouts">' +
        strongest.map(function (ax) {
          return '<div class="standout"><span class="num">' + signed(sc[ax].v) + "</span><b>" + esc(META[ax].name) + "</b><span>" + esc(leanText(sc[ax].v, META[ax])) + "</span></div>";
        }).join("") + "</div></section>";
    }
    html += '<section class="results-block"><h2>All ' + shown.length + " axes</h2><p class=\"scope\">" + (opt.drill ? "Tap any axis to see which answers moved it. " : "") + "Scores run from −100 to +100." +
      (other ? ' <span class="legend"><span class="dot-key you"></span>' + (opt.they ? "Them" : "You") + ' <span class="dot-key other"></span>' + esc(otherLabel) + "</span>" : "") +
      (prev ? ' <span class="legend"><span class="dot-key you"></span>Now <span class="dot-key prev"></span>Last time</span>' : "") + "</p>";
    B.axes.families.forEach(function (f) {
      var rows = f.axes.filter(function (a) { return sc[a.id] && sc[a.id].n >= MIN_N; });
      if (!rows.length) return;
      html += '<div class="family"><h3>' + esc(f.name) + "</h3>" + rows.map(function (a) {
        return barHtml(a, sc[a.id], { drill: opt.drill, other: other && other[a.id], otherLabel: otherLabel, prev: prev && prev[a.id] ? prev[a.id].v : null });
      }).join("") + "</div>";
    });
    html += "</section>";
    return html;
  }

  // ---------- results page ----------
  function answerText(it, a) {
    if (!a) return null;
    if (a.e === 1) return "None of these fit my view" + (a.x ? ': "' + a.x + '"' : "");
    if (a.e === 2) return "I don't know enough to say";
    if (a.t) return "Torn between " + it.sides[0].label + " and " + it.sides[1].label;
    if (a.c == null) return null;
    if (it.format === "tradeoff") {
      var side = a.c <= 1 ? it.sides[0] : it.sides[1];
      return (a.c === 0 || a.c === 3 ? "Strongly: " : "Somewhat: ") + side.label + ". " + side.text;
    }
    return it.options[a.c];
  }
  function priorityRanking() {
    return S.pri && Array.isArray(S.pri.top) ? S.pri.top.map(function (d) { return { d: d }; }) : [];
  }
  function previousResult() {
    var h = lsGet(HIST, []).filter(function (x) { return x.rid !== S.rid; });
    return h.length ? h[h.length - 1] : null;
  }
  function renderResults() {
    var sc = computeScores(S.ans), code = encodeScores(sc), link = shareLink(code);
    var prevRec = previousResult(), prev = prevRec ? decodeScores(prevRec.c) : null;
    var status = {
      sent: "Your anonymous answers were saved. Thanks for helping improve the quiz.",
      sending: "Saving your answers…",
      failed: "Your answers couldn't be saved (no connection?). They're still on this device; try again below.",
      local: "This copy isn't connected to a server, so your answers stay on this device.",
      minor: "Thanks for taking it. Because you're under 18, your answers weren't saved.",
    }[S.submitted] || "";
    var html = resultsSections(sc, { drill: true, kicker: "Your results", other: compare && compare.scores, otherLabel: compare && compare.label, prev: compare ? null : prev }) +
      '<p class="scope">Early scoring: hand-set weights that will sharpen as more people take the quiz. <button type="button" class="link" id="method">How scoring works</button></p>';
    if (prev && !compare) {
      var moves = AXES.filter(function (ax) { return sc[ax] && sc[ax].n >= MIN_N && prev[ax]; })
        .map(function (ax) { return { ax: ax, d: sc[ax].v - prev[ax].v }; })
        .filter(function (m) { return Math.abs(m.d) >= 0.1; })
        .sort(function (a, b) { return Math.abs(b.d) - Math.abs(a.d); }).slice(0, 5);
      html += '<section class="results-block"><h2>Since last time</h2><p class="scope">Compared with your result from ' + esc(prevRec.d) + " (shown as a hollow dot on the bars).</p>" +
        (moves.length ? '<ul class="moves">' + moves.map(function (m) {
          return "<li><b>" + esc(META[m.ax].name) + '</b> <span class="num">' + (m.d > 0 ? "+" : "") + Math.round(100 * m.d) + "</span> toward " + esc(m.d > 0 ? META[m.ax].plus : META[m.ax].minus) + "</li>";
        }).join("") + "</ul>" : "<p>Nothing moved by more than 10 points.</p>") + "</section>";
    }
    html += '<section class="results-block share"><h2>Share and compare</h2>' +
      (link ? '<p>Send this link to show your results (it contains only your scores, not your answers):</p><div class="copyrow"><input type="text" id="sharelink" readonly value="' + esc(link) + '"><button class="btn ghost" id="copylink">Copy link</button></div>'
        : '<p>Your share code (paste it into the quiz site to show your results):</p><div class="copyrow"><input type="text" id="sharelink" readonly value="' + esc(code) + '"><button class="btn ghost" id="copylink">Copy code</button></div>') +
      '<label for="cmpin" class="scope">Compare with a friend: paste their link or code.</label><div class="copyrow"><input type="text" id="cmpin" placeholder="Their link or code" value=""><button class="btn ghost" id="cmpgo">Compare</button></div>' +
      (compare ? '<p class="scope">Showing ' + esc(compare.label) + ' as the gold dots. <button class="link" id="cmpclear">Stop comparing</button></p>' : "") +
      '<p class="scope" id="cmpmsg"></p></section>';
    var rank = priorityRanking();
    if (rank.length) {
      html += '<section class="results-block"><h2>What matters most to you</h2><ol class="rank">' + rank.slice(0, 5).map(function (r) { return "<li>" + esc(B.priorities.labels[r.d]) + "</li>"; }).join("") + "</ol></section>";
    }
    html += '<div class="notice' + (S.submitted === "failed" ? " warn" : "") + '">' + esc(status) + (S.submitted === "failed" ? ' <button class="link" id="retry">Try again</button>' : "") + "</div>";
    html += '<details class="issue-map"><summary>Your answers, topic by topic</summary><div class="map">';
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
    html += "</div></details>";
    var fit = B.about.items.filter(function (q) { return q.id === "result_fit"; })[0];
    if (fit) {
      html += '<section class="results-block"><h2>' + esc(fit.stem) + '</h2><div class="escapes">' + fit.options.map(function (o, k) {
        return '<button type="button" class="chip" data-fit="' + k + '" aria-pressed="' + (S.resultFit === k) + '">' + esc(o) + "</button>";
      }).join("") + '</div><label for="fittext" class="scope">' + esc(fit.free_text) + '</label><textarea id="fittext" maxlength="800">' + esc(S.resultFitText || "") + "</textarea></section>";
    }
    html += '<div class="nav results-actions"><span class="nav-right"><button class="btn ghost" id="copy">Copy my answers</button>' + (window.claude ? "" : '<button class="btn ghost" id="dl">Download</button>') + '</span><span class="nav-right"><button class="btn" id="retake">Take it again</button></span></div>' +
      '<textarea id="raw" readonly hidden></textarea><div id="confirm"></div>';
    show(html);
    afterResults();
    screen.querySelectorAll("[data-fit]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.resultFit = +b.getAttribute("data-fit");
        screen.querySelectorAll("[data-fit]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        save(); if (S.submitted === "sent" || S.submitted === "failed") sendFeedback();
      });
    });
    var ft = document.getElementById("fittext");
    if (ft) { ft.addEventListener("input", function () { S.resultFitText = ft.value.slice(0, 800); save(); }); ft.addEventListener("change", function () { if (S.submitted === "sent") sendFeedback(); }); }
    bind("#method", openAbout);
    bind("#retry", function () { submit().then(render); });
    bind("#copylink", function () { copyText(document.getElementById("sharelink").value, document.getElementById("copylink")); });
    bind("#cmpgo", function () {
      var c = codeFromInput(document.getElementById("cmpin").value), s = decodeScores(c);
      if (!s) { document.getElementById("cmpmsg").textContent = "That doesn't look like a results link or code. Ask them to copy it again from their results page."; return; }
      compare = { label: "Them", scores: s }; render();
    });
    bind("#cmpclear", function () { compare = null; render(); });
    bind("#copy", function () {
      var txt = JSON.stringify(payload(), null, 1), raw = document.getElementById("raw");
      copyText(txt, document.getElementById("copy"), function () { raw.hidden = false; raw.value = txt; raw.focus(); raw.select(); });
    });
    bind("#dl", function () {
      var blob = new Blob([JSON.stringify(payload(), null, 1)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "where-you-stand-" + S.code + ".json";
      document.body.appendChild(a); a.click(); a.remove();
    });
    bind("#retake", function () {
      var box = document.getElementById("confirm");
      box.innerHTML = '<div class="notice">Start a new quiz? Your results are kept on this device for comparison next time. <button class="link" id="yes">Start again</button> <button class="link" id="no">Cancel</button></div>';
      bind("#yes", function () { lsDel(KEY); compare = null; S = newState(); save(); render(); });
      bind("#no", function () { box.innerHTML = ""; });
    });
  }
  function copyText(txt, btn, fallback) {
    function done() { if (btn) { var t = btn.textContent; btn.textContent = "Copied"; setTimeout(function () { btn.textContent = t; }, 1600); } }
    function fb() {
      if (fallback) return fallback();
      var inp = document.getElementById("sharelink"); if (inp) { inp.focus(); inp.select(); }
    }
    try { navigator.clipboard.writeText(txt).then(done, fb); } catch (e) { fb(); }
  }

  // ---------- shared results (?r=) ----------
  function renderShared() {
    var sc = decodeScores(sharedCode);
    var mine = lastResult(), mineSc = mine ? decodeScores(mine.c) : null;
    var isMine = mine && mine.c === sharedCode;
    if (!sc) {
      show("<h1>That link didn't work</h1><p>The results code is incomplete or from a different version of the quiz.</p><div class=\"nav\"><span></span><button class=\"btn\" id=\"home\">Take the quiz</button></div>");
      return bind("#home", goHome);
    }
    var cmpOn = !isMine && compare && compare.shared;
    var html = resultsSections(sc, { kicker: isMine ? "Your results from " + mine.d : "Shared results", they: !isMine, other: cmpOn ? mineSc : null, otherLabel: "You" }) +
      (isMine ? '<p class="scope">Only scores are saved on this device, not answers, so this view can\'t show which answers moved each axis.</p>'
        : '<p class="scope">Someone shared their quiz results with you. Only their scores are in the link, never their answers.</p>') +
      '<div class="nav"><span class="nav-right">' + (!isMine && mineSc ? '<button class="btn ghost" id="cmp">' + (cmpOn ? "Hide my results" : "Compare with mine") + "</button>" : "") +
      '</span><span class="nav-right"><button class="btn" id="home">' + (isMine ? "Back" : "Take the quiz yourself") + "</button></span></div>";
    show(html);
    afterResults();
    bind("#cmp", function () { compare = cmpOn ? null : { shared: true }; render(); });
    bind("#home", goHome);
  }
  function goHome() {
    view = null; sharedCode = null; compare = null;
    try { if (location.search) history.replaceState(null, "", location.pathname); } catch (e) { /* ignore */ }
    if (S.phase === "done" || S.phase === "home" || S.phase === "howto") { if (S.phase !== "done") S.phase = "home"; }
    render();
  }

  // ---------- about page ----------
  var returnTo = null;
  function openAbout() { returnTo = { view: view, y: window.scrollY }; view = "about"; render(); }
  function renderAboutPage() {
    var html = '<h1>How this quiz works</h1>' +
      '<p class="lede">A personal project to build a more honest political quiz for the US: more dimensions, clearer questions, and no thumb on the scale.</p>' +
      '<section class="prose"><h2>What makes it different</h2><ul>' +
      "<li><b>Answers are positions.</b> Instead of “agree or disagree” with a vague statement, you pick the policy you actually want, with real numbers where they exist.</li>" +
      "<li><b>Scope lines and exceptions.</b> Each question says what case to picture. Edge cases (rape and incest exceptions, say, or which groups of immigrants) are asked separately, so a strict rule with exceptions isn't confused with either extreme.</li>" +
      "<li><b>Honest ways out.</b> “None of these fit” and “I don't know enough” are never scored as a middle position.</li>" +
      "<li><b>No party cues.</b> No party or politician names, and rules about power are asked for any president of either party. Some rules are asked twice, once with each side benefiting, to separate principle from partisanship.</li>" +
      "<li><b>29 candidate dimensions.</b> Trust, populism, free speech, presidential power, federalism and more get their own axes, because they cut across left and right.</li>" +
      "</ul><h2>How scoring works</h2>" +
      "<p>Each answer becomes a number from −1 (one end of the answer list) to +1 (the other end). Every question is keyed to the axes it measures and to overall left–right, with a direction. An axis score is the average of the answers keyed to it, shown as −100 to +100 once it has at least 3 answers. Follow-up cases count half as much as full questions.</p>" +
      "<p>These weights are set by hand for now. As more people take the quiz, the plan is to check which questions are the best measuring sticks and let those count more. That's why results are labeled early scoring.</p>" +
      "<p>The party comparisons are hand-placed from platforms, voting records and historians' accounts. Historical parties are only compared on issues they took positions on. Treat the match percentages as a fun guide, not a measurement.</p>" +
      "<h2>The axes</h2><dl class=\"glossary\">" +
      [B.axes.overall].concat([].concat.apply([], B.axes.families.map(function (f) { return f.axes; }))).map(function (a) {
        return "<dt>" + esc(a.name) + ' <span class="era">' + esc(a.minus) + " ↔ " + esc(a.plus) + "</span></dt><dd>" + esc(a.about || "") + "</dd>";
      }).join("") + "</dl>" +
      "<h2>The " + B.profiles.length + " comparison groups</h2>" + CATS.map(function (c) {
        return "<h3>" + esc(c.name) + '</h3><p class="scope">' + esc(c.about) + '</p><dl class="glossary">' + B.profiles.filter(function (p) { return p.cat === c.id; }).map(function (p) {
          return "<dt>" + esc(p.name) + ' <span class="era">' + esc(p.era) + "</span></dt><dd>" + esc(p.about) + "</dd>";
        }).join("") + "</dl>";
      }).join("") +
      "<h2>Privacy</h2><p>No account, and no names, emails or IP addresses. Your answers are saved with a random code so the quiz can be improved. The optional questions about you come at the end and never change your results. Share links contain only your scores. People under 18 can take the quiz, but their answers aren't saved.</p>" +
      "<h2>Limits</h2><p>This covers US politics only. The questions were drafted by one project and are still being reviewed, so some will be improved; the “Report a problem” link under each question goes straight to that list. Scores are approximate until there's enough data to calibrate them.</p>" +
      '<h2>Open source</h2><p>The questions, scoring keys and code are public: <a href="https://github.com/GriffinFoster06/political-axes" target="_blank" rel="noopener">github.com/GriffinFoster06/political-axes</a>.</p></section>' +
      '<div class="nav"><span></span><button class="btn" id="back">Back</button></div>';
    show(html);
    bind("#back", closeAbout);
  }
  function closeAbout() {
    var r = returnTo || { view: null, y: 0 };
    view = r.view; returnTo = null; render();
    window.scrollTo(0, r.y || 0);
  }

  // ---------- keyboard ----------
  document.addEventListener("keydown", function (ev) {
    var tag = (ev.target && ev.target.tagName) || "";
    if (/INPUT|TEXTAREA|SELECT/.test(tag) || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    if (keyHandler) keyHandler(ev);
    if (ev.defaultPrevented) return;
    if (ev.key === "Enter" && !/BUTTON|A|SUMMARY/.test(tag)) {
      var nx = document.getElementById("next");
      if (nx && !nx.disabled) { nx.click(); ev.preventDefault(); }
    } else if (ev.key === "ArrowLeft") {
      var bk = document.getElementById("bk");
      if (bk && !bk.hidden) { bk.click(); ev.preventDefault(); }
    }
  });

  // ---------- start ----------
  function resumeScreen(saved) {
    var tops = 0, done = Object.keys(saved.ans || {}).length;
    show('<h1>Welcome back</h1>' +
      "<p>You have " + plural(done, "answer") + " saved on this device. Pick up where you left off?</p>" +
      '<div class="cta-row"><button class="btn" id="cont">Continue</button><button class="btn ghost" id="fresh">Start over</button></div>');
    bind("#cont", function () { S = saved; render(); });
    bind("#fresh", function () { lsDel(KEY); S = newState(); save(); render(); });
    return tops;
  }
  function start() {
    applyTheme(lsGet(THEME, null));
    document.getElementById("nav-theme").addEventListener("click", function () {
      var t = effectiveDark() ? "light" : "dark"; lsSet(THEME, t); applyTheme(t);
    });
    document.getElementById("nav-about").addEventListener("click", function () { if (view !== "about") openAbout(); });
    document.getElementById("nav-home").addEventListener("click", function () {
      if (view === "about") return closeAbout();
      if (view === "shared") return goHome();
      if (S && (S.phase === "home" || S.phase === "howto")) { S.phase = "home"; render(); }
    });
    if (!B) { screen.innerHTML = '<p class="lede">The question bank didn\'t load. Rebuild with scripts/build_app.py.</p>'; return; }
    var saved = lsGet(KEY, null);
    if (saved && PHASE_RENAMES[saved.phase]) saved.phase = PHASE_RENAMES[saved.phase];
    var r = null;
    try { r = new URLSearchParams(location.search).get("r"); } catch (e) { r = null; }
    if (saved && saved.v === 1 && saved.bank === B.version) {
      S = saved;
      if (S.submitted === "sending") S.submitted = "failed";
    } else {
      S = newState(); save();
    }
    if (r) { sharedCode = r; view = "shared"; return render(); }
    if (S.phase !== "home" && S.phase !== "howto" && S.phase !== "done") return resumeScreen(S);
    render();
  }
  window.__wys = {
    state: function () { return S; }, bank: B, render: function () { render(); }, payload: function () { return payload(); },
    scores: function () { return computeScores(S.ans); }, encode: function (sc) { return encodeScores(sc); }, decode: decodeScores,
  };
  start();
})();
