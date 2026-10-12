# ANES 2024 results (model v0.2.0-anes-bifactor)

Data: ANES 2024 Time Series (release 2026-05-19), 5,521 respondents, weight
`V240107a`. 141 attitude items recoded (`pipeline/anes_items.py`,
`items/anes_crosswalk.csv`); verbatim wording in `items/anes_wording.csv`.
The microdata is not in this repository (ANES terms); only aggregate results
are. Reproduce with `pipeline/step3_anes_dimensionality.py` then
`pipeline/step4_anes_models.py` (~12 minutes).

## 1. One general left-right factor dominates

Parallel analysis keeps 18 factors (over-retention at this n is normal), but
the first eigenvalue is 36.2, against 8.6 for the second. A Schmid-Leiman
decomposition of the 9-factor solution gives:

| | GSS 2016–2024 | ANES 2024 |
|---|---|---|
| omega total | .955 | .977 |
| **omega hierarchical** (share that is one general factor) | **.52** | **.72** |
| explained common variance of the general factor | .25 | .44 |

ANES 2024 crosses the common .70 threshold: most of what its policy items
measure is a single left-right factor. GSS's older item set (civil liberties,
institutional confidence, spending) is less dominated. Share of each ANES
factor's reliable variance that is really the general factor:

| Factor | Share general |
|---|---|
| Distrust of mainstream media/elections/experts | 73% |
| Perceived discrimination & group equity | 70% |
| Moral traditionalism | 66% |
| Role of government | 63% |
| Resentment of women's equality claims | 57% |
| Foreign threat perception | 28% |
| Support for Israel & foreign engagement | 22% |
| Democratic norms | 16% |
| Trust in government institutions | 1% |

(`general_factor_k9.csv`)

## 2. Agree/disagree wording splits batteries by direction, not topic

The 4-item racial resentment battery and the 4-item egalitarianism battery
are each balanced: two items where agreeing is the conservative answer, two
where disagreeing is. In the 9-factor solution the "agree = conservative"
items from both batteries (`rr_try_harder` .56, `rr_no_favors` .53,
`egal_worry_less` .45, `egal_not_big_problem` .40) load together on one
factor, while the "disagree = conservative" items land elsewhere
(`rr_less_deserve` .47 and `rr_slavery` .45 with the discrimination items;
`egal_equal_opp` .43 and `egal_treated_fairly` .37 with role of government).

That is the signature of acquiescence: a tendency to agree, regardless of
content, shows up as a "factor." The model keeps each battery together on its
content dimension so the two directions cancel, and the quiz itself avoids
agree/disagree formats.

## 3. Which structure predicts people best? (out of sample)

15% of each person's answers were hidden for 1,500 random respondents
(27,905 hidden answers). Every model was fit without them and asked to
predict them from the person's other answers.

| Model | Log loss | Accuracy | Improvement over "average American" |
|---|---|---|---|
| Average American (marginal) | 1.364 | 40.9% | — |
| Liberal–conservative self-label | 1.271 | 46.3% | 6.8% |
| Party ID (7-point) | 1.273 | 46.4% | 6.7% |
| Self-label × party ID | 1.270 | 46.3% | 6.9% |
| 1 dimension (single left–right) | 1.218 | 49.0% | 10.7% |
| 2 dimensions (compass-style) | 1.210 | 49.3% | 11.3% |
| 9 correlated dimensions | 1.181 | 50.8% | 13.5% |
| **Bifactor: general + 9 specific** | **1.155** | **51.8%** | **15.3%** |

Paired bootstrap over respondents (2,000 resamples), difference in log loss
per hidden answer: bifactor minus 9-correlated [−.028, −.022]; bifactor minus
2-axis [−.059, −.051]. Both exclude zero.

## 4. The final model

General factor G plus 9 specific factors, all independent. 136 items (5
dropped for loading under .25 on everything; 4 measure only G).

| Dimension | What it captures | Items | Reliability |
|---|---|---|---|
| G | General left–right | 136 | **.95** |
| GOV | Role of government (economy, environment, guns) | 29 | .73 |
| EQUITY | Perceived discrimination & group equity | 20 | .71 |
| CULT | Moral traditionalism & authority in child-rearing | 15 | .61 |
| GENDER | Resentment of women's equality claims | 13 | .57 |
| NORMS | Indifference to democratic checks & a free press | 15 | .78 |
| ESTAB | Distrust of mainstream media, elections & experts | 17 | .76 |
| TRUST | Distrust of government institutions | 9 | .72 |
| THREAT | Foreign threat perception | 8 | .72 |
| FOREIGN | Support for Israel & foreign engagement | 6 | .72 |

Specific factors in a bifactor model measure what is left after general
left-right is removed, so .6–.76 is typical and honest. They are below the .80
target; the quiz should show them with wider uncertainty bands than G.

Strongest items: G is best measured by siding with Israelis vs Palestinians,
perceived discrimination against Black people, the border wall, transgender
bathroom access and same-sex marriage. NORMS by the importance of checks and
balances and of consequences for misconduct. TRUST by trust in government and
Congress, which is unrelated to left–right.

## 5. Known groups

Average general-factor score by self-label runs monotonically from −1.54
(extremely liberal) to +1.17 (extremely conservative). Specific factors are
mostly flat across self-labels, as they should be once G is removed, with two
real patterns:
- **Democratic norms:** moderates (+0.13) are *less* attached to checks and a
  free press than both the extremely liberal (−0.20) and the extremely
  conservative (−0.32).
- **Distrust of government institutions** is highest at both ends.

## 6. Predicting the 2024 vote (Harris vs Trump)

5-fold cross-validated AUC:

| Predictors | AUC |
|---|---|
| Liberal–conservative self-label | .923 |
| Party ID (reference only; never a model input) | .964 |
| General factor only | **.969** |
| General + 9 specific | .981 |
| General + 9 specific + self-label | .984 |

Attitudes alone, with no party questions, predict the vote better than party
identification does.

## 7. Checks

- `tests/test_bifactor.py`: the bifactor estimator recovers known slopes from
  simulated data with 30% missing, and its scores track an oracle that knows
  the true parameters to within .03 on every dimension.
- The TypeScript scorer reproduces the Python reference to 1e-6 on 30
  response patterns for this 10-dimension model.
