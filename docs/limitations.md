# Known limitations (v0.2: GSS model + ANES 2024 bifactor model)

Honest list, kept current. Every item here should either get fixed or stay
visible on the results page.

## What the current model is

A 7-dimension graded response model calibrated on the General Social Survey,
2016–2024 (about 15,700 adults, weighted with `wtssps`). It is a *calibration
of existing national survey items*, not yet the quiz. It is the anchor the
quiz's own items will be linked to.

## Limits of the data

- **GSS item content is old-fashioned in places.** Several items date from the
  1970s (school prayer refers to a 1960s Supreme Court ruling; civil-liberties
  items ask about communists and "militarists"). They work statistically, but
  the quiz needs modern items linked to them.
- **Missing domains (GSS model).** GSS barely asks about foreign policy,
  trade, democratic norms or populism. The ANES 2024 model covers these;
  AI/technology is still missing from both.
- **The economic dimension (ECON) has only 4 items** (the GSS "help" and
  income-differences items). Its reliability is good (.84) but its content is
  narrow. ANES's 7-point scales will broaden it.
- **Split ballots.** Many GSS items are asked of only half or a third of the
  sample. The IRT model handles this, but some item pairs are never observed
  together, which limits the factor analysis (4 items had to be left out of it).
- **Mode change.** The GSS moved largely to the web from 2021. Pooling 2016–2024
  assumes items behave the same across modes; that is untested here.

## Limits of the method

- **Dimensions were chosen by exploratory factor analysis on the same data
  used to calibrate.** The held-out prediction test guards against overfitting
  answers, but not against choosing the structure on this sample. A
  confirmatory check on a separate dataset (ANES or a fresh sample) is still
  owed.
- **Seven hand overrides** of the factor-loading rule are documented in
  `model/params.json` ("overrides"), plus seven dropped items ("dropped_items").
- **Between-item model.** Every item measures exactly one dimension. Some items
  plainly cross-load (affirmative action loads on both economics and race).
  An ESEM/bifactor version is a planned comparison.
- **Item parameters were calibrated one dimension at a time**, then the
  correlations were estimated with the items fixed. A full joint
  multidimensional fit would be slightly more efficient.
- **Polychoric correlations use a pairwise two-step estimator.** Standard, but
  the matrix needed smoothing to be positive-definite.
- **Scores use importance sampling.** With 2,000 antithetic draws the Monte
  Carlo error is well under the reported uncertainty, but it is not zero.

## Limits of the interpretation

- **Institutional confidence (TRUST) is not left-right.** It barely varies by
  liberal/conservative self-label. It is reported as its own trait, not as an
  ideological position.
- **Civil-liberties tolerance (TOLER)** is only weakly related to left-right
  (correlation about .3 with moral traditionalism, near 0 with economics).
  This is a finding, not a bug: the Political Compass's "authoritarian" axis
  mixes this with social conservatism.
- **Directions are named, not judged.** "High" on a dimension means closer to
  the pole named in `params.json`; it is not better or worse.
- **Who is "average"** comes from the weighted GSS sample, not from quiz-takers.

## Added with the ANES 2024 model

- **One survey, one year.** The ANES model is calibrated on a single 2024
  election survey, fielded during a campaign. Items about Israel, Gaza,
  Ukraine and election integrity are tied to that moment, and several are
  among the strongest measures of the general factor. They need re-checking
  against later data before they anchor a quiz.
- **Mixed weights.** Pre- and post-election items are modelled together with
  the pre-election weight (`V240107a`); post-election items have about 10%
  fewer respondents.
- **Specific dimensions are less reliable (.57–.78) than the general factor
  (.95).** That is inherent to bifactor models; the quiz must show wider
  uncertainty on them.
- **The "GENDER" specific factor is really two items** (women seeking special
  favors; women complaining about discrimination). Other items assigned to it
  carry almost no specific variance. It needs more items before it means much.
- **Acquiescence is handled by design, not modelled.** Balanced batteries are
  kept on one dimension so agreement bias cancels, but there is no explicit
  acquiescence factor yet.
- **Two separate models.** GSS and ANES share no identically worded items in
  this version, so their scores are not on a common scale yet. Linking them
  needs anchor items asked in both, or a sample that answers both sets.
- **ANES respondent timings and voter validation files are not used yet.**
  They allow a speeder check and a validated-turnout check respectively.
