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
- `records.py`: record-in-office answer sets for Clinton, Bush 43 and Obama (views today plus
  overrides where the presidency points elsewhere), used to place the president groups.
- `evaluate.py`: a line-for-line Python port of the app's scoring (checked against app.js by
  `tests/test_sim.py`), plus party separation, signatures, matches (leave-one-out: groups built
  from simulated members are re-placed without the politician being matched), reliability, item
  diagnostics, labels, lopsidedness on the balanced axes, map dimensions, and how far simulated
  placement moved each group from its old hand placement.
- `tests/test_sim.py` runs all of this as a regression test with fixed thresholds.
- `out/`: `scores.csv` (every politician on every axis), `summary.json`, `evaluation.txt`.

The answers are a reconstruction of each politician's record, so this tests whether the
quiz maps known positions to the right scores, not how real people answer.

Since the October 2026 fixes, signature expectations for LIBERTY were written for the old
"personal freedom" axis (now split into vice laws and health rules), and the match expectations
predate the Moderate Republicans group; both are kept as written and the differences are
reported rather than re-registered.
