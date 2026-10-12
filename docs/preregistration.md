# Pre-registered analysis plan

**Status: DRAFT.** This becomes binding when it is committed with the tag
`prereg-v1` **before any Pilot B data is downloaded**. After that, any change
is listed in the "Deviations" section at the bottom with its reason, and
results are reported both ways. Pilot A (free, convenience sample) may be
used to fix wording and to tune software, but never to change a threshold
below.

The point: every decision about which questions survive and which axes are
reported is fixed in advance, so the results can't be tuned after looking at
them.

---

## 1. Questions this analysis answers

1. Which draft questions work well enough to keep?
2. How many dimensions does US political opinion need, measured with these
   questions? Specifically, which of the 29 candidate axes
   ([`question-bank-plan.md`](question-bank-plan.md) §3) pass the five checks
   in [`how-many-dimensions.md`](how-many-dimensions.md)?
3. Does a bifactor structure (one general factor G plus specific axes) predict
   held-out answers better than correlated axes, two axes, or one axis?
4. Are the reported intervals honest (calibrated)?

### Predictions recorded in advance

From the GSS and ANES analyses (`reports/`), before any quiz data exists:

- G will carry the largest share of common variance (omega-hierarchical
  between .60 and .80).
- Likely to survive as distinct axes: NORMS, TRUST, SPEECH, LIBERTY, TECH,
  HOUSING, HAWK or GLOBAL, ESTAB, POP.
- Likely to merge: REDIS+REG+SOCINS; MORAL+GENDERID+RELIGION; IMMIG+NATION;
  ORDER+GUNS.
- Uncertain: FAMILY, EDUC, FED, VOTING, TRADE, ENV.
- Final count: G plus 12–18 specific axes.

These are predictions, not targets; being wrong about them is a finding.

## 2. Data

| | Pilot A | Pilot B | Retest |
|---|---|---|---|
| Sample | Convenience (own audiences, online communities) | Paid panel, quotas on age × sex, race/ethnicity, education, region, 2024 vote | Random 20% of Pilot B, invited 14–28 days later |
| Target n (complete) | 300–1,000 | 1,500 | 250 |
| Used for | Wording fixes, timing, software, option-order sanity | **All decisions below** | Retest checks |
| Design | Link + 3 of 9 blocks (`items/pilot_design.json`) | Same | Same form as their first time |

**Weighting (Pilot B):** raking to adult-population margins: age (6
groups) × sex, race/ethnicity (5), education (4), Census region (4), 2024
presidential vote (Harris / Trump / other / didn't vote), using CPS 2024 and
official vote returns. Weights trimmed at the 1st and 99th percentiles.
Structural analyses (sections 4–5) are run **unweighted and weighted**; a
decision counts only if it holds in both. Norms (percentiles shown to users)
use weights.

## 3. Exclusions

Exactly the rule in `items/modules/quality.json`. A response is excluded
from calibration if **any** of these holds:

- fails 2 or more of the 3 instructed-response checks;
- flagged for both speed (over 30% of answered items under 2 s, or under 1 s
  for exception cases) and straightlining (same on-screen position on 12+
  consecutive multi-option items);
- self-reports "I clicked through a lot of it without thinking".

Also excluded: duplicate responses (same resume code), people under 18,
and responses with fewer than 60% of their assigned questions answered.
"None of these fit" and "I don't know enough" are treated as missing, never
as a middle category. The analysis is rerun with exclusions included; any
decision that flips is reported as fragile.

## 4. Item screening (before structure)

A question is **flagged** if any of these holds; flagged questions are
revised before v1 and excluded from the structural models in this round:

| Check | Threshold |
|---|---|
| "None fit" + "Don't know" | > 15% of people shown the question |
| "It really depends" firmness | > 40% of those who answered (a sign the scope line isn't working) |
| Free-text "none fit" | Coded; any missing position named by ≥ 3% of people shown the question is added |
| Category use | Any option chosen by < 1% → merge with its neighbor for estimation (reported, not a flag by itself) |
| Option order | Nominal response model: an option's estimated slope out of its written order with 95% CI excluding the written order → flag |
| Median time | > 3 × the bank median for its format (too hard to read) |
| Exception cases | Case answered identically by > 97% (no information) → drop the case |

## 5. Structure

### 5.1 Exploration (half the sample)

Pilot B is split at random, stratified by quota cell, into an
**exploration half** and a **confirmation half** (seed 20261012).

On the exploration half:

1. Pairwise polychoric correlations (two-step, weighted and unweighted;
   pairs with fewer than 60 joint answers are left missing and smoothed
   with `nearest_pd`).
2. Parallel analysis (95th percentile, 200 random sets) for an upper bound.
3. EFA with minres + oblimin for k = 1 to the upper bound, using
   `pipeline/efa.py` (correct oblique Phi). Schmid–Leiman to estimate
   omega-hierarchical and ECV.
4. Candidate structure = the 29 hypothesized axes (each item on its tagged
   primary axis) + G, then data-driven merges and splits under the rules in
   5.3.

### 5.2 Confirmation (other half)

The structure chosen on the exploration half is fit, without changes, on the
confirmation half as a bifactor graded response model
(`pipeline/bifactor.py`). All checks in section 6 use the confirmation half.

### 5.3 Merge and split rules (decided on the exploration half)

- **Merge** two candidate axes if their specific-factor correlation
  (after G) is ≥ .85, **or** if a model with them merged predicts held-out
  answers no worse than the separate model (the 95% bootstrap CI of the
  log-loss difference includes 0). Merges are applied one pair at a time,
  largest correlation first, re-estimating after each.
- **Split** a candidate axis if EFA within its items (after partialling G)
  finds 2 factors each with ≥ 4 items loading ≥ .40, and the split model
  improves held-out log loss with a 95% CI excluding 0.
- **Drop to issue map** any axis left with fewer than 4 items loading
  ≥ .30 on its specific factor.
- An item may load on its primary axis only, plus G. Secondary tags in
  `axis` are tested as alternatives: an item moves to a secondary axis only
  if its loading there exceeds its primary loading by ≥ .15 on the
  exploration half.

## 6. The five checks for reporting an axis

An axis (specific factor) is **reported** only if it passes all five on the
confirmation half. Otherwise its questions stay in the issue map and count
toward G.

| # | Check | Pass threshold |
|---|---|---|
| 1 | Reliability | Empirical marginal reliability ≥ .70 using the questions a typical **precision-mode** taker would answer (simulated by replaying confirmation-half answers through the adaptive algorithm) |
| 2 | Held-out prediction | Mask 15% of each person's answers (5 random folds, seeds 1–5). Adding the axis to the bifactor model lowers mean held-out log loss; the 95% paired bootstrap CI (2,000 resamples of people) of the improvement excludes 0 |
| 3 | Test–retest | Correlation of EAP scores between occasions ≥ .70 (retest subsample, scores computed from the same questions both times) |
| 4 | Not a keying artifact | Refit without `agree_defined` and `frequency` items; the axis must still be identified (≥ 4 items loading ≥ .30) with Tucker congruence ≥ .90 to the full-model loadings |
| 5 | Same meaning across groups | DIF (below) on ≤ 20% of the axis's items, **and** the differential test functioning on the axis score is < 0.20 SD for every grouping variable |

### DIF method

Ordinal logistic regression per item on the matched score (G + its specific
axis), testing group main effect (uniform DIF) and group × score
(non-uniform). Flag DIF when the likelihood-ratio test is significant after
Benjamini–Hochberg correction at q = .05 **and** McFadden ΔR² ≥ .035
(moderate, Jodoin & Gierl). Grouping variables: party identification
(3-way), 2024 vote, age (18–34 / 35–54 / 55+), race/ethnicity (White / Black
/ Hispanic / Asian / other), education (degree vs not), sex. Flagged items
are revised for v1; they are kept in this round's scoring only if removing
them changes axis scores by < 0.10 SD on average.

## 7. Model comparison (headline result)

On held-out answers (same folds as check 2), compare:

1. Bifactor: G + surviving axes (the chosen structure)
2. Correlated factors: the same axes without G
3. Two axes (economic, social), compass-style
4. One axis (G only)
5. Baseline: national item marginals ("average American")
6. Self-label × party (7-point self-placement crossed with 3-way party ID;
   cell marginals)

Report mean log loss and % improvement over (5) with 95% bootstrap CIs, as
in `reports/anes/RESULTS.md`. The bifactor model is the reported model only
if it beats (2) with a CI excluding 0; otherwise the correlated-factors
model is reported and the results page is built on it.

## 8. Precision targets and item selection (for v1)

- Keep the smallest set of non-flagged questions such that, by simulation on
  the confirmation half, posterior SD ≤ 0.20 on G for ≥ 95% of people and
  ≤ 0.35 on each reported axis for ≥ 90%, in full mode.
- Every subtopic keeps at least one question (issue map).
- Among questions of equal information, keep the one with fewer "none
  fit"/"don't know" answers.
- Precision mode: stop when all targets are met or after 120 questions.
  It passes if its scores correlate ≥ .95 with full-mode scores on G and
  ≥ .85 on each axis, and its median length is reported as measured.

## 9. Calibrated intervals

For each reported score, check that the 80% posterior interval from occasion
1 contains the occasion-2 EAP (from the retest) for 75–85% of people, after
adjusting for occasion-2 measurement error (compare against the expected
coverage of the difference of two posteriors). If coverage is outside
75–85%, intervals are widened or narrowed by a single multiplier per axis,
fitted on the retest data, and that multiplier is published.

## 10. Factions

Latent profile analysis on confirmation-half scores (G + reported axes),
k = 2 to 12, chosen by BIC with the constraint that every profile holds
≥ 3% of the weighted sample. Profiles are named only after they are found,
by describing their average positions, with no party names in the profile
labels. Users see membership probabilities, never a single forced label.

## 11. What gets published regardless of outcome

- Every item's screening statistics (section 4), parameters and DIF results.
- The full axis decision table (pass/fail on each of the five checks, with
  numbers), including the axes that failed.
- Model comparison table with CIs.
- The exclusion counts and the with/without-exclusion rerun.
- Code and the exact commit used.

## 12. Software and seeds

Pipeline in this repo (`pipeline/`), Python 3.12+, versions pinned in
`requirements.txt` at the `prereg-v1` tag. Random seeds: sample split
20261012; held-out folds 1–5; bootstraps 7 (people resampling); EAP scoring
uses the shared mulberry32 generator with seed 12345 (as in `scorer/`).

## Deviations

None yet. Any change after the `prereg-v1` tag is listed here with date,
reason and both sets of results.
