"""Review revisions, part B: new questions for the coverage gaps (reports/question_review.md §1.1, §2).
Also appends the new subtopics to items/blueprint.csv. Run once.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bankedit import Bank, item, FREQ, TRADE, AGREE, MEAN, ROOT  # noqa: E402

b = Bank()
C = "2026-10-12"
NEW_SUBTOPICS = []  # (domain_id, domain, subtopic, axis, draft, min, format, tag, note)


def sub(did, dname, name, axis, n, fmt, tag="core", note="Added in review 2026-10-12"):
    NEW_SUBTOPICS.append((did, dname, name, axis, n, 1, fmt, tag, note))
    return name


def tradeoff(iid, st, axis, stem, scope, a, b_, **kw):
    return item(iid, st, axis, "tradeoff", stem, scope, list(TRADE), "Clearly B",
                sides=[{"label": a[0], "text": a[1]}, {"label": b_[0], "text": b_[1]}], **kw)


def agree_pair(id1, id2, st, axis, s1, s2):
    """s1 keyed toward the high pole when agreed with; s2 the reverse."""
    m_rev = list(reversed(MEAN))
    return (item(id1, st, axis, "agree_defined", s1, "Use the meanings shown for each answer.", list(AGREE), "Strongly agree",
                 point_meanings=list(MEAN), pair=id2),
            item(id2, st, axis, "agree_defined", s2, "Use the meanings shown for each answer.", list(reversed(AGREE)), "Strongly disagree",
                 point_meanings=m_rev, pair=id1))


# ================= D01 =================
D = "Taxes & redistribution"
s = sub("D01", D, "Federal deficit and debt", "REDIS", 2, "position")
b.append("d01_taxes_redistribution.json",
    item("deficit_approach", s, ["REDIS", "SOCINS"], "position",
         "The federal government spends much more than it collects in taxes. Which comes closest to what should be done?",
         "Think about the next ten years.",
         ["Borrowing is fine for now; focus on other priorities", "Close the gap mainly by raising taxes on high earners and corporations",
          "Close the gap with an even mix of tax increases and spending cuts", "Close the gap mainly by cutting spending",
          "Close the gap entirely by cutting spending, with no tax increases"], "spending cuts only",
         context="In 2025 the federal government spent about $1.8 trillion more than it collected.",
         facts=[{"claim": "FY2025 federal deficit about $1.8 trillion", "source": "Congressional Budget Office, Monthly Budget Review (Oct 2025)", "checked": C, "verify": True}],
         notes="Option 0 is held on both left (spend now) and right (cut taxes now); expect a non-monotone curve and check with the nominal model."),
    item("balanced_budget_amendment", s, ["REDIS", "FED"], "position",
         "Should the Constitution require the federal government to balance its budget every year?",
         "Spending could not exceed tax revenue in a year.",
         ["No; the government needs to be able to borrow", "Only in normal times, with exceptions for wars and recessions", "Yes, every year, with no exceptions"],
         "every year"))
s = sub("D01", D, "Causes of poverty (belief)", "REDIS", 1, "belief")
b.append("d01_taxes_redistribution.json",
    item("poverty_cause", s, ["REDIS"], "belief",
         "When people in the US are poor, what is usually the main reason?",
         "Think about working-age adults without disabilities.",
         ["An economic system that is unfair to them", "Circumstances they didn't choose, like where they grew up or bad luck",
          "A mix of their circumstances and their own choices", "Their own choices, like dropping out of school or not working",
          "Lack of effort"], "individual causes"))
s = sub("D01", D, "Job guarantee", "REDIS", 1, "position")
b.append("d01_taxes_redistribution.json",
    item("job_guarantee", s, ["REDIS", "REG"], "position",
         "Should the federal government guarantee a job to anyone who wants to work but can't find one?",
         "Public jobs such as care work or infrastructure, paid at least the minimum wage.",
         ["Yes, for anyone who wants one", "Only in areas with high unemployment", "No; help with job searches and training instead", "No; jobs should come from the private sector"],
         "private sector"))
s = sub("D01", D, "Taxes on tips and overtime", "REDIS", 1, "position")
b.append("d01_taxes_redistribution.json",
    item("tips_overtime_tax", s, ["REDIS", "POP"], "position",
         "Should income from tips and overtime pay be taxed the same as other wages?",
         "Federal income tax only.",
         ["Yes, all income should be taxed the same way", "Exempt it only for workers with low or middle incomes", "Exempt it for everyone"],
         "exempt for everyone",
         notes="Popular across parties; a POP candidate as much as REDIS."))

# ================= D02 =================
D = "Labor & business regulation"
s = sub("D02", D, "Markets vs public ownership", "REG", 3, "position")
b.append("d02_labor_business.json",
    item("economic_system", s, ["REG", "REDIS"], "position",
         "Which kind of economy do you think works best?",
         "Think about how the economy is organized overall.",
         ["Most major industries owned by the public or by their workers", "Private businesses, but with government running key industries like energy and health care",
          "Private businesses and markets, with strong government rules and a large safety net", "Private businesses and markets, with modest rules and a basic safety net",
          "Private businesses and free markets, with as little government as possible"], "free markets"),
    item("public_ownership", s, ["REG"], "position",
         "Should the government own and run industries like electricity, railroads and internet service?",
         "Owned by federal, state or local government, as some cities do with electricity today.",
         ["Yes, most of them", "Some of them, where private companies have failed", "Only in places with no private provider", "No; private companies should run them"],
         "private"),
    item("workers_on_boards", s, ["REG"], "position",
         "Should workers at large companies elect some members of the company's board of directors?",
         "Companies with more than 1,000 employees. Germany requires this.",
         ["Yes, about half the board", "Yes, about a third of the board", "Allow it if companies choose, but don't require it", "No"],
         "no"))
s = sub("D02", D, "Noncompete agreements and right to repair", "REG", 2, "position")
b.append("d02_labor_business.json",
    item("noncompetes", s, ["REG"], "position",
         "Should employers be allowed to make workers agree not to work for a competitor after they leave?",
         "Agreements that block a worker from a similar job for a period after leaving.",
         ["No, ban them for all workers", "Only for top executives", "Allow them, but limit them to a year or less", "Allow them; it's a contract both sides agreed to"],
         "allow"),
    item("right_to_repair", s, ["REG", "TECH"], "position",
         "Should companies be required to make parts, tools and manuals available so owners and independent shops can repair products?",
         "Products like phones, cars and farm equipment.",
         ["Yes, for most products", "Only for products where repair matters most, like cars and farm equipment", "No; companies should decide"],
         "no"))
s = sub("D02", D, "Business subsidies", "REG", 2, "position")
b.append("d02_labor_business.json",
    item("farm_subsidies", s, ["REG"], "position",
         "What should happen to federal payments and subsidized insurance for farmers?",
         "Programs that pay farmers when prices or harvests fall.",
         ["Expand them", "Keep them about as they are", "Limit them to small and mid-size farms", "Phase them out"],
         "phase out",
         notes="Expected to cross-cut: opposed by free-market and some left voters, supported in farm regions of both parties."),
    item("business_incentives", s, ["REG", "POP"], "position",
         "Should states and cities offer tax breaks to persuade companies to build factories or offices there?",
         "Deals like tax breaks for a company that brings jobs to an area.",
         ["Yes, they bring jobs", "Only with strict job guarantees and repayment if the company leaves", "No; ban these deals"],
         "ban"))
s = sub("D02", D, "Federal Reserve and interest rates", "REG", 1, "position")
b.append("d02_labor_business.json",
    item("fed_independence", s, ["NORMS", "REG"], "position",
         "Who should decide the interest rates set by the Federal Reserve?",
         "Answer for any president of either party.",
         ["The Federal Reserve alone, with no pressure from elected officials", "The Federal Reserve, but Congress should review its decisions more closely",
          "The president should be able to direct the Federal Reserve"], "president"))
s = sub("D02", D, "Infrastructure investment", "REG", 1, "position")
b.append("d02_labor_business.json",
    item("infrastructure", s, ["REG", "REDIS"], "position",
         "How much should the federal government spend on roads, bridges, water systems and the power grid?",
         "Compared with today. Assume the money is borrowed or comes from taxes.",
         ["Much more", "Somewhat more", "About the same", "Less; leave more to states and private companies"], "less"))

# ================= D03 =================
D = "Health care & social insurance"
s = sub("D03", D, "Food additives and fluoride", "LIBERTY", 2, "position")
b.append("d03_health_social_insurance.json",
    item("water_fluoride", s, ["LIBERTY", "ESTAB"], "position",
         "Should cities add fluoride to drinking water to prevent tooth decay?",
         "Most US public water systems do this today.",
         ["Yes, as health agencies recommend", "Let each city decide", "No; it should be banned"], "banned",
         notes="New cross-party coalition since 2024; tests ESTAB and LIBERTY apart from left-right."),
    item("food_additives", s, ["REG", "ESTAB"], "position",
         "Should the government ban food additives, such as some artificial dyes, that are allowed in the US but banned in other countries?",
         "Additives approved by US regulators.",
         ["Yes, ban them", "Require clear warning labels instead", "No; trust US regulators' approval"], "trust regulators"))
s = sub("D03", D, "Long-term care", "SOCINS", 1, "position")
b.append("d03_health_social_insurance.json",
    item("long_term_care", s, ["SOCINS"], "position",
         "Who should pay for nursing home and home care for older people who can no longer care for themselves?",
         "Today Medicare covers little long-term care; Medicaid pays after people spend down their savings.",
         ["A new government insurance program for everyone", "Government help for middle-income families too, not only the poor",
          "Keep today's system", "Families and private insurance, with less government help"], "families"))

# ================= D04 =================
D = "Housing & land use"
s = sub("D04", D, "Investors and short-term rentals", "HOUSING", 2, "position")
b.append("d04_housing_land_use.json",
    item("investor_homes", s, ["HOUSING", "POP"], "position",
         "Should large investment firms be allowed to buy single-family homes to rent out?",
         "Firms owning hundreds or thousands of homes.",
         ["No, ban it", "Allow it, but with limits or extra taxes", "Yes, they add rental housing"], "allow"),
    item("short_term_rentals", s, ["HOUSING", "REG"], "position",
         "Should cities limit short-term rentals like Airbnb in residential neighborhoods?",
         "Whole homes rented to visitors by the night.",
         ["Ban them in most neighborhoods", "Allow them only in the owner's own home", "Allow them with registration and taxes", "No limits"],
         "no limits"))
s = sub("D04", D, "Homeownership subsidies", "HOUSING", 1, "position")
b.append("d04_housing_land_use.json",
    item("mortgage_deduction", s, ["HOUSING", "REDIS"], "position",
         "Should homeowners be able to deduct mortgage interest from their federal income taxes?",
         "Today this deduction mostly benefits higher-income homeowners who itemize.",
         ["No; end it and use the money for renters or first-time buyers", "Keep it, but only for smaller mortgages", "Keep it as is", "Expand it"],
         "expand"))
s = sub("D04", D, "Transit vs roads", "HOUSING", 1, "position")
b.append("d04_housing_land_use.json",
    item("transit_vs_roads", s, ["HOUSING", "ENV"], "position",
         "How should transportation money be split between public transit and roads?",
         "Federal and state transportation spending.",
         ["Much more to transit, less to new roads", "Somewhat more to transit", "Keep about today's split", "More to roads and highways"],
         "roads"))

# ================= D05 =================
D = "Environment & energy"
s = sub("D05", D, "Adaptation vs emissions cuts", "ENV", 1, "tradeoff")
b.append("d05_environment_energy.json",
    tradeoff("adaptation_tradeoff", s, ["ENV"], "For climate change, where should government money mainly go?",
             "Answer even if you doubt climate change matters much.",
             ("Cut emissions", "Cutting emissions, even if less is spent protecting communities from floods and heat."),
             ("Prepare for effects", "Protecting communities from floods and heat, even if emissions are cut more slowly."))),
s = sub("D05", D, "Local environmental rules", "ENV", 1, "position")
b.append("d05_environment_energy.json",
    item("plastic_bags", s, ["ENV", "LIBERTY"], "position",
         "Should single-use plastic bags be banned or charged for in stores?",
         "Bags given out at checkout.",
         ["Banned", "Allowed, with a fee per bag", "Allowed, free, as each store chooses"], "allowed free"))

# ================= D06 =================
D = "Trade & economic nationalism"
s = sub("D06", D, "Export controls and friend-shoring", "TRADE", 2, "position")
b.append("d06_trade.json",
    item("export_controls", s, ["TRADE", "HAWK"], "position",
         "Should the US block sales of advanced technology, like top computer chips, to rival countries?",
         "Rivals such as China and Russia.",
         ["No; let companies sell to anyone", "Only for technology with clear military uses", "Yes, for most advanced technology, even if US companies lose sales"],
         "block"),
    item("friend_shoring", s, ["TRADE", "GLOBAL"], "position",
         "Should trade policy favor allies, with lower tariffs for them than for other countries?",
         "Allies like Canada, Japan and European countries.",
         ["Yes, favor allies clearly", "Somewhat", "No; treat all trading partners the same", "No; allies should face tariffs too if they sell more to us than they buy"],
         "tariffs on allies too",
         notes="Last option is a distinct trade-balance position; check ordering with the nominal model."))

# ================= D07 =================
D = "Technology & AI"
s = sub("D07", D, "Cryptocurrency and digital money", "TECH", 2, "position")
b.append("d07_technology_ai.json",
    item("crypto_rules", s, ["TECH", "REG"], "position",
         "How should cryptocurrencies like Bitcoin be regulated?",
         "Rules for companies that sell and trade them.",
         ["Ban most of them", "Regulate them like stocks and banks", "Light rules focused on fraud", "No special rules"], "no rules"),
    item("digital_dollar", s, ["PRIVACY", "TECH"], "position",
         "Should the Federal Reserve create a digital dollar that people could hold directly in an account with it?",
         "Electronic money issued by the government, like cash but digital.",
         ["Yes", "Only with strict privacy protections", "No; ban it"], "ban"))
s = sub("D07", D, "AI and copyright", "TECH", 1, "position")
b.append("d07_technology_ai.json",
    item("ai_copyright", s, ["TECH"], "position",
         "Should AI companies need permission or pay to train their systems on books, art and articles?",
         "Copyrighted work, such as published books and news articles.",
         ["Yes, permission and payment", "Payment, but no permission needed", "No; training on published work should be allowed freely"],
         "freely"))
s = sub("D07", D, "AI companions and minors", "TECH", 1, "position")
b.append("d07_technology_ai.json",
    item("ai_companions_minors", s, ["TECH", "LIBERTY"], "position",
         "Should AI chatbots that act as friends or romantic partners be allowed for users under 18?",
         "Apps designed for ongoing personal conversation.",
         ["Banned for minors", "Allowed with parental consent and safety limits", "Allowed; parents can decide at home"], "allowed"))

# ================= D08 =================
D = "Privacy & surveillance"
s = sub("D08", D, "DNA databases", "PRIVACY", 1, "position")
b.append("d08_privacy_surveillance.json",
    item("dna_databases", s, ["PRIVACY", "ORDER"], "position",
         "Should police be able to search consumer DNA databases, like ancestry sites, to find suspects through their relatives?",
         "Sites where people upload their DNA to find family.",
         ["No, never", "Only with a warrant, for violent crimes", "Only for violent crimes", "Yes, for any crime"], "any crime"))
s = sub("D08", D, "Workplace monitoring", "PRIVACY", 1, "position")
b.append("d08_privacy_surveillance.json",
    item("workplace_monitoring", s, ["PRIVACY", "REG"], "position",
         "Should employers be allowed to monitor workers' computers, keystrokes and locations during work hours?",
         "Company devices and work time.",
         ["No, only with the worker's agreement for specific reasons", "Yes, but they must tell workers exactly what is monitored", "Yes, freely"],
         "freely"))

# ================= D09 =================
D = "Abortion & reproduction"
s = sub("D09", D, "Moral status of the unborn (belief)", "MORAL", 1, "belief")
b.append("d09_abortion_reproduction.json",
    item("life_begins", s, ["MORAL"], "belief",
         "At what point does a developing human have the same right to life as a born person?",
         "Your own view, whatever the law says.",
         ["Only at birth", "Around viability, when it could survive outside the womb", "When a heartbeat is detectable, about 6 weeks", "At conception"],
         "conception",
         definitions=[{"term": "viability", "text": "The point after which a fetus could survive outside the womb with medical care, usually around 22 to 24 weeks.", "source": "descriptive", "verify": False}]))
s = sub("D09", D, "Surrogacy", "MORAL", 1, "position")
b.append("d09_abortion_reproduction.json",
    item("surrogacy", s, ["MORAL", "LIBERTY"], "position",
         "Should it be legal to pay a woman to carry a pregnancy for someone else?",
         "Surrogacy arranged by contract between adults.",
         ["Yes, legal and regulated", "Only unpaid surrogacy, with expenses covered", "No; ban surrogacy"], "ban"))

# ================= D10 =================
D = "Sexuality & gender identity"
s = sub("D10", D, "Sex and gender (belief)", "GENDERID", 1, "belief")
b.append("d10_sexuality_gender_identity.json",
    item("gender_belief", s, ["GENDERID"], "belief",
         "What do you think determines whether someone is a man or a woman?",
         "Your own view, whatever the law says.",
         ["Their gender identity only", "Mostly their gender identity", "Both sex at birth and gender identity", "Mostly their sex at birth", "Their sex at birth only"],
         "sex at birth"))

# ================= D11 =================
D = "Religion in public life"
s = sub("D11", D, "Evolution in science classes", "RELIGION", 1, "position")
b.append("d11_religion_public_life.json",
    item("evolution_class", s, ["RELIGION", "EDUC"], "position",
         "How should public school science classes handle the origin of life and species?",
         "Middle and high school science.",
         ["Teach evolution only", "Teach evolution, and mention that many people hold religious beliefs about creation",
          "Teach evolution alongside creation or intelligent design as alternative explanations", "Teach creation or intelligent design instead"],
         "creation"))
s = sub("D11", D, "Faith-based charities and public funds", "RELIGION", 1, "position")
b.append("d11_religion_public_life.json",
    item("faith_charities", s, ["RELIGION"], "position",
         "Should religious charities get government money to run services like shelters and addiction programs?",
         "Services open to anyone, run by churches or religious groups.",
         ["No; keep public money away from religious groups", "Yes, if they keep religion out of the services", "Yes, on equal terms with other charities, including faith content people can opt out of"],
         "equal terms"))

# ================= D12 =================
D = "Family & gender roles"
s = sub("D12", D, "Women in the draft and combat", "FAMILY", 1, "position")
b.append("d12_family_gender_roles.json",
    item("women_draft", s, ["FAMILY", "HAWK"], "position",
         "If the US ever brought back a military draft, should women be drafted too?",
         "Today only men must register for the draft.",
         ["Yes, on the same terms as men", "Yes, but only for non-combat roles", "No; only men"], "only men"))
s = sub("D12", D, "Nature vs culture in gender roles (belief)", "FAMILY", 1, "belief")
b.append("d12_family_gender_roles.json",
    item("natural_roles", s, ["FAMILY"], "belief",
         "Where do differences in men's and women's roles in family life mostly come from?",
         "Think about typical differences, not every person.",
         ["Almost entirely from upbringing and culture", "Mostly from culture, partly from nature", "About equally from both",
          "Mostly from natural differences between the sexes", "Almost entirely from nature; men and women are suited to different roles"],
         "nature"))

# ================= D13 =================
s = "How much discrimination exists"
b.insert_after("discrimination_white",
    item("discrimination_groups", s, ["EQUITY"], "exceptions",
         "How much discrimination does each of these groups face in the US today?",
         "Answer each group separately.",
         ["Little or none", "Some", "A lot"], "A lot",
         cases=[{"id": "dg_hispanic", "text": "Hispanic Americans"}, {"id": "dg_asian", "text": "Asian Americans"},
                {"id": "dg_women", "text": "Women"}, {"id": "dg_men", "text": "Men"},
                {"id": "dg_christians", "text": "Christians"}, {"id": "dg_muslims", "text": "Muslims"},
                {"id": "dg_gay", "text": "Gay and lesbian people"}, {"id": "dg_rural", "text": "People in rural areas"}],
         notes="Broad set separates general perception of discrimination from sympathy for particular groups; cases for men, Christians and rural people are expected to load in the opposite direction."))
s = sub("D13", "Race & equity", "Monuments and names", "EQUITY", 1, "position")
b.append("d13_race_equity.json",
    item("confederate_monuments", s, ["EQUITY", "NATION"], "position",
         "What should happen to public monuments honoring Confederate leaders?",
         "Statues and names on public land and buildings.",
         ["Remove them", "Move them to museums with historical context", "Keep them, but add historical context", "Keep them as they are"],
         "keep"))

# ================= D14 =================
D = "Immigration & national identity"
s = sub("D14", D, "Immigrant selection by culture or religion", "NATION", 1, "position")
b.append("d14_immigration_nation.json",
    item("immigrant_selection_culture", s, ["NATION", "IMMIG"], "position",
         "Should the US consider an immigrant's culture or religion when deciding who may come?",
         "Legal immigration, after security screening.",
         ["No; culture and religion should never count", "Only knowledge of English and US civics should count",
          "Give some preference to people from countries with cultures closer to America's", "Yes, and bar people from some religions or cultures"],
         "bar some"))
s = sub("D14", D, "Enforcement methods", "IMMIG", 2, "exceptions")
b.append("d14_immigration_nation.json",
    item("enforcement_limits", s, ["IMMIG"], "exceptions",
         "When enforcing immigration law against people without legal status, should agents be allowed to do each of these?",
         "Answer each case separately.",
         ["Should not be allowed", "Should be allowed"], "Should be allowed",
         cases=[{"id": "el_schools", "text": "Make arrests at schools"}, {"id": "el_churches", "text": "Make arrests at places of worship"},
                {"id": "el_hospitals", "text": "Make arrests at hospitals"}, {"id": "el_families", "text": "Hold families with children in detention"},
                {"id": "el_third_country", "text": "Deport people to a country that isn't their own"}, {"id": "el_masks", "text": "Wear masks to hide their identity while working"}]))

# ================= D15 =================
D = "Crime policing & punishment"
s = sub("D15", D, "Civil asset forfeiture", "ORDER", 1, "position")
b.append("d15_crime_policing.json",
    item("asset_forfeiture", s, ["ORDER", "LIBERTY"], "position",
         "Should police be able to take cash or property they suspect is linked to a crime, without convicting the owner?",
         "Called civil asset forfeiture. The owner can go to court to get it back.",
         ["No; only after a criminal conviction", "Only with strong evidence, and the government must prove its case", "Yes, as most states allow today"],
         "allow",
         notes="Expected to cross-cut: libertarian and left opposition."))
s = sub("D15", D, "Stop-and-frisk", "ORDER", 1, "position")
b.append("d15_crime_policing.json",
    item("stop_and_frisk", s, ["ORDER", "EQUITY"], "position",
         "Should police be able to stop and pat down people they find suspicious in high-crime areas?",
         "Stops without an arrest, based on an officer's suspicion.",
         ["No", "Only with specific reasons, recorded and reviewed for bias", "Yes, it helps prevent crime"], "yes"))

# ================= D16 =================
s = sub("D16", "Guns", "Self-defense laws", "GUNS", 1, "position")
b.append("d16_guns.json",
    item("self_defense_law", s, ["GUNS", "ORDER"], "position",
         "When someone is attacked in a public place, should they have to try to safely retreat before using deadly force?",
         "Situations where the person reasonably fears serious harm.",
         ["Yes, retreat first if it can be done safely", "Only if they started the conflict", "No; they can stand their ground anywhere they have a right to be"],
         "stand ground"))
s = sub("D16", "Guns", "Gun maker liability", "GUNS", 1, "position")
b.append("d16_guns.json",
    item("gun_maker_liability", s, ["GUNS"], "position",
         "Should gun makers and sellers be able to be sued when their guns are used in crimes?",
         "A 2005 federal law blocks most such lawsuits.",
         ["Yes, like makers of other dangerous products", "Only if they broke the law or marketed irresponsibly", "No; keep today's protection"],
         "protection",
         facts=[{"claim": "Protection of Lawful Commerce in Arms Act (2005) bars most civil suits against gun makers and dealers over criminal misuse", "source": "15 U.S.C. sec. 7901-7903", "checked": C, "verify": False}]))
s = sub("D16", "Guns", "Gun registration", "GUNS", 1, "position")
b.append("d16_guns.json",
    item("gun_registry", s, ["GUNS"], "position",
         "Should there be a national registry of who owns which guns?",
         "Federal law now bars the government from creating one.",
         ["Yes, for all guns", "Only for handguns and semi-automatic rifles", "No"], "no"))
s = sub("D16", "Guns", "Suppressors", "GUNS", 1, "position")
b.append("d16_guns.json",
    item("suppressors", s, ["GUNS"], "position",
         "What should the rules be for buying a gun suppressor (silencer)?",
         "Today buyers need federal registration and a long approval process.",
         ["Ban them for civilians", "Keep today's rules", "Treat them like ordinary gun parts, with no special registration"], "fewer rules"))

# ================= D17 =================
D = "Drugs & personal liberty"
s = sub("D17", D, "Drinking age", "LIBERTY", 1, "position")
b.append("d17_drugs_liberty.json",
    item("drinking_age", s, ["LIBERTY"], "position",
         "What should the legal drinking age be?",
         "Buying and drinking alcohol.",
         ["18", "18 for beer and wine, 21 for liquor", "21, as today", "Older than 21"], "older"))
s = sub("D17", D, "Vaping and tobacco bans", "LIBERTY", 1, "position")
b.append("d17_drugs_liberty.json",
    item("vape_flavors", s, ["LIBERTY"], "position",
         "Should flavored vapes and cigarettes be banned for adults?",
         "Sales to adults 21 and older.",
         ["No; adults should choose", "Allowed, with higher taxes", "Banned"], "banned"))
s = sub("D17", D, "Organ sales", "LIBERTY", 1, "position")
b.append("d17_drugs_liberty.json",
    item("kidney_payment", s, ["LIBERTY", "MORAL"], "position",
         "Should people be allowed to be paid for donating a kidney?",
         "Living donors, with medical screening. Federal law bans payment today.",
         ["Yes, in a regulated market", "Only a fixed payment from the government, not a market", "No; keep the ban"], "keep ban"))
s = sub("D17", D, "Right to try experimental treatments", "LIBERTY", 1, "position")
b.append("d17_drugs_liberty.json",
    item("right_to_try", s, ["LIBERTY", "REG"], "position",
         "Should seriously ill patients be able to use treatments that haven't finished FDA approval?",
         "Patients with life-threatening illnesses, with their doctor's support.",
         ["Yes, any treatment that passed early safety testing", "Only through FDA-supervised programs", "No; wait for full approval"], "wait"))
s = sub("D17", D, "Raw milk and food freedom", "LIBERTY", 1, "position")
b.append("d17_drugs_liberty.json",
    item("raw_milk", s, ["LIBERTY"], "position",
         "Should stores be allowed to sell unpasteurized (raw) milk?",
         "Sold with a warning label.",
         ["Yes, anywhere", "Only directly from farms", "No"], "no"))

# ================= D18 =================
D = "Free speech & civil liberties"
s = sub("D18", D, "Defamation law", "SPEECH", 1, "position")
b.append("d18_speech_civil_liberties.json",
    item("defamation_public_figures", s, ["SPEECH"], "position",
         "Should it be easier for public figures to sue news outlets for false stories about them?",
         "Today a public figure must prove the outlet knew the story was false or recklessly ignored the truth.",
         ["No; keep today's high bar", "Somewhat easier", "Much easier: proving the story was false and harmful should be enough"], "much easier"))
s = sub("D18", D, "Public broadcasting", "SPEECH", 1, "position")
b.append("d18_speech_civil_liberties.json",
    item("public_broadcasting", s, ["SPEECH", "ESTAB"], "position",
         "Should the federal government fund public broadcasting, like public radio and TV stations?",
         "Funding for local stations and national programs.",
         ["Yes, more than in the past", "Yes, about as in the past", "No federal funding"], "none",
         notes="Federal funding was cut in 2025; wording avoids 'today' so it doesn't cue the current administration."))
s = sub("D18", D, "Campus speech codes", "SPEECH", 1, "position")
b.append("d18_speech_civil_liberties.json",
    item("campus_speech_codes", s, ["SPEECH", "EDUC"], "position",
         "Should public universities be able to discipline students for offensive speech that isn't a threat or harassment?",
         "Speech on campus, such as remarks about race, religion or sex.",
         ["Yes", "Only for repeated speech aimed at a specific person", "No"], "no"))

# ================= D19 =================
D = "Democratic norms & executive power"
s = sub("D19", D, "Supreme Court size", "NORMS", 1, "position")
b.append("d19_democratic_norms.json",
    item("court_expansion", s, ["NORMS"], "position",
         "Should Congress change the number of Supreme Court justices?",
         "There have been 9 since 1869. Answer whichever party would gain.",
         ["Yes, add justices when the majority wants different rulings", "Only as part of a bipartisan reform", "No; keep it at 9"],
         "keep 9",
         notes="High pole here is 'keep' (more restraint), the reverse of most NORMS items."))
s = sub("D19", D, "Presidential immunity", "NORMS", 1, "position")
b.append("d19_democratic_norms.json",
    item("presidential_immunity", s, ["NORMS"], "position",
         "Should former presidents be immune from criminal prosecution for things they did as president?",
         "Answer for any president of either party.",
         ["No; they can be prosecuted like anyone else", "Only for core duties set by the Constitution", "Yes, for all official acts"],
         "full immunity",
         context="In 2024 the Supreme Court ruled that former presidents have broad immunity for official acts.",
         facts=[{"claim": "Supreme Court held former presidents have absolute immunity for core constitutional acts and presumptive immunity for other official acts", "source": "603 U.S. 593 (2024)", "checked": C, "verify": False}]))
s = sub("D19", D, "Government action against news outlets", "NORMS", 1, "position")
b.append("d19_democratic_norms.json",
    item("press_retaliation", s, ["NORMS", "SPEECH"], "position",
         "Should a president be able to punish news outlets that cover them unfairly, such as by pulling broadcast licenses or press access?",
         "Answer for any president of either party.",
         ["Never", "Only limit access to events like briefings, not licenses", "Yes, outlets that spread falsehoods should face consequences"],
         "yes"))
s = sub("D19", D, "Court deference to agencies", "NORMS", 1, "position")
b.append("d19_democratic_norms.json",
    item("agency_deference", s, ["TRUST", "NORMS"], "position",
         "When a law is unclear, should courts defer to the judgment of the federal agency experts who carry it out?",
         "Agencies of any administration.",
         ["Yes, courts should usually defer", "Only on technical or scientific questions", "No; judges should decide what the law means themselves"],
         "judges decide",
         context="In 2024 the Supreme Court ended a rule that required courts to defer to agencies in many such cases.",
         facts=[{"claim": "Loper Bright Enterprises v. Raimondo (2024) overruled Chevron deference", "source": "603 U.S. 369 (2024)", "checked": C, "verify": False}]))

# ================= D20 =================
D = "Elections & voting"
s = sub("D20", D, "Ranked-choice voting", "VOTING", 1, "position")
b.append("d20_elections_voting.json",
    item("ranked_choice", s, ["VOTING"], "position",
         "Should elections use ranked-choice voting, where voters rank candidates instead of picking one?",
         "A few states and cities use it today.",
         ["Yes, for all elections", "Let each state or city decide", "No; ban it"], "ban"))
s = sub("D20", D, "DC and Puerto Rico statehood", "VOTING", 1, "exceptions")
b.append("d20_elections_voting.json",
    item("statehood", s, ["VOTING", "FED"], "exceptions",
         "Should each of these become a state, with its own senators and representatives?",
         "Answer each separately.",
         ["No", "Only if its residents vote for it", "Yes"], "No",
         cases=[{"id": "st_dc", "text": "Washington, DC"}, {"id": "st_pr", "text": "Puerto Rico"}]))
b["statehood"]["options"] = ["Yes", "Only if its residents vote for it", "No"]
s = sub("D20", D, "Voting age", "VOTING", 1, "position")
b.append("d20_elections_voting.json",
    item("voting_age", s, ["VOTING"], "position",
         "What should the voting age be?",
         "For federal elections.",
         ["16", "17, if you'll be 18 by the next general election", "18, as today", "21"], "older"))
s = sub("D20", D, "Noncitizen voting in local elections", "VOTING", 1, "position")
b.append("d20_elections_voting.json",
    item("noncitizen_local_voting", s, ["VOTING", "IMMIG"], "position",
         "Should legal permanent residents who aren't citizens be able to vote in local elections, like school board races?",
         "Federal elections are citizens-only under every option.",
         ["Yes", "Let each city decide", "No; ban it everywhere"], "ban"))

# ================= D21 =================
D = "Trust & anti-establishment"
s = sub("D21", D, "Trust shown in behavior", "TRUST", 4, "position", note="Added in review 2026-10-12: position-format trust items so TRUST/ESTAB aren't measured by one answer format")
b.append("d21_trust_establishment.json",
    item("recall_response", s, ["ESTAB", "TRUST"], "position",
         "If a federal safety agency recalled a product you use, saying it might be dangerous, what would you most likely do?",
         "Think of a food, medicine or car part.",
         ["Stop using it right away", "Stop using it, then check other sources", "Check other sources before deciding", "Keep using it unless I saw a problem myself"],
         "keep using"),
    item("budget_office_reliance", s, ["TRUST"], "position",
         "When Congress votes on a major bill, how much should it rely on cost estimates from its own nonpartisan budget office?",
         "The Congressional Budget Office, under either party's control of Congress.",
         ["Treat them as the final word", "Rely on them heavily, along with other evidence", "Treat them as one opinion among many", "Mostly ignore them; they're often wrong"],
         "ignore"),
    item("more_power_outcome", s, ["TRUST"], "position",
         "If the federal government got more money and power to fix a problem you care about, what would most likely happen?",
         "Under either party.",
         ["It would mostly fix it", "It would make real progress", "It would make a little progress and waste a lot", "It would make things worse"],
         "worse"),
    item("accept_certified_loss", s, ["ESTAB", "VOTING"], "position",
         "If officials certified a close election that your preferred candidate lost, what would you need before accepting the result?",
         "A close race for president or governor.",
         ["Nothing more; I'd accept it once certified", "Any recounts required by law", "An independent audit", "Confirmation from observers on my own side"],
         "own side"))
s = sub("D21", D, "Science vs elected officials", "ESTAB", 1, "position")
b.append("d21_trust_establishment.json",
    item("science_vs_officials", s, ["ESTAB"], "position",
         "When public health scientists and elected officials disagree about a health rule, who should have the final say?",
         "For example, rules during a disease outbreak.",
         ["Public health scientists", "Elected officials, following scientists' advice in most cases",
          "Elected officials, treating scientists' advice as one input", "Elected officials; scientists should advise only when asked"],
         "officials"))
s = sub("D21", D, "Congressional stock trading", "POP", 1, "position")
b.append("d21_trust_establishment.json",
    item("congress_stock_ban", s, ["POP"], "position",
         "Should members of Congress be banned from trading individual stocks while in office?",
         "Today they may trade, but must report trades.",
         ["Yes, ban it for members, their spouses and senior staff", "Yes, for members only", "No; reporting trades is enough"],
         "no ban"))

# ================= D22 =================
D = "Foreign policy & defense"
s = sub("D22", D, "Iran", "HAWK", 1, "position", tag="current", note="Added in review 2026-10-12; rotating module")
b.append("d22_foreign_defense.json",
    item("iran_nuclear", s, ["HAWK"], "position",
         "If Iran moved to build a nuclear weapon, what should the US do?",
         "Assume US intelligence was confident of it.",
         ["Negotiate, and accept some risk", "Negotiate, backed by tough sanctions", "Strike its nuclear sites if talks fail", "Strike its nuclear sites right away"],
         "strike now"))
s = sub("D22", D, "Acquiring territory", "HAWK", 1, "position", tag="current", note="Added in review 2026-10-12; rotating module")
b.append("d22_foreign_defense.json",
    item("acquire_territory", s, ["HAWK", "NATION"], "position",
         "Should the US try to gain new territory, such as Greenland?",
         "Territory now belonging to another country.",
         ["No", "Only if the people living there vote for it", "Yes, through purchase or negotiation, even if local people object",
          "Yes, by any means, including economic or military pressure"], "any means"))

# ================= D23 =================
s = sub("D23", "Education", "Legacy and donor admissions", "EDUC", 1, "position")
b.append("d23_education.json",
    item("legacy_admissions", s, ["EDUC", "POP"], "position",
         "Should colleges give an advantage to children of graduates or donors?",
         "Colleges that get any federal funding, public or private.",
         ["No; ban it", "Allow it, but disclose it publicly", "Yes; colleges should decide"], "allow"))

# ================= D25 =================
D = "Values (cross-cutting)"
s = sub("D25", D, "Purity and sanctity", "VALUES", 2, "agree_defined")
for it in agree_pair("sacred_limits", "harm_only", s, ["VALUES", "MORAL"],
                     "\"Some things are wrong even if nobody is harmed, because they go against what is sacred or natural.\"",
                     "\"If an act harms nobody, it shouldn't be considered wrong.\""):
    b.append("d25_values.json", it)
s = sub("D25", D, "Zero-sum thinking", "VALUES", 2, "agree_defined")
for it in agree_pair("zero_sum", "positive_sum", s, ["VALUES", "POP"],
                     "\"When one group in society gets ahead, it is usually at another group's expense.\"",
                     "\"Most of the time, different groups in society can all get ahead together.\""):
    b.append("d25_values.json", it)
s = sub("D25", D, "Proportionality vs need", "VALUES", 1, "tradeoff")
b.append("d25_values.json",
    tradeoff("proportional_vs_need", s, ["VALUES", "REDIS"], "When sharing out something valuable, which is fairer?",
             "Think of things like pay, benefits or public help.",
             ("By need", "Those who need it most get more, even if they contributed less."),
             ("By contribution", "Those who contributed more get more, even if some with greater need get less.")))
s = sub("D25", D, "What decides who gets ahead", "VALUES", 3, "position")
b.append("d25_values.json",
    item("get_ahead", s, ["VALUES", "REDIS"], "position",
         "In the US today, what mostly decides who gets ahead?",
         "Think about people in general, not any one person.",
         ["Family background and connections", "Luck and circumstances", "A mix of background, luck and effort", "Talent and skills", "Hard work"],
         "effort"),
    item("moral_rules", s, ["VALUES", "MORAL"], "position",
         "Which comes closest to your view of right and wrong?",
         "Basic moral questions, not matters of taste.",
         ["Right and wrong depend entirely on the culture and the situation", "Mostly depend on the situation, with a few fixed rules",
          "There are many fixed rules, but some depend on the situation", "Right and wrong are the same for all people and all times"],
         "fixed"),
    item("pace_of_change", s, ["VALUES"], "position",
         "When society is changing, what pace of change is usually best?",
         "Changes in customs, laws and institutions.",
         ["Fast and sweeping", "Steady", "Slow and careful", "As little as possible; keep what works"], "little change"))

b.save()

# ---------- blueprint ----------
bp = ROOT / "items" / "blueprint.csv"
rows = list(csv.reader(open(bp, newline="")))
have = {r[2] for r in rows[1:]}
with open(bp, "a", newline="") as f:
    w = csv.writer(f)
    for r in NEW_SUBTOPICS:
        if r[2] not in have:
            w.writerow(r)
print(f"part B applied: {len(NEW_SUBTOPICS)} new subtopics")
