# First-pass results: GSS 2016–2024 (model v0.1.0-gss)

Data: General Social Survey cumulative file (Release 3), survey years 2016,
2018, 2021, 2022, 2024. 15,700 adults, weighted with `wtssps`, each year
given equal total weight. 86 attitude items recoded so a higher code is the
pole named in `items/gss_crosswalk.csv`.

Reproduce: `python3 pipeline/step1_dimensionality.py` then
`python3 pipeline/step2_fit_and_validate.py` (about 10 minutes on a laptop).

## 1. How many dimensions?

Parallel analysis on the weighted polychoric matrix (82 items) keeps 13
factors, which is the usual over-retention at large n. Exploratory factor
analysis (minres, oblimin) was read at 1–8 factors. The 7-factor solution is
the first where every factor is interpretable and only 5 items load below .30:

| Factor | What it is | Example items |
|---|---|---|
| CULT | Moral traditionalism | 7 abortion items, euthanasia, same-sex relations, premarital sex |
| TOLER | Civil-liberties tolerance | Letting atheists, racists, communists, anti-American clergy speak/teach/have books |
| TRUST | Institutional confidence | Confidence in Congress, banks, medicine, science, military, press … |
| GROUP | Race, immigration & law-and-order | Racial-discrimination items, immigration level, death penalty, courts |
| SPEND | Domestic spending priorities | Spending on education, health, cities, child care, Social Security |
| GENDER | Traditional gender roles | Man works/woman at home, working mothers, women in politics |
| ECON | Redistribution & role of government | Reduce income differences, help the poor, help pay for medical care |

Full loadings: `reports/efa_loadings_k7.csv`.

## 2. Does it predict people better? (out-of-sample)

15% of each person's answers were hidden for 4,000 random respondents
(26,608 hidden answers). Each model was fit without them, then asked to
predict them from the person's other answers.

| Model | Log loss (lower = better) | Accuracy | Improvement over "average American" |
|---|---|---|---|
| Average American (marginal) | 0.921 | 55.2% | — |
| Liberal–conservative self-label | 0.880 | 58.4% | 4.5% |
| Party ID | 0.884 | 58.2% | 4.0% |
| Self-label × party ID | 0.873 | 58.7% | 5.2% |
| 1 dimension (single left–right) | 0.838 | 61.0% | 9.1% |
| 2 dimensions (compass-style) | 0.826 | 61.6% | 10.3% |
| **7 dimensions (data-driven)** | **0.769** | **65.5%** | **16.6%** |

The 7-dimension model beats the compass-style model on every dimension's
items; the biggest gains are on tolerance and institutional confidence, the
two traits a two-axis model has no place for
(`reports/step2_holdout_by_dimension.csv`).

## 3. Reliability

| Dimension | Items | Empirical reliability |
|---|---|---|
| ECON | 4 | .84 |
| SPEND | 15 | .78 |
| CULT | 16 | .76 |
| GENDER | 5 | .74 |
| GROUP | 14 | .82 |
| TOLER | 12 | .79 |
| TRUST | 13 | .82 |

Among people who answered at least 3 items on that dimension. Targets are .80
for core dimensions; four fall short, mostly because GSS split ballots mean a
typical person answers only part of each dimension. A quiz that asks
everyone the strongest items will do better.

## 4. Correlations between dimensions (latent)

ECON, SPEND and GROUP are strongly related (.66–.71): in the US, views on
redistribution, spending and race/immigration move together. Moral
traditionalism is moderately related to them (.34–.44). Tolerance is nearly
independent of economics (−.08) and institutional confidence is independent of
everything (|r| ≤ .16). Full matrix: `reports/step2_latent_correlations.csv`.

## 5. Known groups

Average scores rise steadily from "extremely liberal" to "extremely
conservative" on ECON, SPEND, CULT, GENDER and GROUP. TOLER rises only at the
conservative end. TRUST is flat, confirming it is not a left–right trait
(`reports/step2_known_groups_polviews.csv`).

## 6. Predicting the 2020 vote (Trump vs Biden; 2022 and 2024 surveys)

5-fold cross-validated AUC:

| Predictors | AUC |
|---|---|
| Liberal–conservative self-label | .881 |
| 2 axes | .917 |
| 7 dimensions | .926 |
| 7 dimensions + self-label | .944 |

## 7. Pipeline checks

- Simulation recovery (`tests/test_recovery.py`): from data with 30% missing,
  slopes, intercepts and latent correlations are recovered, scores match an
  oracle that knows the true parameters to within .02, and 80% intervals
  cover the truth 74–86% of the time.
- TypeScript scorer (`scorer/`) reproduces the Python reference to 1e-6 on 30
  response patterns.
