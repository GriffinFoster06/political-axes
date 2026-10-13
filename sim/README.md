# Politician simulation

135 major US politicians take the full 469-question bank, answered from their
public record, and the quiz's own scoring is checked against expectations
written before any scoring (`roster.py`).

```bash
python3 sim/dump.py D14        # print one topic's questions in answer order
python3 sim/load.py            # validate every answer file
python3 sim/evaluate.py        # score everyone, check expectations, write sim/out/
```

- `roster.py`: who, party, expected closest groups, expected axis signs, within-party orderings.
- `archetypes.py`: the 11 faction templates each politician starts from.
- `answers/Dxx.txt`: one file per topic: templates, sub-faction lines, individual answers.
- `evaluate.py`: a line-for-line Python port of the app's scoring (checked against app.js),
  plus party separation, signatures, matches, reliability, item diagnostics, profile calibration.
- `out/`: `scores.csv` (every politician on every axis), `summary.json`, `evaluation.txt`.

The answers are a reconstruction of each politician's record, so this tests whether the
quiz maps known positions to the right scores, not how real people answer.
