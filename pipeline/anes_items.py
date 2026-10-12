"""ANES 2024 item specification: source variables, recodes and keying.

Every item is recoded to 0..K-1 with HIGH = the pole named in `high`.
Convention by hypothesized dimension:
  ECON, SPEND, CULT, GENDER, GROUP, ORDER, AUTH : high = conservative/restrictive pole
  TRUST     : high = less trust in institutions
  POP       : high = more anti-elite / populist
  NORMS     : high = less support for democratic checks and norms
  FOREIGN   : high = more international engagement / hawkish
  THREAT    : high = sees the country as more threatened
  TRADE     : high = more protectionist
The hypothesized dimension is only a label for reading the factor analysis;
dimensions are decided by the data.

Recode kinds:
  ("map", var, {orig: score})
  ("rev", var, n)            orig 1..n  -> n-1..0
  ("id", var, n)             orig 1..n  -> 0..n-1
  ("combo", base, strength, pos, neg, neither, nstr, strength_low_first)
      Folds a favor/oppose question and its follow-up strength question into one
      ordered scale. `pos` is the base code for the HIGH side, `neg` for the low
      side, `neither` the middle code (None if not offered). `nstr` = number of
      strength levels. Strength codes run strongest-first unless
      strength_low_first=True.
Negative codes and 99 ("haven't thought") are missing everywhere.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def combo(base, strength, pos, neg, neither=None, nstr=3, low_first=False):
    return ("combo", base, strength, pos, neg, neither, nstr, low_first)


ITEMS = [
    # id, spec, domain, hyp, high pole, short wording
    # ---------------- economics / role of government
    ("svc_spending7", ("rev", "V241239", 7), "economy", "ECON", "fewer services, less spending",
     "7-pt: government should provide many fewer services ... many more services"),
    ("health_insurance7", ("id", "V241245", 7), "health", "ECON", "private insurance plan",
     "7-pt: government insurance plan ... private insurance plan"),
    ("jobs_income7", ("id", "V241252", 7), "economy", "ECON", "let each person get ahead on their own",
     "7-pt: government should see to jobs and standard of living ... let each person get ahead"),
    ("env_business7", ("id", "V241258", 7), "environment", "ECON", "regulations already too much",
     "7-pt: tougher regulations on business needed ... regulations already too much a burden"),
    ("less_gov", ("rev", "V242248x", 6), "economy", "ECON", "the less government the better",
     "The less government the better vs there are more things government should be doing (with strength)"),
    ("gov_regulation", ("id", "V242249", 7), "economy", "ECON", "much less regulation",
     "Good for society to have more or less government regulation"),
    ("reduce_inequality", ("id", "V242253x", 7), "economy", "ECON", "oppose",
     "Favor/oppose government trying to reduce the difference in incomes"),
    ("millionaire_tax", ("map", "V242316a", {1: 0, 3: 1, 2: 2}), "taxes", "ECON", "oppose",
     "Favor/oppose increasing income taxes on people making over one million dollars a year"),
    ("min_wage", ("map", "V242350", {1: 0, 2: 1, 3: 2, 4: 2}), "economy", "ECON", "lowered/eliminated",
     "Federal minimum wage should be raised, kept the same, lowered or eliminated"),
    ("paid_leave", combo("V241367", "V241368", 2, 1, 3), "economy", "ECON", "oppose",
     "Require employers to offer paid leave to parents of new children"),
    ("deficit_importance", ("rev", "V242315", 5), "economy", "ECON", "extremely important",
     "How important is reducing the federal budget deficit"),
    ("campaign_limits", ("map", "V242214", {1: 0, 3: 1, 2: 2}), "elections", "ECON", "oppose",
     "Favor/oppose limits on how much money candidates can raise and spend"),
    # egalitarianism battery (balanced keying)
    ("egal_equal_opp", ("id", "V242254", 5), "equality", "ECON", "disagree",
     "Society should do whatever is necessary to make sure everyone has an equal opportunity"),
    ("egal_worry_less", ("rev", "V242255", 5), "equality", "ECON", "agree",
     "We'd be better off if we worried less about how equal people are"),
    ("egal_not_big_problem", ("rev", "V242256", 5), "equality", "ECON", "agree",
     "It is not really that big a problem if some people have more of a chance in life than others"),
    ("egal_treated_fairly", ("id", "V242257", 5), "equality", "ECON", "disagree",
     "If people were treated more equally in this country we would have many fewer problems"),
    # ---------------- spending priorities (increase / same / decrease)
    ("spend_socsec", ("map", "V241261", {1: 0, 3: 1, 2: 2}), "safety net", "SPEND", "decrease", "Federal spending on Social Security"),
    ("spend_schools", ("map", "V241264", {1: 0, 3: 1, 2: 2}), "education", "SPEND", "decrease", "Federal spending on public schools"),
    ("spend_welfare", ("map", "V241273", {1: 0, 3: 1, 2: 2}), "safety net", "SPEND", "decrease", "Federal spending on welfare programs"),
    ("spend_highways", ("map", "V241276", {1: 0, 3: 1, 2: 2}), "infrastructure", "SPEND", "decrease", "Federal spending on building and repairing highways"),
    ("spend_poor", ("map", "V241279", {1: 0, 3: 1, 2: 2}), "safety net", "SPEND", "decrease", "Federal spending on aid to the poor"),
    ("spend_environment", ("map", "V241282", {1: 0, 3: 1, 2: 2}), "environment", "SPEND", "decrease", "Federal spending on protecting the environment"),
    ("spend_health", ("id", "V242353x", 7), "health", "SPEND", "decrease", "Increase/decrease government spending to help people pay for health care"),
    ("opioids", ("id", "V242335x", 7), "health", "SPEND", "do less", "Should the government do more or less about opioid drug addiction"),
    # ---------------- environment
    ("climate_gov_action", combo("V241364", "V241365", 2, 1, 3), "environment", "ECON", "doing less",
     "Federal government should be doing more/less about rising temperatures"),
    ("greenhouse_regulation", ("id", "V242324x", 7), "environment", "ECON", "oppose",
     "Favor/oppose increased regulation on greenhouse emissions"),
    ("climate_effect", ("rev", "V242321", 5), "environment", "ECON", "not at all",
     "How much is climate change currently affecting severe weather and temperatures"),
    # ---------------- moral / cultural
    ("abortion7", ("id", "V241248", 7), "abortion", "CULT", "never permitted",
     "7-pt: abortion should always be permitted without restrictions ... never be permitted"),
    ("abortion4", ("map", "V241302", {4: 0, 3: 1, 2: 2, 1: 3}), "abortion", "CULT", "never permitted",
     "Standard 4-option abortion item (never ... always as personal choice)"),
    ("trans_bathrooms", combo("V241370", "V241371", 2, 1, 3), "gender identity", "CULT", "oppose",
     "Transgender people using bathrooms that match the gender they identify with"),
    ("trans_sports_ban", combo("V241373", "V241374", 1, 2, 3), "gender identity", "CULT", "favor ban",
     "Banning transgender girls from participating in K-12 girls' sports"),
    ("trans_military", ("id", "V242364x", 7), "gender identity", "CULT", "oppose",
     "Allowing transgender people to serve in the military"),
    ("gay_job_protection", combo("V241376", "V241377", 2, 1, None, nstr=2), "sexuality", "CULT", "oppose",
     "Laws to protect gays and lesbians against job discrimination"),
    ("gay_adoption", ("id", "V241381x", 6), "sexuality", "CULT", "should not be allowed",
     "Should gay and lesbian couples be allowed to adopt children"),
    ("gay_marriage", ("id", "V241382", 3), "sexuality", "CULT", "no legal recognition",
     "Legal marriage / civil unions only / no legal recognition (split ballot)"),
    ("moral_adjust", ("id", "V242258", 5), "morality", "CULT", "disagree",
     "The world is always changing and we should adjust our view of moral behavior"),
    ("trad_family", ("rev", "V242259", 5), "morality", "CULT", "agree",
     "This country would have many fewer problems if there were more emphasis on traditional family ties"),
    ("vaccines_schools", ("id", "V242319x", 7), "health", "CULT", "oppose",
     "Requiring children to be vaccinated to attend public schools"),
    ("colleges_run", ("id", "V241287x", 7), "education", "CULT", "disapprove",
     "Approve/disapprove of the way colleges and universities are being run"),
    # ---------------- gender roles
    ("man_works", ("rev", "V242279x", 7), "gender", "GENDER", "much better",
     "Better or worse if the man works outside the home and the woman takes care of home and family"),
    ("women_special_favors", ("rev", "V242280", 5), "gender", "GENDER", "always",
     "Women demanding equality seek special favors"),
    ("women_complain", ("rev", "V242281", 5), "gender", "GENDER", "always",
     "Women complaining about discrimination cause more problems than they solve"),
    ("harassment_too_far", ("rev", "V242361x", 5), "gender", "GENDER", "gone much too far",
     "Attention to sexual harassment has gone too far / not far enough"),
    # ---------------- race
    ("aid_blacks7", ("id", "V241255", 7), "race", "GROUP", "Blacks should help themselves",
     "7-pt: government should help Blacks ... Blacks should help themselves"),
    ("dei", ("id", "V241290x", 7), "race", "GROUP", "oppose",
     "Favor/oppose diversity, equity and inclusion (DEI) programs"),
    ("pref_hiring_blacks", ("id", "V242241x", 4), "race", "GROUP", "strongly against",
     "Preferential hiring and promotion of Blacks"),
    ("affirm_action_univ", ("id", "V242245x", 7), "race", "GROUP", "oppose",
     "Affirmative action in universities"),
    ("rr_no_favors", ("rev", "V242300", 5), "race", "GROUP", "agree",
     "Irish, Italians, Jewish and other minorities overcame prejudice; Blacks should do the same without special favors"),
    ("rr_slavery", ("id", "V242301", 5), "race", "GROUP", "disagree",
     "Generations of slavery and discrimination make it difficult for Blacks to work their way out of the lower class"),
    ("rr_less_deserve", ("id", "V242302", 5), "race", "GROUP", "disagree",
     "Over the past few years, Blacks have gotten less than they deserve"),
    ("rr_try_harder", ("rev", "V242303", 5), "race", "GROUP", "agree",
     "It's really a matter of some people not trying hard enough; if Blacks tried harder they could be as well off as whites"),
    ("whites_lose_jobs", ("rev", "V242519", 5), "race", "GROUP", "extremely likely",
     "How likely is it that whites won't get a job because employers hire minorities"),
    ("gov_treats_races", ("id", "V242522x", 7), "race", "GROUP", "treats Blacks much better",
     "Does the federal government treat Blacks or whites better"),
    ("police_treat_races", ("id", "V242525x", 7), "race", "GROUP", "treat Blacks much better",
     "Do the police treat Blacks or whites better"),
    ("disc_blacks", ("id", "V242549", 5), "race", "GROUP", "none at all", "Discrimination in the US against Blacks"),
    ("disc_hispanics", ("id", "V242550", 5), "race", "GROUP", "none at all", "Discrimination in the US against Hispanics"),
    ("disc_gays", ("id", "V242553", 5), "sexuality", "GROUP", "none at all", "Discrimination in the US against gays and lesbians"),
    ("disc_women", ("id", "V242554", 5), "gender", "GROUP", "none at all", "Discrimination in the US against women"),
    ("disc_whites", ("rev", "V242552", 5), "race", "GROUP", "a great deal", "Discrimination in the US against whites"),
    ("disc_men", ("rev", "V242555", 5), "gender", "GROUP", "a great deal", "Discrimination in the US against men"),
    ("diversity_better", ("id", "V242349x", 5), "identity", "GROUP", "a lot worse",
     "Increasing diversity has made the US a better or worse place to live"),
    # ---------------- immigration / national identity
    ("immig_policy", ("map", "V241386", {4: 0, 3: 1, 2: 2, 1: 3}), "immigration", "GROUP", "make felons and deport",
     "Policy toward unauthorized immigrants (felony+deport ... citizenship without penalty)"),
    ("end_birthright", combo("V241387", "V241388", 1, 2, 3), "immigration", "GROUP", "favor ending",
     "Ending birthright citizenship"),
    ("dreamers", combo("V241390", "V241391", 1, 2, None, nstr=3), "immigration", "GROUP", "sent back",
     "Children brought illegally: sent back vs allowed to live and work in the US"),
    ("border_wall", combo("V241393", "V241394", 1, 2, 3), "immigration", "GROUP", "favor", "Building a wall on the US border with Mexico"),
    ("spend_border", ("map", "V241267", {2: 0, 3: 1, 1: 2}), "immigration", "GROUP", "increase",
     "Federal spending on tightening border security to prevent illegal immigration"),
    ("immig_level", ("id", "V242227", 5), "immigration", "GROUP", "decreased a lot",
     "Number of immigrants permitted to come to the US should be increased a lot ... decreased a lot"),
    ("immig_jobs", ("rev", "V242228", 4), "immigration", "GROUP", "extremely likely",
     "How likely recent immigration levels will take jobs away from people already here"),
    ("immig_crime", ("rev", "V242231x", 7), "immigration", "GROUP", "increase a lot",
     "Effect of illegal immigration on the crime rate"),
    ("path_citizenship", ("id", "V242234x", 7), "immigration", "GROUP", "oppose",
     "Providing a path to citizenship for unauthorized immigrants"),
    ("immig_economy", ("id", "V242235", 7), "immigration", "GROUP", "extremely bad",
     "Immigrants are generally good or bad for America's economy"),
    ("immig_adapt", ("id", "V242236", 5), "immigration", "GROUP", "extremely important",
     "How important for immigrants to adapt to the customs and traditions of the US"),
    ("english_important", ("rev", "V241396", 4), "identity", "GROUP", "very important",
     "How important is it that people in the US be able to speak English"),
    ("natid_born", ("rev", "V242454", 4), "identity", "GROUP", "very important",
     "Importance of having been born in the US to being truly American"),
    ("natid_english", ("rev", "V242455", 4), "identity", "GROUP", "very important",
     "Importance of being able to speak English to being truly American"),
    # ---------------- law and order / guns
    ("death_penalty", combo("V241306", "V241307", 1, 2, None, nstr=2), "crime", "ORDER", "favor",
     "Death penalty for persons convicted of murder"),
    ("spend_crime", ("map", "V241270", {2: 0, 3: 1, 1: 2}), "crime", "ORDER", "increase", "Federal spending on dealing with crime"),
    ("urban_unrest7", ("id", "V241397", 7), "crime", "ORDER", "use all available force",
     "7-pt: solve problems of racism and police violence ... use all available force to maintain law and order"),
    ("police_force", ("rev", "V242336", 5), "policing", "ORDER", "never",
     "How often do police officers use more force than is necessary"),
    ("gun_buying", ("map", "V242325", {1: 0, 3: 1, 2: 2}), "guns", "ORDER", "easier",
     "Federal government should make it more difficult or easier to buy a gun"),
    ("gun_background", ("id", "V242328x", 7), "guns", "ORDER", "oppose", "Background checks for gun purchases"),
    ("assault_ban", ("id", "V242331x", 7), "guns", "ORDER", "oppose", "Banning 'assault-style' rifles"),
    ("voter_id", combo("V241317", "V241318", 1, 2, 3), "elections", "ORDER", "favor",
     "Requiring all people to show a government issued photo ID when they vote"),
    ("felon_voting", combo("V241320", "V241321", 2, 1, 3), "elections", "ORDER", "oppose",
     "Allowing convicted felons to vote once they complete their sentence"),
    # ---------------- authoritarian predisposition (child-rearing)
    ("cr_respect", ("map", "V242260", {1: 0, 3: 1, 2: 2}), "child-rearing", "AUTH", "respect for elders", "Independence vs respect for elders"),
    ("cr_manners", ("map", "V242261", {1: 0, 3: 1, 2: 2}), "child-rearing", "AUTH", "good manners", "Curiosity vs good manners"),
    ("cr_obedience", ("map", "V242262", {2: 0, 3: 1, 1: 2}), "child-rearing", "AUTH", "obedience", "Obedience vs self-reliance"),
    ("cr_behaved", ("map", "V242263", {1: 0, 3: 1, 2: 2}), "child-rearing", "AUTH", "well behaved", "Being considerate vs well behaved"),
    # ---------------- institutional trust
    ("trust_gov", ("id", "V241229", 5), "institutions", "TRUST", "never", "How often trust the federal government to do what is right"),
    ("trust_courts", ("id", "V241230", 5), "institutions", "TRUST", "never", "How often trust the court system to do what is right"),
    ("trust_media", ("rev", "V241335", 5), "institutions", "TRUST", "none", "Trust and confidence in the news media"),
    ("trust_congress", ("id", "V242417", 4), "institutions", "TRUST", "not at all", "Trust in Congress"),
    ("trust_government", ("id", "V242418", 4), "institutions", "TRUST", "not at all", "Trust in government"),
    ("trust_judiciary", ("id", "V242419", 4), "institutions", "TRUST", "not at all", "Trust in the judiciary"),
    ("trust_scientists", ("id", "V242420", 4), "institutions", "TRUST", "not at all", "Trust in scientists"),
    ("trust_parties", ("id", "V242421", 4), "institutions", "TRUST", "not at all", "Trust in political parties"),
    ("trust_trad_media", ("id", "V242422", 4), "institutions", "TRUST", "not at all", "Trust in traditional media"),
    ("votes_counted", ("rev", "V241314", 5), "elections", "TRUST", "not at all accurately",
     "How accurately will votes be counted in the November 2024 election"),
    ("trust_election_officials", ("rev", "V241315", 5), "elections", "TRUST", "not at all",
     "Trust the officials who oversee elections where you live"),
    ("vote_denied", ("id", "V241316", 5), "elections", "TRUST", "very often",
     "How often are eligible voters denied the right to vote"),
    # ---------------- anti-elitism / populism
    ("big_interests", ("map", "V241231", {2: 0, 1: 1}), "populism", "POP", "run by a few big interests",
     "Government run by a few big interests vs for the benefit of all"),
    ("gov_waste", ("rev", "V241232", 3), "populism", "POP", "waste a lot", "Do people in government waste tax money"),
    ("gov_corrupt", ("rev", "V241233", 5), "populism", "POP", "all", "How many of the people running the government are corrupt"),
    ("elections_attention", ("id", "V241235", 3), "populism", "POP", "not much",
     "How much do elections make the government pay attention to what people think"),
    ("donors_orgs", ("rev", "V242215", 5), "populism", "POP", "a great deal",
     "Congress passes laws that benefit organizations that contribute"),
    ("donors_individuals", ("rev", "V242216", 5), "populism", "POP", "a great deal",
     "Congress passes laws that benefit individuals who contribute"),
    ("votes_for_donations", ("rev", "V242217", 5), "populism", "POP", "all the time",
     "Members of Congress change their votes because of campaign donations"),
    ("system_insiders", ("id", "V242304", 5), "populism", "POP", "extremely well",
     "'Our political system only works for the insiders with money and power'"),
    ("rich_powerful", ("id", "V242305", 5), "populism", "POP", "extremely well",
     "'Because of the rich and powerful it becomes difficult for the rest of us to get ahead'"),
    ("corruption_widespread", ("rev", "V242456", 4), "populism", "POP", "very widespread",
     "How widespread is corruption such as bribe taking among politicians"),
    # ---------------- democratic norms
    ("norm_press_free", ("rev", "V241324", 5), "democracy", "NORMS", "not important",
     "Importance that news organizations are free to criticize political leaders"),
    ("norm_checks", ("rev", "V241325", 5), "democracy", "NORMS", "not important",
     "Importance that the branches keep one another from having too much power"),
    ("norm_consequences", ("rev", "V241326", 5), "democracy", "NORMS", "not important",
     "Importance that elected officials face serious consequences for misconduct"),
    ("norm_facts", ("rev", "V241327", 5), "democracy", "NORMS", "not important",
     "Importance that people agree on basic facts even if they disagree politically"),
    ("pres_unchecked", combo("V241328", "V241329", 1, 2, 3), "democracy", "NORMS", "helpful",
     "Helpful/harmful if presidents could work without paying attention to Congress and the courts"),
    ("restrict_journalists", combo("V241331", "V241332", 1, 2, 3), "democracy", "NORMS", "favor",
     "Elected officials restricting journalists' access to information about government decision-making"),
    ("media_undermined", ("rev", "V241334", 5), "democracy", "NORMS", "not at all concerned",
     "Concern that people in government might want to undermine the news media's ability to check power"),
    ("prefer_democracy", ("id", "V242409", 5), "democracy", "NORMS", "strongly disagree",
     "'Democracy is always and under all circumstances preferable to any other kind of government'"),
    ("courts_stop_gov", ("id", "V242410", 5), "democracy", "NORMS", "strongly disagree",
     "'The courts should be able to stop the government acting beyond its authority'"),
    ("strong_leader", ("rev", "V242411", 5), "democracy", "NORMS", "strongly agree",
     "'Having a strong leader in government is good even if the leader bends the rules'"),
    ("rule_business", ("rev", "V242413", 5), "democracy", "NORMS", "strongly agree",
     "Country would be run better if decisions were left to successful business leaders"),
    ("rule_experts", ("rev", "V242414", 5), "democracy", "NORMS", "strongly agree",
     "Country would be run better if decisions were left to independent experts"),
    ("rule_referendums", ("rev", "V242415", 5), "democracy", "NORMS", "strongly agree",
     "Country would be run better if decisions were left to citizens' referendums"),
    ("compromise", ("map", "V241336", {1: 0, 2: 1}), "democracy", "NORMS", "sticks to principles",
     "Prefer an official who compromises vs sticks to principles no matter what"),
    # ---------------- foreign policy
    ("stay_home", combo("V241310", "V241311", 2, 1, None, nstr=2), "foreign policy", "FOREIGN", "disagree (engaged)",
     "'This country would be better off if we just stayed home and did not concern ourselves with problems in other parts of the world'"),
    ("use_force", ("rev", "V241313", 5), "foreign policy", "FOREIGN", "extremely willing",
     "How willing should the US be to use military force to solve international problems"),
    ("defense7", ("id", "V241242", 7), "defense", "FOREIGN", "greatly increase", "7-pt: greatly decrease ... greatly increase defense spending"),
    ("ukraine_weapons", combo("V241398", "V241399", 1, 2, 3), "foreign policy", "FOREIGN", "favor",
     "US giving weapons to help Ukraine fight Russia"),
    ("israel_military_aid", combo("V241401", "V241402", 1, 2, 3), "foreign policy", "FOREIGN", "favor",
     "US giving military assistance to Israel"),
    ("palestinian_aid", combo("V241404", "V241405", 1, 2, 3), "foreign policy", "FOREIGN", "favor",
     "US giving humanitarian aid to Palestinians in Gaza"),
    ("side_israel", ("side", "V241407", "V241408"), "foreign policy", "FOREIGN", "Israelis a lot",
     "Side more with Israelis or Palestinians (with strength)"),
    ("gaza_protests", combo("V241410", "V241411", 2, 1, 3, low_first=True), "foreign policy", "FOREIGN", "disapprove a lot",
     "Approve/disapprove of protests against the war in Gaza"),
    ("us_better", ("rev", "V242266x", 5), "identity", "FOREIGN", "a lot better",
     "Is the US better or worse than most other countries"),
    ("threat_china", ("id", "V242365", 5), "foreign policy", "THREAT", "a great deal", "How much is China a threat to the US"),
    ("threat_russia", ("id", "V242366", 5), "foreign policy", "THREAT", "a great deal", "How much is Russia a threat to the US"),
    ("threat_mexico", ("id", "V242367", 5), "foreign policy", "THREAT", "a great deal", "How much is Mexico a threat to the US"),
    ("threat_iran", ("id", "V242368", 5), "foreign policy", "THREAT", "a great deal", "How much is Iran a threat to the US"),
    ("threat_japan", ("id", "V242369", 5), "foreign policy", "THREAT", "a great deal", "How much is Japan a threat to the US"),
    ("threat_israel", ("id", "V242370", 5), "foreign policy", "THREAT", "a great deal", "How much is Israel a threat to the US"),
    # ---------------- trade
    ("import_limits", ("rev", "V242226x", 4), "trade", "TRADE", "favor strongly", "Placing new limits on imports"),
    ("free_trade", ("id", "V242346x", 7), "trade", "TRADE", "oppose", "Free trade agreements with other countries"),
]

OUTCOMES = {
    "polviews": "V241177",      # 1-7, 99 haven't thought
    "pid7": "V241227x",         # 1-7
    "vote2024": "V242096x",     # 1 Harris 2 Trump ...
    "maga": "V241224",
    "age": "V241458x",
    "educ5": "V241465x",
    "race6": "V241501x",
    "sex": "V241550",
    "income6": "V241567x",
    "mode": "V240002a",
}
WEIGHT = "V240107a"   # pre-election full sample (fresh + panel + PAPI); used for all items
WEIGHT_POST = "V240107b"


def _clean(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    return x.where((x > 0) & (x != 99))


def _apply(spec, raw: pd.DataFrame) -> pd.Series:
    kind = spec[0]
    if kind == "map":
        return _clean(raw[spec[1]]).map(spec[2])
    if kind == "rev":
        n = spec[2]
        x = _clean(raw[spec[1]])
        return (n - x).where(x.between(1, n))
    if kind == "id":
        n = spec[2]
        x = _clean(raw[spec[1]])
        return (x - 1).where(x.between(1, n))
    if kind == "combo":
        _, base, strength, pos, neg, neither, nstr, low_first = spec
        b = _clean(raw[base])
        s = _clean(raw[strength])
        # intensity 1..nstr, where nstr = strongest
        inten = (s if low_first else (nstr + 1 - s)).where(s.between(1, nstr))
        mid = nstr if neither is not None else nstr - 1   # index of the middle / last-negative slot
        out = pd.Series(np.nan, index=raw.index)
        out[b == neg] = (nstr - inten[b == neg])                 # strongest neg -> 0
        if neither is not None:
            out[b == neither] = nstr
            out[b == pos] = nstr + inten[b == pos]               # strongest pos -> 2*nstr
        else:
            out[b == pos] = mid + inten[b == pos]
        return out
    if kind == "side":
        side = _clean(raw[spec[1]])
        amt = _clean(raw[spec[2]])       # 1 a little, 2 moderate, 3 a lot
        out = pd.Series(np.nan, index=raw.index)
        out[side == 2] = 3 - amt[side == 2]          # Palestinians a lot -> 0
        out[side.isin([3, 4])] = 3
        out[side == 1] = 3 + amt[side == 1]           # Israelis a lot -> 6
        return out
    raise ValueError(kind)


def ncat_of(spec) -> int:
    kind = spec[0]
    if kind == "map":
        return int(max(spec[2].values())) + 1
    if kind in ("rev", "id"):
        return spec[2]
    if kind == "combo":
        nstr, neither = spec[6], spec[5]
        return 2 * nstr + (1 if neither is not None else 0)
    if kind == "side":
        return 7
    raise ValueError(kind)


def source_vars(spec) -> list[str]:
    if spec[0] in ("map", "rev", "id"):
        return [spec[1]]
    return [spec[1], spec[2]]


def build(raw: pd.DataFrame):
    X = pd.DataFrame({iid: _apply(spec, raw) for iid, spec, *_ in ITEMS})
    ncats = {iid: ncat_of(spec) for iid, spec, *_ in ITEMS}
    for c in X.columns:   # sanity: codes inside 0..K-1
        bad = X[c].dropna()
        assert bad.between(0, ncats[c] - 1).all(), c
    w = pd.to_numeric(raw[WEIGHT], errors="coerce").fillna(0).to_numpy()
    w = w / w[w > 0].mean()
    out = pd.DataFrame({k: _clean(raw[v]) for k, v in OUTCOMES.items()})
    return X, ncats, w, out


def crosswalk() -> pd.DataFrame:
    return pd.DataFrame([{
        "item_id": iid, "anes_vars": "+".join(source_vars(spec)), "domain": dom,
        "hyp_dimension": hyp, "high_pole": high, "question_summary": text, "ncat": ncat_of(spec),
        "recode": repr(spec),
    } for iid, spec, dom, hyp, high, text in ITEMS])
