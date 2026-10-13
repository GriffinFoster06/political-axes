"""Add plain-language band descriptions to every axis in items/modules/axes.json.

Each axis gets five bands, from the minus pole to the plus pole:
  [-1, -0.6)  strongly minus
  [-0.6, -0.2) leaning minus
  [-0.2, 0.2]  middle
  (0.2, 0.6]   leaning plus
  (0.6, 1]     strongly plus
Each line describes what people in that band typically want, written so that
someone at either end would recognize their own view. The results page shows
the band a person falls in.

Run: python3 scripts/revisions/rev_2026_10_13_axis_bands.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "items" / "modules" / "axes.json"

BANDS = {
    "G": [
        "You take the left side on nearly every issue that divides the parties today.",
        "You take the left side on most issues that divide the parties, with some exceptions.",
        "You split your answers across the left–right line, or sit near the middle on many issues.",
        "You take the right side on most issues that divide the parties, with some exceptions.",
        "You take the right side on nearly every issue that divides the parties today.",
    ],
    "REDIS": [
        "Much higher taxes on the wealthy and large transfers, to sharply narrow the gap between rich and poor.",
        "Somewhat more redistribution: higher taxes at the top and a stronger safety net.",
        "Roughly today's mix of taxes and transfers, with targeted changes either way.",
        "Somewhat lower taxes and leaner transfers, favoring growth and work over redistribution.",
        "Low taxes and minimal transfers; incomes should be set by markets and private effort, not government.",
    ],
    "REG": [
        "Strong rules for business: powerful unions, high minimum wages, tough antitrust and consumer protection.",
        "More worker and consumer protection than today, with business still largely private.",
        "A mix: keep most current rules, trim some, add a few.",
        "Fewer rules on business and hiring; regulations often cost more than they save.",
        "Free markets with very light regulation; let contracts, competition and courts handle most problems.",
    ],
    "SOCINS": [
        "Health care and retirement as public guarantees: single-payer care, expanded Social Security.",
        "Bigger public role: a public option, expanded Medicaid and protected benefits.",
        "Keep the current public–private mix and fix it at the edges.",
        "More private choice: market-based plans, accounts and limits on program growth.",
        "Mainly private provision; government's role should be a narrow safety net at most.",
    ],
    "HOUSING": [
        "Override local limits so far more homes get built, including apartments in single-family areas.",
        "Loosen zoning and permitting to allow more housing, with some local say.",
        "Mixed: more building in some places, local control in others.",
        "Let communities keep their character; growth should be gradual and locally decided.",
        "Protect existing neighborhoods from densification; local control over land use comes first.",
    ],
    "TRADE": [
        "Open trade: low tariffs and trade deals, because they lower prices and grow the economy.",
        "Mostly free trade, with some protections and help for workers who lose out.",
        "Case by case: open trade with allies, protection for key industries.",
        "Use tariffs to protect American jobs and industry, even if prices rise somewhat.",
        "Broad tariffs and economic nationalism; bring production home whatever the cost.",
    ],
    "ENV": [
        "Act fast and at scale on climate, accepting real costs and limits on fossil fuels.",
        "Steady climate action through investment and regulation, minding the cost.",
        "Act on climate where it's cheap; keep energy affordable and reliable.",
        "Keep energy cheap and the economy growing; climate rules should be modest.",
        "Prioritize cost and growth; most climate regulation does more harm than good.",
    ],
    "TECH": [
        "Regulate AI and big tech tightly: licensing, liability, and breaking up the largest firms.",
        "Clear rules for AI and social media, especially for safety, kids and competition.",
        "Some targeted rules, but mostly wait and see.",
        "Light-touch rules so innovation isn't slowed; fix specific harms as they appear.",
        "Let technology develop freely; regulation mostly protects incumbents and slows progress.",
    ],
    "PRIVACY": [
        "Strong privacy rights: warrants for nearly everything, strict limits on data collection and surveillance.",
        "Lean toward privacy, with surveillance allowed under clear court oversight.",
        "Balance privacy and security case by case.",
        "Allow more monitoring and data use for security and law enforcement.",
        "Broad surveillance powers are worth it to stop crime and terrorism.",
    ],
    "MORAL": [
        "Personal choice on abortion and other moral questions; the law shouldn't enforce moral rules.",
        "Mostly personal choice, with some limits (for example later in pregnancy).",
        "Mixed: some limits and some choice, depending on the issue.",
        "Law should protect traditional moral standards on most of these issues, with some exceptions.",
        "Traditional morality in law: abortion banned or nearly so, moral rules enforced.",
    ],
    "GENDERID": [
        "Full legal recognition of gender identity, and same-sex marriage as settled.",
        "Support same-sex marriage and most transgender protections, with some exceptions (for example sports).",
        "Mixed: accept same-sex marriage but cautious on some gender identity policies.",
        "Law should mostly follow birth sex; skeptical of gender identity policies in schools and sports.",
        "Traditional definitions of sex, marriage and family in law.",
    ],
    "RELIGION": [
        "Strict separation of church and state: no religion in public schools or government.",
        "Mostly separate, with room for private religious expression and accommodation.",
        "Accommodate religion in public life without favoring it.",
        "More room for religion in public life: school prayer options, broad religious exemptions.",
        "The nation's laws and public life should reflect its religious heritage.",
    ],
    "FAMILY": [
        "Fully egalitarian roles; policy should support every family form equally.",
        "Mostly egalitarian, open to different family arrangements.",
        "Mixed views on marriage, child-rearing and men's and women's roles.",
        "Traditional family arrangements usually work best and deserve support.",
        "Marriage and traditional roles are central and should be favored by policy and culture.",
    ],
    "EQUITY": [
        "Active group-conscious remedies for racial gaps: affirmative action, targeted programs, reparations.",
        "Some group-conscious policies alongside universal ones.",
        "Mixed: universal programs, with some targeted help.",
        "Mostly colorblind rules; help should go by need, not race.",
        "Strictly colorblind law and policy; race-conscious programs should end.",
    ],
    "IMMIG": [
        "Much more immigration and a broad path to citizenship; deportations rare.",
        "More legal immigration and a path to citizenship, with border enforcement.",
        "Roughly current levels, with both enforcement and legalization for some.",
        "Less immigration, tougher enforcement, legal status only in limited cases.",
        "Sharply cut immigration and deport people here illegally.",
    ],
    "NATION": [
        "America is defined by its ideals and its diversity; no single culture is the national one.",
        "Shared ideals matter most, and diversity is a strength.",
        "Both shared ideals and a common culture matter.",
        "A common culture and language hold the country together.",
        "National identity rests on a shared culture, language and heritage that should be preserved.",
    ],
    "ORDER": [
        "Major reform: shrink policing and prisons, focus on rehabilitation and root causes.",
        "Reform-minded: fewer people in prison, more accountability for police.",
        "Both reform and enforcement, depending on the problem.",
        "Support police and firm punishment, with some reforms.",
        "More policing and tougher sentences; public order comes first.",
    ],
    "GUNS": [
        "Strict gun control: licensing, registration, bans on many weapons.",
        "More gun rules such as universal background checks and some weapon limits.",
        "Some added rules, but protect ordinary gun ownership.",
        "Protect gun rights; most new rules burden law-abiding owners.",
        "Broad gun rights with few restrictions; the right to bear arms is near absolute.",
    ],
    "LIBERTY": [
        "Adults decide for themselves on drugs, gambling and health risks.",
        "Mostly personal freedom, with some protective rules.",
        "Mixed: free on some choices, protective on others.",
        "Protective rules are often worth limits on personal freedom.",
        "Law should protect people from harmful choices like drugs and gambling.",
    ],
    "SPEECH": [
        "Protect almost all speech, including offensive, false and hateful speech.",
        "Strong free speech, with narrow limits.",
        "Protect most speech but limit some clearly harmful kinds.",
        "Harmful, false or hateful speech should face real limits.",
        "Broad limits on harmful speech are needed to protect people and society.",
    ],
    "NORMS": [
        "Strong checks and balances: limit presidential power, respect courts and institutional rules, whoever is president.",
        "Lean toward checks on the president, with room to act in emergencies.",
        "Balance presidential action with checks.",
        "Presidents should have more room to act without Congress or courts.",
        "A strong executive that can act decisively, even past traditional limits.",
    ],
    "VOTING": [
        "Make voting as easy as possible and reform elections (mail voting, automatic registration, new systems).",
        "Expand access, with reasonable security.",
        "Balance access and security.",
        "Tighten security (voter ID, cleaner rolls), keep traditional election methods.",
        "Strict security and traditional voting in person on Election Day.",
    ],
    "TRUST": [
        "Government is mostly honest and competent, whoever is in charge.",
        "Fairly trusting of government, with some doubts.",
        "Mixed trust in government.",
        "Fairly distrustful of government's honesty and competence.",
        "Deep distrust of government, whoever is in charge.",
    ],
    "ESTAB": [
        "Trust scientists, experts, the news media and official statistics.",
        "Mostly trust experts and the media, with some skepticism.",
        "Trust some experts and sources, not others.",
        "Skeptical of experts, mainstream media and official numbers.",
        "Deep distrust of experts, mainstream media and official institutions.",
    ],
    "POP": [
        "The system mostly works; elites and institutions mostly act in good faith.",
        "The system works, though it often favors the powerful.",
        "Mixed: some of the system works, some is rigged.",
        "The system is tilted toward elites and insiders.",
        "The system is rigged by elites; ordinary people need to take it back.",
    ],
    "FED": [
        "National standards on most big issues; states shouldn't set their own rules on rights.",
        "Lean toward national rules, with state flexibility on details.",
        "Some issues national, others left to states.",
        "Lean toward states and cities deciding most things.",
        "State and local control over nearly everything the Constitution doesn't reserve to Washington.",
    ],
    "EDUC": [
        "Strong public schools run by educators; no vouchers; curriculum set by professionals.",
        "Mostly public system and professional control, with some parental input.",
        "A mix of public schools, choice and parental say.",
        "More school choice and parental control over what's taught.",
        "Full school choice with public money following the child; parents decide what's taught.",
    ],
    "GLOBAL": [
        "Work through allies, international bodies, treaties and aid.",
        "Mostly work with allies and institutions, keeping some independence.",
        "Engage with the world selectively.",
        "Put America first; be wary of treaties, aid and international bodies.",
        "Go it alone: leave or ignore international bodies, cut foreign aid.",
    ],
    "HAWK": [
        "Military restraint: smaller military, force only as a last resort.",
        "Cautious about force, with a strong enough defense.",
        "Use force when clearly needed, keep a strong military.",
        "Ready to use force to protect interests and allies; a big military.",
        "Use force readily and keep overwhelming military power.",
    ],
    "VALUES": [
        "Equality and change come first; tradition and authority often stand in the way.",
        "Lean toward equality and change, with some respect for tradition.",
        "A balance of equality, change, order and tradition.",
        "Lean toward order, tradition and authority, with openness to change.",
        "Order, tradition and authority come first.",
    ],
}

data = json.loads(P.read_text())
seen = set()
data["overall"]["bands"] = BANDS["G"]; seen.add("G")
for f in data["families"]:
    for a in f["axes"]:
        a["bands"] = BANDS[a["id"]]
        seen.add(a["id"])
assert seen == set(BANDS), set(BANDS) ^ seen
assert all(len(v) == 5 for v in BANDS.values())
data["band_cuts"] = [-0.6, -0.2, 0.2, 0.6]
P.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print("bands written for", len(seen), "axes")
