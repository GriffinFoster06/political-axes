"""Review revisions, part A: fixes to existing questions (reports/question_review.md §1, §3).
Run once: python3 scripts/revisions/rev_2026_10_12a_fixes.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bankedit import Bank, item, FREQ, FREQ_REV, TRADE  # noqa: E402

b = Bank()
C = "2026-10-12"

# ---------- §1.1 reverse-key about half the frequency trust items ----------
def neg(iid, stem, scope=None, note=None):
    it = b[iid]
    it["stem"] = stem
    if scope:
        it["scope"] = scope
    it["options"] = list(FREQ_REV)
    it["high_pole"] = "almost always"
    it["notes"] = (note + " " if note else "") + "Reverse-keyed in review (frequent = distrust) so a 'how often' response style can't drive the axis."

neg("trust_fed_honest", "How often do federal officials hide mistakes or bad news from the public?")
neg("trust_news_fair", "How often do major national news organizations slant political news toward one side?")
neg("trust_statistics", "How often are official statistics, such as the unemployment and inflation rates, shaped to make whoever is in power look good?")
neg("trust_state_gov", "How often does your state government waste the money it spends?")
neg("gov_big_projects", "When the federal government takes on a big project, like building infrastructure or starting a new program, how often does it go far over budget or behind schedule?")
neg("trust_university_research", "When major universities publish research on social issues, like crime or poverty, how often is it slanted by the researchers' own politics?")
neg("trust_public_health", "When national public health agencies, like the CDC, give health advice, how often is it shaped by politics or industry pressure rather than evidence?")
neg("trust_congress_promises", "How often do members of Congress break the main promises they made when running for office?")
b["trust_police_fair"]["notes"] = "Police trust ties to race and to left-right more than other trust items; expected to split from TRUST toward ORDER/EQUITY."
b["trust_military"]["notes"] = "Military trust leans right; expected to load partly on HAWK rather than TRUST."

# ---------- §1.2 clusters: removals and testlet tags ----------
for iid in ["outcomes_vs_chances", "pretrial_danger", "immigration_pause", "corporate_minimum_tax"]:
    b.remove(iid)
for t, ids in {"top_tax": ["top_income_tax", "top_rate_number"],
               "experts": ["experts_vs_voters", "expertise_vs_experience"],
               "history_teaching": ["teach_racism_history", "teach_institutional_racism", "patriotic_education"],
               "nuclear": ["nuclear_power", "nuclear_funding"],
               "congress_trust": ["trust_congress_effort", "trust_congress_promises", "congress_motives"],
               "equality_freedom": ["inequality_tradeoff", "security_vs_choice", "fair_small_gaps", "fair_keep_earnings"]}.items():
    for iid in ids:
        b[iid]["testlet"] = t
for iid in ["drug_import", "medicare_means_test", "marriage_decisions", "dual_citizenship"]:
    b[iid]["issue_map_only"] = True

# ---------- §1.3 double-barreled ----------
cl = b["carry_locations"]
b.replace("carry_locations", item(
    "carry_locations", cl["subtopic"], ["GUNS"], "exceptions",
    "Should people with a carry permit be allowed to carry a gun in each of these places?",
    "Adults with a valid permit, not police. Answer each place separately.",
    ["Should not be allowed", "Should be allowed"], "Should be allowed",
    cases=[{"id": "cl_k12", "text": "K-12 schools, by trained teachers or staff"},
           {"id": "cl_college", "text": "College campuses"},
           {"id": "cl_bars", "text": "Bars and restaurants that serve alcohol"},
           {"id": "cl_gov", "text": "Government buildings, such as city halls"},
           {"id": "cl_worship", "text": "Places of worship"},
           {"id": "cl_business", "text": "Private businesses, unless the owner posts a ban"}]))

ml = b["moderation_level"]
mod_opts = ["Remove much more than they do now", "About as much as now", "Remove less; leave most of these posts up", "Remove only illegal content"]
b.replace("moderation_level",
          item("moderation_false", ml["subtopic"], ["TECH", "SPEECH"], "position",
               "How much should social media companies remove posts that are legal but false?",
               "Think about the largest platforms and what companies choose to do, not what the law requires.",
               mod_opts, "only illegal"),
          item("moderation_offensive", ml["subtopic"], ["TECH", "SPEECH"], "position",
               "How much should social media companies remove posts that are legal but offensive, such as insults aimed at a group?",
               "Think about the largest platforms and what companies choose to do, not what the law requires.",
               mod_opts, "only illegal"))

tw = b["temp_workers"]
tw_opts = ["Many more than today", "Somewhat more", "About the same", "Somewhat fewer", "Many fewer"]
b.replace("temp_workers",
          item("temp_workers_seasonal", tw["subtopic"], ["IMMIG"], "position",
               "Should the US admit more or fewer temporary foreign workers for seasonal farm and service jobs?",
               "Workers who come on visas for a season or a few years, then return home.", tw_opts, "fewer"),
          item("temp_workers_skilled", tw["subtopic"], ["IMMIG"], "position",
               "Should the US admit more or fewer temporary foreign workers for skilled jobs, such as engineers and programmers?",
               "Workers who come on visas for a set number of years.", tw_opts, "fewer",
               notes="Split from temp_workers in review: views on skilled and seasonal visas differ, including within parties."))

wd = b["workplace_diversity"]
wd["stem"] = "Should large employers run programs to increase the share of racial minorities in their workforce?"
b.append("d12_family_gender_roles.json", item(
    "workplace_gender_programs", "Gender equality policies at work", ["FAMILY", "EQUITY"], "position",
    "Should large employers run programs to increase the share of women in jobs and leadership roles where they are few?",
    "Private companies with more than 500 employees.",
    ["Yes, with specific hiring targets and required training", "Yes, through outreach and mentoring, without targets",
     "Only general training on treating everyone equally", "No such programs, but leave the choice to each company",
     "No such programs, and government should bar them at companies with federal contracts"], "no programs"))

ts = b["trans_adult_sports"]
ts["stem"] = "In college sports, should transgender women compete in women's events?"
ts["scope"] = "Competitive college teams with titles and records. Professional leagues set their own rules."

ct = b["carbon_tax"]
ct["options"] = ["Yes, a high and rising tax, around $100 a ton", "Yes, a moderate tax, around $25 to $50 a ton", "No carbon tax"]
b.insert_after("carbon_tax", item(
    "carbon_tax_use", "Carbon pricing", ["ENV", "REDIS"], "position",
    "If there were a federal carbon tax, what should the money mainly be used for?",
    "Answer even if you oppose a carbon tax.",
    ["Clean energy and climate programs", "Equal rebates paid to every household", "Cutting other taxes, such as income or payroll taxes"],
    "cut other taxes"))

fa = b["family_arrangement"]
b.replace("family_arrangement",
          item("work_arrangement", fa["subtopic"], ["FAMILY"], "position",
               "For a married couple with young children, which arrangement do you think is usually best?",
               "Assume any of these is affordable for them.",
               ["Both parents work full time and share childcare", "Both work, with one part time",
                "One parent stays home while the children are young"], "one at home"),
          item("caregiver_parent", fa["subtopic"], ["FAMILY"], "position",
               "When one parent stays home with young children, who should it usually be?",
               "Married couples of a man and a woman.",
               ["Whoever wants to or earns less; it shouldn't depend on sex", "Usually the mother, but either is fine",
                "The mother; young children need their mother at home"], "mother"))

cf = b["childcare_funding"]
b.replace("childcare_funding",
          item("childcare_spending", cf["subtopic"], ["FAMILY", "REDIS"], "position",
               "How much should government spend to help families with the cost of care for children under 5?",
               "Think about families of all incomes. How the help is given is asked next.",
               ["Enough to make childcare free for every family", "Enough that no family pays more than about 7% of its income",
                "Help for low-income families only, as today", "No government help"], "none"),
          item("childcare_form", cf["subtopic"], ["FAMILY"], "position",
               "Should government help for families with young children go mainly to childcare programs or directly to parents?",
               "Answer about the form of help, whatever amount you prefer.",
               ["Mainly to childcare programs, so parents can work", "Split between both",
                "Mainly to parents as cash, whether they use childcare or stay home"], "cash to parents"))

b["union_organizing"]["options"][3] = "Harder: hold new votes every few years for workers to keep the union"
b["border_security"]["options"][0] = "Fewer agents and barriers than today"
b["ubi"]["stem"] = "Should the federal government send every adult a regular cash payment, regardless of income or whether they work?"
ca = b["contraception_access"]
ca["options"][1] = "Insurance must cover it at no extra cost, as today"
for iid in ["hate_speech_law", "hate_crime_sentences"]:
    b[iid]["stem"] = b[iid]["stem"].replace("race, religion or sexual orientation", "race, religion, sexual orientation or gender identity")
b["dei_offices"]["stem"] = "Should public universities have offices focused on diversity, equity and inclusion?"

# ---------- §1.4 mixed dimensions ----------
b["corporate_rate"]["options"] = b["corporate_rate"]["options"][:4]
ov = b["outbreak_vaccine_jobs"]
b.replace("outbreak_vaccine_jobs",
          item("outbreak_gov_mandate", ov["subtopic"], ["LIBERTY"], "position",
               "During a serious outbreak of a contagious disease, should government require most workers to be vaccinated?",
               "Assume a vaccine widely judged safe and effective. Medical exemptions always apply.",
               ["Yes, most workers", "Only health care and other close-contact jobs", "No government requirement"], "no requirement"),
          item("outbreak_employer", ov["subtopic"], ["LIBERTY", "REG"], "position",
               "During a serious outbreak, should employers be allowed to require their own workers to be vaccinated?",
               "Assume a vaccine widely judged safe and effective. Medical exemptions always apply.",
               ["Yes, any employer", "Only health care employers", "No employer"], "no employer"))
aw = b["abortion_who_decides"]
aw["options"][1] = "Mostly by Congress, with room for states to adjust details"
ss = b["same_sex_marriage"]
ss["options"] = ["Legal marriage in every state, as today", "Civil unions with the same legal rights, but not called marriage", "No legal recognition"]
b["bailouts"]["axis"] = ["REG", "POP"]
b["private_prisons"]["axis"] = ["REG", "ORDER"]
b["aid_form"]["axis"] = ["LIBERTY", "REDIS"]
lit = b["low_income_tax"]
lit["options"] = ["Owe nothing, and get larger refundable credits than today", "Owe nothing, with about today's refundable credits",
                  "Owe nothing, but with smaller refundable credits than today", "Pay a small minimum income tax, such as $100 a year",
                  "Pay the same flat rate as everyone else, with no tax-free amount"]
b["ubi"]["options"] = ["Yes, enough to live on: about $1,500 a month or more", "Yes, a smaller payment of about $500 a month",
                       "No universal payment, but a guaranteed minimum income for anyone below a set level",
                       "No guaranteed income of any kind"]
b["ubi"]["high_pole"] = "no guaranteed income"

# ---------- §1.5 mirror cases ----------
NA = ["Should not be able to", "Should be able to"]
def mirror(parent, iid, stem, scope, cases, opts=NA):
    p = b[parent]
    p["followup"] = iid
    b.insert_after(parent, item(iid, p["subtopic"], p["axis"], "exceptions", stem, scope, opts, opts[-1], cases=cases,
                                notes="Mirror cases: the same rule with each side benefiting. Consistency across cases is scored separately (preregistration §6a)."))

mirror("emergency_funding", "emergency_funding_cases",
       "Should a president be able to declare an emergency to spend money that Congress refused to provide, for each of these?",
       "Answer each case separately, for any president.",
       [{"id": "em_wall", "text": "Building a wall on the southern border"},
        {"id": "em_clean", "text": "Building clean-energy projects"},
        {"id": "em_student_debt", "text": "Canceling student loan debt"},
        {"id": "em_hurricane", "text": "Rebuilding after a major hurricane"}])
mirror("refuse_to_spend", "refuse_to_spend_cases",
       "Should a president be able to refuse to spend money Congress approved for each of these?",
       "Answer each case separately, for any president.",
       [{"id": "rs_foreign_aid", "text": "Foreign aid"}, {"id": "rs_border", "text": "Border security"},
        {"id": "rs_clean", "text": "Clean-energy grants"}, {"id": "rs_police", "text": "Grants to local police departments"}])
mirror("filibuster", "filibuster_cases",
       "Suppose 51 senators but not 60 support each of these. Should the majority be able to pass it?",
       "Answer each case separately, whatever you think of the bill itself.",
       [{"id": "fb_abortion_protect", "text": "A national law protecting abortion access"},
        {"id": "fb_abortion_restrict", "text": "A national law restricting abortion"},
        {"id": "fb_mail_voting", "text": "A law expanding mail voting nationwide"},
        {"id": "fb_voter_id", "text": "A law requiring photo ID to vote nationwide"}],
       ["No; keep the 60-vote rule", "Yes; let the majority pass it"])
mirror("tariff_authority", "tariff_authority_cases",
       "Should a president be able to take each of these trade actions without a vote of Congress?",
       "Answer each case separately, for any president.",
       [{"id": "ta_raise", "text": "Raising tariffs on imports from a major trading partner"},
        {"id": "ta_cut", "text": "Cutting tariffs to lower prices"},
        {"id": "ta_human_rights", "text": "Blocking trade with a country over human rights abuses"}])
mirror("grant_conditions", "grant_conditions_cases",
       "Should the federal government be able to cut funding to states or cities for each of these reasons?",
       "Answer each case separately, under any administration.",
       [{"id": "gc_immigration", "text": "Refusing to help with federal immigration enforcement"},
        {"id": "gc_abortion", "text": "Passing strict limits on abortion"},
        {"id": "gc_sports_allow", "text": "Letting transgender girls play on girls' school teams"},
        {"id": "gc_sports_ban", "text": "Banning transgender girls from girls' school teams"},
        {"id": "gc_police_cuts", "text": "Cutting police budgets sharply"}])
mirror("state_refusal", "state_refusal_cases",
       "Should a state be able to refuse to help enforce each of these federal laws?",
       "Answer each case separately.",
       [{"id": "sr_immigration", "text": "Immigration laws"}, {"id": "sr_marijuana", "text": "Marijuana laws"},
        {"id": "sr_guns", "text": "Gun laws"}, {"id": "sr_abortion_pills", "text": "Federal rules on abortion pills"}],
       ["Must help enforce", "Can refuse"])
b["state_refusal"]["scope"] = "Think about federal laws in general, under any administration. Specific laws come next."

# ---------- §1.6 context without event cues ----------
b["climate_agreements"]["context"] = "The US is not currently part of the Paris Agreement."
b["ev_tax_credit"]["context"] = "There is currently no federal tax credit for buying an electric vehicle."
fal = b["foreign_aid_level"]
fal.pop("context", None)
fal["scope"] = "Economic, health and humanitarian aid, not military aid. It has usually been about 1% of the federal budget."

# ---------- §1.7 knowledge-heavy ----------
g = b["gains_at_death"]
g["stem"] = "Stock bought for $100,000 is worth $1 million when its owner dies. Under today's rules, the $900,000 gain is never taxed as income. What should happen?"
g["scope"] = "Think about large estates. Family farms and small businesses could get special treatment under any option."
for iid in ["gains_at_death", "capital_gains_rate", "refuse_to_spend", "emergency_duration", "independent_agencies",
            "platform_liability", "disparate_impact", "carbon_border_fee", "mail_ballot_deadline", "encryption_access",
            "tariff_authority", "international_courts", "qualified_immunity"]:
    b[iid]["knowledge_heavy"] = True

# ---------- §1.8 tradeoffs ----------
b["regulation_tradeoff"]["sides"][1]["text"] = "Fewer rules so businesses grow and prices stay low, even if more workers and consumers are harmed by unsafe practices."
b["courts_vs_majority"]["sides"][1]["text"] = "When most voters clearly support a law, courts should rarely overrule it, even if the law takes away some people's rights."
b["weigh_foreigners"]["sides"][1]["label"] = "Americans' interests first"
b["precaution_tradeoff"]["sides"][1]["label"] = "Allow first, fix problems"

# ---------- §1.9 options ----------
hc = b["hate_crime_sentences"]
hc["options"] = ["Yes, much longer", "Somewhat longer", "Only for crimes against people, not property", "No; punish the crime the same whatever the motive"]
pn = b["parent_notification"]
pn["options"] = ["Only if the student agrees", "Yes for students under 16; older students decide",
                 "Yes, unless staff believe the student would be at risk of abuse", "Yes, always"]
sp = b["school_pronouns"]
sp["options"] = ["Yes, whenever the student asks", "Yes, but only with a parent's consent",
                 "Teachers may use them, but no teacher can be required to", "No; use names and pronouns matching sex at birth"]
vi = b["voter_id"]
vi["options"] = ["No; signature checks and other methods are enough",
                 "Yes, but accept many kinds of ID, give IDs free, and allow a backup option for people without one",
                 "Yes, a photo ID, with free IDs for anyone who needs one, but no backup option",
                 "Yes, a government-issued photo ID, with no backup option"]
jb = b["jawboning"]
jb["options"] = ["No; officials should never pressure companies over legal speech", "Only for clear legal violations, like threats",
                 "Yes, but every request must be made public", "Yes, they can ask, and companies decide"]
al = b["ai_licensing"]
al["options"] = ["Yes, after government safety testing", "Yes, but licensed by an independent safety body, not a government agency",
                 "No approval, but companies must test for dangers and report results to the government", "No requirements beyond existing laws"]
ps = b["police_spending"]
ps["options"].insert(0, "Replace police departments with other public-safety services")
cla = b["climate_action"]
cla["options"].append("Repeal existing climate rules and expand fossil fuel production")
sa = b["semi_auto_rifles"]
sa["options"].append("Allow sales with no federal background check")
b["nato"]["options"][3] = "No; withdraw from NATO and bring US forces home from Europe"

# ---------- §1.10 campus speakers paired by extremity ----------
b["campus_speakers"]["cases"] = [
    {"id": "sp_abortion_illegal", "text": "Someone who argues that abortion should be illegal in all cases"},
    {"id": "sp_abortion_any", "text": "Someone who argues that abortion should be legal at any point in pregnancy"},
    {"id": "sp_trans_women", "text": "Someone who argues that transgender women are not women"},
    {"id": "sp_abolish_police", "text": "Someone who argues that police departments should be abolished"},
    {"id": "sp_stolen_election", "text": "Someone who argues that a recent presidential election was stolen"},
    {"id": "sp_israel", "text": "Someone who argues that Israel should not exist as a Jewish state"},
    {"id": "sp_race_iq", "text": "Someone who argues that some races are naturally less intelligent than others"},
    {"id": "sp_revolution", "text": "Someone who argues that violent revolution against the US government is justified"},
    {"id": "sp_expert_rule", "text": "Someone who argues that democracy should be replaced by rule by experts"},
]
b["campus_speakers"]["notes"] = "Targets paired by extremity (mild: abortion; medium: trans/police and election/Israel; strong: race/revolution) plus one disliked on both sides."

# ---------- §1.11 ----------
b["rule_bending_leader"]["stem"] = "How do you feel about a president who bends or works around rules that block what voters elected them to do?"

# ---------- §1.12 facts ----------
s = b["ss_shortfall"]
s["context"] = "Its trust funds are projected to run out between 2032 and 2034. After that, incoming taxes would pay about 80% of promised benefits."
s["facts"] = [{"claim": "2026 Trustees Report: OASI reserves depleted in Q4 2032; combined OASDI in Q3 2034, when about 83% of scheduled benefits would be payable",
               "source": "Congressional Research Service IF13256, 'Social Security: Selected Findings of the 2026 Annual Report' (June 2026)", "checked": C, "verify": False}]
d = b["defense_spending"]
d["scope"] = "Today it is roughly $900 billion to $1 trillion a year, more than the next several countries combined."
d["facts"][0]["claim"] = "US national defense spending about $0.9-1.0 trillion in FY2026 including 2025 reconciliation funds; exceeds the next ~9 countries combined"
gp = b["gun_purchase_age"]
gp["facts"][0]["verify"] = True
gp["facts"][0]["note"] = "A 2025 Fifth Circuit ruling (Reese v. ATF) held the dealer handgun age limit unconstitutional in that circuit; confirm status and add 'in most of the country' if it stands."
ih = b["immigrant_health_benefits"]
ih["options"][2] = "Most legal immigrants after 5 years, as today"
ih["facts"][0]["verify"] = True
ih["facts"][0]["note"] = "Public Law 119-21 (2025) narrows Medicaid eligibility for some lawfully present immigrants from late 2026; confirm and adjust context."
ed = b["education_department"]
ed["facts"] = [{"claim": "Department's main functions: federal student aid, civil rights enforcement, Title I funding", "source": "US Department of Education",
                "checked": C, "verify": True, "note": "Several functions were being moved to other agencies in late 2025; confirm the scope line."}]

# ---------- §1.13 wording ----------
for c in b["minors_transition_cases"]["cases"]:
    if c["id"] == "mt_surgery":
        c["text"] = "Chest surgery to remove the breasts (mastectomy)"
for dfn in b["minors_transition"]["definitions"]:
    if dfn["term"] == "puberty blockers":
        dfn["source"] = "descriptive; FDA labeling for GnRH agonists"
for dfn in b["bathrooms"]["definitions"]:
    if dfn["term"] == "gender identity":
        dfn["source"] = "descriptive"
b["hate_speech_law"]["options"][2] = "Yes, with fines or jail"
b["climate_belief"]["options"][0] = "Mostly caused by humans, and a serious threat"
b["teach_racism_history"]["options"][2] = "Teach the facts of slavery and segregation fully, but not as the defining story of the country"
for iid in ["discrimination_black", "discrimination_white"]:
    b[iid]["options"] = [o.replace("Often (about 7 in 10)", "Most of the time (about 7 in 10)") for o in b[iid]["options"]]

# ---------- §3 domain notes ----------
lf = b["large_fortunes"]
lf["options"] = ["They are a problem in themselves; taxes should be set to shrink them over time", "The richest should pay much more in taxes than now",
                 "The richest should pay somewhat more than now", "The richest pay about the right amount now",
                 "Taxes on the richest are already too high and discourage investment"]
b["wealth_tax"]["scope"] = "Assume the tax applies only to wealth above $50 million, a tiny fraction of households."
b["wealth_tax"]["facts"][0]["note"] = "Scope now says 'a tiny fraction' instead of an unverified count."
sd = b["sick_days"]
sd["options"] = ["Yes, at least 7 days a year, for all employers", "Yes, but only employers with more than 50 workers", "No requirement; leave it to states and employers"]
b["big_company_breakup"]["options"][1] = "Break them up only if they are proven to hurt consumers, workers or competitors"
bt = b["bathrooms"]
bt["options"] = ["Those matching their gender identity", "Private single-person facilities, or those matching their sex at birth", "Only those matching their sex at birth"]
b["vouchers_religious_schools"]["scope"] = "Answer even if you oppose public money for private schools, and regardless of current law."
amc = b["american_criteria"]
amc["cases"].insert(0, {"id": "am_laws", "text": "Respecting American laws and institutions"})

b.save()
print("part A applied")
