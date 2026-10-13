# political-axes

A personal project to build the most accurate US political-ideology quiz I
can: dimensions chosen by data instead of by assumption, item weights
estimated instead of hand-set, scores reported with uncertainty, and
"average" defined by national probability surveys instead of by whoever takes
the quiz. Not affiliated with any university, company, party or campaign.

## Where it stands

**v0.2.0: two calibrated models.**

**ANES 2024 bifactor model** (`model/params_anes.json`, see
[`reports/anes/RESULTS.md`](reports/anes/RESULTS.md)). One general left–right
factor (reliability .95) plus 9 specific dimensions measured as deviations from
it. Predicting held-out answers, it improves on the "average American" baseline
by 15.3%, against 11.3% for a compass-style two-axis model and 6.9% for knowing
someone's party and liberal/conservative label. With no party questions, it
predicts the 2024 vote (AUC .969 from the general factor alone) better than
party identification does (.964).

**GSS 2016–2024 model** (v0.1.0-gss):
See [`reports/RESULTS.md`](reports/RESULTS.md). Headline: predicting held-out
answers, the 7-dimension model improves on the "average American" baseline by
16.6%, against 10.3% for a two-axis compass-style model and 5.2% for knowing
someone's party and liberal/conservative label.

The seven dimensions found in the data:

1. **ECON**: redistribution and role of government
2. **SPEND**: domestic spending priorities
3. **CULT**: moral traditionalism (abortion, sexuality, end of life)
4. **GENDER**: traditional gender roles
5. **GROUP**: race, immigration and law-and-order
6. **TOLER**: civil-liberties tolerance (nearly independent of economics)
7. **TRUST**: institutional confidence (not a left–right trait at all)

Known gaps (no foreign policy, trade, AI, democratic norms or populism yet)
are in [`docs/limitations.md`](docs/limitations.md).

**Question bank (drafted 2026-10-12).** The quiz's own questions are written:
469 questions in `items/drafts/`, covering 294 subtopics and 29 candidate
axes, each one a concrete position with a scope line, definitions, sourced
facts and exception follow-ups where edge cases matter. They are drafts: the
next step is two-sided review and think-aloud interviews (kit in `review/`),
then pilots ([`docs/question-bank-plan.md`](docs/question-bank-plan.md) §8–9).
The quiz site (`app/`, "Where You Stand") is ready to deploy on Netlify:
home page with three lengths, provisional scores on 29 axes, a 2D map,
closest of 83 parties, presidents, movements and ideologies, share/compare links and an About page
(details in [`app/README.md`](app/README.md)).

## Layout

| Path | What |
|---|---|
| `items/gss_crosswalk.csv` | Every GSS item used, its recode and which end is "high" |
| `items/anes_crosswalk.csv`, `items/anes_wording.csv` | ANES 2024 items: recodes, keying, verbatim questionnaire wording |
| `pipeline/step3_anes_dimensionality.py`, `pipeline/step4_anes_models.py` | ANES factor analysis; model comparison and bifactor fit |
| `pipeline/bifactor.py` | Bifactor graded response model (EM with dimension reduction) |
| `items/item_inventory.csv` | Candidate items from Pew 2026 and ANES 2024 with exact wording and verification status |
| `pipeline/` | Python: streaming .rda reader, polychoric correlations, graded response model (EM), scoring |
| `pipeline/step1_dimensionality.py` | Polychoric matrix, parallel analysis, EFA 1–8 factors |
| `pipeline/step2_fit_and_validate.py` | Fit, held-out prediction vs baselines, reliability, vote AUC, norms |
| `model/params.json` | Item parameters, latent correlations, national norms: the scorer's input |
| `scorer/` | TypeScript scorer for the website, tested against the Python reference |
| `tests/` | Simulation recovery test |
| `reports/` | All outputs, including `RESULTS.md` |
| `scripts/` + `.github/workflows/fetch-data.yml` | Data fetching (see `DATA.md`) |
| `docs/question-bank-plan.md`, `items/blueprint.csv` | The full plan: 25 topic areas, 294 subtopics, 469 draft questions, 29 candidate axes, pilot design and decision rules |
| `docs/item-writing-standard.md` | How every quiz question must be written: positions not agreement, scope + exceptions, definitions, no party cues |
| `docs/how-many-dimensions.md` | The rule for deciding how many axes to report |
| `items/drafts/` | **The full draft question bank**: 469 original questions (555 scored units), revised after a full review (`reports/question_review.md`) across all 25 topic areas, one file per area |
| `items/modules/` | Intro, priorities, comparison groups, quality checks and optional about-you questions |
| `scripts/validate_items.py`, `scripts/coverage.py`, `scripts/audit_items.py` | Rule checker, coverage against the blueprint, balance audit (`reports/item_audit.md`) |
| `review/` | Reviewer kit for the two-sided review and think-aloud interviews: readable packet, fill-in sheet, protocol |
| `items/pilot_design.json` | Planned-missing pilot design: link block + 3 of 9 balanced blocks per person |
| `docs/preregistration.md` | Every pilot decision rule and threshold, fixed before data |
| `app/` | The pilot quiz app (static site); `server/` has a free Google Sheets collector; `scripts/pilot_responses.py` turns responses into analysis files with quality flags |
| `docs/` | Privacy notice, limitations |

## Run it

```bash
python3 -m pip install -r requirements.txt
python3 scripts/restore_data.py gss          # after the data Action has run once
python3 pipeline/step0_extract_gss.py
python3 pipeline/step1_dimensionality.py
python3 pipeline/step2_fit_and_validate.py   # ~10 min
python3 -m pytest -q tests/
python3 scripts/validate_items.py           # draft quiz items
# ANES (download it yourself into data/raw/anes/, see DATA.md)
python3 pipeline/step3_anes_dimensionality.py
python3 pipeline/step4_anes_models.py        # ~12 min
python3 scorer/make_fixtures.py params.json fixtures.json
python3 scorer/make_fixtures.py params_anes.json fixtures_anes.json
npm test                                     # Node 22.18+
```

## Data

See [`DATA.md`](DATA.md). Public sources are fetched by a GitHub Action onto
the `data` branch; ANES and Pew need a login, so they're pushed by hand with
`scripts/push_local_data.sh` (private repo only).

## Licenses

Code: MIT. Item parameters and reports: CC BY 4.0. Survey item wordings
belong to their sources and are used with attribution.
