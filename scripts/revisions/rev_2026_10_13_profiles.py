"""Rebuild items/modules/profiles.json with the expanded comparison groups.

Positions are hand-placed on the quiz's axes (-1 = minus pole, +1 = plus pole,
see items/modules/axes.json) from platforms, voting records, survey reports and
historians' accounts. An axis is left out where the group took no clear
position or the issue didn't exist yet. Approximate, for fun.

Run: python3 scripts/revisions/rev_2026_10_13_profiles.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "items" / "modules" / "profiles.json"

CATS = [
    {"id": "today", "name": "US today", "about": "Parties and factions in the 2020s."},
    {"id": "typology", "name": "Voter types", "about": "The nine groups in Pew Research Center's political typology of American voters."},
    {"id": "president", "name": "Presidents", "about": "Placed from their record in office, not their rhetoric."},
    {"id": "history", "name": "US history", "about": "Parties and movements from earlier eras, compared only on issues they took positions on."},
    {"id": "ideology", "name": "Ideologies", "about": "Schools of thought, as their mainstream US advocates would apply them."},
    {"id": "world", "name": "Abroad", "about": "Parties in other democracies, translated onto US-style issues. Their home debates differ, so treat these loosely."},
]

# id | name | short label for the map | era | category | description | positions
P = []


def add(pid, name, short, era, cat, about, pos):
    vals = {}
    for tok in pos.split():
        ax, v = tok.split("=")
        vals[ax] = float(v)
    P.append({"id": pid, "name": name, "short": short, "era": era, "cat": cat, "about": about, "pos": vals})


# ---------------- US today ----------------
add("dem_progressive", "Progressive Democrats", "Progressives", "2020s", "today",
    "The party's left wing: Medicare for All, Green New Deal, criminal justice reform, a smaller military budget.",
    "G=-.85 REDIS=-.8 REG=-.7 SOCINS=-.85 HOUSING=-.3 ENV=-.85 TRADE=.1 TECH=-.5 PRIVACY=-.4 MORAL=-.85 GENDERID=-.85 RELIGION=-.7 FAMILY=-.7 EQUITY=-.85 IMMIG=-.7 NATION=-.7 ORDER=-.7 GUNS=-.8 LIBERTY=-.4 SPEECH=.2 NORMS=-.5 VOTING=-.85 POP=.4 EDUC=-.6 GLOBAL=-.2 HAWK=-.6 VALUES=-.8")
add("dem_mainstream", "Mainstream Democrats", "Democrats", "2020s", "today",
    "The party's center: protect and expand the ACA, climate investment, abortion rights, alliances abroad.",
    "G=-.55 REDIS=-.5 REG=-.45 SOCINS=-.5 HOUSING=-.3 ENV=-.6 TRADE=0 TECH=-.3 MORAL=-.6 GENDERID=-.55 RELIGION=-.5 FAMILY=-.5 EQUITY=-.55 IMMIG=-.3 NATION=-.35 ORDER=-.2 GUNS=-.6 LIBERTY=-.1 SPEECH=.1 NORMS=-.6 VOTING=-.7 TRUST=-.2 ESTAB=-.6 POP=-.2 FED=-.4 EDUC=-.5 GLOBAL=-.6 HAWK=0 VALUES=-.5")
add("blue_dog", "Moderate Democrats", "Moderate Dems", "2020s", "today",
    "Blue Dogs and swing-district Democrats: fiscal caution, energy production, tougher on the border and crime than the party's base.",
    "G=-.2 REDIS=-.2 REG=-.2 SOCINS=-.3 ENV=-.2 TRADE=.2 MORAL=-.3 GENDERID=.1 RELIGION=0 FAMILY=0 EQUITY=0 IMMIG=.2 NATION=.1 ORDER=.3 GUNS=.1 SPEECH=0 NORMS=-.5 VOTING=-.3 ESTAB=-.4 POP=0 FED=0 EDUC=-.2 GLOBAL=-.5 HAWK=.2 VALUES=-.1")
add("abundance", "Abundance liberals", "Abundance libs", "2020s", "today",
    "YIMBY, build-more Democrats: zoning reform, permitting reform, clean energy buildout, high-skill immigration, pro-technology.",
    "G=-.4 REDIS=-.3 REG=.2 SOCINS=-.4 HOUSING=-.95 ENV=-.5 TRADE=-.5 TECH=.4 MORAL=-.6 GENDERID=-.4 RELIGION=-.5 FAMILY=-.5 EQUITY=-.2 IMMIG=-.6 NATION=-.4 ORDER=.1 GUNS=-.5 LIBERTY=-.3 SPEECH=-.3 NORMS=-.6 ESTAB=-.5 POP=-.4 FED=-.5 EDUC=-.1 GLOBAL=-.7 HAWK=.1 VALUES=-.4")
add("dem_socialist", "Democratic Socialists", "DSA", "2010s–20s", "today",
    "Democratic Socialists of America: public ownership of key industries, strong unions, sharply reduced inequality, anti-war.",
    "G=-.95 REDIS=-1 REG=-.95 SOCINS=-1 HOUSING=-.4 ENV=-.85 TRADE=.2 TECH=-.6 PRIVACY=-.7 MORAL=-.8 GENDERID=-.85 RELIGION=-.7 FAMILY=-.7 EQUITY=-.9 IMMIG=-.85 NATION=-.8 ORDER=-.85 GUNS=-.3 SPEECH=-.2 VOTING=-.9 ESTAB=.6 POP=.8 EDUC=-.8 GLOBAL=-.2 HAWK=-.85 VALUES=-.9")
add("green", "Green Party", "Greens", "2000s–20s", "today",
    "Environment first, nonviolence, grassroots democracy, social justice, ranked-choice voting.",
    "G=-.9 REDIS=-.85 REG=-.9 SOCINS=-.9 ENV=-1 TRADE=.3 TECH=-.5 PRIVACY=-.5 MORAL=-.75 GENDERID=-.8 RELIGION=-.6 FAMILY=-.6 EQUITY=-.85 IMMIG=-.8 NATION=-.7 ORDER=-.8 GUNS=-.6 NORMS=-.6 VOTING=-.9 ESTAB=.6 POP=.6 HAWK=-.95 GLOBAL=-.4 VALUES=-.85")
add("civil_libertarian", "Civil libertarian left", "Civil libertarians", "today", "today",
    "ACLU-style liberals: free speech for everyone, privacy, due process, church-state separation, skeptical of police and surveillance.",
    "G=-.5 REDIS=-.4 REG=-.3 SOCINS=-.4 TECH=-.3 PRIVACY=-1 MORAL=-.9 GENDERID=-.7 RELIGION=-.9 FAMILY=-.6 EQUITY=-.4 IMMIG=-.7 NATION=-.6 ORDER=-.8 GUNS=-.2 LIBERTY=-.9 SPEECH=-1 NORMS=-.9 VOTING=-.7 HAWK=-.6 VALUES=-.6")
add("centrist", "Independents and centrists", "Centrists", "today", "today",
    "Mixed views, mostly near the middle, wary of both parties and of strong presidents.",
    "G=0 REDIS=0 REG=0 SOCINS=-.1 HOUSING=0 ENV=0 TRADE=0 TECH=0 MORAL=-.1 GENDERID=.1 RELIGION=-.1 FAMILY=0 EQUITY=.1 IMMIG=.15 NATION=.1 ORDER=.1 GUNS=0 SPEECH=-.1 NORMS=-.4 VOTING=0 TRUST=.3 ESTAB=.3 POP=.3 FED=.1 EDUC=0 GLOBAL=0 HAWK=0 VALUES=0")
add("libertarian", "Libertarian Party", "Libertarians", "1970s–today", "today",
    "Minimal government in both the economy and personal life; free trade; restraint abroad.",
    "G=.3 REDIS=.9 REG=.9 SOCINS=.9 HOUSING=-.6 TRADE=-.9 ENV=.6 TECH=.85 PRIVACY=-.9 MORAL=-.6 GENDERID=-.2 RELIGION=-.5 FAMILY=0 EQUITY=.6 IMMIG=-.4 NATION=-.3 ORDER=-.4 GUNS=.95 LIBERTY=-.95 SPEECH=-.9 NORMS=-.7 TRUST=.7 ESTAB=.7 FED=.6 EDUC=.85 GLOBAL=.5 HAWK=-.75 VALUES=0")
add("mises", "Mises Caucus libertarians", "Mises Caucus", "2020s", "today",
    "The Libertarian Party's current leadership: anti-state and anti-war, but culturally conservative and restrictive on immigration.",
    "G=.6 REDIS=1 REG=.95 SOCINS=.95 TRADE=-.6 ENV=.8 TECH=.8 PRIVACY=-.9 MORAL=.2 GENDERID=.6 RELIGION=0 FAMILY=.3 EQUITY=.9 IMMIG=.5 NATION=.3 ORDER=-.2 GUNS=1 LIBERTY=-.9 SPEECH=-1 NORMS=-.3 TRUST=.95 ESTAB=.95 POP=.9 FED=.9 EDUC=.95 GLOBAL=.8 HAWK=-.9 VALUES=.4")
add("never_trump", "Never-Trump conservatives", "Never-Trump right", "2016–today", "today",
    "Pre-Trump conservatives who broke with the party: free trade, alliances, institutional checks, moderate social conservatism.",
    "G=.3 REDIS=.5 REG=.5 SOCINS=.4 ENV=.2 TRADE=-.8 TECH=.4 MORAL=.3 GENDERID=.3 RELIGION=.3 FAMILY=.3 EQUITY=.5 IMMIG=-.1 NATION=.2 ORDER=.4 GUNS=.4 LIBERTY=0 SPEECH=-.5 NORMS=-.9 VOTING=-.2 TRUST=-.3 ESTAB=-.5 POP=-.6 FED=.4 EDUC=.5 GLOBAL=-.9 HAWK=.7 VALUES=.3")
add("gop_current", "Mainstream Republicans", "Republicans", "2020s", "today",
    "Today's party: border enforcement, tariffs, tax cuts, traditional social views, skeptical of institutions.",
    "G=.7 REDIS=.6 REG=.5 SOCINS=.3 HOUSING=.4 ENV=.75 TRADE=.7 TECH=.5 PRIVACY=0 MORAL=.6 GENDERID=.85 RELIGION=.55 FAMILY=.5 EQUITY=.75 IMMIG=.85 NATION=.75 ORDER=.65 GUNS=.85 LIBERTY=-.1 SPEECH=-.2 NORMS=.5 VOTING=.8 TRUST=.6 ESTAB=.75 POP=.5 FED=.4 EDUC=.65 GLOBAL=.5 HAWK=.2 VALUES=.6")
add("maga", "America First / MAGA", "MAGA", "2016–today", "today",
    "The movement around Trump: mass deportation, high tariffs, a strong presidency, fighting the 'deep state', no new foreign wars.",
    "G=.8 REDIS=.4 REG=.4 SOCINS=0 HOUSING=.5 ENV=.85 TRADE=.95 TECH=.4 PRIVACY=.2 MORAL=.6 GENDERID=.95 RELIGION=.6 FAMILY=.6 EQUITY=.9 IMMIG=1 NATION=.9 ORDER=.85 GUNS=.9 LIBERTY=0 SPEECH=-.3 NORMS=.9 VOTING=.9 TRUST=.8 ESTAB=.95 POP=.9 FED=.3 EDUC=.75 GLOBAL=.9 HAWK=-.1 VALUES=.7")
add("freedom_caucus", "House Freedom Caucus", "Freedom Caucus", "2015–today", "today",
    "The House's hard-right bloc: deep spending cuts, border hawks, social conservatives, willing to buck party leaders.",
    "G=.85 REDIS=.85 REG=.8 SOCINS=.6 ENV=.85 TRADE=.4 TECH=.4 PRIVACY=-.3 MORAL=.8 GENDERID=.95 RELIGION=.7 FAMILY=.7 EQUITY=.9 IMMIG=.95 NATION=.8 ORDER=.7 GUNS=.95 LIBERTY=.1 SPEECH=-.5 NORMS=.6 VOTING=.9 TRUST=.8 ESTAB=.9 POP=.8 FED=.8 EDUC=.9 GLOBAL=.8 HAWK=-.2 VALUES=.8")
add("natcon", "National conservatives", "NatCons", "2020s", "today",
    "NatCon intellectuals: restrict immigration, protect industry, use government for families and workers, skeptical of foreign wars.",
    "G=.8 REDIS=.2 REG=.1 SOCINS=-.1 ENV=.6 TRADE=.9 TECH=0 MORAL=.8 GENDERID=.95 RELIGION=.7 FAMILY=.75 EQUITY=.85 IMMIG=.95 NATION=.95 ORDER=.8 GUNS=.85 LIBERTY=.4 NORMS=.7 TRUST=.85 ESTAB=.95 POP=.85 EDUC=.7 GLOBAL=.8 HAWK=-.1 VALUES=.8")
add("religious_right", "Religious conservatives", "Religious right", "1980s–today", "today",
    "Faith and family first: ending abortion, religious liberty, traditional marriage, parental rights in schools.",
    "G=.7 REDIS=.4 REG=.3 SOCINS=.3 ENV=.5 MORAL=1 GENDERID=.9 RELIGION=1 FAMILY=.9 EQUITY=.5 IMMIG=.4 NATION=.6 ORDER=.6 GUNS=.6 LIBERTY=.6 SPEECH=.1 NORMS=.3 EDUC=.8 GLOBAL=.3 HAWK=.4 VALUES=.9")
add("tech_right", "Tech right", "Tech right", "2020s", "today",
    "Silicon Valley's turn rightward: deregulate AI and crypto, build fast, high-skill immigration, against DEI and speech rules.",
    "G=.5 REDIS=.7 REG=.8 SOCINS=.5 HOUSING=-.5 TRADE=.3 ENV=.6 TECH=1 PRIVACY=.3 MORAL=-.1 GENDERID=.7 RELIGION=0 FAMILY=.2 EQUITY=.9 IMMIG=.3 NATION=.4 ORDER=.7 GUNS=.5 LIBERTY=-.5 SPEECH=-.8 NORMS=.6 TRUST=.5 ESTAB=.9 POP=.6 EDUC=.8 GLOBAL=.5 HAWK=.3 VALUES=.3")
add("postliberal", "Post-liberal right", "Post-liberals", "2020s", "today",
    "Catholic integralists and 'common good' conservatives: use state power for traditional morality, families and workers.",
    "G=.85 REDIS=-.2 REG=-.3 SOCINS=-.3 ENV=.2 TRADE=.8 TECH=-.6 PRIVACY=.4 MORAL=1 GENDERID=1 RELIGION=1 FAMILY=1 EQUITY=.6 IMMIG=.8 NATION=.9 ORDER=.8 GUNS=.5 LIBERTY=.9 SPEECH=.6 NORMS=.8 ESTAB=.9 POP=.8 EDUC=.7 GLOBAL=.6 HAWK=-.2 VALUES=1")

# ---------------- Pew typology (2021 report) ----------------
add("pew_progressive", "Progressive Left", "Progressive Left", "Pew typology", "typology",
    "Young, highly educated and very liberal on every issue; want sweeping change to the system.",
    "G=-.9 REDIS=-.85 REG=-.75 SOCINS=-.85 ENV=-.85 TRADE=0 MORAL=-.9 GENDERID=-.9 RELIGION=-.8 FAMILY=-.8 EQUITY=-.9 IMMIG=-.8 NATION=-.8 ORDER=-.8 GUNS=-.8 NORMS=-.5 VOTING=-.9 ESTAB=.2 POP=.5 EDUC=-.6 GLOBAL=-.5 HAWK=-.6 VALUES=-.9")
add("pew_estlib", "Establishment Liberals", "Estab. Liberals", "Pew typology", "typology",
    "Liberal but pragmatic; trust institutions more and prefer compromise and incremental change.",
    "G=-.7 REDIS=-.6 REG=-.5 SOCINS=-.6 ENV=-.7 TRADE=-.4 MORAL=-.8 GENDERID=-.7 RELIGION=-.7 FAMILY=-.7 EQUITY=-.6 IMMIG=-.6 NATION=-.6 ORDER=-.3 GUNS=-.7 NORMS=-.7 VOTING=-.8 TRUST=-.3 ESTAB=-.7 POP=-.4 EDUC=-.5 GLOBAL=-.8 HAWK=0 VALUES=-.6")
add("pew_mainstays", "Democratic Mainstays", "Dem. Mainstays", "Pew typology", "typology",
    "The party's largest and most diverse bloc: liberal on economics, more moderate and religious on social issues.",
    "G=-.5 REDIS=-.5 REG=-.4 SOCINS=-.5 ENV=-.4 TRADE=.1 MORAL=-.2 GENDERID=0 RELIGION=.2 FAMILY=0 EQUITY=-.6 IMMIG=-.2 NATION=0 ORDER=.1 GUNS=-.6 NORMS=-.5 VOTING=-.6 ESTAB=-.4 POP=.1 GLOBAL=-.4 HAWK=.1 VALUES=-.2")
add("pew_outsider", "Outsider Left", "Outsider Left", "Pew typology", "typology",
    "Young, very liberal and frustrated with the system and with the Democratic Party itself.",
    "G=-.6 REDIS=-.7 REG=-.6 SOCINS=-.7 ENV=-.7 TRADE=.2 MORAL=-.7 GENDERID=-.6 RELIGION=-.6 FAMILY=-.6 EQUITY=-.7 IMMIG=-.6 NATION=-.6 ORDER=-.6 GUNS=-.5 TRUST=.6 ESTAB=.6 POP=.7 HAWK=-.5 GLOBAL=0 VALUES=-.6")
add("pew_sideliners", "Stressed Sideliners", "Sideliners", "Pew typology", "typology",
    "Politically disengaged, financially stressed, mixed views: liberal-leaning on economics, conservative-leaning on culture.",
    "G=0 REDIS=-.3 REG=-.2 SOCINS=-.3 ENV=-.1 TRADE=.4 MORAL=.1 GENDERID=.3 RELIGION=.2 FAMILY=.2 EQUITY=.1 IMMIG=.3 NATION=.3 ORDER=.3 GUNS=0 TRUST=.6 ESTAB=.6 POP=.7 GLOBAL=.3 VALUES=.1")
add("pew_ambivalent", "Ambivalent Right", "Ambivalent Right", "Pew typology", "typology",
    "Younger, right-leaning on economics and immigration but moderate on abortion, marijuana and same-sex marriage.",
    "G=.35 REDIS=.5 REG=.4 SOCINS=.3 ENV=.3 TRADE=.3 MORAL=-.1 GENDERID=.3 RELIGION=.1 FAMILY=.2 EQUITY=.5 IMMIG=.4 NATION=.4 ORDER=.5 GUNS=.5 LIBERTY=-.3 ESTAB=.4 POP=.5 EDUC=.4 GLOBAL=.3 HAWK=.1 VALUES=.3")
add("pew_populist", "Populist Right", "Populist Right", "Pew typology", "typology",
    "Less affluent conservatives: very restrictive on immigration, critical of big business and free trade, distrust elites.",
    "G=.75 REDIS=.3 REG=.2 SOCINS=.1 ENV=.6 TRADE=.9 MORAL=.5 GENDERID=.8 RELIGION=.5 FAMILY=.5 EQUITY=.85 IMMIG=1 NATION=.9 ORDER=.7 GUNS=.8 NORMS=.5 VOTING=.8 TRUST=.8 ESTAB=.9 POP=1 EDUC=.5 GLOBAL=.8 HAWK=0 VALUES=.7")
add("pew_committed", "Committed Conservatives", "Committed Cons.", "Pew typology", "typology",
    "Traditional pro-business conservatives: low taxes, limited government, free trade, an active role in the world.",
    "G=.7 REDIS=.85 REG=.8 SOCINS=.7 ENV=.6 TRADE=-.4 MORAL=.6 GENDERID=.7 RELIGION=.5 FAMILY=.5 EQUITY=.7 IMMIG=.6 NATION=.6 ORDER=.6 GUNS=.7 NORMS=0 ESTAB=.4 POP=.2 EDUC=.6 GLOBAL=-.2 HAWK=.6 VALUES=.6")
add("pew_faithflag", "Faith and Flag Conservatives", "Faith & Flag", "Pew typology", "typology",
    "The most conservative group: religion should shape law and public life, strongly traditional, intensely partisan.",
    "G=.9 REDIS=.7 REG=.6 SOCINS=.5 ENV=.8 TRADE=.5 MORAL=.95 GENDERID=.95 RELIGION=1 FAMILY=.85 EQUITY=.85 IMMIG=.9 NATION=.9 ORDER=.8 GUNS=.9 NORMS=.6 VOTING=.85 TRUST=.6 ESTAB=.8 POP=.6 EDUC=.7 GLOBAL=.7 HAWK=.4 VALUES=.9")

# ---------------- Presidents (record in office) ----------------
add("pres_tr", "Theodore Roosevelt", "T. Roosevelt", "1901–1909", "president",
    "Trust-busting, food and drug safety, national parks, a big navy and a broad view of presidential power.",
    "REDIS=-.2 REG=-.6 ENV=-.8 TRADE=.4 NATION=.6 ORDER=.4 NORMS=.7 ESTAB=-.2 POP=.3 FED=-.6 GLOBAL=-.2 HAWK=.8 VALUES=.3")
add("pres_wilson", "Woodrow Wilson", "Wilson", "1913–1921", "president",
    "Income tax, Federal Reserve, lower tariffs, the League of Nations, and wartime limits on speech.",
    "REDIS=-.5 REG=-.5 TRADE=-.6 IMMIG=.3 NATION=.5 ORDER=.5 PRIVACY=.6 SPEECH=.9 NORMS=.4 FED=-.5 GLOBAL=-.9 HAWK=.4 VALUES=.2")
add("pres_fdr", "Franklin D. Roosevelt", "FDR", "1933–1945", "president",
    "The New Deal: Social Security, labor rights, public works, bank regulation; four terms and a wartime presidency.",
    "G=-.6 REDIS=-.8 REG=-.8 SOCINS=-.8 ENV=-.4 TRADE=-.4 IMMIG=.5 NATION=.3 PRIVACY=.6 NORMS=.8 ESTAB=-.5 POP=.3 FED=-.8 GLOBAL=-.8 HAWK=.5 VALUES=-.3")
add("pres_truman", "Harry Truman", "Truman", "1945–1953", "president",
    "Fair Deal, proposed national health insurance, desegregated the military, NATO and the Marshall Plan.",
    "G=-.4 REDIS=-.5 REG=-.4 SOCINS=-.8 TRADE=-.6 EQUITY=-.4 IMMIG=0 ORDER=.3 NORMS=.5 FED=-.6 GLOBAL=-.9 HAWK=.6 VALUES=-.1")
add("pres_ike", "Dwight Eisenhower", "Eisenhower", "1953–1961", "president",
    "Kept the New Deal, built the interstates, enforced school desegregation, balanced budgets, alliances abroad.",
    "G=.1 REDIS=.2 REG=.1 SOCINS=-.1 TRADE=-.5 ENV=0 RELIGION=.5 EQUITY=-.2 IMMIG=.5 ORDER=.3 NORMS=-.3 ESTAB=-.6 POP=-.5 FED=-.4 GLOBAL=-.8 HAWK=.3 VALUES=.3")
add("pres_jfk", "John F. Kennedy", "JFK", "1961–1963", "president",
    "Tax cuts and trade expansion, a civil rights bill, the space race, a hard line against the Soviets.",
    "G=-.3 REDIS=-.2 REG=-.3 SOCINS=-.5 ENV=-.2 TRADE=-.7 RELIGION=-.5 EQUITY=-.4 IMMIG=-.4 ORDER=.2 FED=-.5 GLOBAL=-.8 HAWK=.6 VALUES=-.2")
add("pres_lbj", "Lyndon B. Johnson", "LBJ", "1963–1969", "president",
    "The Great Society: Medicare, Medicaid, the Civil Rights and Voting Rights Acts, open immigration, and the Vietnam escalation.",
    "G=-.6 REDIS=-.8 REG=-.6 SOCINS=-.85 ENV=-.5 TRADE=-.5 EQUITY=-.7 IMMIG=-.6 ORDER=.3 GUNS=-.5 NORMS=.4 VOTING=-.9 FED=-.9 EDUC=-.7 GLOBAL=-.6 HAWK=.8 VALUES=-.4")
add("pres_nixon", "Richard Nixon", "Nixon", "1969–1974", "president",
    "Created the EPA, imposed wage and price controls, law and order, opened China, and Watergate.",
    "G=.3 REDIS=0 REG=-.3 SOCINS=-.2 ENV=-.5 TRADE=.4 MORAL=.4 EQUITY=-.3 NATION=.5 ORDER=.8 PRIVACY=.9 NORMS=.9 TRUST=-.4 ESTAB=-.3 POP=.3 FED=.3 GLOBAL=-.3 HAWK=.5 VALUES=.5")
add("pres_carter", "Jimmy Carter", "Carter", "1977–1981", "president",
    "Deregulated airlines and trucking, energy conservation, human rights abroad, the Camp David Accords.",
    "G=-.2 REDIS=-.2 REG=.3 SOCINS=-.4 ENV=-.7 TRADE=-.4 MORAL=.1 RELIGION=.3 EQUITY=-.4 IMMIG=-.3 NORMS=-.6 FED=-.3 EDUC=-.5 GLOBAL=-.8 HAWK=-.3 VALUES=-.1")
add("pres_reagan", "Ronald Reagan", "Reagan", "1981–1989", "president",
    "Big tax cuts, deregulation, a military buildup, the 1986 immigration amnesty, and a hard line on the Soviet Union.",
    "G=.7 REDIS=.8 REG=.75 SOCINS=.5 ENV=.6 TRADE=-.4 MORAL=.6 RELIGION=.6 FAMILY=.5 EQUITY=.6 IMMIG=-.2 NATION=.6 ORDER=.7 GUNS=.5 ESTAB=.4 FED=.6 EDUC=.4 GLOBAL=-.4 HAWK=.85 VALUES=.6")
add("pres_bush41", "George H. W. Bush", "Bush (41)", "1989–1993", "president",
    "Raised taxes to cut the deficit, the Clean Air Act and the ADA, the Gulf War coalition, NAFTA talks.",
    "G=.45 REDIS=.4 REG=.3 SOCINS=.3 ENV=-.2 TRADE=-.8 MORAL=.5 RELIGION=.4 EQUITY=.3 IMMIG=-.3 ORDER=.6 GUNS=.3 NORMS=-.4 ESTAB=-.6 GLOBAL=-.8 HAWK=.6 VALUES=.5")
add("pres_clinton", "Bill Clinton", "Clinton", "1993–2001", "president",
    "Balanced budgets, welfare reform, NAFTA, the 1994 crime bill and assault weapons ban, DOMA.",
    "G=-.3 REDIS=-.2 REG=0 SOCINS=-.4 ENV=-.4 TRADE=-.8 MORAL=-.4 GENDERID=.3 RELIGION=-.1 FAMILY=0 EQUITY=-.4 IMMIG=.3 ORDER=.6 GUNS=-.6 NORMS=-.3 POP=-.4 GLOBAL=-.7 HAWK=.3 VALUES=-.2")
add("pres_bush43", "George W. Bush", "Bush (43)", "2001–2009", "president",
    "Tax cuts, No Child Left Behind, Medicare drug benefit, the Patriot Act, and the Iraq and Afghanistan wars.",
    "G=.6 REDIS=.6 REG=.5 SOCINS=.2 ENV=.5 TRADE=-.6 MORAL=.7 GENDERID=.7 RELIGION=.7 FAMILY=.6 EQUITY=.4 IMMIG=-.2 NATION=.4 ORDER=.6 GUNS=.6 PRIVACY=.9 NORMS=.6 FED=-.3 EDUC=.3 GLOBAL=-.1 HAWK=.95 VALUES=.6")
add("pres_obama", "Barack Obama", "Obama", "2009–2017", "president",
    "The ACA, Wall Street reform, the Paris climate deal, DACA, same-sex marriage support, drone strikes.",
    "G=-.55 REDIS=-.5 REG=-.5 SOCINS=-.6 ENV=-.6 TRADE=-.5 TECH=-.2 PRIVACY=.4 MORAL=-.6 GENDERID=-.5 RELIGION=-.3 FAMILY=-.4 EQUITY=-.5 IMMIG=-.3 NATION=-.4 ORDER=-.3 GUNS=-.7 NORMS=-.2 VOTING=-.7 ESTAB=-.6 POP=-.4 FED=-.5 EDUC=-.2 GLOBAL=-.8 HAWK=.1 VALUES=-.5")
add("pres_trump", "Donald Trump", "Trump", "2017–21, 2025–", "president",
    "Tariffs, tax cuts, border enforcement and deportations, deregulation, an expansive view of presidential power.",
    "G=.75 REDIS=.5 REG=.6 SOCINS=.2 ENV=.9 TRADE=1 TECH=.5 MORAL=.5 GENDERID=.9 RELIGION=.5 FAMILY=.4 EQUITY=.9 IMMIG=1 NATION=.9 ORDER=.9 GUNS=.8 SPEECH=0 NORMS=1 VOTING=.9 TRUST=.6 ESTAB=.9 POP=.9 FED=.2 EDUC=.7 GLOBAL=.9 HAWK=0 VALUES=.6")
add("pres_biden", "Joe Biden", "Biden", "2021–2025", "president",
    "Infrastructure and climate spending, kept and added tariffs on China, union support, student debt relief, aid to Ukraine.",
    "G=-.55 REDIS=-.55 REG=-.55 SOCINS=-.5 HOUSING=-.4 ENV=-.7 TRADE=.4 TECH=-.4 MORAL=-.6 GENDERID=-.7 RELIGION=-.4 FAMILY=-.5 EQUITY=-.6 IMMIG=-.2 NATION=-.4 ORDER=-.1 GUNS=-.7 NORMS=-.5 VOTING=-.7 ESTAB=-.6 POP=-.2 FED=-.5 EDUC=-.6 GLOBAL=-.8 HAWK=.2 VALUES=-.5")

# ---------------- US history ----------------
add("federalists", "Federalists", "Federalists", "1790s", "history",
    "Hamilton and Adams: a strong national government and bank, tariffs for industry, the Alien and Sedition Acts.",
    "REG=-.2 TRADE=.5 RELIGION=.3 IMMIG=.6 ORDER=.6 SPEECH=.8 NORMS=.5 VOTING=.7 POP=-.8 FED=-.9 GLOBAL=-.2 HAWK=.4 VALUES=.6")
add("jeffersonians", "Jeffersonian Republicans", "Jeffersonians", "1790s–1820s", "history",
    "Jefferson and Madison: limited federal power, farmers over bankers, church-state separation, against the Sedition Act.",
    "REG=.6 TRADE=-.3 RELIGION=-.7 IMMIG=-.4 ORDER=-.2 SPEECH=-.6 NORMS=-.6 VOTING=-.3 POP=.6 FED=.9 GLOBAL=.4 HAWK=-.2 VALUES=-.1")
add("jacksonians", "Jacksonian Democrats", "Jacksonians", "1830s–1840s", "history",
    "Andrew Jackson's party: kill the national bank, power to the common (white) man, a forceful president, westward expansion.",
    "REDIS=.3 REG=.6 TRADE=-.2 RELIGION=-.2 IMMIG=-.4 NATION=.3 ORDER=.3 NORMS=.8 VOTING=-.5 POP=.9 FED=.6 HAWK=.6")
add("whigs", "Whigs", "Whigs", "1830s–1850s", "history",
    "Henry Clay's American System: tariffs, a national bank, roads and canals, moral reform, and checks on 'King Andrew'.",
    "REG=-.4 TRADE=.7 MORAL=.6 RELIGION=.5 IMMIG=.4 NATION=.5 ORDER=.5 NORMS=-.8 POP=-.5 FED=-.5 HAWK=-.4 VALUES=.4")
add("radical_gop", "Radical Republicans", "Radical Reps.", "1860s–1870s", "history",
    "Abolition, Reconstruction, the 14th and 15th Amendments, federal protection for freed people's rights and votes.",
    "REG=-.2 TRADE=.7 MORAL=.4 RELIGION=.4 EQUITY=-.9 ORDER=.4 NORMS=-.6 VOTING=-.9 FED=-1 HAWK=.6 VALUES=-.6")
add("gilded_gop", "Gilded Age Republicans", "Gilded Age GOP", "1870s–1900s", "history",
    "Party of business and high tariffs: gold standard, light regulation, railroads and industry first.",
    "REDIS=.9 REG=.9 SOCINS=.9 ENV=.8 TRADE=.9 MORAL=.5 RELIGION=.4 IMMIG=.1 NATION=.5 POP=-.8 ESTAB=-.6 FED=-.2 GLOBAL=.3 HAWK=.4 VALUES=.5")
add("peoples_party", "People's (Populist) Party", "Populists 1890s", "1890s", "history",
    "Farmers and workers against railroads and banks: public ownership of railroads, an income tax, direct elections.",
    "REDIS=-.6 REG=-.85 TRADE=.2 MORAL=.4 RELIGION=.4 IMMIG=.4 VOTING=-.5 ESTAB=.6 POP=1 FED=-.3")
add("socialist_debs", "Socialist Party (Debs era)", "Debs Socialists", "1900s–1920s", "history",
    "Eugene Debs's party: public ownership, labor rights, women's suffrage, opposition to World War I.",
    "REDIS=-1 REG=-1 SOCINS=-.9 RELIGION=-.5 FAMILY=-.6 IMMIG=-.4 ORDER=-.5 SPEECH=-.8 VOTING=-.8 ESTAB=.8 POP=.9 GLOBAL=-.3 HAWK=-1 VALUES=-.8")
add("bull_moose", "Bull Moose Progressives", "Bull Moose 1912", "1912", "history",
    "Theodore Roosevelt's party: trust-busting, conservation, social insurance, direct democracy, a strong nation.",
    "G=-.2 REDIS=-.4 REG=-.7 SOCINS=-.45 ENV=-.6 NATION=.4 VOTING=-.6 POP=.6 FED=-.5 GLOBAL=-.2 HAWK=.5")
add("dem_new_deal", "New Deal Democrats", "New Deal Dems", "1930s–60s", "history",
    "FDR-to-LBJ coalition: Social Security, unions, public works, Cold War internationalism, socially traditional.",
    "G=-.35 REDIS=-.7 REG=-.6 SOCINS=-.65 TRADE=-.2 MORAL=.3 RELIGION=.2 FAMILY=.5 IMMIG=.2 NATION=.3 ORDER=.3 FED=-.6 GLOBAL=-.6 HAWK=.3")
add("rockefeller", "Rockefeller Republicans", "Rockefeller GOP", "1950s–70s", "history",
    "Liberal Northeastern Republicans: pro-business but accepting the welfare state, civil rights, environmental laws, internationalism.",
    "G=.15 REDIS=.2 REG=.1 SOCINS=0 ENV=-.4 TRADE=-.6 MORAL=-.2 RELIGION=0 FAMILY=.2 EQUITY=-.3 IMMIG=0 ORDER=.4 GUNS=0 NORMS=-.4 ESTAB=-.7 POP=-.8 FED=-.2 GLOBAL=-.8 HAWK=.5 VALUES=.1")
add("goldwater", "Goldwater conservatives", "Goldwater '64", "1964", "history",
    "Barry Goldwater's insurgency: roll back the New Deal, states' rights, all-out anti-communism.",
    "G=.75 REDIS=.95 REG=.95 SOCINS=.9 TRADE=-.6 MORAL=.3 RELIGION=.2 EQUITY=.9 ORDER=.7 GUNS=.8 LIBERTY=-.3 ESTAB=.5 POP=.3 FED=.95 GLOBAL=0 HAWK=.95 VALUES=.5")
add("great_society", "Great Society liberals", "Great Society", "1960s", "history",
    "Johnson-era liberals: war on poverty, Medicare, civil rights and voting rights, federal aid to schools, Cold War resolve.",
    "G=-.6 REDIS=-.8 REG=-.6 SOCINS=-.8 ENV=-.4 MORAL=-.1 RELIGION=-.1 EQUITY=-.7 IMMIG=-.4 ORDER=-.1 GUNS=-.4 VOTING=-.9 ESTAB=-.7 POP=-.4 FED=-.8 EDUC=-.7 GLOBAL=-.7 HAWK=.5 VALUES=-.5")
add("new_left", "New Left", "New Left '60s", "1960s–70s", "history",
    "Student radicals and the counterculture: against the Vietnam War, for civil rights, sexual freedom and participatory democracy.",
    "G=-.9 REDIS=-.8 REG=-.8 SOCINS=-.8 ENV=-.6 PRIVACY=-.8 MORAL=-.9 RELIGION=-.7 FAMILY=-.8 EQUITY=-.8 ORDER=-.8 LIBERTY=-.8 SPEECH=-.9 VOTING=-.8 TRUST=.7 ESTAB=.9 POP=.7 HAWK=-1 VALUES=-.9")
add("gop_reagan", "Reagan coalition", "Reagan GOP", "1980s", "history",
    "Tax cuts, deregulation, free trade, strong defense and traditional values, uniting business and religious conservatives.",
    "G=.65 REDIS=.75 REG=.7 SOCINS=.5 ENV=.4 TRADE=-.6 MORAL=.6 RELIGION=.5 FAMILY=.5 EQUITY=.5 IMMIG=0 NATION=.5 ORDER=.7 GUNS=.6 LIBERTY=.3 NORMS=.1 TRUST=.5 FED=.5 EDUC=.4 GLOBAL=-.5 HAWK=.85")
add("dem_new", "New Democrats", "New Dems '90s", "1990s", "history",
    "Clinton-era centrists: balanced budgets, welfare reform, free trade, tough on crime.",
    "G=-.3 REDIS=-.2 REG=-.1 SOCINS=-.3 ENV=-.4 TRADE=-.7 MORAL=-.35 RELIGION=-.2 FAMILY=-.1 EQUITY=-.3 IMMIG=.1 ORDER=.4 GUNS=-.4 NORMS=-.3 POP=-.4 GLOBAL=-.6 HAWK=.3")
add("gingrich", "Contract with America Republicans", "Gingrich '94", "1990s", "history",
    "Newt Gingrich's House majority: balanced budget amendment, welfare reform, tough-on-crime laws, term limits.",
    "G=.7 REDIS=.8 REG=.8 SOCINS=.7 ENV=.6 TRADE=-.6 MORAL=.6 RELIGION=.5 FAMILY=.5 EQUITY=.7 IMMIG=.4 ORDER=.85 GUNS=.8 NORMS=.3 ESTAB=.5 POP=.5 FED=.7 EDUC=.6 GLOBAL=-.3 HAWK=.5 VALUES=.6")
add("gop_establishment", "Bush–Romney Republicans", "Bush-era GOP", "2000s–2010s", "history",
    "Lower taxes, free trade, an active foreign policy, compassionate conservatism and respect for institutions.",
    "G=.55 REDIS=.7 REG=.6 SOCINS=.5 ENV=.45 TRADE=-.6 TECH=.4 MORAL=.55 GENDERID=.5 RELIGION=.45 FAMILY=.4 EQUITY=.5 IMMIG=.3 NATION=.4 ORDER=.5 GUNS=.6 NORMS=-.4 ESTAB=.2 EDUC=.5 GLOBAL=-.6 HAWK=.65 VALUES=.5")
add("tea_party", "Tea Party", "Tea Party", "2009–2014", "history",
    "Grassroots revolt against bailouts, the ACA and federal spending: cut government, follow the Constitution, primary the moderates.",
    "G=.85 REDIS=.95 REG=.9 SOCINS=.6 ENV=.85 TRADE=-.2 MORAL=.6 GENDERID=.7 RELIGION=.6 FAMILY=.6 EQUITY=.85 IMMIG=.8 NATION=.7 ORDER=.6 GUNS=.95 LIBERTY=-.2 NORMS=-.2 TRUST=.9 ESTAB=.9 POP=.8 FED=.85 EDUC=.8 GLOBAL=.5 HAWK=.4 VALUES=.7")
add("occupy", "Occupy Wall Street", "Occupy", "2011", "history",
    "'We are the 99%': against bailouts, inequality and corporate power in politics.",
    "G=-.85 REDIS=-1 REG=-.95 SOCINS=-.9 ENV=-.8 TRADE=.4 PRIVACY=-.8 EQUITY=-.6 ORDER=-.8 TRUST=.8 ESTAB=.9 POP=1 GLOBAL=0 HAWK=-.8 VALUES=-.8")

# ---------------- Ideologies ----------------
add("ancap", "Anarcho-capitalism", "Ancaps", "ideology", "ideology",
    "Abolish the state; private property, markets and voluntary contracts provide everything, including courts and security.",
    "G=.4 REDIS=1 REG=1 SOCINS=1 HOUSING=-.8 TRADE=-1 ENV=.9 TECH=1 PRIVACY=-1 MORAL=-.7 GENDERID=0 RELIGION=-.4 EQUITY=.8 IMMIG=-.6 ORDER=-.5 GUNS=1 LIBERTY=-1 SPEECH=-1 NORMS=-.9 TRUST=1 ESTAB=1 FED=1 EDUC=1 GLOBAL=.9 HAWK=-1")
add("classical_liberal", "Classical liberalism", "Classical liberals", "ideology", "ideology",
    "Limited constitutional government, free markets and free trade, individual rights, free speech and the rule of law.",
    "G=.2 REDIS=.7 REG=.7 SOCINS=.6 HOUSING=-.7 TRADE=-1 ENV=.2 TECH=.6 PRIVACY=-.7 MORAL=-.5 GENDERID=-.2 RELIGION=-.8 FAMILY=-.2 EQUITY=.7 IMMIG=-.6 NATION=-.3 ORDER=-.1 GUNS=.4 LIBERTY=-.8 SPEECH=-1 NORMS=-1 ESTAB=-.2 POP=-.6 FED=.3 EDUC=.6 GLOBAL=-.6 HAWK=-.3 VALUES=-.2")
add("neoliberal", "Neoliberalism", "Neoliberals", "ideology", "ideology",
    "Markets with a safety net: free trade, open immigration, carbon pricing, build more housing, trust expertise.",
    "G=0 REDIS=.2 REG=.4 SOCINS=.1 HOUSING=-.9 TRADE=-1 ENV=-.4 TECH=.5 MORAL=-.6 GENDERID=-.4 RELIGION=-.5 FAMILY=-.4 EQUITY=0 IMMIG=-.8 NATION=-.6 ORDER=0 GUNS=-.4 SPEECH=-.5 NORMS=-.8 ESTAB=-.7 POP=-.9 FED=-.2 EDUC=.4 GLOBAL=-1 HAWK=.3 VALUES=-.3")
add("social_democracy", "Social democracy", "Social democrats", "ideology", "ideology",
    "Regulated capitalism with a universal welfare state: public health care, strong unions, high taxes, broad equality.",
    "G=-.65 REDIS=-.8 REG=-.6 SOCINS=-.9 HOUSING=-.3 ENV=-.7 TRADE=-.2 TECH=-.6 PRIVACY=-.5 MORAL=-.6 GENDERID=-.5 RELIGION=-.6 FAMILY=-.7 EQUITY=-.5 IMMIG=-.3 NATION=-.3 ORDER=-.5 GUNS=-.9 LIBERTY=.2 SPEECH=.3 NORMS=-.6 ESTAB=-.4 FED=-.7 EDUC=-.8 GLOBAL=-.8 HAWK=-.3 VALUES=-.6")
add("ecosocialism", "Eco-socialism", "Eco-socialists", "ideology", "ideology",
    "Capitalism is driving climate collapse: public ownership, degrowth or planned transition, global climate justice.",
    "G=-.95 REDIS=-.95 REG=-1 SOCINS=-.9 HOUSING=-.3 ENV=-1 TRADE=.5 TECH=-.6 MORAL=-.7 GENDERID=-.8 EQUITY=-.9 IMMIG=-.9 ORDER=-.8 ESTAB=.7 POP=.8 GLOBAL=-.3 HAWK=-.9 VALUES=-.9")
add("communism", "Marxism–Leninism", "Communists", "ideology", "ideology",
    "State ownership of the economy under a single vanguard party, in the Soviet and Chinese tradition.",
    "G=-1 REDIS=-1 REG=-1 SOCINS=-1 TRADE=.6 ENV=-.4 TECH=-.8 PRIVACY=.9 MORAL=-.4 RELIGION=-1 FAMILY=-.5 EQUITY=-.9 NATION=0 ORDER=.6 GUNS=-.6 LIBERTY=.8 SPEECH=.9 NORMS=.9 ESTAB=1 POP=.9 FED=-1 EDUC=-1 GLOBAL=.3 HAWK=-.5 VALUES=-.5")
add("left_anarchism", "Left anarchism", "Anarchists", "ideology", "ideology",
    "No state, no bosses: mutual aid, worker and community self-management, abolish police, prisons and borders.",
    "G=-1 REDIS=-1 REG=-.9 SOCINS=-.8 ENV=-.9 TECH=-.4 PRIVACY=-1 MORAL=-1 GENDERID=-1 RELIGION=-1 FAMILY=-1 EQUITY=-.9 IMMIG=-1 NATION=-1 ORDER=-1 GUNS=.3 LIBERTY=-1 SPEECH=-.6 NORMS=-1 TRUST=1 ESTAB=1 POP=1 FED=.7 GLOBAL=-.2 HAWK=-1 VALUES=-1")
add("christian_democracy", "Christian democracy", "Christian Dems", "ideology", "ideology",
    "Catholic social teaching in politics: a social market economy, family policy, moral tradition and international cooperation.",
    "G=.2 REDIS=-.3 REG=-.2 SOCINS=-.5 ENV=-.3 TRADE=-.4 MORAL=.6 GENDERID=.4 RELIGION=.7 FAMILY=.7 EQUITY=.2 IMMIG=.2 NATION=.4 ORDER=.5 GUNS=-.5 LIBERTY=.4 NORMS=-.6 ESTAB=-.5 POP=-.5 GLOBAL=-.7 HAWK=.2 VALUES=.6")
add("neoconservatism", "Neoconservatism", "Neocons", "ideology", "ideology",
    "Spread democracy with American power: strong military, interventions abroad, free markets, moderate social conservatism.",
    "G=.5 REDIS=.5 REG=.5 SOCINS=.3 TRADE=-.7 PRIVACY=.7 MORAL=.4 RELIGION=.4 FAMILY=.4 EQUITY=.7 IMMIG=0 NATION=.5 ORDER=.7 SPEECH=-.2 NORMS=.4 ESTAB=-.3 POP=-.5 GLOBAL=-.4 HAWK=1 VALUES=.5")
add("paleoconservatism", "Paleoconservatism", "Paleocons", "ideology", "ideology",
    "Old Right: tradition, local community and national identity; against mass immigration, free trade and foreign wars.",
    "G=.8 REDIS=.5 REG=.4 SOCINS=.4 TRADE=.9 ENV=.4 MORAL=.9 GENDERID=.9 RELIGION=.8 FAMILY=.9 EQUITY=.8 IMMIG=1 NATION=1 ORDER=.7 GUNS=.9 NORMS=-.2 ESTAB=.9 POP=.7 FED=.9 EDUC=.8 GLOBAL=1 HAWK=-.8 VALUES=.9")

# ---------------- Abroad ----------------
add("uk_labour", "UK Labour", "UK Labour", "2020s", "world",
    "Britain's center-left governing party: the NHS, workers' rights, clean energy, housebuilding, NATO.",
    "G=-.4 REDIS=-.4 REG=-.4 SOCINS=-.9 HOUSING=-.8 ENV=-.6 TRADE=-.3 TECH=-.3 PRIVACY=.2 MORAL=-.5 GENDERID=-.2 RELIGION=-.5 FAMILY=-.5 EQUITY=-.4 IMMIG=.1 NATION=-.2 ORDER=.2 GUNS=-1 SPEECH=.5 NORMS=-.5 ESTAB=-.5 GLOBAL=-.6 HAWK=.3 VALUES=-.4")
add("uk_conservatives", "UK Conservatives", "UK Tories", "2020s", "world",
    "Britain's center-right: lower taxes, Brexit, lower immigration, but firm support for the NHS and strict gun laws.",
    "G=.3 REDIS=.3 REG=.3 SOCINS=-.5 ENV=-.2 TRADE=-.6 MORAL=-.2 GENDERID=.5 RELIGION=.1 FAMILY=.2 EQUITY=.5 IMMIG=.5 NATION=.5 ORDER=.6 GUNS=-.9 SPEECH=.3 NORMS=0 GLOBAL=-.2 HAWK=.5 VALUES=.4")
add("reform_uk", "Reform UK", "Reform UK", "2020s", "world",
    "Nigel Farage's insurgent right: net-zero immigration, scrap net-zero climate targets, anti-establishment.",
    "G=.7 REDIS=.5 REG=.6 SOCINS=-.2 ENV=.9 TRADE=-.2 MORAL=.2 GENDERID=.8 RELIGION=.3 FAMILY=.5 EQUITY=.8 IMMIG=1 NATION=.9 ORDER=.8 GUNS=-.5 SPEECH=-.5 ESTAB=.9 POP=.9 GLOBAL=.9 HAWK=.1 VALUES=.7")
add("ca_liberals", "Canadian Liberals", "Canada Liberals", "2020s", "world",
    "Canada's governing center-left: public health care, carbon pricing (now scaled back), high immigration, strict gun laws.",
    "G=-.5 REDIS=-.5 REG=-.4 SOCINS=-.9 HOUSING=-.6 ENV=-.6 TRADE=-.7 MORAL=-.8 GENDERID=-.7 RELIGION=-.6 FAMILY=-.6 EQUITY=-.6 IMMIG=-.6 NATION=-.9 ORDER=-.2 GUNS=-.9 SPEECH=.5 NORMS=-.5 GLOBAL=-.9 HAWK=0 VALUES=-.5")
add("ca_conservatives", "Canadian Conservatives", "Canada Cons.", "2020s", "world",
    "Canada's center-right: cut taxes and the carbon tax, build homes and pipelines, tougher on crime; keeps public health care.",
    "G=.35 REDIS=.4 REG=.4 SOCINS=-.5 HOUSING=-.5 ENV=.5 TRADE=-.7 MORAL=0 GENDERID=.4 RELIGION=.2 FAMILY=.3 EQUITY=.6 IMMIG=.3 NATION=.4 ORDER=.7 GUNS=.2 SPEECH=-.5 ESTAB=.5 POP=.4 GLOBAL=-.3 HAWK=.4 VALUES=.4")
add("nordic_sd", "Nordic Social Democrats", "Nordic SDs", "2020s", "world",
    "Sweden's and Denmark's center-left: universal welfare, high taxes, flexible labor markets, free trade, and (in Denmark) strict immigration.",
    "G=-.55 REDIS=-.8 REG=-.3 SOCINS=-.95 ENV=-.7 TRADE=-.6 MORAL=-.8 GENDERID=-.5 RELIGION=-.7 FAMILY=-.9 EQUITY=-.3 IMMIG=.3 NATION=.1 ORDER=-.5 GUNS=-.7 SPEECH=.3 NORMS=-.7 TRUST=-.9 ESTAB=-.8 POP=-.6 EDUC=-.6 GLOBAL=-.8 HAWK=0 VALUES=-.6")
add("de_cdu", "German Christian Democrats", "German CDU", "2020s", "world",
    "Germany's center-right: social market economy, fiscal discipline, tighter asylum rules, strong support for the EU and NATO.",
    "G=.2 REDIS=0 REG=.1 SOCINS=-.7 ENV=-.4 TRADE=-.7 MORAL=.1 GENDERID=.1 RELIGION=.4 FAMILY=.4 EQUITY=.2 IMMIG=.4 NATION=.3 ORDER=.5 GUNS=-.9 SPEECH=.6 NORMS=-.7 ESTAB=-.6 POP=-.6 GLOBAL=-.9 HAWK=.2 VALUES=.3")
add("de_greens", "German Greens", "German Greens", "2020s", "world",
    "Climate-first progressives who became a governing party: rapid energy transition, civil liberties, pro-EU, firm on Ukraine.",
    "G=-.8 REDIS=-.6 REG=-.6 SOCINS=-.8 ENV=-1 TRADE=-.2 TECH=-.6 PRIVACY=-.9 MORAL=-.8 GENDERID=-.9 RELIGION=-.7 FAMILY=-.8 EQUITY=-.7 IMMIG=-.8 NATION=-.9 ORDER=-.6 GUNS=-.95 SPEECH=.6 NORMS=-.7 GLOBAL=-1 HAWK=.2 VALUES=-.8")
add("fr_rn", "French National Rally", "National Rally", "2020s", "world",
    "Marine Le Pen's party: sharply cut immigration, protect French industry, keep a generous welfare state, skeptical of the EU.",
    "G=.6 REDIS=-.2 REG=-.1 SOCINS=-.6 ENV=.4 TRADE=.9 PRIVACY=.5 MORAL=0 GENDERID=.5 RELIGION=-.2 FAMILY=.5 EQUITY=.7 IMMIG=1 NATION=1 ORDER=.9 GUNS=-.5 SPEECH=.3 ESTAB=.8 POP=.9 GLOBAL=.8 HAWK=-.2 VALUES=.7")
add("fr_renaissance", "Macron's Renaissance", "Macronists", "2020s", "world",
    "France's liberal center: pro-business reforms, a raised retirement age, strict secularism, a stronger EU.",
    "G=0 REDIS=.1 REG=.1 SOCINS=-.6 ENV=-.5 TRADE=-.5 TECH=.2 PRIVACY=.3 MORAL=-.6 GENDERID=-.2 RELIGION=-.8 FAMILY=-.4 EQUITY=.4 IMMIG=.3 NATION=.3 ORDER=.4 GUNS=-.9 SPEECH=.4 NORMS=.2 ESTAB=-.7 POP=-.8 GLOBAL=-.9 HAWK=.3 VALUES=-.1")

ids = [p["id"] for p in P]
assert len(ids) == len(set(ids)), "duplicate ids"
axes = json.loads((ROOT / "items" / "modules" / "axes.json").read_text())
valid = {"G"} | {a["id"] for f in axes["families"] for a in f["axes"]}
for p in P:
    bad = set(p["pos"]) - valid
    assert not bad, (p["id"], bad)
    assert all(-1 <= v <= 1 for v in p["pos"].values()), p["id"]
    assert len(p["pos"]) >= 8, (p["id"], len(p["pos"]))
    assert len(p["short"]) <= 18, p["id"]

OUT.write_text(json.dumps({
    "module": "profiles",
    "note": "Hand-placed reference points for comparison, from party platforms, voting records, survey reports and historians' accounts. Scale -1 to +1 on the axes in axes.json; an axis is left out where the group had no clear position (historical parties never weighed in on AI or gender identity). Approximate and meant for fun, not a measurement. Generated by scripts/revisions/rev_2026_10_13_profiles.py.",
    "categories": CATS,
    "profiles": P,
}, indent=1, ensure_ascii=False) + "\n")
print(len(P), "profiles;", {c["id"]: sum(p["cat"] == c["id"] for p in P) for c in CATS})
