"""Politician simulation: roster and pre-registered expectations.

Written BEFORE any answers were scored (2026-10-13). Each politician takes the
full 469-question bank, answered as closely as possible to their public record
(votes, platforms, statements). sim/evaluate.py then checks the expectations
below against the scores the quiz produces.

party: D, R, I (independent), L (Libertarian), G (Green)
expect_match: comparison groups (items/modules/profiles.json) that should be
  among the politician's 5 closest matches; any one counts as a hit.
sig: expected signs on specific axes, "AX+" = score > +0.2, "AX-" = score < -0.2,
  "AX0" = within ±0.35 (genuinely mixed or middle).
order: pairs (a, b) where a's overall (G) score should be left of b's.
"""

R = []


def add(pid, name, party, role, expect_match=(), sig=""):
    R.append({"id": pid, "name": name, "party": party, "role": role,
              "expect_match": list(expect_match), "sig": sig.split()})


# ---------------- Democrats ----------------
add("biden", "Joe Biden", "D", "President 2021–25", ["pres_biden", "dem_mainstream", "pew_estlib"], "G- TRADE+ ESTAB- NORMS- GLOBAL-")
add("harris", "Kamala Harris", "D", "Vice President 2021–25", ["dem_mainstream", "pres_biden", "pew_estlib"], "G- GUNS- MORAL- GLOBAL-")
add("obama", "Barack Obama", "D", "President 2009–17", ["pres_obama", "dem_mainstream", "pew_estlib"], "G- GLOBAL- ESTAB- POP-")
add("bclinton", "Bill Clinton", "D", "President 1993–2001", ["pres_clinton", "dem_new", "blue_dog"], "G- TRADE- ORDER+ GLOBAL-")
add("hclinton", "Hillary Clinton", "D", "Secretary of State, 2016 nominee", ["dem_mainstream", "pres_obama", "pew_estlib"], "G- HAWK+ GLOBAL- ESTAB-")
add("sanders", "Bernie Sanders", "I", "Senator, Vermont", ["dem_socialist", "dem_progressive", "pew_progressive"], "G- REDIS- SOCINS- TRADE+ POP+ HAWK-")
add("warren", "Elizabeth Warren", "D", "Senator, Massachusetts", ["dem_progressive", "pew_progressive", "pew_estlib"], "G- REDIS- REG- TECH- TRADE+")
add("aoc", "Alexandria Ocasio-Cortez", "D", "Representative, New York", ["dem_progressive", "dem_socialist", "pew_progressive"], "G- REDIS- ENV- IMMIG- ORDER- POP+")
add("omar", "Ilhan Omar", "D", "Representative, Minnesota", ["dem_progressive", "dem_socialist", "pew_progressive"], "G- IMMIG- HAWK- ORDER-")
add("tlaib", "Rashida Tlaib", "D", "Representative, Michigan", ["dem_socialist", "dem_progressive", "pew_progressive"], "G- HAWK- REDIS- ORDER-")
add("pressley", "Ayanna Pressley", "D", "Representative, Massachusetts", ["dem_progressive", "pew_progressive", "dem_socialist"], "G- ORDER- EQUITY-")
add("jayapal", "Pramila Jayapal", "D", "Representative, Washington; Progressive Caucus chair", ["dem_progressive", "pew_progressive", "dem_socialist"], "G- SOCINS- IMMIG-")
add("khanna", "Ro Khanna", "D", "Representative, California", ["dem_progressive", "pew_progressive", "abundance"], "G- TRADE+ HAWK- TECH0")
add("schumer", "Chuck Schumer", "D", "Senate Democratic leader", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- HAWK+ GLOBAL-")
add("pelosi", "Nancy Pelosi", "D", "Former Speaker of the House", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- NORMS- GLOBAL-")
add("jeffries", "Hakeem Jeffries", "D", "House Democratic leader", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- GLOBAL-")
add("manchin", "Joe Manchin", "I", "Former Senator, West Virginia", ["blue_dog", "centrist", "pew_mainstays"], "G0 ENV+ GUNS+ MORAL0")
add("sinema", "Kyrsten Sinema", "I", "Former Senator, Arizona", ["blue_dog", "centrist", "dem_new"], "G0 NORMS-")
add("tester", "Jon Tester", "D", "Former Senator, Montana", ["blue_dog", "pew_mainstays", "centrist"], "G- GUNS+ TRADE+")
add("klobuchar", "Amy Klobuchar", "D", "Senator, Minnesota", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- TECH- GLOBAL-")
add("buttigieg", "Pete Buttigieg", "D", "Former Transportation Secretary", ["dem_mainstream", "abundance", "pew_estlib"], "G- GENDERID- GLOBAL-")
add("newsom", "Gavin Newsom", "D", "Governor, California", ["dem_mainstream", "pew_estlib", "dem_progressive"], "G- ENV- GUNS- HOUSING-")
add("shapiro", "Josh Shapiro", "D", "Governor, Pennsylvania", ["dem_mainstream", "pew_estlib", "blue_dog"], "G- EDUC0")
add("whitmer", "Gretchen Whitmer", "D", "Governor, Michigan", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- MORAL-")
add("pritzker", "JB Pritzker", "D", "Governor, Illinois", ["dem_mainstream", "dem_progressive", "pew_estlib"], "G- GUNS- MORAL-")
add("beshear", "Andy Beshear", "D", "Governor, Kentucky", ["dem_mainstream", "pew_mainstays", "blue_dog"], "G- RELIGION0")
add("booker", "Cory Booker", "D", "Senator, New Jersey", ["dem_mainstream", "dem_progressive", "pew_estlib"], "G- ORDER- LIBERTY-")
add("cmurphy", "Chris Murphy", "D", "Senator, Connecticut", ["dem_mainstream", "dem_progressive", "pew_estlib"], "G- GUNS- POP+")
add("fetterman", "John Fetterman", "D", "Senator, Pennsylvania", ["dem_mainstream", "blue_dog", "pew_mainstays"], "G- HAWK+ LIBERTY-")
add("warnock", "Raphael Warnock", "D", "Senator, Georgia", ["dem_mainstream", "pew_mainstays", "dem_progressive"], "G- VOTING- RELIGION0")
add("polis", "Jared Polis", "D", "Governor, Colorado", ["abundance", "dem_mainstream", "neoliberal"], "G- TRADE- LIBERTY- HOUSING- TECH+")
add("walz", "Tim Walz", "D", "Governor, Minnesota", ["dem_mainstream", "dem_progressive", "pew_estlib"], "G- SOCINS- MORAL-")
add("raskin", "Jamie Raskin", "D", "Representative, Maryland", ["dem_mainstream", "dem_progressive", "pew_estlib"], "G- NORMS- VOTING- RELIGION-")
add("schiff", "Adam Schiff", "D", "Senator, California", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- NORMS- HAWK+")
add("golden", "Jared Golden", "D", "Representative, Maine", ["blue_dog", "pew_mainstays", "centrist"], "G0 GUNS+ TRADE+")
add("cuellar", "Henry Cuellar", "D", "Representative, Texas", ["blue_dog", "pew_mainstays", "centrist"], "G0 MORAL+ IMMIG0")
add("mgp", "Marie Gluesenkamp Perez", "D", "Representative, Washington", ["blue_dog", "pew_mainstays", "centrist"], "G0 POP+ TECH-")
add("gottheimer", "Josh Gottheimer", "D", "Representative, New Jersey", ["blue_dog", "dem_mainstream", "dem_new"], "G- REDIS0 HAWK+")
add("torres", "Ritchie Torres", "D", "Representative, New York", ["dem_mainstream", "blue_dog", "pew_mainstays"], "G- HAWK+ HOUSING-")
add("kelly", "Mark Kelly", "D", "Senator, Arizona", ["dem_mainstream", "blue_dog", "pres_biden"], "G- GUNS- IMMIG0")
add("gallego", "Ruben Gallego", "D", "Senator, Arizona", ["dem_mainstream", "blue_dog", "pew_mainstays"], "G- IMMIG0")
add("vanhollen", "Chris Van Hollen", "D", "Senator, Maryland", ["dem_mainstream", "dem_progressive", "pew_estlib"], "G- HAWK-")
add("whitehouse", "Sheldon Whitehouse", "D", "Senator, Rhode Island", ["dem_mainstream", "pew_estlib", "dem_progressive"], "G- ENV-")
add("clyburn", "Jim Clyburn", "D", "Representative, South Carolina", ["dem_mainstream", "pew_mainstays", "pres_biden"], "G- EQUITY- RELIGION0")
add("cuomo", "Andrew Cuomo", "D", "Former Governor, New York", ["dem_mainstream", "blue_dog", "dem_new"], "G- GUNS- ORDER0")
add("adams", "Eric Adams", "D", "Mayor, New York City", ["blue_dog", "pew_mainstays", "centrist"], "G0 ORDER+ RELIGION+")
add("mamdani", "Zohran Mamdani", "D", "Mayor-elect, New York City (DSA)", ["dem_socialist", "pew_progressive", "dem_progressive"], "G- REDIS- ORDER- POP+")
add("bjohnson", "Brandon Johnson", "D", "Mayor, Chicago", ["dem_socialist", "dem_progressive", "pew_progressive"], "G- ORDER- EDUC-")
add("gore", "Al Gore", "D", "Vice President 1993–2001", ["dem_mainstream", "pres_clinton", "pew_estlib"], "G- ENV- GLOBAL-")
add("kerry", "John Kerry", "D", "Secretary of State, 2004 nominee", ["dem_mainstream", "pew_estlib", "pres_obama"], "G- GLOBAL- ENV-")
add("bloomberg", "Michael Bloomberg", "D", "Former Mayor, New York City", ["neoliberal", "dem_new", "pew_estlib"], "G0 GUNS- LIBERTY+ TRADE- REDIS0")
add("moore", "Wes Moore", "D", "Governor, Maryland", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- EQUITY-")
add("crockett", "Jasmine Crockett", "D", "Representative, Texas", ["dem_progressive", "dem_mainstream", "pew_progressive"], "G- EQUITY- ORDER-")
add("phillips", "Dean Phillips", "D", "Former Representative, Minnesota", ["dem_new", "blue_dog", "centrist"], "G- ESTAB0")
add("kaine", "Tim Kaine", "D", "Senator, Virginia", ["dem_mainstream", "pew_estlib", "pres_obama"], "G- NORMS-")
add("wyden", "Ron Wyden", "D", "Senator, Oregon", ["dem_mainstream", "civil_libertarian", "pew_estlib"], "G- PRIVACY- TECH0")
add("emanuel", "Rahm Emanuel", "D", "Former Mayor of Chicago, ambassador", ["dem_new", "dem_mainstream", "neoliberal"], "G- EDUC0 ORDER0")
add("williamson", "Marianne Williamson", "D", "2020 and 2024 presidential candidate", ["dem_progressive", "pew_progressive", "dem_socialist"], "G- HAWK-")
add("hochul", "Kathy Hochul", "D", "Governor, New York", ["dem_mainstream", "pew_estlib", "pres_biden"], "G- GUNS-")
add("ossoff", "Jon Ossoff", "D", "Senator, Georgia", ["dem_mainstream", "pew_estlib", "pres_biden"], "G-")
add("spanberger", "Abigail Spanberger", "D", "Former Representative; Virginia governor candidate", ["blue_dog", "dem_mainstream", "pew_mainstays"], "G- HAWK+")
add("mbennet", "Michael Bennet", "D", "Senator, Colorado", ["dem_mainstream", "pew_estlib", "abundance"], "G- EDUC0")

# ---------------- Republicans ----------------
add("trump", "Donald Trump", "R", "President 2017–21, 2025–", ["pres_trump", "maga", "pew_populist"], "G+ TRADE+ IMMIG+ NORMS+ ESTAB+ GLOBAL+")
add("vance", "JD Vance", "R", "Vice President", ["maga", "natcon", "pres_trump"], "G+ TRADE+ HAWK- ESTAB+ REDIS0")
add("pence", "Mike Pence", "R", "Vice President 2017–21", ["religious_right", "gop_establishment", "pres_bush43"], "G+ MORAL+ RELIGION+ TRADE- HAWK+ NORMS-")
add("desantis", "Ron DeSantis", "R", "Governor, Florida", ["freedom_caucus", "gop_current", "maga"], "G+ EDUC+ ESTAB+ IMMIG+")
add("haley", "Nikki Haley", "R", "Former UN ambassador, Governor", ["gop_establishment", "pew_committed", "gop_current"], "G+ HAWK+ GLOBAL- TRADE-")
add("romney", "Mitt Romney", "R", "Former Senator, Utah; 2012 nominee", ["never_trump", "gop_establishment", "pew_committed"], "G+ NORMS- HAWK+ TRADE- POP-")
add("lcheney", "Liz Cheney", "R", "Former Representative, Wyoming", ["never_trump", "gop_establishment", "neoconservatism"], "G+ NORMS- HAWK+")
add("kinzinger", "Adam Kinzinger", "R", "Former Representative, Illinois", ["never_trump", "gop_establishment", "neoconservatism"], "G+ NORMS- HAWK+ ESTAB-")
add("gwbush", "George W. Bush", "R", "President 2001–09", ["pres_bush43", "gop_establishment", "neoconservatism"], "G+ HAWK+ PRIVACY+ RELIGION+ TRADE-")
add("dcheney", "Dick Cheney", "R", "Vice President 2001–09", ["neoconservatism", "pres_bush43", "gop_establishment"], "G+ HAWK+ PRIVACY+ NORMS+")
add("mccain", "John McCain", "R", "Senator, Arizona; 2008 nominee", ["gop_establishment", "neoconservatism", "never_trump"], "G+ HAWK+ IMMIG0 TRADE-")
add("mcconnell", "Mitch McConnell", "R", "Senator, Kentucky; former leader", ["gop_establishment", "pew_committed", "gop_current"], "G+ HAWK+ TRADE- SPEECH-")
add("cruz", "Ted Cruz", "R", "Senator, Texas", ["freedom_caucus", "gop_current", "tea_party"], "G+ REDIS+ RELIGION+ IMMIG+")
add("rubio", "Marco Rubio", "R", "Secretary of State", ["gop_current", "gop_establishment", "pres_trump"], "G+ HAWK+ MORAL+")
add("rpaul", "Rand Paul", "R", "Senator, Kentucky", ["libertarian", "freedom_caucus", "mises"], "G+ HAWK- PRIVACY- REDIS+ FED+ TRADE-")
add("massie", "Thomas Massie", "R", "Representative, Kentucky", ["libertarian", "mises", "freedom_caucus"], "G+ HAWK- PRIVACY- FED+")
add("hawley", "Josh Hawley", "R", "Senator, Missouri", ["natcon", "postliberal", "maga"], "G+ TECH- TRADE+ REG0 MORAL+")
add("mlee", "Mike Lee", "R", "Senator, Utah", ["freedom_caucus", "tea_party", "libertarian"], "G+ FED+ REDIS+")
add("cotton", "Tom Cotton", "R", "Senator, Arkansas", ["gop_current", "neoconservatism", "freedom_caucus"], "G+ HAWK+ ORDER+ IMMIG+")
add("graham", "Lindsey Graham", "R", "Senator, South Carolina", ["gop_current", "neoconservatism", "gop_establishment"], "G+ HAWK+")
add("collins", "Susan Collins", "R", "Senator, Maine", ["rockefeller", "centrist", "gop_establishment"], "G0 MORAL- GENDERID0 NORMS-")
add("murkowski", "Lisa Murkowski", "R", "Senator, Alaska", ["rockefeller", "centrist", "never_trump"], "G0 MORAL- NORMS-")
add("mtg", "Marjorie Taylor Greene", "R", "Representative, Georgia", ["maga", "freedom_caucus", "pew_faithflag"], "G+ ESTAB+ POP+ HAWK- GENDERID+")
add("gaetz", "Matt Gaetz", "R", "Former Representative, Florida", ["maga", "freedom_caucus", "pew_populist"], "G+ ESTAB+ HAWK- LIBERTY-")
add("boebert", "Lauren Boebert", "R", "Representative, Colorado", ["freedom_caucus", "maga", "pew_faithflag"], "G+ GUNS+ RELIGION+")
add("jordan", "Jim Jordan", "R", "Representative, Ohio", ["freedom_caucus", "maga", "tea_party"], "G+ ESTAB+ REDIS+")
add("mjohnson", "Mike Johnson", "R", "Speaker of the House", ["religious_right", "freedom_caucus", "gop_current"], "G+ RELIGION+ MORAL+")
add("mccarthy", "Kevin McCarthy", "R", "Former Speaker of the House", ["gop_current", "gop_establishment", "pew_committed"], "G+")
add("stefanik", "Elise Stefanik", "R", "Representative, New York", ["gop_current", "maga", "pres_trump"], "G+ IMMIG+")
add("donalds", "Byron Donalds", "R", "Representative, Florida", ["freedom_caucus", "gop_current", "maga"], "G+ EDUC+ EQUITY+")
add("ramaswamy", "Vivek Ramaswamy", "R", "Businessman; Ohio governor candidate", ["maga", "tech_right", "freedom_caucus"], "G+ ESTAB+ EQUITY+ ENV+")
add("christie", "Chris Christie", "R", "Former Governor, New Jersey", ["gop_establishment", "never_trump", "pew_committed"], "G+ HAWK+ NORMS-")
add("abbott", "Greg Abbott", "R", "Governor, Texas", ["gop_current", "maga", "freedom_caucus"], "G+ IMMIG+ GUNS+")
add("kemp", "Brian Kemp", "R", "Governor, Georgia", ["gop_current", "pew_committed", "gop_establishment"], "G+ NORMS0 MORAL+")
add("youngkin", "Glenn Youngkin", "R", "Governor, Virginia", ["gop_current", "pew_committed", "gop_establishment"], "G+ EDUC+")
add("hsanders", "Sarah Huckabee Sanders", "R", "Governor, Arkansas", ["gop_current", "maga", "pew_faithflag"], "G+ EDUC+ GENDERID+")
add("noem", "Kristi Noem", "R", "Homeland Security Secretary", ["maga", "gop_current", "pew_faithflag"], "G+ IMMIG+")
add("tscott", "Tim Scott", "R", "Senator, South Carolina", ["gop_current", "pew_committed", "religious_right"], "G+ EQUITY+ EDUC+")
add("tuberville", "Tommy Tuberville", "R", "Senator, Alabama", ["maga", "freedom_caucus", "pew_faithflag"], "G+ MORAL+ GENDERID+")
add("thune", "John Thune", "R", "Senate Majority Leader", ["gop_current", "gop_establishment", "pew_committed"], "G+ REDIS+")
add("roy", "Chip Roy", "R", "Representative, Texas", ["freedom_caucus", "tea_party", "pew_faithflag"], "G+ REDIS+ IMMIG+")
add("ryan", "Paul Ryan", "R", "Former Speaker of the House", ["gop_establishment", "pew_committed", "gop_reagan"], "G+ REDIS+ SOCINS+ TRADE- IMMIG0")
add("gingrich_p", "Newt Gingrich", "R", "Former Speaker of the House", ["gingrich", "gop_current", "pew_committed"], "G+ ORDER+")
add("huckabee", "Mike Huckabee", "R", "Former Governor, Arkansas; ambassador to Israel", ["religious_right", "pew_faithflag", "gop_current"], "G+ RELIGION+ MORAL+ HAWK+")
add("santorum", "Rick Santorum", "R", "Former Senator, Pennsylvania", ["religious_right", "postliberal", "pew_faithflag"], "G+ MORAL+ FAMILY+")
add("cox", "Spencer Cox", "R", "Governor, Utah", ["gop_establishment", "centrist", "christian_democracy"], "G+ NORMS- POP-")
add("pscott", "Phil Scott", "R", "Governor, Vermont", ["rockefeller", "centrist", "blue_dog"], "G0 MORAL- NORMS-")
add("hogan", "Larry Hogan", "R", "Former Governor, Maryland", ["rockefeller", "never_trump", "centrist"], "G0 NORMS-")
add("sununu", "Chris Sununu", "R", "Former Governor, New Hampshire", ["rockefeller", "gop_establishment", "centrist"], "G+ MORAL0")
add("cassidy", "Bill Cassidy", "R", "Senator, Louisiana", ["gop_establishment", "gop_current", "pew_committed"], "G+ ESTAB0")
add("rscott", "Rick Scott", "R", "Senator, Florida", ["gop_current", "freedom_caucus", "pew_committed"], "G+ REDIS+")
add("burgum", "Doug Burgum", "R", "Interior Secretary", ["gop_current", "pew_committed", "tech_right"], "G+ ENV+")
add("lake", "Kari Lake", "R", "Former Arizona candidate; media official", ["maga", "pew_populist", "freedom_caucus"], "G+ VOTING+ ESTAB+")
add("rpaul_sr", "Ron Paul", "R", "Former Representative, Texas", ["libertarian", "mises", "paleoconservatism"], "G+ HAWK- FED+ LIBERTY- GLOBAL+")
add("pompeo", "Mike Pompeo", "R", "Former Secretary of State", ["gop_current", "neoconservatism", "religious_right"], "G+ HAWK+")
add("hegseth", "Pete Hegseth", "R", "Defense Secretary", ["maga", "pew_faithflag", "freedom_caucus"], "G+ GENDERID+ ESTAB+")
add("carson", "Ben Carson", "R", "Former HUD Secretary", ["religious_right", "pew_faithflag", "gop_current"], "G+ RELIGION+")
add("jindal", "Bobby Jindal", "R", "Former Governor, Louisiana", ["gop_current", "religious_right", "pew_committed"], "G+ EDUC+")
add("bannon", "Steve Bannon", "R", "Former White House strategist", ["natcon", "maga", "paleoconservatism"], "G+ TRADE+ HAWK- ESTAB+ POP+")
add("gabbard", "Tulsi Gabbard", "R", "Director of National Intelligence (former Democrat)", ["maga", "pew_populist", "natcon"], "HAWK- ESTAB+")
add("rfk", "Robert F. Kennedy Jr.", "I", "HHS Secretary (former independent candidate)", ["pew_sideliners", "pew_outsider", "maga"], "ESTAB+ POP+ HAWK0")
add("schwarzenegger", "Arnold Schwarzenegger", "R", "Former Governor, California", ["rockefeller", "centrist", "never_trump"], "G0 ENV- NORMS-")
add("kasich", "John Kasich", "R", "Former Governor, Ohio", ["rockefeller", "gop_establishment", "never_trump"], "G+ NORMS- SOCINS0")
add("jeb", "Jeb Bush", "R", "Former Governor, Florida", ["gop_establishment", "pres_bush43", "pew_committed"], "G+ EDUC+ IMMIG0 TRADE-")
add("hutchinson", "Asa Hutchinson", "R", "Former Governor, Arkansas", ["gop_establishment", "never_trump", "pew_committed"], "G+ NORMS-")

# ---------------- Third parties and independents ----------------
add("stein", "Jill Stein", "G", "Green Party nominee 2012, 2016, 2024", ["green", "ecosocialism", "dem_socialist"], "G- ENV- HAWK- POP+")
add("gjohnson", "Gary Johnson", "L", "Libertarian nominee 2012, 2016", ["libertarian", "classical_liberal", "neoliberal"], "MORAL- LIBERTY- REDIS+ HAWK- TRADE-")
add("amash", "Justin Amash", "L", "Former Representative, Michigan", ["libertarian", "classical_liberal", "mises"], "LIBERTY- PRIVACY- HAWK- NORMS- TRADE-")
add("nader", "Ralph Nader", "G", "Consumer advocate, Green/independent candidate", ["green", "dem_socialist", "pew_outsider"], "REG- POP+ TRADE+ HAWK-")
add("aking", "Angus King", "I", "Senator, Maine", ["dem_mainstream", "centrist", "pew_estlib"], "G- NORMS-")
add("yang", "Andrew Yang", "I", "Forward Party co-founder", ["centrist", "abundance", "pew_outsider"], "REDIS- TECH- VOTING-")
add("chase_oliver", "Chase Oliver", "L", "Libertarian nominee 2024", ["libertarian", "classical_liberal", "civil_libertarian"], "LIBERTY- PRIVACY- HAWK- IMMIG- ORDER-")
add("cornel_west", "Cornel West", "I", "2024 independent candidate", ["dem_socialist", "pew_progressive", "ecosocialism"], "G- REDIS- HAWK- POP+")

# Within-party orderings on the overall score (a should be left of b)
ORDER = [
    ("aoc", "biden"), ("sanders", "biden"), ("biden", "manchin"), ("warren", "klobuchar"),
    ("tlaib", "gottheimer"), ("pressley", "golden"), ("jayapal", "cuellar"), ("schumer", "manchin"),
    ("collins", "mcconnell"), ("mcconnell", "mtg"), ("murkowski", "cruz"), ("romney", "jordan"),
    ("pscott", "desantis"), ("hogan", "boebert"), ("kasich", "roy"), ("cox", "tuberville"),
    ("manchin", "collins"), ("biden", "romney"), ("stein", "biden"), ("mamdani", "adams"),
]

if __name__ == "__main__":
    import collections
    print(len(R), collections.Counter(r["party"] for r in R))
    ids = [r["id"] for r in R]
    assert len(ids) == len(set(ids))
