# Item-writing standard

Goal: every person who reads a question understands the same thing, and every
answer stands for one specific position. Most online quizzes fail here. Their
statements are vague ("The freer the market, the freer the people"), so each
person silently answers a different question: some picture the typical case,
some an extreme edge case, and "neutral" can mean "moderate", "torn",
"it depends" or "no idea".

This standard has seven rules. `scripts/validate_items.py` enforces the
mechanical ones on every item file in `items/drafts/`.

## Evidence this matters

In ANES 2024, questions where each answer is a concrete position (for example
"by law, abortion should never be permitted / only in case of rape, incest or
danger to the woman's life / ...") separate people far better than
agree/disagree statements. Median general-factor discrimination: **1.62** for
position and 7-point anchored items vs **1.06** for agree/disagree items
(`model/params_anes.json`). The agree/disagree batteries also split by wording
direction rather than topic (acquiescence; `reports/anes/RESULTS.md` §2).

## Rule 1: Every answer is a position, not a degree of agreement

Write the options as the actual positions people hold, ordered from one pole to
the other. The person picks the one closest to their view; nobody has to
translate "somewhat agree" into a policy.

Bad: *"Abortion should be legal." Strongly agree … Strongly disagree*

Good: *"Which comes closest to what the law on abortion should be?"*
- Legal for any reason at any point in pregnancy
- Legal for any reason until about the point of viability (around 24 weeks); after that only for serious health risks
- Legal for any reason in roughly the first trimester; after that only in specific circumstances
- Legal only in specific circumstances such as rape, incest, or a threat to the woman's life or health
- Legal only to save the woman's life
- Never legal

Requirements:
- 3–7 options, mutually exclusive, ordered along one dimension.
- Each option is a complete position someone could hold and defend; no straw men.
- Use real quantities when the issue has them (dollar amounts, weeks, years,
  numbers of people) instead of "more" or "less".
- The middle option is a real moderate position, never a blank "neutral".
- Where agreement scales are unavoidable (values items), every point gets a
  defined meaning (Rule 6).

## Rule 2: State the scope: the general rule, then the exceptions

Edge cases are real views, not noise, so measure them instead of hoping people
ignore them:

1. **The rule question** asks about the usual case and says so in a short
   scope line: *"Pick the rule you'd want in most situations. You'll be able to
   add exceptions next."*
2. **An exceptions follow-up** lists the specific edge cases people raise
   (rape, threat to health, fatal fetal condition…) as separate yes/no or
   stricter/same/more-lenient items. Each is scored as its own item on the same
   dimension, the way the GSS's seven abortion circumstances are.

So a person who supports a strict general rule with exceptions is not mistaken
for either extreme, and nobody answers the main question while picturing
the rarest case.

## Rule 3: Define every term that people read differently

- Any term with competing meanings ("assault weapon", "DEI", "socialism",
  "unauthorized immigrant", "viability", "public option") gets a short, neutral,
  sourced definition, shown by tapping the term.
- Definitions describe; they never argue. Each records its source.
- Everyone sees the same definition. The app logs whether it was opened, so we
  can check later whether opening it changes answers.
- Facts used in a question (current law, current amounts) carry a
  `fact_check` date and source; the validator flags any older than a year.

## Rule 4: No cues about who holds which position

- No party names, politicians, or ideological labels ("liberal",
  "conservative", "progressive", "MAGA", "woke", "socialist").
- No loaded wording on either side ("illegal alien" / "undocumented
  migrant": use "people living in the US without legal immigration status";
  "pro-life"/"pro-choice": describe the law instead).
- Where a question is about power (presidents, courts, protests), write it for
  **any president / any group, of either party**, and say so in the scope line.
  Otherwise answers track who is in power instead of a principle.

## Rule 5: Always offer honest ways out, and never score them as "moderate"

Every item has two extra options, scored as missing, never as the middle:
- **"None of these fit my view"**, with an optional one-line text box. Free
  text is reviewed between versions to add missing positions.
- **"I don't know enough about this to say"**.

And an optional, skippable firmness question after each answer:
**"How settled is this view?"** Firm / Fairly firm / It really depends on the
details. Firmness is not part of the position score; it is reported as
conviction and lets the results page show which views are strongly held.

## Rule 6: If an agreement or frequency scale is unavoidable, define every point

Some values items work best as statements. Then each point has a fixed meaning,
shown on screen:

| Point | Meaning shown to the person |
|---|---|
| Strongly agree | True in nearly every case I can think of |
| Agree | True in most cases, with some real exceptions |
| Torn | I can see it both ways about equally |
| Disagree | False in most cases, with some real exceptions |
| Strongly disagree | False in nearly every case I can think of |

Frequency scales get numbers: "Most of the time (about 7 in 10)". Statements
come in balanced pairs (one keyed each way) so agreement bias cancels.

## Rule 7: Short, concrete, one idea

- One question, one idea: no "and" joining two policies.
- Stem at most 35 words; each option at most 30 words; grade 8 reading level.
- Each tradeoff names its cost, as ANES does ("even if it means higher prices").
- Answer order is shown in both directions (randomized per person) so
  "first option" effects cancel; the score direction never changes.

## Formats

| Format | When | Rules the validator enforces |
|---|---|---|
| `position` | Default for any policy question | 3–7 ordered options |
| `exceptions` | Edge cases after a rule question, or one question across several targets | 2–3 options; `cases`, each scored as its own item |
| `tradeoff` | When the real disagreement is a choice between two goods | Exactly 2 `sides` (label ≤6 words, text ≤35 words, each naming its cost with "even if…"); fixed scale `Clearly A / Lean A / Lean B / Clearly B`, shown with the side labels. No middle: the point is to make the choice. "None fit" and "Don't know" are still offered |
| `frequency` | Trust and perception questions | Every option has a numeric anchor ("about 7 in 10") |
| `belief` | Empirical beliefs (causes of racial gaps, climate science) | Same as position; reported separately and tested for whether it belongs on an axis |
| `agree_defined` | Values statements only | Defined meaning for every point; a reverse-keyed `pair` using the same scale reversed |

## Item file format

One JSON file per domain in `items/drafts/`. Each item has:

- `id` (unique across the whole bank, including exception case ids)
- `subtopic` (must match `items/blueprint.csv`) and `axis` (candidate axes; the
  first is the one the item is written for, later ones are tested)
- `format`, `stem`, `scope`, optional `context`
- `options` in code order 0..K-1; `high_pole` describes code K-1. Display
  direction is randomized per person; codes never change
- optional `definitions` [{term, text, source, verify}], `facts` [{claim,
  source, checked, verify, note}], `followup` / `show_if`, `cases`, `sides`,
  `point_meanings` + `pair`, `notes` (open concerns for reviewers), `links`
  (ANES/GSS counterparts, for national comparison only)

Checks to run after any edit:

```bash
python3 scripts/validate_items.py   # rules (errors) and things to check (warnings)
python3 scripts/coverage.py         # every subtopic and axis has enough items
python3 scripts/audit_items.py      # balance review list -> reports/item_audit.md
```

## Global instructions (shown once, before the first question)

> There are no trick questions. Each question asks about the usual case. When
> exceptions might matter to you, you'll get a follow-up to say which. Tap any
> underlined term for a definition. If no answer fits, pick "None of these fit
> my view" and tell us why. That helps us improve the quiz.

## Testing items before they count

1. **Validator** (`scripts/validate_items.py`): structure, lengths, reading
   level, banned terms, definitions, fact-check dates.
2. **Two-sided review**: at least two left-leaning, two right-leaning and one
   unaffiliated reader rate each item for slant (1–5) and say what they think
   it asks. Revise anything any group rates 3+.
3. **Think-aloud interviews** (5–10 people): read aloud, say what each option
   means. Revise items where people describe different questions.
4. **Pilot statistics** per item: rate of "none fit" / "don't know" /
   "depends"; whether the options stay in their intended order (checked with a
   nominal response model; options that swap order get rewritten); test–retest
   agreement after 2–4 weeks; differences by party at the same position (DIF).
   Items with more than 15% "none fit + don't know", or whose options swap
   order, are revised before release.
5. **Anchors**: a few ANES/GSS questions are kept word for word, even where
   they break these rules, so new items can be put on the national scale.
   They are marked `anchor: true` and are never edited.
