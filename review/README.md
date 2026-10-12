# Review kit (milestone M2)

Two kinds of review happen before any pilot: **two-sided expert-ish
reading** (does any question lean?) and **think-aloud interviews** (does
everyone read the question the same way?). Both are cheap and catch most
problems a pilot would otherwise pay to find.

| File | What it is |
|---|---|
| `packet.md` | Every question as a quiz taker reads it, grouped by topic. Send this to reviewers |
| `review_sheet.csv` | One row per question and per exception case, with blank columns for the reviewer. Import into Google Sheets, make one copy per reviewer |
| `../items/review_log.csv` | Where every revision is logged (what changed, why, who flagged it) |

Regenerate the packet and sheet after editing questions:
`python3 scripts/make_review_kit.py`.

---

## Part 1: Two-sided review

### Who

At least **6 readers**, chosen so no side can dominate:

- 2 who lean left
- 2 who lean right
- 1 unaffiliated / politically disengaged
- 1 libertarian-leaning (the group most compass-style quizzes misread)

Ideally each reads every topic. If that's too much (~4 hours for the full
bank), split the 25 topics so **every topic gets at least one left, one
right and one other reader**. Pay or thank them; this is real work.

Avoid people who will review as advocates ("make my side look good"). Ask
for people who can describe the other side's view in a way the other side
would accept.

### What to send them

> Thanks for helping. This is a draft political quiz that tries to place
> people on many issues without any party bias. I need you to read questions
> as a careful critic, **not** to say what you believe.
>
> For each question in your sheet, please fill in:
>
> 1. **In your own words, what is it asking?** One short sentence. If you
>    had to guess, say so.
> 2. **Your answer letter** (optional, it helps me spot questions everyone
>    answers the same way).
> 3. **Slant, 1 to 5:** 1 = completely even-handed, 3 = noticeably tilted,
>    5 = obviously pushes one answer. Judge the wording, not the topic.
> 4. **If slanted, which side does it favor?**
> 5. **Straw man:** is any answer written so that nobody who holds that view
>    would sign it? Give its letter.
> 6. **Missing position:** is a real view, held by a meaningful number of
>    people, missing from the answers?
> 7. **Confusing words:** anything you had to reread or could read two ways.
> 8. **Other notes.**
>
> Every question also offers "None of these fit my view" and "I don't know
> enough", and answers appear in random order in the real quiz, so you
> don't need to comment on those.

### Decision rules (write them down before reading the sheets)

A question is **revised** if any of these holds:

- Any reader rates slant **3 or higher**, or two readers from the same side
  rate it 2+ in the same direction.
- Any reader marks a **straw man** and you can't find a real person or
  organization who would sign that option's wording as written.
- Any reader names a **missing position** that you can show is held by
  roughly 3%+ of Americans (poll, platform, or major organization).
- Readers' "in your own words" answers describe **different questions**.
  (Two readers paraphrasing different things is the single most important
  warning sign.)

Every revision goes in `items/review_log.csv`. Revised questions go back to
at least one reader from each side for a second look.

---

## Part 2: Think-aloud interviews

### Who

10–15 people, mixed on age, education, region and politics, with at least
3 who don't follow politics closely. Not the same people as Part 1.

### Setup

About 45 minutes each, on video call or in person, recorded with consent
(audio is enough). Use the pilot app in a test mode or the packet. Pick
~30 questions per person so that, across all interviews, every question is
read aloud by at least 2 people, with the hardest ones (high reading level
in `reports/item_audit.md`, any flagged in Part 1) read by 4+.

### Script

> I'm testing questions, not you. There are no wrong answers, and I didn't
> write these to trick anyone. Please read each question out loud, then
> think out loud as you choose an answer: say whatever goes through your
> head, even "I don't get this".

After each question, ask only the probes that apply:

1. "In your own words, what was that asking?"
2. "What made you pick that answer over the one next to it?"
3. "Was there an answer you wanted that wasn't there?"
4. (If they hesitated) "What were you weighing just now?"
5. (If there's a scope line) "When you answered, were you picturing a
   typical case, or a specific one?" (Tests whether the scope line works.)
6. (If there's a defined term) "What does [term] mean here?" Then: "Would
   you have tapped it for the definition?"

Don't explain the question or correct them during the interview. Their
misreading is the data.

### What to record per question

Paraphrase matches intent (yes / partly / no), hesitation (none / some /
long), wanted a missing answer (what), misread a term (which), picked
"none fit" or "don't know" (why).

### Decision rule

Revise any question that 2 or more people paraphrase as a different
question, or where 2 or more people want the same missing answer.

---

## Part 3: After review

1. Apply revisions; log every one.
2. `python3 scripts/validate_items.py`, `coverage.py`, `audit_items.py`.
3. Regenerate this kit and the pilot design (`make_pilot_design.py`).
4. Tag the bank `bank-v0.2` and move to Pilot A.
