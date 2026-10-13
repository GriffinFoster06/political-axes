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
    if (b) {
      var dark = effectiveDark();
      b.innerHTML = dark
        ? '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
        : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z" fill="currentColor"/></svg>';
      b.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
      b.title = dark ? "Light theme" : "Dark theme";
    }
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
    if (view === "explore") return renderExplore();
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
  // Progress bar: one segment per topic, sized by its number of questions, so you can see
  // how far into this topic you are as well as the whole quiz.
  var segKey = "";
  function paintProgress(inQuiz) {
    if (!inQuiz) { progEl.innerHTML = ""; segKey = ""; return; }
    var segs = [];
    S.queue.forEach(function (e, i) {
      if (e.k === "repeat") return;
      var last = segs[segs.length - 1];
      if (last && last.d === e.d) last.end = i; else segs.push({ d: e.d, start: i, end: i });
    });
    var key = S.rid + S.mode + S.queue.length;
    if (key !== segKey) {
      segKey = key;
      progEl.innerHTML = segs.map(function (s) { return '<span class="seg" style="flex:' + (s.end - s.start + 1) + '"><i></i></span>'; }).join("");
    }
    var pos = S.phase === "quiz" || S.phase === "break" ? S.pos : S.queue.length;
    progEl.querySelectorAll(".seg").forEach(function (el2, k) {
      var s = segs[k], f = pos > s.end ? 1 : pos < s.start ? 0 : (pos - s.start) / (s.end - s.start + 1);
      el2.firstChild.style.width = (100 * f).toFixed(1) + "%";
      el2.classList.toggle("now", pos >= s.start && pos <= s.end);
    });
  }
  function updateMeta() {
    var label = "", inQuiz = false;
    if (!view && (S.phase === "quiz" || S.phase === "break")) {
      var c = counter();
      label = S.phase === "break" ? "Break" : c.at + " of " + c.n + "|about " + minutesLeft() + " min left";
      inQuiz = true;
    } else if (!view && (S.phase === "pri" || S.phase === "aboutyou" || S.phase === "honesty")) { label = "Almost done"; inQuiz = true; }
    screen.classList.toggle("wide", !!view || S.phase === "home" || S.phase === "done");
    document.body.classList.toggle("in-quiz", !view && /quiz|break|pri|aboutyou|honesty/.test(S.phase));
    paintProgress(inQuiz);
    var parts = label.split("|");
    metaEl.innerHTML = esc(parts[0]) + (parts[1] ? '<span class="meta-more"> · ' + esc(parts[1]) + "</span>" : "");
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
  var SAMPLE_ID = "min_wage";
  function renderHome() {
    var last = lastResult(), lastSc = last ? decodeScores(last.c) : null;
    var modes = MODES.filter(function (m) { return m.id !== "full" || CFG.allowFullMode !== false; });
    var lastPt = lastSc ? { x: userPos(lastSc, dimAxes(MAP_X)), y: userPos(lastSc, dimAxes(MAP_Y)) } : null;
    var sample = B.items[SAMPLE_ID];
    var html = '<div class="home-grid"><section class="hero">' +
      "<h1>Where do you stand?</h1>" +
      '<p class="lede">A US politics quiz where you pick actual policies (a $15 minimum wage, a 37% top tax rate, 500,000 green cards a year) instead of agreeing with slogans. You get a score on ' + (AXES.length - 1) + " separate issues and a match against " + B.profiles.length + " parties, factions, presidents and ideologies.</p>" +
      "</section>" +
      '<section class="start" aria-labelledby="pick"><h2 id="pick" class="contest">Choose a length</h2>' +
      '<div class="ballot" role="radiogroup" aria-labelledby="pick">' + modes.map(function (m) {
        return '<button type="button" class="ballot-row" role="radio" data-mode="' + m.id + '" aria-checked="' + (S.mode === m.id) + '">' +
          '<span class="oval" aria-hidden="true"></span><span class="ballot-text"><b>' + esc(m.title) + "</b><span>" + esc(m.text) + "</span></span>" +
          '<span class="ballot-meta num"><span>' + m.n() + " questions</span> <span>" + esc(m.time) + "</span></span></button>";
      }).join("") + "</div>" +
      '<div class="cta-row"><button class="btn big" id="go">Start the quiz</button>' +
      (last ? '<button class="btn ghost" id="last">Your results from ' + esc(last.d) + "</button>" : "") + "</div>" +
      '<p class="fine">Your progress saves on this device, so you can stop and come back. There\'s no account, and the quiz never asks for your name or email.</p></section>' +
      '<section class="field-wrap" aria-label="Map of comparison groups"><h2 class="field-title">' + B.profiles.length + ' groups on two of the axes</h2>' +
      plotHtml({ cat: "all", hero: true, label: HERO_LABELS, user: lastPt && lastPt.x != null ? lastPt : null, userLabel: "You, last time" }) +
      '<button type="button" class="link" id="browse">See every group and axis</button></section></div>' +
      '<section class="sample" aria-labelledby="sample-h"><div class="sample-text"><h2 id="sample-h">What the questions look like</h2>' +
      "<p>This one is from the labor topic. Every question gives you concrete choices, a line saying which case to picture, and a way out if none of them fit.</p>" +
      "<p>No question names a party or a politician. Rules about presidential power are asked about any president, and a few are asked twice with each side benefiting, which separates principle from team loyalty.</p>" +
      '<p id="sample-say" class="sample-say" aria-live="polite">Try it: pick an answer to see which way it moves you.</p></div>' +
      '<div class="sample-q"><p class="contest">' + esc(topicName(sample.domain)) + '</p><div class="q-box"><p class="stem">' + esc(sample.stem) + '</p><p class="scope">' + esc(sample.scope) + "</p>" +
      '<div class="options" role="radiogroup" aria-label="Sample answers">' + sample.options.map(function (o, k) {
        return '<button type="button" class="opt" role="radio" data-sample="' + k + '" aria-checked="false"><span class="oval" aria-hidden="true"></span><span class="otext">' + esc(o) + "</span></button>";
      }).join("") + "</div></div></div></section>";
    show(html);
    wirePlot();
    screen.querySelectorAll("[data-mode]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.mode = b.getAttribute("data-mode");
        screen.querySelectorAll("[data-mode]").forEach(function (x) { x.setAttribute("aria-checked", String(x === b)); });
        save();
      });
    });
    screen.querySelectorAll("[data-sample]").forEach(function (b) {
      b.addEventListener("click", function () {
        var c = +b.getAttribute("data-sample"), K = sample.options.length, x = 2 * c / (K - 1) - 1, k = B.keying[SAMPLE_ID];
        screen.querySelectorAll("[data-sample]").forEach(function (y) { y.setAttribute("aria-checked", String(y === b)); });
        var says = Object.keys(k).filter(function (ax) { return ax !== "G" && k[ax]; }).map(function (ax) {
          var v = k[ax] * x;
          return Math.abs(v) < 0.01 ? "the middle of " + lc(META[ax].name) : "“" + (v < 0 ? META[ax].minus : META[ax].plus) + "” on " + lc(META[ax].name) + " (" + signed(v) + ")";
        });
        var g = k.G * x;
        document.getElementById("sample-say").textContent = "That answer counts toward " + says.join(" and ") +
          (Math.abs(g) < 0.01 ? ", and sits in the middle overall." : ", and " + (g < 0 ? "left" : "right") + " overall (" + signed(g) + "). Your scores average every answer like this.");
      });
    });
    bind("#go", function () { S.phase = "howto"; save(); render(); });
    bind("#browse", function () { openExplore("groups"); });
    bind("#last", function () { sharedCode = last.c; view = "shared"; render(); });
  }
  function renderHowTo() {
    var m = MODES.filter(function (x) { return x.id === S.mode; })[0] || MODES[0];
    show('<h1>Before you start</h1>' +
      '<p class="lede">' + esc(m.title) + " quiz: " + m.n() + " questions across " + B.domains.length + " topics, " + esc(m.time) + ".</p>" +
      '<div class="howto-grid"><ol class="howto">' +
      "<li><b>Fill in the answer closest to your view.</b> The quiz moves on by itself. Use Back to change an answer.</li>" +
      "<li><b>Picture the usual case.</b> The grey line under each question says which case to think about. Exceptions get their own follow-up.</li>" +
      "<li><b>Some questions set two goals against each other.</b> Pick how far you lean toward one.</li>" +
      "<li><b>You don't have to have an opinion.</b> “I don't know” and “None of these fit” are under every question, and neither counts as a middle answer.</li>" +
      "<li><b>Dotted words have a definition.</b> Tap one to read it.</li>" +
      "</ol>" +
      '<div class="demo" aria-hidden="true"><p class="contest">Example</p><div class="q-box"><p class="stem">Overall, how big should the federal government be?</p>' +
      '<div class="options"><div class="opt"><span class="oval"></span><span class="otext">Somewhat bigger</span></div><div class="opt is-on"><span class="oval"></span><span class="otext">About the same as now</span></div><div class="opt"><span class="oval"></span><span class="otext">Somewhat smaller</span></div></div></div></div></div>' +
      '<p class="scope keys-hint">On a keyboard, number keys pick an answer and ← goes back.</p>' +
      '<div class="nav"><button class="link" id="bk">← Back</button><button class="btn big" id="go">Begin</button></div>');
    bind("#bk", function () { S.phase = "home"; save(); render(); });
    bind("#go", function () {
      if (!S.queue.length || S.queueMode !== S.mode) { buildQueue(); S.queueMode = S.mode; }
      S.phase = "quiz"; spend(); S.lastBreak = S.activeMs; save(); render();
    });
  }

  // ---------- question text with tappable definitions ----------
  // Question text with definitions. In the stem and scope, a defined term is a button that shows
  // its definition. Inside an answer (itself a button) it can't be, so it's underlined and the
  // definition buttons are listed under the answers instead.
  function richFactory(it) {
    var defs = (it.definitions || []).slice(), used = {};
    function mark(text, inOption) {
      var out = esc(text);
      defs.forEach(function (d, k) {
        if (used[k]) return;
        var t = esc(d.term), i = out.toLowerCase().indexOf(t.toLowerCase());
        if (i < 0) return;
        used[k] = 1;
        var open = inOption ? '<span class="term-in">' : '<button type="button" class="term" data-def="' + k + '">';
        if (inOption) fn.optTerms.push(k);
        out = out.slice(0, i) + open + out.slice(i, i + t.length) + (inOption ? "</span>" : "</button>") + out.slice(i + t.length);
      });
      return out;
    }
    var fn = function (text) { return mark(text, false); };
    fn.opt = function (text) { return mark(text, true); };
    fn.optTerms = [];
    fn.optDefs = function () {
      if (!fn.optTerms.length) return "";
      return '<p class="optdefs">Defined: ' + fn.optTerms.map(function (k) { return '<button type="button" class="term" data-def="' + k + '">' + esc(defs[k].term) + "</button>"; }).join(", ") + "</p>";
    };
    return fn;
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
  // Where this question sits in its topic: [number in topic, visible questions in topic]
  function topicPos(e) {
    var n = 0, at = 0;
    S.queue.forEach(function (q, i) {
      if (q.k !== "item" || q.d !== e.d || !visible(q)) return;
      n++; if (i <= S.pos) at = n;
    });
    return [Math.max(1, at), n];
  }
  // The contest header: a black bar like the one over each race on a paper ballot.
  function topicLine(e, it, isRep) {
    if (isRep) return '<p class="contest"><span>Second look</span><span class="contest-n">You saw this one earlier. Answer it as you see it now.</span></p>';
    var name = domain(e.d || it.domain).name.replace(/\s*\(.*\)$/, ""), tp = topicPos(e);
    var note = e.k === "item" && firstOfTopic() ? "New topic · " + plural(tp[1], "question") : "Question " + tp[0] + " of " + tp[1];
    return '<p class="contest"><span>' + esc(name) + '</span><span class="contest-n">' + esc(note) + "</span></p>";
  }

  function renderItem(e) {
    var it = B.items[e.id], isRep = e.k === "repeat";
    var key = isRep ? e.id + "#r" : e.id;
    var a = S.ans[key] || (S.ans[key] = {});
    var dir = displayDir(it, isRep);
    a.d = dir;
    var rich = richFactory(it);
    var html = '<article class="q q-' + it.format + '">' + topicLine(e, it, isRep) + '<div class="q-box">';
    html += '<h2 class="stem">' + rich(it.stem) + "</h2>";
    if (it.scope) html += '<p class="scope">' + rich(it.scope) + "</p>";
    if (it.context) {
      if (a.cx == null) a.cx = (S.exp && S.exp.context && !isRep) ? hash(S.rid + "|cx|" + it.id) % 2 : 1;
      if (isRep) a.cx = (S.ans[it.id] && S.ans[it.id].cx != null) ? S.ans[it.id].cx : 1;
      if (a.cx) html += '<p class="context"><b>Background:</b> ' + rich(it.context) + "</p>";
    }
    var body = it.format === "exceptions" ? casesHtml(it, dir, rich) : it.format === "tradeoff" ? tradeoffHtml(it, dir, rich) : optionsHtml(it, dir, rich);
    html += body + rich.optDefs() + '<div id="defs" class="defs"></div></div>';
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
    var r = rich.opt || rich;
    return '<div class="options" role="radiogroup">' + codes.map(function (c, p) {
      var meaning = it.point_meanings ? "<small>" + esc(it.point_meanings[c]) + "</small>" : "";
      return '<button type="button" class="opt" role="radio" data-code="' + c + '" data-pos="' + p + '"><span class="oval" aria-hidden="true"></span><span class="otext">' + r(it.options[c]) + meaning + "</span>" + (p < 9 ? '<kbd class="key" aria-hidden="true">' + (p + 1) + "</kbd>" : "") + "</button>";
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
      '<div class="tug"><div class="tug-ends" aria-hidden="true"><span>' + esc(left.label) + "</span><span>" + esc(right.label) + "</span></div>" +
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

  // Exceptions: a grid like a ballot's yes/no measures. Answer names across the top, one row per case.
  function casesHtml(it, dir, rich) {
    var codes = it.options.map(function (_, k) { return k; });
    if (dir) codes.reverse();
    var cols = codes.length + 1;
    return '<div class="grid-q" style="--cols:' + cols + '"><div class="grid-head" aria-hidden="true"><span>Fill in one oval on each line</span>' +
      codes.map(function (code) { return "<span>" + esc(it.options[code]) + "</span>"; }).join("") + "<span>Not sure</span></div>" +
      '<div class="cases">' + it.cases.map(function (c) {
        return '<div class="case" data-case="' + esc(c.id) + '"><div class="case-text">' + rich(c.text) + '</div><div class="case-opts" role="radiogroup" aria-label="' + esc(c.text) + '">' +
          codes.map(function (code, p) { return '<button type="button" class="chip" role="radio" data-code="' + code + '" data-pos="' + p + '" aria-label="' + esc(it.options[code]) + '"><span class="oval" aria-hidden="true"></span><span class="chip-l">' + esc(it.options[code]) + "</span></button>"; }).join("") +
          '<button type="button" class="chip esc" data-esc="2" aria-label="Not sure"><span class="oval" aria-hidden="true"></span><span class="chip-l">Not sure</span></button></div></div>';
      }).join("") + "</div></div>";
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
    show('<article class="q q-' + q.format + '"><p class="contest"><span>' + esc(domain(e.d).name.replace(/\s*\(.*\)$/, "")) + '</span></p><div class="q-box"><h2 class="stem">' + esc(q.stem) + '</h2><p class="scope">' + esc(q.scope) + "</p>" +
      (q.format === "tradeoff" ? tradeoffHtml(fake, dir, esc) : optionsHtml(fake, dir, esc)) + "</div></article>" + navHtml(rec.c != null, false));
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
    var done = topicsInQueue().filter(function (d) { return S.queue.slice(S.pos).every(function (e) { return e.d !== d || e.k !== "item"; }); }).length;
    if (sc.G && sc.G.n >= MIN_N) preview = '<div class="break-preview">' + barHtml(META.G, sc.G, { big: true }) +
      (top ? '<p class="scope">Closest so far: <b>' + esc(top.p.name) + "</b>. That will shift as you answer more.</p>" : "") + "</div>";
    show("<h1>" + pct + "% done</h1>" +
      '<p class="lede">You\'ve finished ' + done + " of " + topicsInQueue().length + " topics. About " + minutesLeft() + " minutes to go.</p>" +
      "<p>Your answers are saved on this device, so you can close the page and pick up later.</p>" + preview +
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
    show('<p class="contest"><span>Almost done</span><span class="contest-n">Optional</span></p><h1>Which issues matter most to you?</h1>' +
      '<p class="scope">Pick up to ' + PRI_MAX + ", most important first. Tap one again to take it off. Your results will include a second match that weights these issues.</p>" +
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
    var html = '<p class="contest"><span>About you</span><span class="contest-n">Optional</span></p><h1>A few questions about you</h1><p class="scope">' + esc(B.about.intro_text) + ' All optional, and they never change your results.</p><div class="form">';
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
    show('<article class="q"><p class="contest"><span>Last question</span></p><div class="q-box"><h2 class="stem">' + esc(q.stem) + '</h2><p class="scope">' + esc(q.scope) + '</p><div class="options" role="radiogroup">' +
      q.options.map(function (o, k) { return '<button type="button" class="opt" role="radio" data-k="' + k + '" aria-checked="' + (S.honesty === k) + '"><span class="oval" aria-hidden="true"></span><span class="otext">' + esc(o) + "</span></button>"; }).join("") +
      '</div></div></article><div class="nav"><span></span><button class="btn big" id="go"' + (S.honesty == null ? " disabled" : "") + ">See my results</button></div>");
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
    Object.keys(BAL).forEach(function (ax) { if (out[ax]) balance(ax, out[ax]); });
    return out;
  }
  // Balanced axes (free speech, federalism): questions are tagged by which side the protective
  // answer helps. Left-coded and right-coded questions get equal total weight, so protecting only
  // your own side's speech doesn't read as protecting all speech. The gap is kept as `lop`.
  var BAL = B.axes.balanced || {};
  function balance(ax, o) {
    var cfg = BAL[ax], g = { L: [0, 0, 0], R: [0, 0, 0], N: [0, 0, 0] };
    o.parts.forEach(function (p) {
      var side = cfg.sides[p.cid || p.id] || "N", a = g[side];
      a[0] += p.s * p.w; a[1] += p.w; a[2]++;
    });
    if (!g.L[1] || !g.R[1]) return;
    var mL = g.L[0] / g.L[1], mR = g.R[0] / g.R[1], W = (g.L[1] + g.R[1]) / 2;
    o.raw = o.v;
    o.v = (mL * W + mR * W + g.N[0]) / (2 * W + g.N[1]);
    o.lop = { L: cfg.protect * mL, R: cfg.protect * mR, nL: g.L[2], nR: g.R[2] };
  }
  // Share codes: a version digit, then one byte per axis (0-200 = -1..+1, 255 = no score).
  // Version 2 uses the current AXES order. Version 1 (before the October 2026 split of personal
  // freedom and the new China axis) is still read, so old links and saved history keep working.
  var V1_AXES = ["G", "REDIS", "REG", "SOCINS", "HOUSING", "TRADE", "ENV", "TECH", "PRIVACY", "MORAL", "GENDERID", "RELIGION", "FAMILY",
    "EQUITY", "IMMIG", "NATION", "ORDER", "GUNS", "LIBERTY", "SPEECH", "NORMS", "VOTING", "TRUST", "ESTAB", "POP", "FED", "EDUC", "GLOBAL", "HAWK", "VALUES"];
  function encodeScores(sc) {
    var bytes = AXES.map(function (ax) { return sc[ax] && sc[ax].n >= MIN_N ? Math.round((Math.max(-1, Math.min(1, sc[ax].v)) + 1) * 100) : 255; });
    var bin = String.fromCharCode.apply(null, bytes);
    return "2" + btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function decodeScores(code) {
    var ver = code && code.charAt(0), order = ver === "2" ? AXES : ver === "1" ? V1_AXES : null;
    if (!order) return null;
    try {
      var b64 = code.slice(1).replace(/-/g, "+").replace(/_/g, "/");
      while (b64.length % 4) b64 += "=";
      var bin = atob(b64), out = {};
      order.forEach(function (ax, i) {
        var c = bin.charCodeAt(i);
        if (META[ax] && !isNaN(c) && c <= 200) out[ax] = { v: c / 100 - 1, n: MIN_N, parts: [] };
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
  function lc(t) { return String(t).split(" ").map(function (w) { return /^[A-Z]{2,}/.test(w) ? w : w.toLowerCase(); }).join(" "); }
  function clamp(v) { return Math.max(-1, Math.min(1, v)); }
  function ok(sc, ax) { return !!(sc && sc[ax] && sc[ax].n >= MIN_N); }
  function shownAxes(sc) { return AXES.filter(function (ax) { return ax !== "G" && ok(sc, ax); }); }
  var CUTS = B.axes.band_cuts || [-0.6, -0.2, 0.2, 0.6];
  var BAND_NAMES = ["Strongly ", "Leaning ", "Middle", "Leaning ", "Strongly "];
  function bandIdx(v) { return v < CUTS[0] ? 0 : v < CUTS[1] ? 1 : v <= CUTS[2] ? 2 : v <= CUTS[3] ? 3 : 4; }
  function bandName(meta, k) { return k === 2 ? "In the middle" : BAND_NAMES[k] + lc(k < 2 ? meta.minus : meta.plus); }
  function bandText(meta, v) { return meta.bands ? meta.bands[bandIdx(v)] : leanText(v, meta); }
  function confText(n) { return n >= 8 ? "Based on " + n + " answers." : n >= 5 ? "Based on " + n + " answers: a fair read." : "Based on only " + n + " answers, so treat it as rough."; }

  function barHtml(meta, sc, opt) {
    opt = opt || {};
    var v = clamp(sc.v);
    var other = opt.other && opt.other.v != null ? '<span class="dot other" style="left:' + pct(opt.other.v) + '%" title="' + esc(opt.otherLabel || "") + '"></span>' : "";
    var prev = opt.prev != null ? '<span class="dot prev" style="left:' + pct(opt.prev) + '%"></span>' : "";
    var grp = opt.group != null ? '<span class="dot grp" style="left:' + pct(opt.group) + '%" title="' + esc(opt.groupLabel || "") + '"></span>' : "";
    var you = opt.noYou ? (opt.mine != null ? '<span class="dot" style="left:' + pct(opt.mine) + '%"></span>' : "") : '<span class="dot" style="left:' + pct(v) + '%"></span>';
    var inner = '<div class="axis-head"><span class="axis-name">' + esc(meta.name) + "</span>" +
      '<span class="axis-val">' + esc(leanText(v, meta)) + ' <span class="num">' + signed(v) + "</span></span></div>" +
      '<div class="track" role="img" aria-label="' + esc(meta.name + ": " + leanText(v, meta)) + '"><span class="mid"></span>' + prev + grp + other + you + "</div>" +
      '<div class="poles"><span>' + esc(meta.minus) + "</span><span>" + esc(meta.plus) + "</span></div>";
    return '<div class="axis' + (opt.big ? " big" : "") + (opt.small ? " small" : "") + '">' + inner + "</div>";
  }
  function partText(p) {
    var it = B.items[p.id];
    if (p.cid) {
      var c = it.cases.filter(function (x) { return x.id === p.cid; })[0], ca = S && S.ans[p.cid];
      return { q: it.stem + " — " + c.text, a: ca && ca.c != null ? it.options[ca.c] : "" };
    }
    return { q: it.stem, a: S ? answerText(it, S.ans[p.id]) : "" };
  }
  function drillHtml(meta, sc, limit) {
    var parts = sc.parts.slice().sort(function (a, b) { return Math.abs(b.s * b.w) - Math.abs(a.s * a.w); });
    limit = limit || 12;
    return '<ul class="drill">' + parts.slice(0, limit).map(function (p) {
      var t = partText(p), toward = p.s > 0.05 ? meta.plus : p.s < -0.05 ? meta.minus : "the middle";
      return "<li><span class=\"dq\">" + esc(t.q) + "</span><span class=\"da\">" + esc(t.a) + '</span><span class="dt">Pulls toward ' + esc(lc(toward)) + "</span></li>";
    }).join("") + "</ul>" + (parts.length > limit ? '<p class="scope">…and ' + (parts.length - limit) + " more.</p>" : "");
  }

  // ---------- comparison groups ----------
  function profilePos(p, axes) {
    var vals = axes.filter(function (a) { return p.pos[a] != null; }).map(function (a) { return p.pos[a]; });
    return vals.length ? vals.reduce(function (s, x) { return s + x; }, 0) / vals.length : null;
  }
  function userPos(sc, axes) {
    var vals = axes.filter(function (a) { return ok(sc, a); }).map(function (a) { return sc[a].v; });
    return vals.length ? vals.reduce(function (s, x) { return s + x; }, 0) / vals.length : null;
  }
  var CATS = B.profileCats || [];
  function catName(id) { var c = CATS.filter(function (x) { return x.id === id; })[0]; return c ? c.name : "All"; }
  function catAbout(id) { var c = CATS.filter(function (x) { return x.id === id; })[0]; return c ? c.about : ""; }
  function profileMeta(p) {
    if (p.cat === "typology") return "Pew voter type";
    if (p.cat === "ideology") return "Ideology";
    if (p.cat === "president") return "President, " + p.era;
    if (p.cat === "world") return p.era + ", outside the US";
    return "US, " + p.era;
  }
  // How a group was placed: simulated members (escaped text) or hand placement ("").
  function basisText(p) {
    if (!p.basis || p.basis.kind !== "sim") return "";
    var m = p.basis.members;
    return esc(m.length === 1 ? " Placed by answering the whole quiz as " + m[0] + "." :
      " Placed from the average of simulated answers for " + m.slice(0, -1).join(", ") + " and " + m[m.length - 1] + ".");
  }
  var PROFILE = {}; B.profiles.forEach(function (p) { PROFILE[p.id] = p; });
  function profileScores(p) { var o = {}; Object.keys(p.pos).forEach(function (ax) { o[ax] = { v: p.pos[ax], n: MIN_N, parts: [] }; }); return o; }

  // axes each topic feeds, from the scoring keys
  var DOMAIN_AXES = {};
  Object.keys(B.items).forEach(function (id) {
    var it = B.items[id], k = B.keying[id];
    if (!k || !it.domain) return;
    var d = DOMAIN_AXES[it.domain] || (DOMAIN_AXES[it.domain] = {});
    Object.keys(k).forEach(function (ax) { if (ax !== "G" && k[ax]) d[ax] = (d[ax] || 0) + 1; });
  });
  function priorityWeights(top) {
    var w = {}, any = false;
    (top || []).forEach(function (d, r) {
      var axes = DOMAIN_AXES[d] || {}, tot = 0;
      Object.keys(axes).forEach(function (ax) { tot += axes[ax]; });
      Object.keys(axes).forEach(function (ax) { w[ax] = (w[ax] || 0) + (5 - r) * axes[ax] / tot; any = true; });
    });
    return any ? w : null;
  }
  // Match = 100 x (1 - weighted RMS distance / 2) over shared axes. Overall counts double;
  // with priority weights, axes behind your top issues count most.
  function matchOne(sc, pos, weights) {
    var sum = 0, wsum = 0, diffs = [];
    Object.keys(pos).forEach(function (ax) {
      if (!ok(sc, ax)) return;
      var w = weights ? (ax === "G" ? 0 : 0.15 + (weights[ax] || 0)) : (ax === "G" ? 2 : 1), d = Math.abs(sc[ax].v - pos[ax]);
      sum += w * d * d; wsum += w;
      if (ax !== "G") diffs.push({ ax: ax, d: d, you: sc[ax].v, them: pos[ax] });
    });
    if (diffs.length < 6) return null;
    var prior = weights ? 0.2 : 1, rms = Math.sqrt((sum + prior * 0.25) / (wsum + prior));
    diffs.sort(function (a, b) { return a.d - b.d; });
    return { match: Math.max(0, Math.round(100 * (1 - rms / 2))), diffs: diffs };
  }
  function profileMatches(sc, weights) {
    return B.profiles.map(function (p) {
      var m = matchOne(sc, p.pos, weights);
      if (!m) return null;
      return { p: p, match: m.match, diffs: m.diffs, agree: m.diffs.slice(0, 3), differ: m.diffs.slice(-3).reverse(), n: m.diffs.length };
    }).filter(Boolean).sort(function (a, b) { return b.match - a.match; });
  }
  function axisList(arr) {
    var names = arr.map(function (x) { return lc(META[x.ax || x].name); });
    return names.length > 1 ? names.slice(0, -1).join(", ") + " and " + names[names.length - 1] : names[0] || "";
  }

  // ---------- reading the scores ----------
  function overallLean(sc) {
    if (!ok(sc, "G")) return "";
    var g = sc.G.v;
    return Math.abs(g) < 0.1 ? "near the center overall" : leanText(g, META.G).toLowerCase().replace(":", "").replace(/^leans /, "leaning ") + " overall";
  }
  function summarySentence(sc, they) {
    if (!ok(sc, "G")) return "";
    var g = sc.G.v;
    var breaks = shownAxes(sc).filter(function (ax) { return LR_AXES.indexOf(ax) >= 0 && Math.abs(g) > 0.15 && sc[ax].v * g < 0 && Math.abs(sc[ax].v) > 0.2; });
    return (they ? "They're " : "You're ") + overallLean(sc) + (breaks.length ? ", but " + (they ? "they break" : "you break") + " from that lean on " + axisList(breaks) + "." : ".");
  }
  // A short label from the economic and cultural summaries plus the strongest cross-cutting views.
  // Same-side cells are tiered by intensity (the simulation put 41 of 42 mainstream Democrats in
  // "Progressive" without tiers), and strong economic plus personal-freedom views read as libertarian
  // whatever the cultural summary says (immigration and equity questions pull libertarians right).
  var TIER = 0.65, CENTER_TIER = 0.35;
  function archetype(sc) {
    var e = userPos(sc, ECON), c = userPos(sc, CULT);
    if (e == null || c == null) return null;
    var E = e < -0.2 ? 0 : e > 0.2 ? 2 : 1, C = c < -0.2 ? 0 : c > 0.2 ? 2 : 1, s = (e + c) / 2;
    var free = userPos(sc, ["LIBERTY", "PUBHEALTH"]);
    var core = [["", "Economic progressive", "Communitarian"], ["Social liberal", "Moderate", "Traditionalist"], ["Libertarian", "Free-market moderate", ""]][E][C];
    var coreWhy = [
      ["left on both economics and culture", "left on economics, in the middle on culture", "left on economics but traditional on culture"],
      ["in the middle on economics, left on culture", "near the middle on both economics and culture", "in the middle on economics, traditional on culture"],
      ["pro-market on economics, left on culture", "pro-market on economics, in the middle on culture", "pro-market on economics and traditional on culture"],
    ][E][C];
    if (E === 0 && C === 0) core = s <= -TIER ? "Progressive" : s <= -CENTER_TIER ? "Liberal" : "Center-left";
    else if (E === 2 && C === 2) core = s >= TIER ? "Very conservative" : s >= CENTER_TIER ? "Conservative" : "Center-right";
    else if (core !== "Moderate" && Math.max(Math.abs(e), Math.abs(c)) > TIER) core = "Committed " + core.toLowerCase();
    if (e > 0.5 && free != null && free < -0.5) {
      core = "Libertarian";
      coreWhy = "pro-market on economics and for leaving personal choices to adults";
    }
    if (core === "Center-left" || core === "Center-right") coreWhy = "mildly " + coreWhy.replace("left on both", "left of center on both").replace("pro-market on economics and traditional on culture", "right of center on both economics and culture");
    var mods = [];
    function v(ax) { return ok(sc, ax) ? sc[ax].v : 0; }
    var cand = [
      { w: Math.max(v("POP"), v("ESTAB") - 0.1), t: 0.4, word: "anti-establishment", why: "you distrust elites and institutions" },
      { w: -Math.min(v("POP"), v("ESTAB")), t: 0.45, word: "institutionalist", why: "you trust institutions and experts" },
      { w: -v("HAWK"), t: 0.5, word: "anti-war", why: "you favor military restraint" },
      { w: v("HAWK"), t: 0.5, word: "hawkish", why: "you're ready to use military force" },
      { w: v("CHINA"), t: 0.65, word: "China-hawk", why: "you'd confront China on trade, technology and security" },
      { w: v("TRADE"), t: 0.5, word: "protectionist", why: "you favor tariffs to protect industry" },
      { w: -v("TRADE"), t: 0.55, word: "free-trade", why: "you favor open trade" },
      { w: -(v("LIBERTY") + v("PUBHEALTH") + v("SPEECH") + v("PRIVACY")) / 4, t: 0.5, word: "civil-libertarian", why: "you protect speech, privacy and personal choices" },
      { w: -v("ENV"), t: 0.65, word: "green", why: "climate is a top concern for you" },
      { w: v("NORMS"), t: 0.5, word: "strong-executive", why: "you'd give presidents more room to act" },
      { w: v("FED"), t: 0.55, word: "states'-rights", why: "you want most decisions made locally" },
      { w: -v("HOUSING"), t: 0.6, word: "pro-growth", why: "you want far more housing built" },
    ];
    if (core.indexOf("ibertarian") >= 0) cand = cand.filter(function (x) { return x.word !== "civil-libertarian"; });
    cand.filter(function (x) { return x.w > x.t; }).sort(function (a, b) { return (b.w - b.t) - (a.w - a.t); }).slice(0, 2).forEach(function (x) { mods.push(x); });
    var label = mods.map(function (m) { return m.word; }).join(", ");
    label = label ? label.charAt(0).toUpperCase() + label.slice(1) + " " + core.toLowerCase() : core;
    return { label: label, why: coreWhy, mods: mods, e: e, c: c };
  }
  function consistency(sc) {
    var axes = shownAxes(sc).filter(function (ax) { return LR_AXES.indexOf(ax) >= 0; });
    var L = 0, R = 0, M = 0;
    axes.forEach(function (ax) { var v = sc[ax].v; if (v < -0.1) L++; else if (v > 0.1) R++; else M++; });
    var n = L + R, minor = Math.min(L, R), share = n ? minor / n : 0;
    var label = share < 0.12 ? "Consistent" : share < 0.3 ? "Mostly consistent" : "Cross-pressured";
    var about = {
      "Consistent": "Your views line up neatly on one side of today's left–right divide.",
      "Mostly consistent": "You mostly line up with one side, with a few real exceptions.",
      "Cross-pressured": "You mix views from both sides, which puts you between the parties' coalitions. Many Americans are like this.",
    }[label];
    return { L: L, R: R, M: M, total: axes.length, label: label, about: about };
  }
  function tensions(sc) {
    var g = ok(sc, "G") ? sc.G.v : 0, side = g < 0 ? -1 : 1;
    var off = shownAxes(sc).filter(function (ax) { return LR_AXES.indexOf(ax) >= 0 && Math.abs(g) > 0.1 && sc[ax].v * side < -0.2; })
      .sort(function (a, b) { return Math.abs(sc[b].v) - Math.abs(sc[a].v); });
    var cross = shownAxes(sc).filter(function (ax) { return LR_AXES.indexOf(ax) < 0 && Math.abs(sc[ax].v) > 0.35; })
      .sort(function (a, b) { return Math.abs(sc[b].v) - Math.abs(sc[a].v); });
    return { off: off, cross: cross };
  }
  function familyParagraphs(sc, they) {
    var you = they ? "They" : "You";
    return B.axes.families.map(function (f) {
      var axes = f.axes.filter(function (a) { return ok(sc, a.id); });
      if (!axes.length) return null;
      var strong = axes.slice().sort(function (a, b) { return Math.abs(sc[b.id].v) - Math.abs(sc[a.id].v); });
      var lines = strong.slice(0, 2).filter(function (a) { return Math.abs(sc[a.id].v) > 0.2; }).map(function (a) {
        return '<button type="button" class="link strong" data-goto="axes#ax-' + a.id + '">' + esc(a.name) + "</button> " + esc(bandText(a, sc[a.id].v));
      });
      var mid = axes.filter(function (a) { return Math.abs(sc[a.id].v) <= 0.2; }).map(function (a) { return lc(a.name); });
      if (mid.length) lines.push(esc(you + (they ? " sit" : " sit") + " near the middle on " + (mid.length > 1 ? mid.slice(0, -1).join(", ") + " and " + mid[mid.length - 1] : mid[0]) + "."));
      return { name: f.name, html: lines.join(" ") };
    }).filter(Boolean);
  }
  function domainLeans(sc) {
    var acc = {};
    ((sc.G && sc.G.parts) || []).forEach(function (p) {
      var d = B.items[p.id] && B.items[p.id].domain; if (!d) return;
      var o = acc[d] || (acc[d] = { s: 0, w: 0, n: 0 });
      o.s += p.s * p.w; o.w += p.w; o.n++;
    });
    var out = {};
    Object.keys(acc).forEach(function (d) { out[d] = { v: acc[d].s / acc[d].w, n: acc[d].n }; });
    return out;
  }
  function topicName(d) { return domain(d).name.replace(/\s*\(.*\)$/, ""); }

  // ---------- the field (any two axes) ----------
  // Map dimensions: single axes, or composites averaged over several axes. The default map is
  // overall left-right against liberty vs. authority: in the 135-politician simulation that was the
  // largest dimension left once left-right was removed (47% of the remaining variance), with
  // establishment vs. populist second (33%). The economic and cultural summaries correlated .94
  // and .99 with overall left-right, so a map of the two is mostly a diagonal.
  var DIMS = {
    auth: { name: "Liberty vs. authority", axes: ["SPEECH", "LIBERTY", "PUBHEALTH", "PRIVACY", "HAWK"], poles: ["Liberty", "Authority"],
      about: "How far government should go in policing speech, personal choices, health risks and privacy, and in using force abroad." },
    popu: { name: "Establishment vs. populist", axes: ["POP", "ESTAB", "TRUST", "NORMS", "TRADE"], poles: ["Establishment", "Populist"],
      about: "Trust in institutions, experts and the system, versus a sense that elites rig it, plus support for a strong president and tariffs." },
    econ: { name: "Economic summary", axes: ECON, poles: ["Public economy", "Market economy"], about: "" },
    cult: { name: "Cultural summary", axes: CULT, poles: ["Change", "Tradition"], about: "" },
  };
  var MAP_X = "G", MAP_Y = "auth";
  var MAP_PRESETS = [
    { id: "main", name: "Left–right × liberty", x: "G", y: "auth" },
    { id: "popu", name: "Left–right × populism", x: "G", y: "popu" },
    { id: "ec", name: "Economy × culture", x: "econ", y: "cult" },
    { id: "power", name: "Presidential power × populism", x: "NORMS", y: "POP" },
    { id: "world", name: "Engagement × force", x: "GLOBAL", y: "HAWK" },
    { id: "china", name: "China × trade", x: "TRADE", y: "CHINA" },
    { id: "trust", name: "Trust in experts × government", x: "ESTAB", y: "TRUST" },
    { id: "liberty", name: "Vice laws × health rules", x: "LIBERTY", y: "PUBHEALTH" },
  ];
  function dimAxes(k) { return DIMS[k] ? DIMS[k].axes : [k]; }
  function dimPoles(k) { return DIMS[k] ? DIMS[k].poles : [META[k].minus, META[k].plus]; }
  function dimName(k) { return DIMS[k] ? DIMS[k].name : k === "G" ? "Overall left–right" : META[k].name; }
  function dimAbout(k) {
    if (!DIMS[k]) return META[k].about;
    return (DIMS[k].about ? DIMS[k].about + " " : "") + "The average of " + DIMS[k].axes.map(function (a) { return lc(META[a].name); }).join(", ") + ".";
  }
  function textW(t) { var w = 2; for (var i = 0; i < t.length; i++) w += /[A-Z]/.test(t[i]) ? 6.4 : /[ .il']/.test(t[i]) ? 2.8 : 5; return w; }
  // o: {cat, label: {id:1} or null for all, xk, yk, user:{x,y}, userLabel, other:{x,y}, otherLabel, hero}
  function plotHtml(o) {
    var W = 360, P = 30, R = W - 2 * P, xk = o.xk || MAP_X, yk = o.yk || MAP_Y;
    var xs = dimAxes(xk), ys = dimAxes(yk), xp = dimPoles(xk), yp = dimPoles(yk);
    function X(v) { return +(P + (v + 1) / 2 * R).toFixed(1); }
    function Y(v) { return +(P + (1 - (v + 1) / 2) * R).toFixed(1); }
    var placed = [];
    if (o.user) {
      var ux0 = X(o.user.x), uy0 = Y(o.user.y), uw = 7.5 * (o.userLabel || "You").length / 2 + 5;
      placed.push({ x0: ux0 - uw, x1: ux0 + uw, y: uy0 - 17 }, { x0: ux0 - 13, x1: ux0 + 13, y: uy0 - 3 }, { x0: ux0 - 13, x1: ux0 + 13, y: uy0 + 7 });
    }
    var missing = 0;
    var pts = B.profiles.map(function (p) {
      var x = profilePos(p, xs), y = profilePos(p, ys);
      var inCat = o.cat === "all" || p.cat === o.cat;
      if (x == null || y == null) { if (inCat) missing++; return null; }
      return { p: p, cx: X(x), cy: Y(y), right: x > 0.4, on: inCat, lab: inCat && (!o.label || o.label[p.id]) };
    }).filter(Boolean).sort(function (a, b) { return (a.lab - b.lab) || (a.cy - b.cy); });
    pts.forEach(function (q) { if (q.on) placed.push({ x0: q.cx - 3.5, x1: q.cx + 3.5, y: q.cy + 3.5, dot: 1 }); });
    function free(x0, w, ty) { return !placed.some(function (b) { return x0 < b.x1 && x0 + w > b.x0 && Math.abs(ty - b.y) < (b.dot ? 7 : 10); }); }
    var dots = pts.map(function (q) {
      var label = "";
      if (q.lab) {
        var w = textW(q.p.short), ty = q.cy + 3.5, x0 = null, right = q.right;
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
    return '<figure class="plot' + (o.hero ? " hero-plot" : "") + '"><svg viewBox="0 0 ' + W + " " + W + '" role="group" aria-label="' + esc("Map of comparison groups: " + dimName(xk) + " across, " + dimName(yk) + " up and down") + '">' +
      '<rect class="field" x="' + P + '" y="' + P + '" width="' + R + '" height="' + R + '"/>' +
      '<line class="axisline" x1="' + M + '" y1="' + P + '" x2="' + M + '" y2="' + (W - P) + '"/><line class="axisline" x1="' + P + '" y1="' + M + '" x2="' + (W - P) + '" y2="' + M + '"/>' +
      '<text class="axlabel" x="' + M + '" y="' + (P - 9) + '" text-anchor="middle">' + esc(yp[1]) + "</text>" +
      '<text class="axlabel" x="' + M + '" y="' + (W - P + 18) + '" text-anchor="middle">' + esc(yp[0]) + "</text>" +
      '<text class="axlabel" x="' + (P - 9) + '" y="' + M + '" text-anchor="middle" transform="rotate(-90 ' + (P - 9) + " " + M + ')">' + esc(xp[0]) + "</text>" +
      '<text class="axlabel" x="' + (W - P + 9) + '" y="' + M + '" text-anchor="middle" transform="rotate(90 ' + (W - P + 9) + " " + M + ')">' + esc(xp[1]) + "</text>" +
      dots + odot + udot + "</svg>" +
      '<figcaption class="plotcap" aria-live="polite">' + (o.hero ? "Each dot is a party, president, movement or ideology. Tap one to see who it is." : "Tap any dot to see who it is." + (missing ? " " + plural(missing, "group") + " took no clear position on these and aren't shown." : "")) + "</figcaption></figure>";
  }
  var plotMatch = null; // id -> match %, for captions on the results page
  function wirePlot(root) {
    (root || screen).querySelectorAll(".plot").forEach(function (fig) {
      var cap = fig.querySelector(".plotcap");
      function pick(g) {
        fig.querySelectorAll(".pdot.sel").forEach(function (x) { x.classList.remove("sel"); });
        g.classList.add("sel");
        var p = PROFILE[g.getAttribute("data-pid")];
        cap.innerHTML = "<b>" + esc(p.name) + "</b> <span class=\"era\">" + esc(profileMeta(p)) + (plotMatch && plotMatch[p.id] != null ? ", " + plotMatch[p.id] + "% match" : "") + '</span><br>' + esc(p.about) + ' <button type="button" class="link" data-open-group="' + p.id + '">Full profile</button>';
        var b = cap.querySelector("[data-open-group]");
        if (b) b.addEventListener("click", function () { openExplore("group", p.id); });
      }
      fig.querySelectorAll(".pdot").forEach(function (g) {
        g.addEventListener("click", function () { pick(g); });
        g.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); pick(g); } });
      });
    });
  }

  // strip: every group (in the chosen category) placed along one axis, with you on it
  function stripHtml(ax, v, cat, other) {
    var groups = B.profiles.filter(function (p) { return p.pos[ax] != null && (cat === "all" || p.cat === cat); });
    var ticks = groups.map(function (p) { return '<span class="tick" style="left:' + pct(p.pos[ax]) + '%" title="' + esc(p.name + ": " + signed(p.pos[ax])) + '"></span>'; }).join("");
    return '<div class="strip" role="img" aria-label="' + esc(groups.length + " groups placed on " + META[ax].name) + '"><span class="mid"></span>' + ticks +
      (other != null ? '<span class="dot other" style="left:' + pct(other) + '%"></span>' : "") +
      (v != null ? '<span class="dot" style="left:' + pct(v) + '%"></span>' : "") + "</div>" +
      '<div class="poles"><span>' + esc(META[ax].minus) + "</span><span>" + esc(META[ax].plus) + "</span></div>";
  }
  function nearestOnAxis(ax, v, cat, n) {
    return B.profiles.filter(function (p) { return p.pos[ax] != null && (cat === "all" || p.cat === cat); })
      .sort(function (a, b) { return Math.abs(a.pos[ax] - v) - Math.abs(b.pos[ax] - v); }).slice(0, n || 3);
  }
  function bandLadderHtml(meta, v, other) {
    if (!meta.bands) return "";
    var k = v == null ? -1 : bandIdx(v), ko = other == null ? -1 : bandIdx(other);
    return '<ol class="ladder">' + meta.bands.map(function (t, i) {
      return '<li class="' + (i === k ? "here" : "") + (i === ko ? " there" : "") + '"><b>' + esc(bandName(meta, i)) + "</b><span>" + esc(t) + "</span></li>";
    }).join("") + "</ol>";
  }

  // ---------- the report ----------
  var TABS = [
    { id: "summary", name: "Summary" },
    { id: "matches", name: "Matches" },
    { id: "map", name: "Map" },
    { id: "axes", name: "Axes" },
    { id: "topics", name: "Topics", own: true },
    { id: "answers", name: "Answers", own: true },
  ];
  var resTab = "summary", resCat = "all", showAll = false, mapX = MAP_X, mapY = MAP_Y, openGroup = null, ctx = null;

  // ctx: {sc, they, own, other, otherLabel, prev, prevRec, kicker}
  function reportHeadHtml(c) {
    var sc = c.sc, matches = profileMatches(sc), top = matches[0], arch = archetype(sc), g = sc.G;
    return '<header class="res-head">' + (c.kicker ? '<p class="kicker">' + esc(c.kicker) + "</p>" : "") +
      (top ? "<h1>" + (c.they ? "Their" : "Your") + " closest match is " + esc(top.p.name) + "</h1>" : "<h1>" + (c.they ? "Where they stand" : "Where you stand") + "</h1>") +
      (arch ? '<p class="label-line">' + (c.they ? "They come" : "You come") + ' out as <mark class="hl">' + esc(arch.label.toLowerCase()) + "</mark></p>" : "") +
      (top ? '<p class="res-sub"><b class="num">' + top.match + "% match.</b> " + esc(profileMeta(top.p)) + ". " + esc(top.p.about) + "</p>" : "") +
      (ok(sc, "G") ? '<div class="res-overall"><p class="summary">' + esc(summarySentence(sc, c.they)) + "</p>" + barHtml(META.G, g, { big: true, other: c.other && c.other.G, otherLabel: c.otherLabel, prev: c.prev && c.prev.G ? c.prev.G.v : null }) + "</div>" : "") +
      "</header>";
  }
  function tabsHtml(c) {
    return '<nav class="tabs" role="tablist" aria-label="Report sections">' + TABS.filter(function (t) { return c.own || !t.own; }).map(function (t) {
      return '<button type="button" role="tab" class="tab" data-tab="' + t.id + '" aria-selected="' + (resTab === t.id) + '">' + esc(t.name) + "</button>";
    }).join("") + "</nav>";
  }
  function renderPanel() {
    var box = document.getElementById("panel");
    if (!box || !ctx) return;
    if (!ctx.own && (resTab === "topics" || resTab === "answers")) resTab = "summary";
    var fn = { summary: panelSummary, matches: panelMatches, map: panelMap, axes: panelAxes, topics: panelTopics, answers: panelAnswers }[resTab];
    box.innerHTML = fn(ctx);
    screen.querySelectorAll(".tab").forEach(function (t) { t.setAttribute("aria-selected", String(t.getAttribute("data-tab") === resTab)); });
    wirePanel(box);
  }
  function goTab(t, anchor) {
    resTab = t; renderPanel();
    var tabs = screen.querySelector(".tabs");
    if (anchor) { var el2 = document.getElementById(anchor); if (el2) { if (el2.tagName === "DETAILS") el2.open = true; el2.scrollIntoView({ block: "start" }); return; } }
    if (tabs && tabs.getBoundingClientRect().top < 0) tabs.scrollIntoView({ block: "start" });
  }
  function wirePanel(box) {
    box.querySelectorAll("[data-goto]").forEach(function (b) {
      b.addEventListener("click", function () { var g = b.getAttribute("data-goto").split("#"); goTab(g[0], g[1]); });
    });
    box.querySelectorAll("[data-cat]").forEach(function (b) {
      b.addEventListener("click", function () { resCat = b.getAttribute("data-cat"); showAll = false; renderPanel(); });
    });
    box.querySelectorAll("[data-open-group]").forEach(function (b) {
      b.addEventListener("click", function () { openExplore("group", b.getAttribute("data-open-group")); });
    });
    box.querySelectorAll("[data-open-axis]").forEach(function (b) {
      b.addEventListener("click", function () { openExplore("axis", b.getAttribute("data-open-axis")); });
    });
    var sa = box.querySelector("#showall"); if (sa) sa.addEventListener("click", function () { showAll = true; renderPanel(); });
    var sl = box.querySelector("#showless"); if (sl) sl.addEventListener("click", function () { showAll = false; renderPanel(); });
    box.querySelectorAll("[data-preset]").forEach(function (b) {
      b.addEventListener("click", function () { var p = MAP_PRESETS.filter(function (x) { return x.id === b.getAttribute("data-preset"); })[0]; mapX = p.x; mapY = p.y; renderPanel(); });
    });
    var sx = box.querySelector("#mapx"), sy = box.querySelector("#mapy");
    if (sx) sx.addEventListener("change", function () { mapX = sx.value; renderPanel(); });
    if (sy) sy.addEventListener("change", function () { mapY = sy.value; renderPanel(); });
    var sw = box.querySelector("#mapswap"); if (sw) sw.addEventListener("click", function () { var t = mapX; mapX = mapY; mapY = t; renderPanel(); });
    var cp = box.querySelector("#copy");
    if (cp) cp.addEventListener("click", function () {
      var txt = JSON.stringify(payload(), null, 1), raw = document.getElementById("raw");
      copyText(txt, cp, function () { raw.hidden = false; raw.value = txt; raw.focus(); raw.select(); });
    });
    var dl = box.querySelector("#dl");
    if (dl) dl.addEventListener("click", function () {
      var blob = new Blob([JSON.stringify(payload(), null, 1)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "where-you-stand-" + S.code + ".json";
      document.body.appendChild(a); a.click(); a.remove();
    });
    plotMatch = {}; profileMatches(ctx.sc).forEach(function (m) { plotMatch[m.p.id] = m.match; });
    wirePlot(box);
  }
  function chipsHtml() {
    return '<div class="chips" role="tablist" aria-label="Filter comparison groups">' + [{ id: "all", name: "All" }].concat(CATS).map(function (c) {
      return '<button type="button" class="chip" role="tab" data-cat="' + c.id + '" aria-selected="' + (resCat === c.id) + '">' + esc(c.name) + "</button>";
    }).join("") + "</div>";
  }
  function you(c) { return c.they ? "they" : "you"; }
  function You(c) { return c.they ? "They" : "You"; }

  // --- summary ---
  function panelSummary(c) {
    var sc = c.sc, arch = archetype(sc), con = consistency(sc), ten = tensions(sc), html = "";
    var matches = profileMatches(sc);
    if (arch) {
      html += '<section class="block"><h2>' + (c.they ? "Their" : "Your") + " political profile</h2>" +
        '<p class="lede">The label means ' + esc(c.they ? "they're " : "you're ") + esc(arch.why) +
        (arch.mods.length ? ", and " + esc(arch.mods.map(function (m) { return c.they ? m.why.replace(/\byou're\b/g, "they're").replace(/\byou\b/g, "they").replace(/\byour\b/g, "their") : m.why; }).join(", and ")) : "") + ".</p>" +
        '<dl class="fam-list">' + familyParagraphs(sc, c.they).map(function (f) {
          return "<div><dt>" + esc(f.name) + "</dt><dd>" + f.html + "</dd></div>";
        }).join("") + "</dl></section>";
    }
    if (con.total) {
      var segs = [["l", con.L], ["m", con.M], ["r", con.R]].map(function (s) { return s[1] ? '<span class="seg ' + s[0] + '" style="flex:' + s[1] + '"></span>' : ""; }).join("");
      html += '<section class="block"><h2>How consistent ' + you(c) + " are</h2>" +
        '<p class="kpi">' + esc(con.label) + '</p><p class="kpi-about">' + esc(con.about) + "</p>" +
        '<div class="meter" aria-hidden="true">' + segs + "</div>" +
        '<p class="meter-key"><span><i class="k l"></i>Left side: ' + con.L + "</span><span><i class=\"k m\"></i>Middle: " + con.M + '</span><span><i class="k r"></i>Right side: ' + con.R + "</span></p>" +
        '<p class="scope">Counted over the ' + con.total + " axes that split along today's left–right line.</p>";
      if (ten.off.length) {
        html += "<h3>Where " + you(c) + " break from " + (c.they ? "their" : "your") + " side</h3><ul class=\"tension\">" + ten.off.map(function (ax) {
          return '<li><button type="button" class="link" data-goto="axes#ax-' + ax + '">' + esc(META[ax].name) + "</button> " + esc(bandText(META[ax], sc[ax].v)) + "</li>";
        }).join("") + "</ul>";
      }
      if (ten.cross.length) {
        html += "<h3>Views that cut across left and right</h3><ul class=\"tension\">" + ten.cross.slice(0, 5).map(function (ax) {
          return '<li><button type="button" class="link" data-goto="axes#ax-' + ax + '">' + esc(META[ax].name) + "</button> " + esc(bandText(META[ax], sc[ax].v)) + "</li>";
        }).join("") + "</ul>";
      }
      html += "</section>";
    }
    if (matches.length) {
      html += '<section class="block"><h2>Closest in each category</h2><table class="cat-table"><tbody>' + CATS.map(function (cat) {
        var m = matches.filter(function (x) { return x.p.cat === cat.id; });
        if (!m.length) return "";
        return '<tr><th scope="row">' + esc(cat.name) + '</th><td><button type="button" class="link strong" data-open-group="' + m[0].p.id + '">' + esc(m[0].p.name) + '</button><span class="then">' +
          (m[1] ? "then " + esc(m[1].p.name) + " " + m[1].match + "%" + (m[2] ? ", " + esc(m[2].p.name) + " " + m[2].match + "%" : "") : "") + '</span></td><td class="num pct">' + m[0].match + "%</td></tr>";
      }).join("") + "</tbody></table>" +
        '<p class="scope">Furthest from ' + you(c) + ": <b>" + esc(matches[matches.length - 1].p.name) + "</b> (" + matches[matches.length - 1].match + "%). <button type=\"button\" class=\"link\" data-goto=\"matches\">All " + matches.length + " matches, with head-to-head comparisons</button></p></section>";
    }
    var weights = !c.they && c.own ? priorityWeights(S.pri && S.pri.top) : null;
    if (weights) {
      var wm = profileMatches(sc, weights);
      html += '<section class="block"><h2>On the issues you care about most</h2><p>You ranked ' + esc(S.pri.top.map(function (d) { return B.priorities.labels[d]; }).join("; ")) + ". Counting the axes behind those issues most heavily, you're closest to:</p>" +
        '<ol class="mini-list">' + wm.slice(0, 3).map(function (m) { return '<li><button type="button" class="link" data-open-group="' + m.p.id + '">' + esc(m.p.name) + "</button> <span class=\"era\">" + m.match + "%</span></li>"; }).join("") + "</ol></section>";
    }
    var strongest = shownAxes(sc).sort(function (a, b) { return Math.abs(sc[b].v) - Math.abs(sc[a].v); }).slice(0, 4);
    if (strongest.length) {
      html += '<section class="block"><h2>Strongest views</h2><ol class="strong-list">' + strongest.map(function (ax) {
        return '<li><span class="num sv">' + signed(sc[ax].v) + '</span><span><button type="button" class="link strong" data-goto="axes#ax-' + ax + '">' + esc(META[ax].name) + "</button> " + esc(bandText(META[ax], sc[ax].v)) + "</span></li>";
      }).join("") + "</ol></section>";
    }
    if (c.prev && !c.other) {
      var moves = AXES.filter(function (ax) { return ok(sc, ax) && c.prev[ax]; })
        .map(function (ax) { return { ax: ax, d: sc[ax].v - c.prev[ax].v }; })
        .filter(function (m) { return Math.abs(m.d) >= 0.1; })
        .sort(function (a, b) { return Math.abs(b.d) - Math.abs(a.d); }).slice(0, 6);
      var pm = profileMatches(c.prev)[0];
      html += '<section class="block"><h2>Since last time</h2><p class="scope">Compared with your result from ' + esc(c.prevRec.d) + " (the dashed dots on the bars)." + (pm ? " Then your closest match was " + esc(pm.p.name) + "." : "") + "</p>" +
        (moves.length ? '<ul class="moves">' + moves.map(function (m) {
          return "<li><b>" + esc(META[m.ax].name) + '</b> <span class="num">' + (m.d > 0 ? "+" : "") + Math.round(100 * m.d) + "</span> toward " + esc(lc(m.d > 0 ? META[m.ax].plus : META[m.ax].minus)) + "</li>";
        }).join("") + "</ul>" : "<p>Nothing moved by more than 10 points.</p>") + "</section>";
    }
    return html;
  }

  // --- matches ---
  function h2hHtml(c, m) {
    return '<ul class="h2h">' + m.diffs.map(function (d) {
      var meta = META[d.ax], verdict = d.d < 0.25 ? "Agree" : d.d < 0.6 ? "Close" : d.d < 1 ? "Differ" : "Opposed";
      return '<li><span class="h2h-name">' + esc(meta.name) + '</span><span class="h2h-v v-' + verdict.toLowerCase() + '">' + verdict + "</span>" +
        '<span class="track mini"><span class="mid"></span><span class="dot grp" style="left:' + pct(d.them) + '%"></span><span class="dot" style="left:' + pct(d.you) + '%"></span></span></li>';
    }).join("") + "</ul>";
  }
  function panelMatches(c) {
    var sc = c.sc, matches = profileMatches(sc);
    if (!matches.length) return '<p class="scope">Not enough answers yet to compare.</p>';
    var list = resCat === "all" ? matches : matches.filter(function (m) { return m.p.cat === resCat; });
    var lim = showAll ? list.length : 10;
    var html = '<section class="block"><h2>Who ' + you(c) + "'re closest to</h2>" + chipsHtml() +
      '<p class="scope cat-about">' + esc(resCat === "all" ? "All " + matches.length + " groups that can be compared on at least six axes, closest first." : catAbout(resCat)) + "</p>" +
      '<p class="legend"><span class="dot-key you"></span>' + esc(You(c)) + ' <span class="dot-key grp"></span>The group</p>' +
      '<ol class="profiles">' + list.slice(0, lim).map(function (m, k) {
        var open = openGroup === m.p.id;
        return '<li><details' + (open ? " open" : "") + '><summary><span class="prof-rank">' + (k + 1) + '</span><span class="prof-main"><span class="prof-head"><b>' + esc(m.p.name) + '</b><span class="era">' + esc(profileMeta(m.p)) + '</span></span><span class="matchbar"><span style="width:' + m.match + '%"></span></span></span><span class="match">' + m.match + "%</span></summary>" +
          '<div class="prof-body"><p>' + esc(m.p.about) + basisText(m.p) + "</p>" +
          "<p><b>Closest on</b> " + esc(axisList(m.agree)) + ". <b>Furthest on</b> " + esc(axisList(m.differ)) + ".</p>" +
          "<p class=\"scope\">Compared on " + m.n + " axes, closest first:</p>" + h2hHtml(c, m) +
          '<button type="button" class="link" data-open-group="' + m.p.id + '">Full profile of ' + esc(m.p.name) + "</button></div></details></li>";
      }).join("") + "</ol>" +
      (list.length > lim ? '<button type="button" class="link" id="showall">Show all ' + list.length + "</button>" : "") +
      (showAll && list.length > 10 ? '<button type="button" class="link" id="showless">Show fewer</button>' : "") +
      '<p class="scope">Match = 100 × (1 − typical distance ÷ 2) across every axis both sides have a position on, with the overall left–right score counted double. Groups placed on fewer axes get a small penalty so they can\'t win on a handful of issues.</p></section>';
    return html;
  }

  // --- map ---
  function panelMap(c) {
    var sc = c.sc, matches = profileMatches(sc), top = {};
    matches.slice(0, 5).forEach(function (m) { top[m.p.id] = 1; });
    var xs = dimAxes(mapX), ys = dimAxes(mapY);
    var ux = userPos(sc, xs), uy = userPos(sc, ys);
    var ox = c.other ? userPos(c.other, xs) : null, oy = c.other ? userPos(c.other, ys) : null;
    var opts = ["G", "auth", "popu", "econ", "cult"].concat(AXES.filter(function (a) { return a !== "G"; })).map(function (k) { return [k, dimName(k)]; });
    function sel(id, cur) {
      return '<select id="' + id + '">' + opts.map(function (o) {
        var has = userPos(sc, dimAxes(o[0])) != null;
        return '<option value="' + o[0] + '"' + (o[0] === cur ? " selected" : "") + (has ? "" : " disabled") + ">" + esc(o[1] + (has ? "" : " (not enough answers)")) + "</option>";
      }).join("") + "</select>";
    }
    if (userPos(sc, xs) == null || userPos(sc, ys) == null) { mapX = MAP_X; mapY = MAP_Y; xs = dimAxes(mapX); ys = dimAxes(mapY); if (userPos(sc, ys) == null) { mapY = "econ"; ys = ECON; } ux = userPos(sc, xs); uy = userPos(sc, ys); }
    var html = '<section class="block"><h2>The map</h2><p class="scope">Pick any two axes. Each dot is a comparison group; ' + you(c) + "'re the yellow dot.</p>" +
      '<div class="presets">' + MAP_PRESETS.filter(function (p) { return userPos(sc, dimAxes(p.x)) != null && userPos(sc, dimAxes(p.y)) != null; }).map(function (p) { return '<button type="button" class="chip pill" data-preset="' + p.id + '" aria-pressed="' + (p.x === mapX && p.y === mapY) + '">' + esc(p.name) + "</button>"; }).join("") + "</div>" +
      '<div class="map-controls"><label>Across ' + sel("mapx", mapX) + '</label><button type="button" class="link" id="mapswap" aria-label="Swap axes">Swap</button><label>Up and down ' + sel("mapy", mapY) + "</label></div>" +
      chipsHtml() +
      '<div class="compare-grid"><div>' + (ux != null && uy != null ? plotHtml({ cat: resCat, label: resCat === "all" ? top : null, xk: mapX, yk: mapY, user: { x: ux, y: uy }, userLabel: c.they ? "Them" : "You", other: ox != null && oy != null ? { x: ox, y: oy } : null, otherLabel: c.otherLabel }) : '<p class="scope">' + esc(You(c)) + " don't have a score on one of these axes yet.</p>") + "</div>" +
      '<div class="map-notes">' + (ux != null && uy != null ? "<h3>" + esc(dimName(mapX)) + "</h3><p>" + esc(dimAbout(mapX)) + "</p>" +
        (!DIMS[mapX] ? "<p><b>" + esc(You(c)) + ":</b> " + esc(bandText(META[mapX], ux)) + "</p>" : "") +
        "<h3>" + esc(dimName(mapY)) + "</h3><p>" + esc(dimAbout(mapY)) + "</p>" +
        (!DIMS[mapY] ? "<p><b>" + esc(You(c)) + ":</b> " + esc(bandText(META[mapY], uy)) + "</p>" : "") +
        "<h3>Nearest on this map</h3><ol class=\"mini-list\">" + B.profiles.filter(function (p) { return (resCat === "all" || p.cat === resCat) && profilePos(p, xs) != null && profilePos(p, ys) != null; })
          .map(function (p) { return { p: p, d: Math.hypot(profilePos(p, xs) - ux, profilePos(p, ys) - uy) }; })
          .sort(function (a, b) { return a.d - b.d; }).slice(0, 5)
          .map(function (o) { return '<li><button type="button" class="link" data-open-group="' + o.p.id + '">' + esc(o.p.name) + '</button> <span class="era">' + esc(profileMeta(o.p)) + "</span></li>"; }).join("") + "</ol>" : "") + "</div></div></section>";
    return html;
  }

  // --- axes ---
  // One dense row per axis (name, track, value), each opening to the full explanation.
  function axisRowHtml(a, o, c) {
    var v = clamp(o.v), oth = c.other && c.other[a.id] ? c.other[a.id].v : null, prev = c.prev && !c.other && c.prev[a.id] ? c.prev[a.id].v : null;
    return '<span class="ar-name">' + esc(a.name) + '</span>' +
      '<span class="ar-track"><span class="track" role="img" aria-label="' + esc(a.name + ": " + leanText(v, a)) + '"><span class="mid"></span>' +
      (prev != null ? '<span class="dot prev" style="left:' + pct(prev) + '%"></span>' : "") +
      (oth != null ? '<span class="dot other" style="left:' + pct(oth) + '%"></span>' : "") +
      '<span class="dot" style="left:' + pct(v) + '%"></span></span><span class="poles"><span>' + esc(a.minus) + "</span><span>" + esc(a.plus) + "</span></span></span>" +
      '<span class="ar-val"><span class="num">' + signed(v) + "</span> " + esc(leanText(v, a).replace(/^(Leans|Moderately:|Strongly:|Very strongly:) ?/, "")) + "</span>";
  }
  function panelAxes(c) {
    var sc = c.sc, html = '<section class="block"><h2>All ' + shownAxes(sc).length + " axes</h2>" +
      '<p class="scope">Scores run from −100 to +100. Open an axis for what the score means, where every group stands' + (c.own ? ", and which of your answers moved it" : "") + "." +
      (c.other ? ' <span class="legend"><span class="dot-key you"></span>' + esc(You(c)) + ' <span class="dot-key other"></span>' + esc(c.otherLabel) + "</span>" : "") +
      (c.prev && !c.other ? ' <span class="legend"><span class="dot-key you"></span>Now <span class="dot-key prev"></span>Last time</span>' : "") + "</p>" + chipsHtml() + "</section>";
    B.axes.families.forEach(function (f) {
      var rows = f.axes.filter(function (a) { return ok(sc, a.id); });
      if (!rows.length) return;
      html += '<section class="family"><h3>' + esc(f.name) + "</h3>" + rows.map(function (a) {
        var v = sc[a.id].v, near = nearestOnAxis(a.id, v, resCat, 3), oth = c.other && c.other[a.id] ? c.other[a.id].v : null;
        return '<details class="axis-card" id="ax-' + a.id + '"><summary class="axis-row">' + axisRowHtml(a, sc[a.id], c) + "</summary>" +
          '<div class="axis-body"><p class="band-now"><b>' + esc(You(c)) + ":</b> " + esc(bandText(a, v)) + "</p>" +
          lopHtml(a.id, sc[a.id], c) +
          '<p class="scope">' + esc(a.about) + (c.own ? " " + confText(sc[a.id].n) : "") + "</p>" +
          '<div class="axis-cols"><div><h4>The range on this axis</h4>' + bandLadderHtml(a, v, oth) + "</div>" +
          "<div><h4>Where the groups stand</h4>" + stripHtml(a.id, v, resCat, oth) +
          '<p class="scope">Nearest to ' + you(c) + ": " + near.map(function (p) { return '<button type="button" class="link" data-open-group="' + p.id + '">' + esc(p.name) + "</button> (" + signed(p.pos[a.id]) + ")"; }).join(", ") + ".</p>" +
          '<button type="button" class="link" data-open-axis="' + a.id + '">Every group on this axis</button></div></div>' +
          (c.own && sc[a.id].parts && sc[a.id].parts.length ? "<h4>The answers that moved it, strongest first</h4>" + drillHtml(a, sc[a.id], 15) : "") +
          "</div></details>";
      }).join("") + "</section>";
    });
    return html;
  }

  // For balanced axes: how evenly the protective answers fall across the two sides.
  function lopHtml(ax, o, c) {
    var cfg = BAL[ax];
    if (!cfg || !o || !o.lop || o.lop.nL < 2 || o.lop.nR < 2) return "";
    var pL = Math.round(50 * (o.lop.L + 1)), pR = Math.round(50 * (o.lop.R + 1)), d = o.lop.L - o.lop.R;
    var more = d > 0 ? cfg.note_L : cfg.note_R, less = d > 0 ? cfg.note_R : cfg.note_L;
    var head = Math.abs(d) < 0.4 ? "Even-handed." : "Lopsided.";
    var body = Math.abs(d) < 0.4
      ? You(c) + " protect " + cfg.note_L + " and " + cfg.note_R + " about equally"
      : You(c) + " protect " + more + " much more than " + less;
    return '<p class="lop"><b>' + head + "</b> " + esc(body + ": " + (d > 0 ? pL : pR) + " vs " + (d > 0 ? pR : pL) + " on a 0–100 protection scale. The score above counts both sides equally.") + "</p>";
  }

  // --- topics ---
  function panelTopics(c) {
    var sc = c.sc, leans = domainLeans(sc);
    var ranked = (S.pri && S.pri.top) || [];
    var html = '<section class="block"><h2>Topic by topic</h2><p class="scope">How you answered on each of the ' + B.domains.length + " topics, and which way those answers lean on today's left–right line. Open a topic to see every answer and the axes it feeds.</p></section><div class=\"topics\">";
    B.domains.forEach(function (dm) {
      var lean = leans[dm.id], rows = "", n = 0;
      B.order[dm.id].forEach(function (id) {
        var it = B.items[id];
        if (it.format === "exceptions") {
          var parts = it.cases.map(function (cs) {
            var ca = S.ans[cs.id]; if (!ca || (ca.c == null && !ca.e)) return null;
            return "<li>" + esc(cs.text) + ": <b>" + esc(ca.c != null ? it.options[ca.c] : "not sure") + "</b></li>";
          }).filter(Boolean);
          if (parts.length) { n++; rows += "<dt>" + esc(it.stem) + "</dt><dd><ul>" + parts.join("") + "</ul></dd>"; }
          return;
        }
        var txt = answerText(it, S.ans[id]);
        if (!txt) return;
        n++; rows += "<dt>" + esc(it.stem) + "</dt><dd>" + esc(txt) + "</dd>";
      });
      if (!n) return;
      var axes = Object.keys(DOMAIN_AXES[dm.id] || {}).filter(function (ax) { return ok(sc, ax); });
      var r = ranked.indexOf(dm.id);
      html += '<details class="topic-card" id="tp-' + dm.id + '"><summary><span class="tp-head"><b>' + esc(topicName(dm.id)) + "</b>" + (r >= 0 ? '<span class="tag">Your #' + (r + 1) + " issue</span>" : "") + '<span class="era">' + plural(n, "answer") + "</span></span>" +
        (lean ? '<span class="tp-lean">' + esc(leanText(lean.v, META.G)) + '</span><span class="track mini"><span class="mid"></span><span class="dot" style="left:' + pct(lean.v) + '%"></span></span>' : '<span class="tp-lean">Not on the left–right line</span>') + "</summary>" +
        '<div class="tp-body"><dl class="answers">' + rows + "</dl>" +
        (axes.length ? "<h4>Axes this topic feeds</h4><ul class=\"mini-axes\">" + axes.map(function (ax) {
          return '<li><button type="button" class="link" data-goto="axes#ax-' + ax + '">' + esc(META[ax].name) + "</button> " + esc(leanText(sc[ax].v, META[ax])) + ' <span class="num">' + signed(sc[ax].v) + "</span></li>";
        }).join("") + "</ul>" : "") + "</div></details>";
    });
    return html + "</div>";
  }

  // --- answers ---
  function panelAnswers(c) {
    var html = "";
    var rank = priorityRanking();
    if (rank.length) html += '<section class="block"><h2>What matters most to you</h2><ol class="rank">' + rank.map(function (r) { return '<li><button type="button" class="link" data-goto="topics#tp-' + r.d + '">' + esc(B.priorities.labels[r.d]) + "</button></li>"; }).join("") + "</ol></section>";
    var counts = { a: 0, dk: 0, nf: 0, skip: 0 };
    S.queue.forEach(function (e) {
      if (e.k !== "item" || !visible(e)) return;
      var it = B.items[e.id];
      if (it.format === "exceptions") return;
      var a = S.ans[e.id];
      if (!a || (a.c == null && !a.e && !a.t)) counts.skip++; else if (a.e === 2) counts.dk++; else if (a.e === 1) counts.nf++; else counts.a++;
    });
    html += '<section class="block"><h2>Your answers</h2><p>' + counts.a + " answered, " + counts.dk + " “I don't know”, " + counts.nf + " “none of these fit”, " + counts.skip + " skipped. Answers that weren't a position never count toward a score.</p>" +
      '<div class="cta-row"><button class="btn ghost" id="copy">Copy my answers</button>' + (window.claude ? "" : '<button class="btn ghost" id="dl">Download</button>') + '</div><textarea id="raw" readonly hidden></textarea>' +
      '<p class="scope">Every answer, topic by topic, is under <button type="button" class="link" data-goto="topics">Topics</button>.</p></section>';
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
  function wireReport() {
    screen.querySelectorAll(".tab").forEach(function (t) { t.addEventListener("click", function () { goTab(t.getAttribute("data-tab")); }); });
    renderPanel();
  }
  function renderResults() {
    var sc = computeScores(S.ans), code = encodeScores(sc), link = shareLink(code);
    var prevRec = previousResult(), prev = prevRec ? decodeScores(prevRec.c) : null;
    ctx = { sc: sc, own: true, they: false, other: compare && compare.scores, otherLabel: compare && compare.label, prev: compare ? null : prev, prevRec: prevRec, kicker: "Your results" };
    var status = {
      sent: "Your anonymous answers were saved. Thanks for helping improve the quiz.",
      sending: "Saving your answers…",
      failed: "Your answers couldn't be saved (no connection?). They're still on this device; try again below.",
      local: "This copy isn't connected to a server, so your answers stay on this device.",
      minor: "Thanks for taking it. Because you're under 18, your answers weren't saved.",
    }[S.submitted] || "";
    var html = reportHeadHtml(ctx) + tabsHtml(ctx) + '<div id="panel" class="panel" role="tabpanel"></div>';
    html += '<section class="results-block share"><div class="share-grid"><div class="share-col"><h2>Share your results</h2>' +
      (link ? '<p class="scope">The link carries your scores only, never your answers.</p><div class="copyrow"><input type="text" id="sharelink" readonly value="' + esc(link) + '"><button class="btn ghost" id="copylink">Copy link</button></div>'
        : '<p class="scope">Paste this code into the quiz site to show your results. It carries your scores only.</p><div class="copyrow"><input type="text" id="sharelink" readonly value="' + esc(code) + '"><button class="btn ghost" id="copylink">Copy code</button></div>') +
      '</div><div class="share-col"><h2>Compare with a friend</h2><label for="cmpin" class="scope">Paste their link or code. Their scores show as magenta dots throughout the report.</label><div class="copyrow"><input type="text" id="cmpin" placeholder="Their link or code" value=""><button class="btn ghost" id="cmpgo">Compare</button></div></div></div>' +
      (compare ? '<p class="scope">Comparing with ' + esc(compare.label) + ". " + (function () { var m = matchOne(sc, scoresToPos(compare.scores)); return m ? "You two are a " + m.match + "% match." : ""; })() + ' <button class="link" id="cmpclear">Stop comparing</button></p>' : "") +
      '<p class="scope" id="cmpmsg"></p></section>';
    if (status) html += '<p class="notice' + (S.submitted === "failed" ? " warn" : "") + '">' + esc(status) + (S.submitted === "failed" ? ' <button class="link" id="retry">Try again</button>' : "") + "</p>";
    var fit = B.about.items.filter(function (q) { return q.id === "result_fit"; })[0];
    if (fit) {
      html += '<section class="results-block feedback"><h2>' + esc(fit.stem) + '</h2><div class="fit-row" role="radiogroup">' + fit.options.map(function (o, k) {
        return '<button type="button" class="chip" role="radio" data-fit="' + k + '" aria-pressed="' + (S.resultFit === k) + '"><span class="oval" aria-hidden="true"></span>' + esc(o) + "</button>";
      }).join("") + '</div><label for="fittext" class="scope">' + esc(fit.free_text) + '</label><textarea id="fittext" maxlength="800">' + esc(S.resultFitText || "") + "</textarea></section>";
    }
    html += '<p class="scope">Early scoring: hand-set weights that will sharpen as more people take the quiz. <button type="button" class="link" id="method">How scoring works</button></p>' +
      '<div class="nav results-actions"><button class="btn ghost" id="explore-btn">Explore all groups and axes</button><button class="btn" id="retake">Take it again</button></div><div id="confirm"></div>';
    show(html);
    wireReport();
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
    bind("#explore-btn", function () { openExplore("groups"); });
    bind("#retry", function () { submit().then(render); });
    bind("#copylink", function () { copyText(document.getElementById("sharelink").value, document.getElementById("copylink")); });
    bind("#cmpgo", function () {
      var cd = codeFromInput(document.getElementById("cmpin").value), s = decodeScores(cd);
      if (!s) { document.getElementById("cmpmsg").textContent = "That doesn't look like a results link or code. Ask them to copy it again from their results page."; return; }
      compare = { label: "Them", scores: s }; render();
    });
    bind("#cmpclear", function () { compare = null; render(); });
    bind("#retake", function () {
      var box = document.getElementById("confirm");
      box.innerHTML = '<div class="notice">Start a new quiz? Your results are kept on this device for comparison next time. <button class="link" id="yes">Start again</button> <button class="link" id="no">Cancel</button></div>';
      bind("#yes", function () { lsDel(KEY); compare = null; resTab = "summary"; S = newState(); save(); render(); });
      bind("#no", function () { box.innerHTML = ""; });
    });
  }
  function scoresToPos(sc) { var o = {}; Object.keys(sc).forEach(function (ax) { if (ok(sc, ax)) o[ax] = sc[ax].v; }); return o; }
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
    ctx = { sc: sc, own: false, they: !isMine, other: cmpOn ? mineSc : null, otherLabel: "You", kicker: isMine ? "Your results from " + mine.d : "Shared results" };
    var pair = cmpOn ? matchOne(sc, scoresToPos(mineSc)) : null;
    var html = reportHeadHtml(ctx) +
      (isMine ? '<p class="scope">Only scores are saved on this device, not answers, so this view can\'t show which answers moved each axis.</p>'
        : '<p class="scope">Someone shared their quiz results with you. Only their scores are in the link, never their answers.' + (pair ? " You two are a <b>" + pair.match + "% match</b>." : "") + "</p>") +
      '<div class="nav"><span class="nav-right">' + (!isMine && mineSc ? '<button class="btn ghost" id="cmp">' + (cmpOn ? "Hide my results" : "Compare with mine") + "</button>" : "") +
      '</span><span class="nav-right"><button class="btn" id="home">' + (isMine ? "Back" : "Take the quiz yourself") + "</button></span></div>" +
      tabsHtml(ctx) + '<div id="panel" class="panel" role="tabpanel"></div>';
    show(html);
    wireReport();
    bind("#cmp", function () { compare = cmpOn ? null : { shared: true }; render(); });
    bind("#home", goHome);
  }
  function goHome() {
    view = null; sharedCode = null; compare = null; resTab = "summary";
    try { if (location.search) history.replaceState(null, "", location.pathname); } catch (e) { /* ignore */ }
    if (S.phase === "done" || S.phase === "home" || S.phase === "howto") { if (S.phase !== "done") S.phase = "home"; }
    render();
  }

  // ---------- explore: every group and axis, no quiz needed ----------
  var exTab = "groups", exSel = null, exCat = "all", exReturn = null;
  function openExplore(tab, sel) {
    if (view !== "explore") exReturn = { view: view, y: window.scrollY };
    exTab = tab === "group" ? "groups" : tab === "axis" ? "axes" : tab || "groups";
    exSel = sel || null;
    view = "explore"; render();
  }
  function closeExplore() {
    var r = exReturn || { view: null, y: 0 };
    view = r.view; exReturn = null; render();
    window.scrollTo(0, r.y || 0);
  }
  function mySc() {
    if (S && S.done) return computeScores(S.ans);
    var last = lastResult(); return last ? decodeScores(last.c) : null;
  }
  function similarGroups(p, n) {
    return B.profiles.filter(function (q) { return q.id !== p.id; }).map(function (q) {
      var m = matchOne(profileScores(q), p.pos, null);
      return m ? { p: q, match: m.match } : null;
    }).filter(Boolean).sort(function (a, b) { return b.match - a.match; }).slice(0, n || 5);
  }
  function renderExplore() {
    var me = mySc(), html = '<nav class="crumbs"><button type="button" class="link" id="ex-back">← Back</button></nav>';
    html += '<nav class="tabs" role="tablist"><button type="button" class="tab" role="tab" data-ex="groups" aria-selected="' + (exTab === "groups") + '">' + B.profiles.length + ' groups</button><button type="button" class="tab" role="tab" data-ex="axes" aria-selected="' + (exTab === "axes") + '">' + (AXES.length - 1) + " axes</button></nav>";
    if (exTab === "groups" && exSel && PROFILE[exSel]) {
      var p = PROFILE[exSel], m = me ? matchOne(me, p.pos, null) : null, sims = similarGroups(p, 6);
      html += '<header class="res-head"><p class="topic">' + esc(catName(p.cat)) + "</p><h1>" + esc(p.name) + '</h1><p class="res-sub">' + esc(profileMeta(p)) + ". " + esc(p.about) + basisText(p) + "</p>" +
        (m ? '<p class="summary">You and ' + esc(p.name) + " are a " + m.match + "% match.</p>" : "") + "</header>";
      html += '<section class="block"><h2>Positions</h2><p class="scope">Placed on ' + Object.keys(p.pos).filter(function (k) { return k !== "G"; }).length + " of " + (AXES.length - 1) + " axes (the rest weren't live issues for this group or it took no clear stand)." +
        (me ? ' <span class="legend"><span class="dot-key grp"></span>' + esc(p.short) + ' <span class="dot-key you"></span>You</span>' : "") + "</p>";
      [{ name: "Overall", axes: [B.axes.overall] }].concat(B.axes.families).forEach(function (f) {
        var rows = f.axes.filter(function (a) { return p.pos[a.id] != null; });
        if (!rows.length) return;
        html += '<div class="family">' + (f.name === "Overall" ? "" : "<h3>" + esc(f.name) + "</h3>") + rows.map(function (a) {
          var v = p.pos[a.id], mine = me && ok(me, a.id) ? me[a.id].v : null;
          return '<div class="ex-axis axis-row"><span class="ar-name">' + esc(a.name) + '</span><span class="ar-track"><span class="track"><span class="mid"></span><span class="dot grp" style="left:' + pct(v) + '%" title="' + esc(p.short) + '"></span>' +
            (mine != null ? '<span class="dot" style="left:' + pct(mine) + '%"></span>' : "") + '</span><span class="poles"><span>' + esc(a.minus) + "</span><span>" + esc(a.plus) + "</span></span></span>" +
            '<span class="ar-val"><span class="num">' + signed(v) + '</span></span><p class="ar-band">' + esc(bandText(a, v)) + "</p></div>";
        }).join("") + "</div>";
      });
      html += "</section>";
      html += '<section class="block"><h2>Most similar groups</h2><ol class="mini-list">' + sims.map(function (s) {
        return '<li><button type="button" class="link" data-ex-group="' + s.p.id + '">' + esc(s.p.name) + '</button> <span class="era">' + esc(profileMeta(s.p)) + ", " + s.match + "%</span></li>";
      }).join("") + "</ol></section>";
      html += '<div class="nav"><button type="button" class="link" data-ex-list="1">All groups</button></div>';
    } else if (exTab === "groups") {
      html += "<h1>Comparison groups</h1><p class=\"lede\">" + B.profiles.length + " parties, factions, voter types, presidents, historical movements, ideologies and parties abroad, placed on the quiz's axes. Today's factions and recent presidents come from simulated answers for their leading politicians; the rest are placed by hand from platforms, voting records, surveys and historians' accounts.</p>" +
        '<div class="chips" role="tablist">' + [{ id: "all", name: "All" }].concat(CATS).map(function (c) { return '<button type="button" class="chip" role="tab" data-excat="' + c.id + '" aria-selected="' + (exCat === c.id) + '">' + esc(c.name) + "</button>"; }).join("") + "</div>" +
        '<div class="search"><label for="ex-q">Find a group</label><input type="search" id="ex-q" placeholder="Try Whigs, Obama or Labour" autocomplete="off"><p class="scope" id="ex-none" hidden>No group matches that.</p></div>';
      html += plotHtml({ cat: exCat, label: exCat === "all" ? HERO_LABELS : null, user: me && userPos(me, dimAxes(MAP_X)) != null && userPos(me, dimAxes(MAP_Y)) != null ? { x: userPos(me, dimAxes(MAP_X)), y: userPos(me, dimAxes(MAP_Y)) } : null });
      CATS.filter(function (c) { return exCat === "all" || c.id === exCat; }).forEach(function (c) {
        html += '<section class="block"><h2>' + esc(c.name) + '</h2><p class="scope">' + esc(c.about) + '</p><ul class="group-list">' + B.profiles.filter(function (p) { return p.cat === c.id; }).map(function (p) {
          var m = me ? matchOne(me, p.pos, null) : null;
          return '<li><button type="button" class="group-row" data-ex-group="' + p.id + '"><span><b>' + esc(p.name) + '</b> <span class="era">' + esc(profileMeta(p)) + "</span><br><span class=\"scope\">" + esc(p.about) + "</span></span>" + (m ? '<span class="match">' + m.match + "%</span>" : "") + "</button></li>";
        }).join("") + "</ul></section>";
      });
    } else if (exTab === "axes" && exSel && META[exSel]) {
      var a = META[exSel], groups = B.profiles.filter(function (p) { return p.pos[a.id] != null; }).sort(function (x, y) { return x.pos[a.id] - y.pos[a.id]; });
      var mv = me && ok(me, a.id) ? me[a.id].v : null;
      html += '<header class="res-head"><p class="topic">Axis</p><h1>' + esc(a.name) + '</h1><p class="res-sub">' + esc(a.about) + "</p>" +
        (mv != null ? '<p class="summary">You: ' + esc(leanText(mv, a)) + " (" + signed(mv) + "). " + esc(bandText(a, mv)) + "</p>" : "") + "</header>";
      html += '<section class="block"><h2>The range</h2>' + bandLadderHtml(a, mv, null) + "</section>";
      html += '<section class="block"><h2>Every group on this axis</h2>' + stripHtml(a.id, mv, "all", null) + '<ol class="axis-rank">' + groups.map(function (p) {
        return '<li><button type="button" class="link" data-ex-group="' + p.id + '">' + esc(p.name) + '</button><span class="track mini"><span class="mid"></span><span class="dot grp" style="left:' + pct(p.pos[a.id]) + '%"></span>' + (mv != null ? '<span class="dot" style="left:' + pct(mv) + '%"></span>' : "") + '</span><span class="num">' + signed(p.pos[a.id]) + "</span></li>";
      }).join("") + "</ol></section>";
      var qs = Object.keys(B.items).filter(function (id) { return B.keying[id] && B.keying[id][a.id]; });
      html += '<section class="block"><h2>Questions that measure it</h2><p class="scope">' + plural(qs.length, "question") + " in the full bank feed this axis. A sample:</p><ul class=\"qlist\">" + qs.slice(0, 12).map(function (id) { return "<li>" + esc(B.items[id].stem) + "</li>"; }).join("") + "</ul></section>";
      html += '<div class="nav"><button type="button" class="link" data-ex-list="1">All axes</button></div>';
    } else {
      html += "<h1>The axes</h1><p class=\"lede\">The quiz measures " + (AXES.length - 1) + " separate dimensions, plus an overall left–right score. Many of them cut across the usual left–right line.</p>" +
        '<div class="search"><label for="ex-q">Find an axis</label><input type="search" id="ex-q" placeholder="Try speech, guns or China" autocomplete="off"><p class="scope" id="ex-none" hidden>No axis matches that.</p></div>';
      [{ name: "Overall", axes: [B.axes.overall] }].concat(B.axes.families).forEach(function (f) {
        html += '<section class="block"><h2>' + esc(f.name) + '</h2><ul class="group-list">' + f.axes.map(function (a) {
          var mv = me && ok(me, a.id) ? me[a.id].v : null;
          return '<li><button type="button" class="group-row" data-ex-axis="' + a.id + '"><span><b>' + esc(a.name) + '</b> <span class="era">' + esc(a.minus) + " ↔ " + esc(a.plus) + '</span><br><span class="scope">' + esc(a.about) + "</span></span>" + (mv != null ? '<span class="match">' + signed(mv) + "</span>" : "") + "</button></li>";
        }).join("") + "</ul></section>";
      });
    }
    show(html);
    bind("#ex-back", closeExplore);
    screen.querySelectorAll("[data-ex]").forEach(function (b) { b.addEventListener("click", function () { exTab = b.getAttribute("data-ex"); exSel = null; render(); }); });
    screen.querySelectorAll("[data-excat]").forEach(function (b) { b.addEventListener("click", function () { exCat = b.getAttribute("data-excat"); render(); }); });
    screen.querySelectorAll("[data-ex-group]").forEach(function (b) { b.addEventListener("click", function () { exTab = "groups"; exSel = b.getAttribute("data-ex-group"); render(); }); });
    screen.querySelectorAll("[data-ex-axis]").forEach(function (b) { b.addEventListener("click", function () { exTab = "axes"; exSel = b.getAttribute("data-ex-axis"); render(); }); });
    screen.querySelectorAll("[data-ex-list]").forEach(function (b) { b.addEventListener("click", function () { exSel = null; render(); }); });
    plotMatch = null; wirePlot();
    var q = document.getElementById("ex-q");
    if (q) q.addEventListener("input", function () {
      var t = q.value.trim().toLowerCase(), any = false;
      screen.querySelectorAll(".group-list li").forEach(function (li) {
        var hit = !t || li.textContent.toLowerCase().indexOf(t) >= 0;
        li.hidden = !hit; any = any || hit;
      });
      screen.querySelectorAll(".group-list").forEach(function (ul) {
        var sec = ul.closest(".block"); if (sec) sec.hidden = !Array.prototype.some.call(ul.children, function (li) { return !li.hidden; });
      });
      document.getElementById("ex-none").hidden = any;
    });
  }

  // ---------- about page ----------
  var returnTo = null;
  function openAbout() { returnTo = { view: view, y: window.scrollY }; view = "about"; render(); }
  function renderAboutPage() {
    var html = '<h1>How this quiz works</h1>' +
      '<p class="lede">A personal project to build a more honest political quiz for the US: more dimensions, clearer questions, and no thumb on the scale.</p>' +
      '<nav class="toc" aria-label="On this page"><p>On this page</p><ul><li><a href="#ab-diff">What makes it different</a></li><li><a href="#ab-scoring">How scoring works</a></li><li><a href="#ab-report">Reading the report</a></li><li><a href="#ab-axes">The axes</a></li><li><a href="#ab-groups">The groups</a></li><li><a href="#ab-privacy">Privacy</a></li><li><a href="#ab-limits">Limits</a></li></ul></nav>' +
      '<section class="prose"><h2 id=ab-diff>What makes it different</h2><ul>' +
      "<li><b>Answers are positions.</b> Instead of “agree or disagree” with a vague statement, you pick the policy you actually want, with real numbers where they exist.</li>" +
      "<li><b>Scope lines and exceptions.</b> Each question says what case to picture. Edge cases (rape and incest exceptions, say, or which groups of immigrants) are asked separately, so a strict rule with exceptions isn't confused with either extreme.</li>" +
      "<li><b>Honest ways out.</b> “None of these fit” and “I don't know enough” are never scored as a middle position.</li>" +
      "<li><b>No party cues.</b> No party or politician names, and rules about power are asked for any president of either party. Some rules are asked twice, once with each side benefiting, to separate principle from partisanship.</li>" +
      "<li><b>" + (AXES.length - 1) + " candidate dimensions.</b> Trust, populism, free speech, presidential power, federalism and more get their own axes, because they cut across left and right.</li>" +
      "</ul><h2 id=ab-scoring>How scoring works</h2>" +
      "<p>Each answer becomes a number from −1 (one end of the answer list) to +1 (the other end). Every question is keyed to the axes it measures and to overall left–right, with a direction. An axis score is the average of the answers keyed to it, shown as −100 to +100 once it has at least 3 answers. Follow-up cases count half as much as full questions.</p>" +
      "<p>Free speech and federalism are scored for consistency. Each of their questions is tagged by whose speech, or which side's state policies, the protective answer helps, and the left-coded and right-coded questions count equally. Protecting only the speech your own side likes doesn't count as protecting free speech. If your answers lean hard one way, the report says so.</p>" +
      "<p>These weights are set by hand for now. As more people take the quiz, the plan is to check which questions are the best measuring sticks and let those count more. That's why results are labeled early scoring.</p>" +
      "<p>Today's parties and factions, and the last five presidents, are placed by answering the whole quiz as each of their leading politicians would, from their records and public statements, and averaging the results. Past presidents are answered from their record in office. Voter types, older parties, ideologies and parties abroad are hand-placed from platforms, voting records, surveys and historians' accounts, and are only compared on issues they took positions on. Treat the match percentages as a fun guide, not a measurement.</p>" +
      "<h2 id=ab-report>How the report reads your scores</h2><ul>" +
      "<li><b>Bands.</b> Each axis is split into five bands (strongly one way, leaning, middle, leaning, strongly the other way) at −60, −20, +20 and +60. Each band has a plain-language description, so you can see what your number means.</li>" +
      "<li><b>Your label.</b> The economic summary (the average of taxes, business rules and social programs) and the cultural summary (abortion, gender identity, religion, family roles, race, immigration and national identity) each count as left, middle or right at ±20. The nine combinations give the core label: left on both, economic progressive, communitarian, social liberal, moderate, traditionalist, libertarian, free-market moderate, or right on both. Left on both is split by strength into center-left, liberal and progressive (cuts at −35 and −65, averaging the two summaries); right on both into center-right, conservative and very conservative at +35 and +65. Anyone above +50 on economics and below −50 on drugs and health rules combined is labeled libertarian. “Committed” is added to the other labels past ±65. Up to two strong cross-cutting views are added in front, such as anti-establishment, anti-war, hawkish, China-hawk, protectionist, free-trade, civil-libertarian, green or states'-rights.</li>" +
      "<li><b>Consistency.</b> Over the axes that split along today's left–right line, the report counts how many you took the left side on, the right, or the middle (within ±10). If the smaller side is under 12% of the total you're consistent, under 30% mostly consistent, otherwise cross-pressured.</li>" +
      "<li><b>Priorities.</b> When you rank your top issues, a second match weights the axes behind those issues (found from which questions feed which axes) by your ranking.</li>" +
      "<li><b>Topics.</b> A topic's lean is the average of your answers in that topic that count toward the overall left–right score.</li>" +
      "<li><b>Map.</b> The default map is overall left–right against liberty versus authority. That second dimension was chosen because it was the biggest thing left over once left–right was accounted for, in a test with 135 simulated politicians. The economic and cultural summaries track overall left–right so closely that a map of the two is mostly a diagonal line. Any two axes or summaries can still be plotted. Summaries are averages of their axes, for you and for each group.</li></ul>" +
      "<h2 id=ab-axes>The axes</h2><dl class=\"glossary\">" +
      [B.axes.overall].concat([].concat.apply([], B.axes.families.map(function (f) { return f.axes; }))).map(function (a) {
        return "<dt>" + esc(a.name) + ' <span class="era">' + esc(a.minus) + " ↔ " + esc(a.plus) + "</span></dt><dd>" + esc(a.about || "") + "</dd>";
      }).join("") + "</dl>" +
      '<h2 id=ab-groups>The ' + B.profiles.length + " comparison groups</h2>" + CATS.map(function (c) {
        return "<h3>" + esc(c.name) + '</h3><p class="scope">' + esc(c.about) + '</p><dl class="glossary">' + B.profiles.filter(function (p) { return p.cat === c.id; }).map(function (p) {
          return "<dt>" + esc(p.name) + ' <span class="era">' + esc(p.era) + "</span></dt><dd>" + esc(p.about) + basisText(p) + "</dd>";
        }).join("") + "</dl>";
      }).join("") +
      "<h2 id=ab-privacy>Privacy</h2><p>No account, and no names, emails or IP addresses. Your answers are saved with a random code so the quiz can be improved. The optional questions about you come at the end and never change your results. Share links contain only your scores. People under 18 can take the quiz, but their answers aren't saved.</p>" +
      "<h2 id=ab-limits>Limits</h2><p>This covers US politics only. The questions were drafted by one project and are still being reviewed, so some will be improved; the “Report a problem” link under each question goes straight to that list. Scores are approximate until there's enough data to calibrate them.</p>" +
      '</section>' +
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
    document.getElementById("nav-explore").addEventListener("click", function () {
      openExplore("groups");
    });
    document.getElementById("nav-home").addEventListener("click", function () {
      if (view === "about") return closeAbout();
      if (view === "explore") { view = null; exReturn = null; return goHome(); }
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
    scores: function () { return computeScores(S.ans); }, score: computeScores, archetype: archetype, encode: function (sc) { return encodeScores(sc); }, decode: decodeScores,
  };
  start();
})();
