# Question bank review (bank v0.1, 2026-10-12)

A full read of all 379 draft questions (425 scored answers) against the
project's one goal: **accuracy**. That means each answer should mean the same
thing to everyone, each option should be a real position, options should sit
in a clean order, no wording should lean, and the bank should cover every
position that matters.

**Limit of this review:** I wrote these questions, so I share their blind
spots. This review catches structural and measurement problems well. It is
weaker on slant and on missing positions, which is exactly what the
two-sided readers and the read-aloud interviews (`review/`) are for. Treat
this as the pre-review cleanup, not a substitute.

---

## Verdict in one paragraph

The bank's core design works: concrete positions instead of agree/disagree,
scope lines, exception follow-ups, definitions, "any president of either
party" wording, and coverage of all 230 planned subtopics. But there is **one
design flaw that would make a whole family of axes fail the pre-registered
checks by construction** (trust is measured almost entirely in one answer
format). There are also **about 15 questions that ask two things at once**,
**about 12 whose options mix two different dimensions**, **several clusters
of near-duplicate questions** that will create fake "axes", and **real gaps**:
the federal deficit, socialism vs markets, beliefs about the causes of poverty
and when life begins, Supreme Court expansion, presidential immunity, and
roughly 40 more. None of it is hard to fix. Every item is listed below.

## The 12 most important problems, ranked by damage to accuracy

| # | Problem | Why it matters | Fix | Section |
|---|---|---|---|---|
| 1 | TRUST is 11/11 frequency items; ESTAB 9/10; POP 5/10; VALUES 10/18 agree-scale | Pre-registered check 4 removes those formats, so these axes **cannot pass**. And a shared answer format can create a "format factor" that looks like an axis | Add position-format and reverse-keyed items; revise check 4 | 1.1 |
| 2 | Near-duplicate clusters (e.g. 4 equality-vs-freedom items, 3 history-teaching items) | Locally dependent pairs form spurious "doublet" factors that can pass reliability checks | Merge or model as testlets; add a local dependence check to the prereg | 1.2 |
| 3 | 15 double-barreled questions | People answer different halves, so the same answer means different things | Split or convert to exception cases | 1.3 |
| 4 | 12 ladders mixing two dimensions | Option order isn't monotone for everyone; nominal-model checks will flag them anyway | Split into two questions | 1.4 |
| 5 | Process questions (filibuster, emergency funding, tariff authority, Electoral College) get answered by "which side does this help" | The NORMS and FED axes partly measure partisanship instead of principle | Add mirrored cases (same rule, each side benefiting) | 1.5 |
| 6 | Coverage gaps: deficit, socialism/markets, poverty causes, life begins, gender belief, Court expansion, presidential immunity and more | Whole factions (socialists, post-liberals, fiscal hawks) can't be told apart from neighbors | ~45 new questions | 2 |
| 7 | 44 questions show current-law context, some of which implicitly names the current administration | Context improves understanding but can cue party; the effect is unmeasured | Randomize context on/off in Pilot A | 1.6 |
| 8 | 14 knowledge-heavy questions | Answers partly measure policy knowledge, creating bias by education | Simplify or drop if "don't know" > 15% | 1.7 |
| 9 | Tradeoffs force a choice (no middle) and 3 have lopsided costs | "Torn" people are pushed into noise; uneven costs tilt answers | Fix costs; test a "Torn" option in Pilot A | 1.8 |
| 10 | 43% of ladders have only 3 options | Less information per question, more people at the ends | Extend where a real position exists (list) | 1.9 |
| 11 | Multi-target questions with mismatched extremity (campus speakers) | Comparing "tolerance of left targets" vs "right targets" is confounded with how extreme each target is | Pair targets by extremity | 1.10 |
| 12 | 6 facts out of date or contestable | Wrong context misleads and dates the quiz | Update (list) | 1.12 |

---

## 1. Bank-wide findings

### 1.1 Answer format is confounded with the axis (critical)

| Axis | Scored answers | Frequency or agree-scale | Other formats |
|---|---|---|---|
| TRUST | 11 | **11** | 0 |
| ESTAB | 10 | **9** | 1 |
| POP | 10 | 5 | 5 |
| VALUES | 18 | 10 (agree) | 8 (tradeoff) |

All 25 frequency questions use the same 5-point "how often" scale. Of them,
22 are keyed the same way: "rarely" means distrust. Two consequences:

1. **The pre-registration makes TRUST fail automatically.** Check 4 refits
   without frequency and agree items, and the axis must still have 4 or more
   items. TRUST would have 0, ESTAB 1. That was a mistake in how check 4 is
   written, and it sits in the bank at the same time.
2. **A shared scale can produce a factor that is about the scale.** Some
   people use "most of the time" more than others regardless of topic. With
   one keying direction, that response style is indistinguishable from
   trust.

**Fixes:**

- **Reverse-key about half the frequency items**, so "almost always" means
  distrust. Examples:
  - "How often do federal officials hide mistakes from the public?"
  - "How often do major news organizations leave out facts that hurt the
    side they favor?"
  - "How often are official statistics adjusted to make the party in power
    look good?"
- **Add 4–6 position-format trust questions** that measure behavior or
  policy, not feelings:
  - "If a federal health agency recalled a product you use, what would you
    do?" (stop using it at once / check other sources first / keep using it
    unless I saw problems myself / ignore it).
  - "How much should Congress rely on its own nonpartisan budget office's
    cost estimates?"
  - "If your state's election officials certified a result your side lost,
    would you accept it without seeing an independent audit?"
  - "Should courts defer to federal agencies' expert judgment when a law is
    unclear?" (also NORMS).
  - "When scientists and elected officials disagree about a public health
    rule, who should decide?"
- **Revise pre-registration check 4** to: "survives when the axis is
  re-estimated from its reverse-keyed and non-frequency items only, with
  Tucker congruence ≥ .90". Then the check tests keying instead of excluding
  the axis.
- **VALUES** is fine on keying (agree items come in reversed pairs), but
  check 4 would leave only tradeoffs. Add 3–4 values items in position
  format, e.g. "Which matters more in deciding who gets ahead: effort,
  talent, family background or luck?"

### 1.2 Near-duplicate clusters (local dependence)

When two questions are close rewordings, their answers correlate more than
the axes explain. Factor analysis then finds a two-item "factor". It can look
reliable and even improve held-out prediction slightly, which is exactly how
fake axes get reported.

| Cluster | Questions | Recommendation |
|---|---|---|
| Equality vs freedom | `inequality_tradeoff`, `outcomes_vs_chances`, `security_vs_choice`, `fair_small_gaps`/`fair_keep_earnings` | Keep `inequality_tradeoff` (policy) and the agree pair (values). Drop `outcomes_vs_chances` or rewrite it about opportunity policy specifically. Keep `security_vs_choice` |
| Top tax rate | `top_income_tax` (core), `top_rate_number` | Keep both only if modeled as a testlet. Otherwise drop `top_income_tax` (relative wording; keep it only as the ANES anchor) |
| History teaching | `teach_racism_history`, `teach_institutional_racism`, `patriotic_education` | Keep all three: they're on different axes. Rewrite `teach_racism_history` (straw man, §3 D13) and check their residual correlation |
| Experts | `experts_vs_voters`, `expertise_vs_experience` | Keep both, flag as a testlet |
| Pretrial | `cash_bail`, `pretrial_danger` | Keep `cash_bail`, drop `pretrial_danger` (its first option repeats `cash_bail` option 0) |
| Immigration level | `legal_immigration_level`, `immigration_pause` | Drop `immigration_pause` (adds a moratorium position that `legal_immigration_level`'s last option covers) |
| Who decides | `abortion_who_decides`, `states_differ` | Fine as is: different issues |
| Voter verification | `voter_id`, `proof_of_citizenship` | Fine: different rules |
| China | `china_trade`, `china_ownership`, `china_posture` | Fine: trade vs ownership vs military |
| Size of government | `federal_size`, `gov_role_values` pair | Fine: policy vs values |
| Nuclear | `nuclear_power`, `nuclear_funding` | Fine, but expect a doublet |
| Congress trust | `trust_congress_effort`, `trust_congress_promises`, `congress_motives` | Drop one when reverse-keying (§1.1) |

**Add to the pre-registration:** after fitting, compute Yen's Q3 residual
correlations. Any pair above .20 is modeled as a testlet or one item is
dropped before axis decisions are made. A specific factor whose loadings
come mostly (≥ 60%) from one dependent pair is not an axis.

### 1.3 Double-barreled questions

Each of these asks about two or more things people can feel differently
about.

| Question | The two things | Fix |
|---|---|---|
| `carry_locations` | Schools, bars and government buildings | **Convert to exception cases**: K-12 schools (by trained staff), college campuses, bars, government buildings, places of worship, private businesses by default |
| `moderation_level` | "False **or** offensive" | Split: false-but-legal posts; offensive-but-legal posts |
| `temp_workers` | Farmworkers and engineers | Split: seasonal farm and service workers (H-2A/H-2B); skilled workers (H-1B). Views differ sharply, including within each party |
| `workplace_diversity` | Women and racial minorities | Ask about racial minorities; move the gender version to D12 |
| `trans_adult_sports` | College and professional | Ask about college. Professional leagues set their own rules, so it's a different question |
| `dei_offices` | Agencies and public universities | Acceptable, but universities are where the debate is; consider asking only about universities |
| `carbon_tax` | Tax level and what the money is used for | Split: (a) should there be a carbon tax, at what level; (b) if there were one, should the money go to rebates, clean energy or deficit reduction |
| `family_arrangement` | Whether a parent stays home **and** which parent | Split: (a) both work vs one stays home; (b) if one stays home, should it usually be the mother |
| `childcare_funding` | How much government spends **and** whether it goes to childcare or to parents | Split: amount; then form (childcare centers vs cash to parents) |
| `union_organizing` option 3 | Secret ballot **and** periodic re-votes | Keep one (re-votes are the more distinctive position) |
| `border_security` option 0 | Fewer agents **and** more legal pathways | Reword: "Fewer agents and barriers than today" (pathways are asked elsewhere) |
| `ubi` stem | "Whether or not they work **or need it**" | "regardless of income or whether they work" (also less loaded) |
| `contraception_access` option 1 | Insurance mandate **and** religious exemption | Move the exemption to the religious exemption cases (`rex_employer_bc` already asks it) |
| `hate_speech_law`, `hate_crime_sentences` | Race, religion, sexual orientation (and no gender identity) | Acceptable, but the list should match across questions; decide whether gender identity is in or out and say so in the scope line |
| `campaign_spending` | Corporations, unions, wealthy individuals | Acceptable; note in the pilot whether "none fit" text asks to separate them |

### 1.4 Ladders whose options mix two dimensions

Where the options don't move along one line, a person's choice depends on
which line they're thinking about.

| Question | Problem | Fix |
|---|---|---|
| `corporate_rate` last option | "No corporate tax; tax owners when paid" is a tax-design view held by some economists across the spectrum, not simply the "lowest tax" pole | Move it to a separate question about where business income should be taxed, or drop it |
| `outbreak_vaccine_jobs` | "Each employer can choose" vs "only health care employers can require" puts employer freedom and individual freedom on one line | Ask separately: (a) should government require it; (b) should employers be allowed to |
| `abortion_who_decides` option 1 | "National limits set by Congress" means a floor of access to some people and a national restriction to others | Split into "national law protecting access" vs "national law restricting it", or drop the middle option |
| `same_sex_marriage` | "Each state decides" isn't clearly more restrictive than "civil unions nationwide" | Order: legal everywhere / civil unions everywhere / no federal recognition of either / no recognition anywhere. Move "states decide" to `states_differ` (it's already a case there) |
| `bailouts` | "Let it fail" is held by free-market and populist people alike; the ladder assumes it's one pole | Keep it, tag it POP as well as REG, and expect a non-monotone curve |
| `private_prisons` | Tagged ORDER, but the dimension is privatization | Retag REG; ORDER secondary |
| `aid_form` | Tagged REDIS, but it measures paternalism | Retag LIBERTY primary |
| `drug_import` | Unclear axis (safety vs price vs trade) | Keep for the issue map; don't count toward an axis until the pilot shows where it loads |
| `medicare_means_test` | Direction relative to left/right unclear | Same as above |
| `low_income_tax` | Three of four options say "owe nothing" and differ only in credit size; the real contrast (everyone pays something) has one option | Rebuild: larger credits / today's credits / smaller credits / a small minimum tax for everyone / a flat tax with no exemption |
| `ubi` options 2–3 | Turn into a question about cash aid levels, which `cash_aid_level` already asks | Options: large UBI / small UBI / a guaranteed minimum income only for people below a line / no guaranteed income |
| `cash_bail` option 3 | Moves from "how bail works" to "preventive detention" | Fine for now; recheck with the nominal model |

### 1.5 Process questions answered by who benefits

`filibuster`, `emergency_funding`, `refuse_to_spend`, `tariff_authority`,
`electoral_college`, `redistricting`, `state_refusal`, `grant_conditions`,
`exec_orders_scope`, `troops_in_cities` and `courts_vs_majority` all say
"any president / either party", which helps. But people still picture the
current fight. Research on procedural attitudes shows they swing with
partisan advantage.

**Fix:** add "mirror" exception cases that hold the rule fixed and swap
who benefits. For example, for emergency powers:

> Should a president be able to declare an emergency to spend money
> Congress refused, for each of these?
> - building a border wall
> - building clean-energy projects
> - responding to a major hurricane

The same goes for federal grant conditions (cutting funds to cities that
limit immigration enforcement vs cutting funds to states that restrict
abortion) and for states refusing federal law (immigration vs marijuana vs
guns; `state_refusal` lists all three but asks once).

**Payoff:** a person's NORMS/FED score can then use only their consistent
answers, and the inconsistency itself becomes a reportable "principle vs
outcome" measure. That is a genuinely new and accurate thing no existing
quiz measures.

### 1.6 Current-law context and party cues

44 questions show a "Background" line. Most are neutral facts that help
people understand (the $7.25 minimum wage, the 37% top rate). A few
implicitly point at the current administration:

- `climate_agreements`: "withdrew in January 2026"
- `ev_tax_credit`: "ended in September 2025"
- `foreign_aid_level`: "before 2025 cuts"
- `refugee_cap`: the range includes the 2026 record low

That can turn a policy question into a referendum on the president.

**Fix:**
- Rewrite these to state the level without the event. For example,
  "The US is not currently part of the Paris Agreement", or a neutral range
  only.
- **Run a small experiment in Pilot A:** randomly show or hide the context
  line for each person and question. If showing it shifts answers by party
  (the context × party interaction), rewrite or drop that context. This
  turns a judgment call into a measured one and costs nothing extra.

### 1.7 Knowledge-heavy questions

These need policy knowledge to answer meaningfully. Expect high "don't
know" rates and education-related bias, where answers partly measure
understanding:

`corporate_minimum_tax`, `gains_at_death`, `capital_gains_rate`,
`refuse_to_spend`, `emergency_duration`, `independent_agencies`,
`platform_liability`, `disparate_impact`, `carbon_border_fee`,
`mail_ballot_deadline`, `encryption_access`, `tariff_authority`,
`international_courts`, `qualified_immunity`.

**Fix:** keep them for the full issue map, but:
- Plain-language rewrites first. For example, `gains_at_death` could open
  with a concrete $100k → $1M example as its stem rather than its scope.
- Pre-register that they count toward axes only if "don't know" < 15% and
  they show no education bias.
- Consider dropping `corporate_minimum_tax` outright. It mostly repeats
  `corporate_rate` and is the hardest to understand.

### 1.8 Tradeoff questions

**Uneven costs.** Each side should name a real cost of comparable
weight.

| Question | Problem | Fix |
|---|---|---|
| `regulation_tradeoff` | A's costs are concrete ("prices rise and fewer businesses start"); B's is soft ("some people are less protected") | B: "…even if more workers and consumers are harmed by unsafe products or practices" |
| `outcomes_vs_chances` | B has no cost at all | Add "…even if some people end up far behind through no fault of their own" (or drop the item, §1.2) |
| `courts_vs_majority` | B has no cost | Add "…even if the law takes away some people's rights" |

**No middle option.** The 4-point Clearly/Lean scale forces a choice, by
design. But "torn" is a real position, and "I don't know enough" doesn't
describe it. Forcing it adds random noise to the Lean options.

**Test in Pilot A:** half of respondents get a fifth option, "Torn
between them", scored as the middle. If it is used by more than 15% and
improves retest stability, keep it.

**Labels to adjust:**
- "Americans first" (`weigh_foreigners`) echoes a political slogan. Use
  "Americans' interests come first".
- "Sell first, fix problems" (`precaution_tradeoff`) reads as slightly
  dismissive. Use "Allow first, fix problems".

### 1.9 Three-option ladders (137 of 319, 43%)

Many are fine because there really are only three positions (`gig_workers`,
`misconduct_records`). But where a real fourth position exists, add it.
More real options mean more information per question and fewer people
piled at the ends.

| Question | Missing position |
|---|---|
| `hate_crime_sentences` | "Only for crimes against a person, not property" |
| `abortion_public_funding` | "For low-income women only" between "like any care" and "only rape/incest/life" |
| `parent_notification` | "Yes, for students under 16; older students decide" |
| `school_pronouns` | "Teachers may use them but can't be required to" (a teacher-conscience position; common and missing) |
| `voter_id` | "Photo ID, with free IDs, but no backup option" between options 1 and 2 |
| `dual_citizenship` | Low-salience; leave at 3, or drop (§4) |
| `jawboning` | "Only with public disclosure of every request" |
| `encryption_access` | "Only with a warrant naming one device, and the method must stay with the company" |
| `ai_licensing` | "Licensing by an independent agency, not the government directly" (an industry-supported position) |
| `misinfo_penalty` | "Only for paid political ads" |

**Missing poles.** Each of these lacks a position held by roughly 3% or more:

| Question | Missing pole |
|---|---|
| `police_spending` | "Replace police departments with other public-safety services" (about 5–15% depending on wording in 2020–21 polls) |
| `climate_action` (core) | "Repeal existing climate rules and expand fossil fuel production", beyond "take no action" |
| `semi_auto_rifles` | "No federal background check for these sales" |
| `legal_immigration_level` | "No numerical limit for people who pass background checks" (small but real; keep only if free text shows it) |
| `nato` | "Leave NATO and close US bases in Europe" (current option 3 covers only part) |
| `gap_cause_tests` | Genetic explanations, flagged in notes; keep watching free text |

### 1.10 Multi-target questions with uneven extremity

`campus_speakers` lists three targets disliked more on the left and three
more on the right. The intent is balance, but extremity differs. "Some races
are naturally less intelligent" is far more extreme than "police departments
should be abolished". Tolerance scores will therefore look lower for people
who dislike the right-coded targets, which reflects the target choice, not
the people.

**Fix:** pair by extremity.

| Extremity | Usually disliked on the left | Usually disliked on the right |
|---|---|---|
| Mild | "Abortion should be illegal in all cases" | "Abortion should be legal at any point in pregnancy" |
| Medium | "Transgender women are not women" | "Police departments should be abolished" |
| Strong | "Some races are naturally less intelligent" | "Violent revolution against the US government is justified" |

Plus one target disliked on both sides (e.g. "Democracy should be replaced
by rule by experts"). Do the same check on `employer_speech_cases` (the four
cases are reasonably balanced) and on `use_force_cases` (balanced).

### 1.11 Near-consensus questions (little information)

These will probably draw 80% or more on one answer. That's fine for the
issue map, but expect them to fail screening as axis items. Don't spend
review effort polishing them:

`political_violence`, `accept_results`, `marriage_decisions`,
`preexisting_conditions`, `pardon_allies`, `helmet_law`, cases
`fr_missing_child`, `force_hostages`, `force_shipping`, `rf_restraining`,
`wr_caregiver`, `am_christian`, `mt_social` (possibly).

`rule_bending_leader` is also likely too skewed, because "ignores rules or
laws" is socially undesirable. Soften it to "bends rules" or "works around
rules" to get real variation. The ANES version that works uses "bend the
rules".

### 1.12 Facts to update or recheck

| Question | Issue | Action |
|---|---|---|
| `ss_shortfall` | The 2026 Trustees Report moved retirement trust fund depletion to late 2032 (combined funds 2034, about 83% payable) | Update the fact; the "early 2030s / about 80%" context is still roughly right, but change it to "2032–2034 … about 80%" |
| `defense_spending` | "Roughly $900 billion": FY2026 national defense is near or above $1 trillion when the 2025 reconciliation money is included | Change to "about $900 billion to $1 trillion" and recheck |
| `gun_purchase_age` | A 2025 federal appeals ruling (Fifth Circuit, *Reese v. ATF*) struck down the dealer handgun age limit within that circuit | Verify; if confirmed, add "in most of the country" |
| `immigrant_health_benefits` | The 2025 budget law narrowed Medicaid eligibility for some lawfully present immigrants starting in late 2026 | Verify and adjust "as today" |
| `aid_in_dying` | Count changes yearly (Delaware 2025; New York, Illinois in progress) | Recount before release |
| `education_department` | Functions were being moved to other agencies in late 2025 | Verify the scope line still describes its jobs |
| `foreign_aid_level` | "Before 2025 cuts" is a party cue and unsourced | Rewrite (§1.6) |

### 1.13 Wording and term choices

| Where | Now | Suggested | Why |
|---|---|---|---|
| `mt_surgery` | "Breast removal surgery" | "Chest surgery to remove breasts (mastectomy)" | Each side has its own term ("top surgery" / "breast removal"); combine both into a descriptive one |
| `puberty_blockers` definition | Source: Endocrine Society | Cite FDA labeling plus a descriptive line | One side regards that source as an advocate |
| `gender_identity` definition | Source: APA | Keep the text; source it as "descriptive" | Same reason |
| `hate_speech_law` option 2 | "As in some European countries" | Drop the Europe reference | It works as a cue in both directions |
| `climate_belief` option 0 | "…a serious threat that needs urgent action" | "…and a serious threat" | A belief question shouldn't contain a policy view |
| `teach_racism_history` option 2 | "Briefly, focusing more on progress…" | "Teach the facts of slavery and segregation fully, but not as the defining story of the country" | The current wording is a straw man; few people who hold this view would say "briefly" |
| `discrimination_*` | "Often (about 7 in 10)" | "Most of the time (about 7 in 10)" | Match the frequency scale used elsewhere |
| `hidden_power` | Fine, but name it honestly in the docs | — | It partly measures conspiracy thinking; analyze it separately from POP if it loads oddly |

---

## 2. What's missing (coverage gaps)

Ranked by how much each gap hurts accuracy, meaning which people the quiz
currently can't tell apart.

### 2.1 High priority: whole factions or major predictors

| Add | Proposed question (sketch) | Axis | Why it matters |
|---|---|---|---|
| **Federal deficit and debt** | "The federal government borrows about $1.8 trillion a year. Which comes closest to what to do?" Raise taxes mainly / cut spending mainly / both / borrowing is fine for now / balanced-budget amendment | REDIS (new FISCAL candidate) | The largest fiscal issue, absent; separates fiscal hawks from other conservatives and moderates from the left |
| **Markets vs socialism** | Public ownership of major industries (energy, railroads, banks); workers electing board members; "which system works best" ladder | REDIS / REG | Socialists and liberals currently look alike on most items; these separate them |
| **Causes of poverty (belief)** | "When people are poor in the US, the main reason is usually…" lack of effort / bad choices / circumstances they didn't choose / an unfair system | REDIS belief | One of the strongest known predictors of redistribution views, missing |
| **When life begins / moral status (belief)** | "At what point does a developing human have the same right to life as a born person?" conception / heartbeat (~6 weeks) / viability / birth / never a simple line | MORAL belief | Drives abortion positions; the clearest way to tell religious-moral from libertarian pro-life views |
| **Sex and gender (belief)** | "Whether someone is a man or a woman is determined by…" sex at birth only / mostly sex at birth / both / mostly gender identity / gender identity only | GENDERID belief | Strongest single predictor in the domain; currently only policy is asked |
| **Supreme Court expansion** | "Should Congress add seats to the Supreme Court?" | NORMS | Major live norms debate, missing |
| **Presidential immunity** | "Should a former president be immune from prosecution for official acts?" | NORMS | Central post-2024 question |
| **Government action against news outlets** | "Should a president be able to pull broadcast licenses or cut access for outlets that cover them unfairly?" | NORMS / SPEECH | Press freedom is a core norm, missing |
| **Congressional stock trading** | "Should members of Congress be banned from trading individual stocks?" | POP | Hugely popular across parties; strong POP item in position format (helps §1.1) |
| **Religious or cultural selection of immigrants** | "Should the US give preference to immigrants from countries whose culture is closer to America's / bar immigrants from certain religions?" | NATION / IMMIG | The pole that separates nationalist right from restrictionist right is missing |
| **Enforcement methods and limits** | Arrests at schools or churches; detaining families; deporting to third countries | IMMIG | Current fights are about methods; only levels are asked |

### 2.2 Medium priority: cross-cutting candidates (where the extra axes come from)

| Add | Axis | Note |
|---|---|---|
| Federal Reserve independence and who sets interest rates | NORMS / REG | Has flipped by party recently |
| Infrastructure and public investment level | REG / REDIS | |
| Farm subsidies and corporate subsidies ("corporate welfare") | REG / POP | Libertarians and the left agree against |
| Job guarantee | REDIS | Distinguishes left factions |
| Taxes on tips and overtime | REDIS / POP | Populist, popular across parties |
| Noncompete bans; right to repair | REG / TECH | Cross-cutting |
| Investor purchases of single-family homes | HOUSING / POP | Populist across parties |
| Mortgage interest deduction; transit vs roads; short-term rental limits | HOUSING | Gives HOUSING more than one sub-dimension |
| Fluoride, food dyes and additives (the "food freedom / clean food" agenda) | LIBERTY / ESTAB | New cross-party coalition since 2024 |
| Drinking age (21 vs 18); flavored vape bans; legal kidney sales; right-to-try drugs | LIBERTY | Pure paternalism items without left/right baggage, exactly what tests whether LIBERTY is real |
| Civil asset forfeiture; stop-and-frisk | ORDER / LIBERTY | Libertarian-left agreement |
| Stand-your-ground; gun maker liability; national registry; suppressor rules | GUNS | GUNS has only 12 answers and no self-defense item |
| Cryptocurrency regulation; a government digital dollar | TECH / PRIVACY | Cross-cutting |
| DNA databases and genetic genealogy in investigations | PRIVACY | |
| AI training on copyrighted work | TECH | Cross-cutting |
| Animal welfare / factory farming rules | REG / MORAL | Cross-cutting; real minority positions on both ends |
| Defamation law (should public figures find it easier to sue media?) | SPEECH | Live debate, flips by party |
| Public funding for public broadcasting | SPEECH / ESTAB | |
| Title IX campus misconduct hearings (due process vs protection) | SPEECH / EQUITY / ORDER | Cross-cutting |
| Confederate monuments and names | NATION / EQUITY | |
| Evolution in science classes | RELIGION / EDUC | |
| Legacy and donor admissions | EDUC / POP | Cross-cutting (both sides oppose) |
| Women in the draft and combat roles | FAMILY / HAWK | |
| Ranked-choice voting; DC and Puerto Rico statehood; voting age 16; noncitizens voting in local elections | VOTING | VOTING currently lacks any "reform" sub-dimension beyond access/security |
| Iran (strikes/negotiation); acquiring territory (Greenland, Panama Canal) | HAWK / NATION | Rotating current module |
| Discrimination perceptions for Hispanic, Asian, women, men, Christians | EQUITY belief | Two groups only now; a broader set separates general perception from group sympathy |

### 2.3 Values layer additions

The values module covers equality/freedom, order/liberty, tradition,
hierarchy, child-rearing, loyalty scope and human nature. Missing:

- **Purity/sanctity** (a defined pair: "Some things are sacred and
  shouldn't be done even if no one is harmed" vs its reverse). This is one
  of the best-replicated predictors of cultural views.
- **Zero-sum thinking** (pair: "When one group gains, another usually
  loses" vs reverse). It strongly predicts populism and immigration views on
  both sides.
- **Proportionality vs equality as fairness** (tradeoff: rewards should
  match contribution vs needs come first).
- **Locus of control / meritocracy belief** (position: what decides who
  gets ahead).

With these, VALUES gets the position-format items §1.1 asks for.

---

## 3. Domain-by-domain notes

Only what isn't already covered above. "Works" means no change needed.

**D01 Taxes & redistribution (25).**
- **Works:** `income_tax_structure`, `top_rate_number`, `wealth_tax`,
  `estate_tax_level`, `inheritance_principle`, `cash_aid_level`,
  `work_req_rule` + cases, `child_benefit_level`, `child_benefit_work`,
  `inequality_tradeoff`.
- **Fix:** `low_income_tax`, `ubi`, `corporate_rate`, `outcomes_vs_chances`
  (§1.4, §1.8).
- **Fix:** `large_fortunes` mixes a moral view ("a problem in themselves")
  with tax levels. It's acceptable, but the second and third options are
  close; consider "the richest should pay much more / somewhat more / the
  same / less".
- **Fix:** `wealth_tax` scope says "about 1 in 1,000 households", which is
  unverified. Check against the Survey of Consumer Finances or say "a tiny
  fraction".
- **Remove:** `corporate_minimum_tax` (§1.7).
- **Add:** deficit, poverty-cause belief, job guarantee, tips/overtime (§2).

**D02 Labor & business (16).**
- **Works:** `min_wage_jobs` (expect "none fit" from people who reject the
  premise; that's informative), `right_to_work`, `public_unions`,
  `paid_leave`, `gig_workers`, `merger_rules`, `bank_rules`, `licensing`,
  `price_controls`.
- **Fix:** `union_organizing` option 3, `regulation_tradeoff`, `bailouts`
  (§1.3, §1.8, §1.4).
- **Fix:** `sick_days`: options 2 and 3 differ only in federal vs state, so
  FED leaks in. Merge them into one "no requirement" option (the
  large-employers-only middle already exists), or move the federal/state
  part to `states_differ`.
- **Fix:** `big_company_breakup` option 0, "even if their prices are low",
  is a distinctive neo-Brandeis position. Keep it, and add the word
  "consumer" to option 1 so the contrast is clear.
- **Add:** socialism/ownership, workers on boards, noncompetes,
  subsidies (§2).

**D03 Health & social insurance (21).**
- **Works:** `coverage_guarantee`, `medicare_age`, `drug_prices`,
  `medicaid_scope`, `medicaid_work`, `ss_retirement_age`, `ss_payroll_cap`,
  `ss_private_accounts`, `insurance_mandate`, `preexisting_conditions`
  (low info), `school_vaccines` + cases.
- **Fix:** `ss_shortfall` fact (§1.12); `outbreak_vaccine_jobs` (§1.4).
- **Fix:** `private_insurance_role` is hypothetical ("suppose a government
  plan existed"). Fine, but expect "none fit" from opponents of such a plan.
  Pilot will tell.
- **Fix:** `immigrant_health_benefits` (§1.12).
- **Issue map only:** `drug_import`, `medicare_means_test`.
- **Add:** fluoride/food additives (§2.2); possibly "Should Medicare cover
  long-term nursing care?" (a large unasked cost question).

**D04 Housing (10).**
- **Works:** all ten.
- **Issue:** only 10 answers, every one in position format, all close to
  "build more / protect neighborhoods". To test whether HOUSING is its own
  axis, add 3–4 from §2.2 (investors, mortgage deduction, transit, rental
  limits).

**D05 Environment & energy (18).**
- **Works:** `net_zero_target`, `climate_willing_to_pay`,
  `drilling_public_lands`, `coal_plants`, `nuclear_power`,
  `nuclear_funding`, `ev_requirement`, `env_jobs_tradeoff`,
  `permitting_tradeoff`, `land_protection`, `sell_public_land`,
  `environmental_justice`.
- **Fix:** `carbon_tax` (§1.3), `climate_belief` (§1.13),
  `climate_agreements` and `ev_tax_credit` context (§1.6).
- **Fix:** `climate_action` (core) pole (§1.9).
- **Add:** plastic bans or local environmental rules (light), adaptation
  vs reduction (e.g. "Should government spending focus on preparing for
  climate effects or cutting emissions?"). That one is cross-cutting.

**D06 Trade (10).**
- **Works:** `tariff_level`, `tariff_price_tradeoff`, `trade_agreements`,
  `trade_jobs_tradeoff`, `china_trade`, `china_ownership`, `buy_american`,
  `offshoring_penalty`, `industrial_policy`.
- **Fix:** `tariff_authority`: add mirror cases (§1.5); people currently
  answer by tariff preference.
- **Add:** export controls on technology to rivals (short), and whether
  trade policy should favor allies (friend-shoring).

**D07 Technology & AI (16).**
- **Works:** `ai_regulation_level`, `ai_state_laws`, `ai_china_race`,
  `ai_licensing`, `ai_open_release`, `ai_job_loss`, `ai_layoff_limits`,
  `moderation_law`, `platform_liability`, `social_media_min_age`,
  `age_verification`, `algorithm_bias_testing`, `data_centers`,
  `election_deepfakes`, `automation_tax`.
- **Fix:** `moderation_level` (§1.3).
- **Add:** crypto, AI and copyright, AI companions for minors, autonomous
  vehicles (light). This domain moves fastest; set a 6-month review.

**D08 Privacy (12).**
- **Works:** all.
- **Add:** DNA databases, a workplace monitoring item, and the government
  digital dollar (§2.2).

**D09 Abortion & reproduction (12).**
- **Works:** `abortion_rule` + exceptions (core), `abortion_pills_mail`,
  `abortion_shield_laws`, `ivf_embryos`, `minors_abortion_parents`.
- **Fix:** `abortion_who_decides` (§1.4), `abortion_public_funding`
  (§1.9), `contraception_access` (§1.3).
- **Add:** the moral-status belief question (§2.1); surrogacy (light).

**D10 Sexuality & gender identity (21).**
- **Works:** `same_sex_adoption`, `wedding_vendors` + cases,
  `minors_transition` + cases, `bathrooms`, `id_sex_marker`,
  `lgbt_nondiscrimination` + exemptions.
- **Fix:** `same_sex_marriage` order (§1.4); `trans_adult_sports`
  (§1.3); `school_pronouns` option (§1.9); `mt_surgery` wording (§1.13).
- **Fix:** `bathrooms` options 0 and 1 are almost the same in practice
  (both let people use facilities matching their identity). Merge them,
  leaving three clearly different rules.
- **Add:** the sex/gender belief question (§2.1).

**D11 Religion (12).**
- **Works:** all, including `faith_based_laws` (a fair public-reason
  item).
- **Fix:** `vouchers_religious_schools`: its first option is
  unconstitutional since *Carson v. Makin* (2022). That's fine as a view,
  but say "regardless of current law" in the scope line.
- **Add:** evolution in science classes; government funding of faith-based
  charities.

**D12 Family (10).**
- **Works:** `promote_marriage`, `unmarried_partner_rights`,
  `stay_home_support`, `no_fault_divorce`, `pay_transparency`,
  `board_gender_rules`, `birth_rate_policy`.
- **Fix:** `family_arrangement` and `childcare_funding` (§1.3).
- **Fix:** `marriage_decisions` (near-consensus, §1.11). Replace it with
  something with more variance, such as "Are men and women naturally suited
  to different roles in family life?" (belief, defined options), or keep it
  for the issue map only.
- **Add:** women in the draft (§2.2) and the gender version of
  `workplace_diversity` (§1.3). FAMILY has only 10 answers and is
  "uncertain" in the plan; it needs 4–6 more to get a fair test.

**D13 Race & equity (18).**
- **Works:** `gap_cause_wealth`, `gap_cause_arrests`, `gap_cause_tests`,
  `hiring_race`, `contract_set_asides`, `dei_offices`, `reparations`,
  `local_redlining_compensation`, `hate_crime_sentences`, `race_districts`,
  `teach_institutional_racism`, `tribal_sovereignty`, `disparate_impact`.
- **Fix:** `teach_racism_history` (§1.13), `workplace_diversity` (§1.3),
  `discrimination_*` labels (§1.13).
- **Add:** discrimination perceptions for more groups; Confederate
  monuments (§2.2).

**D14 Immigration & nation (31).**
- **Works:** `legal_immigration_level`, `skills_vs_family`,
  `sponsor_relatives`, `military_border`, `everify`,
  `local_police_cooperation`, `asylum_rules`, `asylum_grounds`,
  `refugee_cap`, `birthright_citizenship`, `assimilation`,
  `american_basis`, `patriotic_education`, `anthem_kneeling`,
  `culture_tradeoff`, `us_exceptional`, `english_official`,
  `citizens_first`, status items (core).
- **Fix:** `temp_workers` (§1.3), `border_security` option 0 (§1.3).
- **Fix:** `american_criteria`: add one civic case ("Respecting American
  laws and institutions") as a reference point. Nearly everyone will rate
  it important, which shows how each person uses the scale.
- **Remove:** `immigration_pause` (§1.2). Also `dual_citizenship` (low
  salience; issue map at most).
- **Add:** enforcement methods; cultural or religious selection (§2.1).

**D15 Crime & policing (20).**
- **Works:** `crisis_responders`, `qualified_immunity`,
  `misconduct_records`, `mandatory_minimums`, `violent_sentences`,
  `death_penalty` + cases, `prison_purpose`, `second_chance`,
  `juveniles_adult_court`, `road_blocking`, `riot_response`,
  `troops_in_cities`, `victims_voice`.
- **Fix:** `police_spending` pole (§1.9); `private_prisons` retag (§1.4).
- **Remove:** `pretrial_danger` (§1.2).
- **Add:** civil asset forfeiture; stop-and-frisk (§2.2).

**D16 Guns (12).**
- **Works:** `private_sale_checks`, `magazine_limit`, `concealed_carry`,
  `red_flag` + cases, `second_amendment_meaning`, `handgun_purchase`
  (core).
- **Fix:** `carry_locations` (§1.3), `semi_auto_rifles` pole (§1.9),
  `gun_purchase_age` fact (§1.12).
- **Add:** self-defense law, maker liability, registry, suppressors. GUNS
  needs these to be tested as its own axis apart from ORDER.

**D17 Drugs & personal liberty (14).**
- **Works:** all.
- **Add:** the pure-paternalism items (drinking age, vape flavors, kidney
  sales, right-to-try, raw milk). LIBERTY is the axis compass-style quizzes
  assume and never test. Right now most of its items are drug or sex
  questions that also load on MORAL, so it needs items without moral
  content to show whether it's real.

**D18 Free speech (21).**
- **Works:** `hateful_speaker_response` (one of the best items in the
  bank), `protest_masks`, `campus_encampments`, `gov_misinformation`,
  `misinfo_penalty`, `jawboning`, `library_book_decisions`,
  `library_explicit`, `employer_speech` + cases, `flag_burning`.
- **Fix:** `campus_speakers` targets (§1.10); `hate_speech_law` wording
  (§1.13).
- **Add:** defamation law, public broadcasting funding, campus speech
  codes (§2.2).

**D19 Democratic norms (15).**
- **Works:** `exec_orders_scope`, `civil_service`,
  `independent_agencies`, `prosecute_opponents`, `pardon_allies`,
  `accept_results`, `checks_vs_action`, `political_violence`.
- **Fix:** mirror cases for `emergency_funding`, `refuse_to_spend` and
  `filibuster` (§1.5); `courts_vs_majority` cost (§1.8);
  `rule_bending_leader` wording (§1.11).
- **Add:** Court expansion, presidential immunity, action against news
  outlets, and court deference to agencies (§1.1, §2.1).

**D20 Elections (13).**
- **Works:** `voter_id` (with the §1.9 option), `proof_of_citizenship`,
  `mail_voting`, `auto_registration`, `felony_voting`, `electoral_college`,
  `popular_vote_loser`, `redistricting`, `campaign_spending`,
  `public_financing`, `congress_term_limits`, `court_term_limits`.
- **Fix:** `mail_ballot_deadline` is knowledge-heavy (§1.7).
- **Add:** ranked-choice voting, statehood, voting age, noncitizen local
  voting (§2.2).

**D21 Trust (31).**
- See §1.1 (format) and §1.2 (Congress items).
- **Fix:** `trust_police_fair` and `trust_military` behave differently from
  the other trust items. Police trust is strongly tied to race and to
  left/right; military trust leans right. Keep them, but expect them to
  split from TRUST in the analysis.
- **Add:** the position-format and reverse-keyed items (§1.1), and the
  stock trading ban (§2.1).

**D22 Foreign policy (25).**
- **Works:** `engagement_tradeoff`, `allies_tradeoff`, `troops_abroad`,
  `use_force_cases`, `global_health_aid`, `israel_military_aid`,
  `palestinian_state`, `ukraine_support`, `taiwan_defense`,
  `china_posture`, `united_nations`, `international_courts`,
  `human_rights_tradeoff`, `nuclear_arms_control`, `national_service`,
  `strikes_on_terrorists`, `arms_sales`.
- **Fix:** `nato` pole (§1.9); `defense_spending` fact (§1.12);
  `foreign_aid_level` context (§1.6).
- **Add:** Iran; territorial expansion (§2.2). Both go in the rotating
  module.

**D23 Education (12).**
- **Works:** all twelve.
- **Add:** evolution, legacy admissions (§2.2), and a phones-in-school or
  testing item only if wanted for engagement (both are low on ideology).
  EDUC has only 12 answers and the plan expects it may split into funding
  vs curriculum; each half needs about 6.

**D24 Federalism (12).**
- **Works:** `national_vs_state_tradeoff`, `closer_government_tradeoff`,
  `states_differ`, `state_preemption`, `federal_size`,
  `experimentation_tradeoff`.
- **Fix:** `grant_conditions` and `state_refusal` need mirror cases
  (§1.5). These are the items most likely to measure "whose side is in
  power".

**D25 Values (18).**
- **Works:** all pairs and tradeoffs.
- **Fix:** `weigh_foreigners` label (§1.8).
- **Add:** purity, zero-sum, proportionality, meritocracy (§2.3).

---

## 4. Summary of changes

| Action | Count | Items |
|---|---|---|
| **Remove** | 4 | `corporate_minimum_tax`, `immigration_pause`, `pretrial_danger`, `dual_citizenship` (issue map at most) |
| **Issue map only** (don't count toward axes yet) | 3 | `drug_import`, `medicare_means_test`, `marriage_decisions` (or replace) |
| **Split** into two or more questions | 9 | `carbon_tax`, `family_arrangement`, `childcare_funding`, `moderation_level`, `temp_workers`, `outbreak_vaccine_jobs`, `workplace_diversity`, `corporate_rate` (last option), `abortion_who_decides` |
| **Convert** to exception cases | 1 | `carry_locations` |
| **Rebuild options** | 6 | `low_income_tax`, `ubi`, `same_sex_marriage`, `bathrooms`, `sick_days`, `teach_racism_history` |
| **Add or extend options** | ~16 | §1.9 tables |
| **Reword** (cost, cue, term) | ~12 | §1.8, §1.13, `rule_bending_leader` |
| **Retag axis** | 3 | `private_prisons`, `aid_form`, `bailouts` (add POP) |
| **Add mirror cases** | 6 | `emergency_funding`, `refuse_to_spend`, `filibuster`, `tariff_authority`, `grant_conditions`, `state_refusal` |
| **Reverse-key / re-format trust** | ~12 changed or new | §1.1 |
| **Update facts / context** | 7 | §1.12 |
| **New questions** | ~45–55 | §2 |

Net result: roughly 380 → 430 questions (about 490 scored answers). Full
mode would go from about 75 to about 85 minutes. The pilot form length
stays the same: the extra questions spread across the 9 blocks make each
block slightly longer (pilot ≈ 48 minutes), or a 10th block can be added
by moving to a different balanced design.

## 5. Changes to the pre-registration and pilot

1. **Rewrite check 4** to test keying balance, not exclude formats (§1.1).
2. **Add the local dependence rule** (Yen's Q3 > .20 → testlet or drop;
   §1.2).
3. **Add the consistency measure** from mirror cases and say how it is
   reported (§1.5).
4. **Pilot A experiments**, all randomized within person:
   - context line shown vs hidden (§1.6);
   - a "Torn" middle on tradeoffs vs none (§1.8);
   - the original `top_income_tax` vs `top_rate_number` order, to check
     order effects within the cluster.
5. **Knowledge-heavy items** count toward axes only if "don't know" < 15%
   and they show no education bias (§1.7).

## 6. Suggested order of work

1. §1.1 trust format and the check 4 fix. These are critical, because
   without them a whole axis family can't be tested.
2. The splits, conversions and rebuilds in §4 (about 25 questions).
3. §2.1 high-priority additions (about 15 questions).
4. Mirror cases (§1.5) and the §1.8/§1.13 rewording.
5. §2.2 and §2.3 additions.
6. Validator, coverage, audit, rebuild the review kit and app, then send to
   the two-sided readers.
