# Pilot quiz app

A static web app (plain HTML, CSS and JavaScript, no framework) that runs
the draft question bank for the pilots. Source in `app/src/`; the build
writes `app/dist/` (not committed).

```bash
python3 scripts/build_app.py          # -> app/dist/index.html (+ bank.js, app.js, style.css, config.js)
open app/dist/index.html              # works straight from the file, no server needed
python3 -m pytest -q tests/test_app.py   # clicks through the whole quiz in a headless browser
```

## What it does

- **Intro**: what the quiz is, privacy and consent, length choice, how
  answers work, and a random resume code (not linked to any identity).
- **Pilot form**: the link block plus 3 of 9 blocks, assigned by the
  balanced design in `items/pilot_design.json` (about 35 minutes of
  questions, ~50 in total). **Full map** asks everything. Precision mode is
  shown as coming after calibration.
- **Every format** in the bank: position ladders, belief, frequency,
  defined agree/disagree scales (with each point's meaning), tradeoffs (two
  side cards plus a Clearly/Lean scale) and exception follow-ups (one row
  per case).
- **Rules from the writing standard**: answer order shown forward or
  reversed per person and question (recorded, codes never change);
  tradeoff sides swapped the same way; "None of these fit my view" (with an
  optional text box) and "I don't know enough" on every question, scored as
  missing; optional firmness after each position and tradeoff; tappable
  definitions (which ones were opened is recorded).
- **Order**: topic areas in random order per person; follow-ups right
  after their question and only when the earlier answer calls for them;
  the second half of each agree/disagree pair placed later in its topic.
- **Quality**: three attention checks placed in the middle third, six
  repeated questions at the end in the opposite display direction, per-
  screen timing (capped at 5 minutes so idle time doesn't count), and a
  last "how carefully did you answer" question.
- **Breaks** about every 12 minutes of active time.
- **Priorities**: 15 best–worst sets (each topic shown 3 times).
- **About you**: optional, after the questions; party lean and evangelical
  follow-ups appear only when relevant. Under-18 answers are never sent.
- **Results**: the person's issue map (every answer by topic, with
  firmness), their top priorities, a "how well does this describe you"
  rating, and copy/download of their answers. Axis scores are not shown:
  they need the pilot calibration first, and showing uncalibrated numbers
  would contradict the accuracy goal.
- **Save and resume**: progress is saved on the device after every answer.

## Sending responses

Set `submitUrl` in `app/src/config.js`. `server/README.md` sets up a free
Google Sheet collector in about 10 minutes. With no URL, answers stay on
the device.

## Hosting

`.github/workflows/pages.yml` publishes `app/dist` with GitHub Pages: turn on
Pages (Settings → Pages → Source: GitHub Actions) and run "Publish quiz
app" from the Actions tab. Any static host works too.

## Data it records

Per answer: code (bank order), escape choice and text, firmness, time on
screen, on-screen position chosen, display direction, tradeoff side swap,
definitions opened. Per person: random id and code, bank version, mode,
assigned blocks, question order, attention checks, priorities, optional
about-you answers, self-reported care, date (no time of day). No names,
emails, IP addresses or browser details.
