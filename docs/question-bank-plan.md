# Question bank plan

The full plan for writing every question, covering every topic, and deciding
the axes. The machine-readable version of the topic list is
[`items/blueprint.csv`](../items/blueprint.csv): 25 domains, 230 subtopics, the
candidate axis each subtopic tests, draft counts and minimum final counts.

Everything here serves one goal: **accuracy**. Question counts, time and
number of axes are outcomes of that goal, not targets in themselves.

---

## 1. What "accurate" means here

A result is accurate when all four of these hold. Every decision below is
judged against them.

1. **It predicts you.** From your answers to some questions, the model
   predicts your answers to questions it didn't use. (Held-out prediction,
   the test already used on GSS and ANES.)
2. **It's stable.** Taking the quiz again in 2–4 weeks gives nearly the same
   result (test–retest).
3. **It means the same thing for everyone.** Two people with the same views
   get the same scores whatever their party, age, race, education or region
   (no differential item functioning).
4. **Its uncertainty is honest.** When the results page says 80% of people
   like you fall in a band, 80% actually do (calibrated intervals).

Corollaries:
- A question earns its place only if it improves 1–4. Questions that don't
  are cut, however interesting.
- An axis is reported only if it passes the five checks in
  [`how-many-dimensions.md`](how-many-dimensions.md).
- Length is whatever reaches the precision target (§5), not a fixed number.

---

## 2. Quiz structure

| Part | What | Scored as | Time (full mode) |
|---|---|---|---|
| Intro | Instructions, consent, how answers work (§7 of the writing standard) | — | 2 min |
| Modules 1–25 | Position questions by topic, with exception follow-ups and definitions | Positions (axes + issue map) | 50–65 min |
| Values | Cross-cutting values (balanced pairs, tradeoffs) | Values layer | 4 min |
| Priorities | Which topics matter most to you (best–worst choice sets) | Importance weights | 3 min |
| About you (end) | Self-placement, party, past vote, broad demographics, all optional | Never an input; used for validation and comparisons | 2 min |
| Quality | 3 instructed-response checks spread through; 6 questions repeated at the end | Data quality, within-session reliability | ~1 min |

Module order is randomized per person (with related modules kept adjacent),
so fatigue never always falls on the same topics. Progress is saved after
every answer; people can stop and resume. A short break screen comes every
~12 minutes, with an optional "here's what we know so far" preview to keep
people engaged.

**Two modes, one scale:**
- **Full mode** asks every question: the complete issue map. About 60–75
  minutes.
- **Precision mode** asks questions adaptively until every axis reaches the
  precision target (§5), always covering every subtopic at least once.
  Expected 30–45 minutes. Scores are on the same scale; only the error bands
  differ.

---

## 3. The axes: 29 candidates, tested, not assumed

Every subtopic in the blueprint is tagged with the candidate axis it tests.
These are **hypotheses**. The pilot (§9) decides which survive, merge or split
using the five checks. Everything is measured on top of a **general
left–right factor (G)**, which ANES 2024 showed carries most of the
ideological signal. Specific axes are reported as deviations from it.

### Families and candidate axes

| Family | Candidate axis (code) | One pole ↔ other pole | Expected relation to G (prior evidence) | Draft items |
|---|---|---|---|---|
| **Economic** | Redistribution (REDIS) | Equalize outcomes through taxes and transfers ↔ leave outcomes to markets | Strongly left–right (ANES GOV 63% general) | 22 |
| | Regulation & labor (REG) | Government sets rules for business and work ↔ minimal rules | Mostly left–right; antitrust and licensing may cut across | 16 |
| | Social insurance & health (SOCINS) | Collective provision ↔ individual provision | Mostly left–right; may merge with REDIS | 15 |
| | Housing & land use (HOUSING) | Build more, override local control ↔ protect neighborhoods, limit growth | **Likely cross-cutting** (both parties split) | 10 |
| | Trade (TRADE) | Open trade ↔ protection | **Realigned recently**; weakly left–right in ANES | 10 |
| **Environment** | Environment & energy (ENV) | Act aggressively at a cost ↔ prioritize cost and growth | Strongly left–right; test split from REDIS | 18 |
| **Technology** | Technology & AI (TECH) | Regulate and slow ↔ let develop freely | **Weakly left–right** (2026 polling shows parties flipped on AI worry) | 16 |
| | Privacy (PRIVACY) | Limit surveillance ↔ allow it for security | Cross-cutting candidate | 10 |
| **Moral & cultural** | Moral traditionalism (MORAL) | Traditional religious morality in law ↔ personal choice | Strongly left–right (ANES CULT 66% general) | 11 |
| | Sexuality & gender identity (GENDERID) | Legal recognition and protection ↔ traditional sex and marriage definitions | Strong; test split from MORAL | 14 |
| | Religion in public life (RELIGION) | Strict separation ↔ religion integrated into public life | Moderate | 10 |
| | Family & gender roles (FAMILY) | Egalitarian roles, public support ↔ traditional roles, family responsibility | Moderate; ANES "gender" factor was weak (2 items), so needs real items | 10 |
| **Identity** | Race & equity (EQUITY) | Structural explanations, group remedies ↔ individual explanations, colorblind rules | Strong (ANES EQUITY 70% general) | 18 |
| | Immigration (IMMIG) | Open, inclusive ↔ restrictive | Strong | 18 |
| | National identity (NATION) | Civic, pluralist nationhood ↔ shared culture, assimilation | Moderate; test split from IMMIG | 10 |
| **Order** | Crime & punishment (ORDER) | Rehabilitation, restrain police ↔ punishment, empower police | Strong | 18 |
| | Guns (GUNS) | Restrict ↔ protect gun rights | Strong; test split from ORDER | 10 |
| **Liberty** | Personal liberty vs paternalism (LIBERTY) | Adults decide for themselves ↔ the state protects people from themselves | **Cross-cutting candidate**: the "libertarian" axis compass tests claim and never test | 14 |
| | Free speech & tolerance (SPEECH) | Protect offensive speech ↔ restrict harmful speech | **Near-orthogonal to economics** (GSS TOLER) | 14 |
| **Governance** | Democratic norms (NORMS) | Checks, courts, press ↔ strong executive, results over process | **Mostly not left–right** (ANES 16% general) | 14 |
| | Elections & voting (VOTING) | Access ↔ security; reform ↔ status quo | Partly left–right | 12 |
| | Trust in government (TRUST) | Trust ↔ distrust of government institutions | **Not left–right** (ANES 1% general; GSS TRUST flat) | 11 |
| | Distrust of media & experts (ESTAB) | Trust mainstream sources ↔ distrust | Right-coded in 2024 (ANES ESTAB 73% general) | 10 |
| | Anti-elitism (POP) | System works for ordinary people ↔ rigged by elites | Cross-cutting; left and right versions | 10 |
| | Federalism (FED) | National standards ↔ state and local control | Often follows who holds power; test stability | 10 |
| | Education (EDUC) | Public system, professional control ↔ choice, parental control | Moderate; may split between funding and curriculum | 12 |
| **Global** | Global engagement (GLOBAL) | Alliances, aid, institutions ↔ go it alone | Weak and mixed (ANES FOREIGN 22% general) | 12 |
| | Hawkishness (HAWK) | Use force readily, big military ↔ restraint | Weak; test split from GLOBAL | 10 |
| **Values** | Values layer (VALUES) | Equality/freedom, order/liberty, tradition/change, hierarchy, loyalty, human nature | Reported separately as "the values behind your views" | 18 |

### Expected outcome

Based on GSS and ANES, my honest expectation is **G plus roughly 12–18
specific axes**. The clearest predictions:
- **Likely to survive as distinct:** NORMS, TRUST, SPEECH, LIBERTY,
  TECH, HOUSING, HAWK/GLOBAL, ESTAB, POP.
- **Likely to merge into fewer:** REDIS + REG + SOCINS (maybe one economic
  axis plus one "markets vs regulation"); MORAL + GENDERID + RELIGION; IMMIG +
  NATION; ORDER + GUNS.
- **Uncertain:** FAMILY, EDUC, FED, VOTING, TRADE, ENV vs economics.

Whatever the data says wins. Merged axes still keep their subtopics in the
issue map.

---

## 4. Topic coverage

25 domains, 230 subtopics. Full list with notes in `items/blueprint.csv`.

| # | Domain | Subtopics | Draft | Min. final | Candidate axes |
|---|---|---|---|---|---|
| D01 | Taxes & redistribution | 11 | 22 | 12 | REDIS |
| D02 | Labor & business regulation | 9 | 16 | 10 | REG |
| D03 | Health care & social insurance | 10 | 18 | 11 | SOCINS, LIBERTY, IMMIG |
| D04 | Housing & land use | 4 | 10 | 6 | HOUSING |
| D05 | Environment & energy | 10 | 18 | 11 | ENV |
| D06 | Trade & economic nationalism | 5 | 10 | 6 | TRADE |
| D07 | Technology & AI | 10 | 16 | 11 | TECH |
| D08 | Privacy & surveillance | 6 | 10 | 7 | PRIVACY |
| D09 | Abortion & reproduction | 8 | 12 | 11 | MORAL, FED |
| D10 | Sexuality & gender identity | 8 | 14 | 8 | GENDERID |
| D11 | Religion in public life | 5 | 10 | 5 | RELIGION |
| D12 | Family & gender roles | 6 | 10 | 6 | FAMILY |
| D13 | Race & equity | 10 | 18 | 12 | EQUITY |
| D14 | Immigration & national identity | 18 | 27 | 21 | IMMIG, NATION |
| D15 | Crime, policing & punishment | 11 | 18 | 11 | ORDER |
| D16 | Guns | 7 | 10 | 7 | GUNS |
| D17 | Drugs & personal liberty | 7 | 12 | 7 | LIBERTY |
| D18 | Free speech & civil liberties | 8 | 14 | 8 | SPEECH |
| D19 | Democratic norms & executive power | 9 | 14 | 9 | NORMS |
| D20 | Elections & voting | 8 | 12 | 8 | VOTING |
| D21 | Trust & anti-establishment | 23 | 31 | 23 | TRUST, ESTAB, POP |
| D22 | Foreign policy & defense | 14 | 22 | 14 | GLOBAL, HAWK |
| D23 | Education | 8 | 12 | 8 | EDUC |
| D24 | Federalism & local control | 7 | 9 | 7 | FED |
| D25 | Values (cross-cutting) | 8 | 18 | 9 | VALUES |
| | **Total** | **230** | **383** | **248** | **29 candidates** |

**Status (2026-10-12): every subtopic is drafted.** The bank is 379 questions
in 26 files under `items/drafts/` (one per domain plus `core_v0.json`), worth
425 scored units because each exception case is scored on its own. Every
subtopic meets or exceeds its planned count and every candidate axis has at
least 10 units. `scripts/coverage.py` checks this against the blueprint
(written per subtopic: `items/coverage.csv`); `scripts/audit_items.py` writes
the balance review list to `reports/item_audit.md`.

Final format mix of scored units: position 286, exceptions 63, tradeoff 33,
frequency 25, agree/disagree pairs 10, belief 8. Exceptions came out higher
than planned because several follow-ups list 3–6 cases; each case is short
(~5 s), so the time cost is small.

---

## 5. How many questions, and why

### Draft bank: 383

- **Every subtopic gets at least one question; important or contested ones
  get 2–4,** so no subtopic depends on a single wording.
- **Every candidate axis gets at least 10 draft questions.** Pilots usually
  cut 30–40% of new questions. Ten leaves at least 6–7 good ones, the minimum
  to judge whether an axis is real.
- **Exceptions** are separate short questions (each case scored on its own),
  so the rule question doesn't have to absorb edge cases.

### Final instrument: about 230–260, set by precision, not by count

After the pilot, a question stays if it does all of these:
- carries real information about its axis or G (discrimination clearly above
  the weakest anchors),
- has options that stay in their intended order,
- has a "none fit" + "don't know" rate under 15%,
- behaves the same across groups,
- isn't redundant with a better question on the same subtopic.

The **precision target** decides when to stop:
- **G:** posterior SD ≤ 0.20 for nearly everyone (reliability ≈ .96).
- **Each specific axis:** posterior SD ≤ 0.35 (reliability ≈ .88). That is
  higher than the .80 usual target, possible because length isn't a
  constraint.
- **Every subtopic** answered at least once in full mode, for the issue map.

If an axis can't reach its target with the surviving questions, more
questions get written for it before v1, or the axis is reported with
wider bands and a flag.

### Time estimate

- Position question: ~15 s on average (reading options); exception case
  ~5 s; firmness ~3 s.
- Full mode at ~250 core questions + ~40 exception cases ≈ **60–75 minutes**.
- Precision mode ≈ **30–45 minutes**, to be confirmed by simulating adaptive
  testing on pilot data.

---

## 6. Format mix

Target shares across the bank (from the blueprint's format column):

| Format | Share | Use |
|---|---|---|
| Position ladder | ~72% | Default for any policy question |
| Exceptions | ~9% | Edge cases after a rule question, or one question across several targets (e.g. speakers from different sides) |
| Tradeoff | ~9% | Two concrete options with their costs, when the real disagreement is a choice between goods |
| Frequency | ~6% | Trust and perception questions, with numeric anchors |
| Belief | ~2% | Empirical beliefs (causes of racial gaps, climate science), reported separately and tested for whether they belong on an axis |
| Defined agree/disagree pairs | ~3% | Values only, always in reverse-keyed pairs |

---

## 7. Writing process (per domain)

1. **Map the real positions.** For each subtopic, list the positions actually
   held by real people and organizations across the spectrum: party
   platforms, think tanks of every orientation, advocacy groups on all sides,
   and public polling showing how opinion is spread. Each ladder must include
   every position held by a meaningful share of the public (roughly 3%+),
   including both ends.
2. **Build the ladder.** Order the positions along one dimension. Mark the
   current-law position as context, never as the "neutral" middle.
3. **Write the question** per the writing standard: stem, scope line,
   options, definitions, facts with sources and dates, exception follow-up if
   edge cases matter.
4. **Steelman test.** For every option: would a sincere holder of this view
   sign this wording as a fair description of what they believe? If not,
   rewrite. Each pole is written as its own best advocate would put it.
5. **Validator** (`scripts/validate_items.py`) must pass.
6. **Balance check per domain:**
   - options on each side of current law are roughly symmetric in number and
     intensity,
   - the "high" pole alternates direction across questions so nobody
     learns that "first option = left",
   - no question's wording is warmer toward one side (adjective audit).
7. **Log it.** Each question records its sources and the open concerns.
8. **Commit the domain** for review (§8).

### Writing order

Domains with the most cross-cutting potential and the biggest gaps go first,
since those are where existing quizzes are weakest:

1. D01–D03 Economics (largest, sets the template)
2. D21 Trust & anti-establishment, D19 Democratic norms (proven non-left–right)
3. D17 Personal liberty, D18 Free speech, D08 Privacy (the "libertarian" family)
4. D07 Technology & AI, D04 Housing, D06 Trade (cross-cutting candidates)
5. D13 Race, D14 Immigration & nation, D15 Crime, D16 Guns
6. D09 Abortion, D10 Sexuality & gender identity, D11 Religion, D12 Family
7. D05 Environment, D22 Foreign policy, D20 Elections, D23 Education, D24 Federalism
8. D25 Values, then the priorities, quality and about-you modules

---

## 8. Review before any data

1. **Self-review** against the steelman test.
2. **Two-sided readers:** at least 2 left-leaning, 2 right-leaning and 1
   unaffiliated (ideally also 1 libertarian-leaning). Each reads a domain and,
   for each question, rates slant (1–5), says in their own words what it
   asks, and notes any missing position. Revise anything any group rates 3+.
3. **Think-aloud interviews** (10–15 people of mixed ages, education and
   politics): read aloud, say what each option means and which they'd pick
   and why. Revise questions where people describe different questions.

---

## 9. Pilot design

No single person can sensibly answer 383 draft questions, and nobody has to.
The pilot uses a **planned-missing design**: the IRT model handles questions a
person wasn't shown.

- Split the bank into 9 balanced blocks of ~43 questions (each block covers
  many domains and every axis).
- Each person gets 3 random blocks plus a fixed 20-question link block of
  strong general-factor questions, about **150 questions, ~40 minutes**.
- With n respondents: each question is answered by about n/3, each pair of
  questions in different blocks by about n/12, and the link block by everyone.

| Pilot | Who | Size | Purpose |
|---|---|---|---|
| 0 | Think-aloud | 10–15 | Wording |
| A | Your audiences (Big A, Lemonade Stand community), friends, Reddit/Discord | 300–1,000 | Free first statistics: option order, "none fit" rates, timing, obvious failures. Skews young, male and online, so not used for norms |
| B | Paid, quota-balanced on age, sex, race, education, region and 2024 vote | ~1,500 | Calibration, factor structure, axis decisions, DIF, norms. ~500 answers per question, ~125 per cross-block pair |
| Retest | Subset of B, 2–4 weeks later | ~200–300 | Test–retest per question and per axis |

Rough cost of Pilot B at ~40 minutes, $12/hour pay and a 33–43% platform fee:
**about $16,000–17,000** (fees from earlier research, partly from secondary
sources; re-check before budgeting). A smaller paid pilot (~500) plus a large
free pilot is the lower-cost path; it gives good item statistics but weaker
national comparisons.

---

## 10. Analysis and decisions

The pipeline that ran on GSS and ANES is reused, plus three additions:

1. **Item screening:** response distributions, "none fit"/"don't know" rates,
   time per question, option-order check with a nominal response model,
   free-text review for missing positions.
2. **Structure:** polychoric correlations, parallel analysis, factor analysis
   with the corrected oblique rotation, general-factor share (omega
   hierarchical), then bifactor model comparison against correlated-axes,
   two-axis and one-axis models on held-out answers, as done for ANES.
3. **Axis decisions:** each candidate gets the five checks (reliability,
   held-out gain with bootstrap interval, retest, keying robustness, DIF).
   Survivors, merges and drops are all recorded with their numbers.
4. **Item selection:** keep the questions that reach the precision targets
   with the fewest weak items; check every subtopic is still covered.
5. **Adaptive simulation:** replay pilot answers through precision mode to
   confirm it matches full-mode scores within the error bands, and measure
   its real length.
6. **Calibration of intervals:** check that 80% bands contain the retest
   score about 80% of the time.
7. **Factions:** latent profile analysis on the final scores, reported as
   probabilities.

Pre-commit to these thresholds in the repo before Pilot B data arrives, so
results can't be tuned after the fact.

---

## 11. What the results page shows (and which questions feed it)

1. **General left–right**: all position questions.
2. **Specific axes** that survived, with uncertainty bands and national
   percentiles: their tagged questions.
3. **Issue map**: every subtopic, with your answer, exceptions and firmness,
   next to how the country splits.
4. **Values behind your views**: the values module.
5. **What matters most to you**: the priorities module.
6. **Coherence**: how consistently your answers follow the structure.
7. **Factions you resemble**, with probabilities.
8. **Label vs answers**: how your self-description compares with your
   positions (from the optional about-you module).

---

## 12. Milestones

| # | Deliverable | Done when | Status |
|---|---|---|---|
| M1 | All 25 domains drafted (383 questions planned) | Validator passes; balance check done per domain | **Done** 2026-10-12: 379 questions / 425 scored units, 0 validator errors; audit in `reports/item_audit.md` |
| M2 | Two-sided review + think-alouds | Every question rated; revisions logged | Next |
| M3 | Priorities, values, about-you and quality modules | Validator passes | **Drafted** 2026-10-12: values in `items/drafts/d25_values.json`; other modules in `items/modules/` |
| M4 | Quiz app (pilot version) | Planned-missing blocks, save/resume, timing, free-text capture | |
| M5 | Pilot A | 300+ complete; item screening report | |
| M6 | Thresholds pre-registered in repo | Committed before Pilot B | |
| M7 | Pilot B + retest | Data in; structure, axis decisions, selection report | |
| M8 | v1 instrument | Precision targets met; adaptive mode validated | |
| M9 | Public launch | Results page, limitations page, open item parameters | |

---

## 13. Risks and how they're handled

| Risk | Handling |
|---|---|
| Fatigue in a long quiz lowers answer quality late | Randomized module order, breaks, save/resume, quality checks, timing flags, precision mode |
| My own wording leans one way | Steelman test, two-sided readers, adjective audit, alternating pole direction |
| Current events make questions date quickly | Tag `current` vs `core`; current questions are kept out of axis scores unless they prove stable; dated facts are re-checked yearly by the validator |
| Free pilot audience is unrepresentative | Used for wording and item statistics only; calibration and norms from the balanced Pilot B |
| Too many axes that don't hold up | The five checks; failures stay in the issue map, not on the axis list |
| Too few questions for a real axis | Every candidate starts with ≥10; write more before v1 if precision isn't reached |
| Pilot B cost | Lower-cost path in §9; national comparisons can be added later |
