"""Starting-point groups for answering. Each topic file (sim/answers/Dxx.txt) gives one
answer template per group; every politician starts from their group's template
and then gets individual overrides wherever their own record differs. A politician
can also be moved to a different group for a single topic (for example a
pro-gun Democrat on guns)."""

GROUPS = {
    "DL": "Progressive / democratic-socialist Democrats",
    "DS": "Left third parties (Green, independent left)",
    "DM": "Mainstream Democrats",
    "DC": "Centrist and Blue Dog Democrats",
    "RM": "Moderate Republicans",
    "RE": "Establishment Republicans",
    "RT": "Trump / MAGA Republicans",
    "RF": "Freedom Caucus / Tea Party Republicans",
    "RR": "Religious-right Republicans",
    "LB": "Libertarians",
    "PO": "Heterodox populists",
}

G = {}
for g, ids in {
    "DL": "sanders aoc omar tlaib pressley jayapal khanna mamdani bjohnson williamson crockett warren",
    "DS": "stein nader cornel_west",
    "DM": "biden harris obama hclinton schumer pelosi jeffries klobuchar buttigieg newsom shapiro whitmer pritzker beshear booker cmurphy fetterman warnock polis walz raskin schiff torres kelly gallego vanhollen whitehouse clyburn cuomo gore kerry bloomberg moore phillips kaine wyden emanuel hochul ossoff spanberger mbennet aking",
    "DC": "manchin sinema tester golden cuellar mgp gottheimer adams bclinton",
    "RM": "collins murkowski pscott hogan schwarzenegger sununu cox kasich",
    "RE": "romney lcheney kinzinger gwbush dcheney mccain mcconnell thune haley ryan christie jeb hutchinson cassidy pompeo graham rubio kemp youngkin mccarthy tscott burgum jindal gingrich_p cotton",
    "RT": "trump vance hawley ramaswamy stefanik noem abbott hsanders hegseth lake bannon tuberville gaetz mtg",
    "RF": "cruz mlee jordan roy donalds rscott desantis boebert",
    "RR": "pence huckabee santorum mjohnson carson",
    "LB": "rpaul massie rpaul_sr gjohnson amash chase_oliver",
    "PO": "rfk yang gabbard",
}.items():
    for i in ids.split():
        G[i] = g

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "sim")
    from roster import R
    missing = [r["id"] for r in R if r["id"] not in G]
    extra = [i for i in G if i not in {r["id"] for r in R}]
    print("missing", missing, "extra", extra, len(G))
