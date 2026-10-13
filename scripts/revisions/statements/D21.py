"""Trust and the establishment."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, freq, write, write_clarity  # noqa: E402

C, T = {}, {}

C["trust_fed_motives"] = {
    "why": "'Special interests' and 'decisions' had no examples.",
    "scope": "Agencies like the FDA, EPA, IRS and Department of Education, whichever party is in charge. Special interests means industries, donors, unions or advocacy groups with a stake in the decision.",
}
T["trust_fed_motives"] = freq("trust_fed_motives",
    "Federal agencies {f} try to serve the public rather than themselves or special interests.",
    ["Out of 10 decisions by agencies like the FDA, EPA or IRS, {n} are mainly meant to serve the public"])

T["trust_fed_honest"] = freq("trust_fed_honest",
    "Federal officials {f} hide mistakes or bad news from the public.",
    ["Out of 10 times something goes wrong, officials hide it {n} times"])

T["trust_courts"] = freq("trust_courts",
    "Federal judges {f} follow the law rather than their own politics in major cases.",
    ["Out of 10 major rulings, {n} follow the law rather than the judge's politics"])

T["trust_news_facts"] = freq("trust_news_facts",
    "Major news organizations {f} get the basic facts right.",
    ["Out of 10 stories from large newspapers and TV networks, {n} get the basic facts right"])

T["trust_news_fair"] = freq("trust_news_fair",
    "Major news organizations {f} slant political news toward one side.",
    ["Out of 10 political stories from large outlets, {n} are slanted"])

T["trust_scientists"] = freq("trust_scientists",
    "Scientists {f} report their findings honestly, even when unpopular.",
    ["Out of 10 university and institute studies, {n} report the results honestly"])

T["trust_expert_consensus"] = freq("trust_expert_consensus",
    "When most experts agree, they {f} turn out to be right.",
    ["Out of 10 things most doctors, economists or engineers agree on, {n} turn out right"])

T["trust_vote_count"] = freq("trust_vote_count",
    "Local election officials {f} count votes accurately.",
    ["Out of 10 federal elections, officials count the votes accurately in {n}"])

C["hidden_power"] = {
    "why": "'A small group of powerful people' was undefined.",
    "scope": "Think about national decisions in general. A small group means people like major donors, corporate executives, bankers or unelected officials acting out of public view.",
}
T["hidden_power"] = freq("hidden_power",
    "Major government decisions are made behind the scenes by a small group of powerful people {f}.",
    ["Out of 10 major national decisions, {n} are really made by donors, executives or insiders rather than voters and elected officials"])

T["corporate_power"] = [
    S("Large corporations have far too much influence; they decide most important things.",
      means=["Lobbying and donations decide most of what Washington does, more than voters"]),
    S("Large corporations have too much influence, though voters still have the final say.",
      means=["Lobbying and donations tilt policy, but elections still decide the big things"]),
    S("Large corporations have about the right amount of influence.",
      means=["Business lobbying is balanced by voters and other groups"]),
    S("Large corporations have too little influence; government and activists push them around.",
      means=["Regulators and activist pressure shape business more than business shapes government"]),
]

T["experts_vs_voters"] = trade(
    S("Experts should mainly make complex decisions like setting interest rates or approving medicines, even if most voters disagree.",
      yes=["An independent Federal Reserve setting rates", "FDA scientists deciding which medicines are approved"],
      no=["Elected officials overruling experts on these decisions"]),
    S("Officials who answer to voters should make these decisions, even if experts think they're wrong.",
      yes=["Elected officials setting rates or overruling medicine approvals"],
      no=["Leaving these decisions to unelected experts"]),
    S("You weigh experts and elected officials about equally.",
      means=["You'd let experts decide but give elected officials power to overrule them in clear cases"]))

C["expertise_vs_experience"] = {
    "why": "'The country's problems' had no examples.",
    "scope": "National problems like inflation, health care costs, crime, failing schools or a pandemic.",
}
T["expertise_vs_experience"] = trade(
    S("You'd rather rely on people with expert training, even if they're out of touch with everyday life.",
      means=["On problems like inflation, health costs or a pandemic, economists and doctors' judgment counts more than ordinary people's"]),
    S("You'd rather rely on the practical judgment of ordinary people, even if they lack expert knowledge.",
      means=["On problems like inflation, health costs or crime, everyday experience counts more than expert training"]),
    S("You'd rely on experts and ordinary people about equally.",
      means=["You'd want expert advice checked against ordinary people's practical sense"]))

T["trust_public_health"] = freq("trust_public_health",
    "Advice from agencies like the CDC is shaped by politics or industry rather than evidence {f}.",
    ["Out of 10 pieces of national health advice, {n} are shaped more by politics or industry than by evidence"])

T["trust_congress_effort"] = freq("trust_congress_effort",
    "When the country faces a serious problem, Congress {f} makes a real effort to solve it.",
    ["Out of 10 serious national problems, Congress makes a real effort on {n}"])

T["trust_congress_promises"] = freq("trust_congress_promises",
    "Members of Congress {f} break their main campaign promises.",
    ["Out of 10 members, {n} break the main promises they ran on"])

T["trust_state_gov"] = freq("trust_state_gov",
    "Your state government {f} wastes the money it spends.",
    ["Out of 10 dollars or programs your state spends on, {n} are wasted"])

T["trust_local_gov"] = freq("trust_local_gov",
    "Your local government {f} responds to what residents want.",
    ["Out of 10 local issues, your city or county follows residents' wishes on {n}"])

T["trust_police_fair"] = freq("trust_police_fair",
    "US police {f} treat the people they stop fairly.",
    ["Out of 10 police stops, {n} are handled fairly"])

T["trust_military"] = freq("trust_military",
    "Senior military leaders {f} give honest assessments to the public and elected officials.",
    ["Out of 10 public assessments of wars and threats by senior officers, {n} are honest"])

T["gov_big_projects"] = freq("gov_big_projects",
    "Big federal projects go far over budget or behind schedule {f}.",
    ["Out of 10 big federal projects, like highways or new programs, {n} go far over budget or run late"])

T["gov_services_work"] = freq("gov_services_work",
    "Federal services like Social Security payments and passports {f} work well.",
    ["Out of 10 times people rely on a federal service, it works well {n} times"])

T["trust_statistics"] = freq("trust_statistics",
    "Official statistics like unemployment and inflation are shaped to make those in power look good {f}.",
    ["Out of 10 official reports on jobs or prices, {n} are shaped to flatter whoever is in power"])

T["trust_university_research"] = freq("trust_university_research",
    "University research on social issues like crime and poverty is slanted by researchers' politics {f}.",
    ["Out of 10 university studies on social issues, {n} are slanted by the researchers' politics"])

T["trust_tech_companies"] = freq("trust_tech_companies",
    "Large tech companies {f} act in the public's interest.",
    ["Out of 10 decisions by social media and search companies, {n} serve the public's interest"])

T["news_source_accuracy"] = [
    S("Major news organizations give a much more accurate picture than independent sources.",
      means=["Large newspapers and TV networks are far more reliable than podcasts, newsletters and online creators"]),
    S("Major news organizations give a somewhat more accurate picture.",
      means=["Large outlets are somewhat more reliable than podcasts, newsletters and online creators"]),
    S("Major and independent sources are about equally accurate.",
      means=["Neither large outlets nor podcasts and newsletters are more reliable overall"]),
    S("Independent sources give a somewhat more accurate picture.",
      means=["Podcasts, newsletters and online creators are somewhat more reliable than large outlets"]),
    S("Independent sources give a much more accurate picture.",
      means=["Podcasts, newsletters and online creators are far more reliable than large newspapers and TV networks"]),
]

T["officials_care"] = freq("officials_care",
    "Elected officials {f} care what people like you think.",
    ["Out of 10 officials, {n} care what people like you think"])

T["economy_rigged"] = freq("economy_rigged",
    "Economic rules on taxes, trade and banking benefit the rich and powerful at everyone else's expense {f}.",
    ["Out of 10 economic rules, {n} favor the rich and powerful over everyone else"])

T["outsider_vs_experience"] = trade(
    S("You'd usually rather elect someone with long government experience, even if they're part of the system.",
      means=["Knowing how Congress and agencies work matters more to you than shaking things up"]),
    S("You'd usually rather elect an outsider who will shake up the system, even without government experience.",
      means=["Shaking up Washington matters more to you than knowing how it works"]),
    S("You value experience and outsiders about equally.",
      means=["You'd judge each candidate rather than prefer insiders or outsiders"]))

T["wall_street_vs_workers"] = freq("wall_street_vs_workers",
    "In downturns, government protects big banks and investors more than ordinary workers {f}.",
    ["Out of 10 downturns, the government favors banks and investors over workers in {n}"])

T["ballot_measures"] = [
    S("Every state should allow ballot measures, and there should be national ones too.",
      yes=["Citizen-initiated laws in every state", "A national ballot measure process"], no=["Leaving lawmaking to legislators"]),
    S("Every state should allow citizens to put laws on the ballot.",
      yes=["Ballot measures in all 50 states"], no=["National ballot measures", "Leaving some states without ballot measures"]),
    S("Each state should decide whether to allow ballot measures, as today.",
      yes=["Today's state-by-state system"], no=["Requiring or expanding them"]),
    S("There should be fewer ballot measures; elected legislators should make laws.",
      yes=["Restricting or ending citizen ballot measures"], no=["Expanding ballot measures"]),
]

T["recall_response"] = [
    S("You'd stop using a recalled product right away.", means=["A federal safety recall is reason enough for you"]),
    S("You'd stop using it, then check other sources.", means=["You'd follow the recall first and verify later"]),
    S("You'd check other sources before deciding.", means=["A federal recall alone wouldn't settle it for you"]),
    S("You'd keep using it unless you saw a problem yourself.", means=["A federal recall wouldn't change what you do"]),
]

T["budget_office_reliance"] = [
    S("Congress should treat the Congressional Budget Office's estimates as the final word.",
      yes=["Binding CBO scores on major bills"], no=["Overriding CBO estimates"]),
    S("Congress should rely heavily on CBO estimates, along with other evidence.",
      yes=["Weighing CBO scores heavily"], no=["Treating them as just one opinion"]),
    S("Congress should treat CBO estimates as one opinion among many.",
      yes=["Weighing CBO alongside outside estimates"], no=["Treating CBO as decisive"]),
    S("Congress should mostly ignore CBO estimates; they're often wrong.",
      yes=["Setting CBO scores aside"], no=["Relying on CBO estimates"]),
]

T["more_power_outcome"] = [
    S("More federal money and power would mostly fix a problem you care about.",
      means=["Giving Washington more resources is a reliable way to solve problems"]),
    S("More federal money and power would make real progress.",
      means=["It would help, though not fully solve the problem"]),
    S("More federal money and power would make a little progress and waste a lot.",
      means=["Most of the added money would be wasted"]),
    S("More federal money and power would make things worse.",
      means=["Washington would deepen the problem rather than fix it"]),
]

T["accept_certified_loss"] = [
    S("You'd accept a close loss once it's certified.", means=["Certification by officials is enough for you"]),
    S("You'd accept it after any recounts the law requires.", means=["Legally required recounts are enough for you"]),
    S("You'd want an independent audit before accepting it.", means=["Certification and recounts alone wouldn't be enough"]),
    S("You'd need confirmation from observers on your own side.", means=["You'd trust the result only if your side's observers agreed"]),
]

T["science_vs_officials"] = [
    S("Public health scientists should have the final say on health rules.",
      yes=["Scientists setting outbreak rules like closures and masks"], no=["Elected officials overruling them"]),
    S("Elected officials should decide, following scientists' advice in most cases.",
      yes=["Officials deciding but usually deferring to scientists"], no=["Scientists deciding alone", "Ignoring their advice"]),
    S("Elected officials should decide, with scientists' advice as one input.",
      yes=["Officials weighing science against economic and other concerns"], no=["Deferring to scientists by default"]),
    S("Elected officials should decide; scientists should advise only when asked.",
      yes=["Officials setting health rules on their own judgment"], no=["Scientists shaping rules by default"]),
]

T["congress_stock_ban"] = [
    S("Ban stock trading by members of Congress, their spouses and senior staff.",
      yes=["A broad congressional stock trading ban"], no=["Allowing trades with reporting"]),
    S("Ban stock trading by members of Congress only.",
      yes=["A ban on members' trades"], no=["Extending it to spouses and staff", "No ban"]),
    S("Reporting trades is enough; no ban.",
      yes=["Today's disclosure rules"], no=["A stock trading ban"]),
]

T["congress_motives"] = freq("congress_motives",
    "Major laws from Congress are mainly meant to help the public rather than donors or party leaders {f}.",
    ["Out of 10 major laws, {n} are mainly meant to help the public"])

if __name__ == "__main__":
    write("D21", T)
    write_clarity("D21", C)
