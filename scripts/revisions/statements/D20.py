"""Elections and voting."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["voter_id"] = [
    S("No photo ID to vote; signature checks and other methods are enough.",
      yes=["Voting with signature checks or non-photo ID"], no=["Photo ID requirements"]),
    S("Photo ID, but with many accepted IDs, free IDs and a backup option for people without one.",
      yes=["Broad ID lists, free IDs and sworn statements as backup"], no=["Strict ID with no backup", "No ID at all"]),
    S("Photo ID, with free IDs for anyone, but no backup option.",
      yes=["Required photo ID with free IDs"], no=["Backup options for people without ID"]),
    S("Government-issued photo ID with no backup option.",
      yes=["Strict government photo ID to vote"], no=["Student IDs, backups or signature checks instead"]),
]

T["proof_of_citizenship"] = [
    S("A sworn statement and existing checks are enough proof of citizenship to register.",
      yes=["Today's sworn statement"], no=["Requiring passports or birth certificates"]),
    S("Require citizenship documents only when government records can't confirm it.",
      yes=["Document checks when records fall short"], no=["Requiring documents from everyone"]),
    S("Everyone registering should show a passport, birth certificate or similar document.",
      yes=["Documentary proof of citizenship for every registrant"], no=["Registering on a sworn statement"]),
]

T["mail_voting"] = [
    S("Every voter should get a mail ballot automatically.",
      yes=["All-mail elections, as in Colorado and Washington"], no=["Limits on mail voting"]),
    S("Any voter who asks should be able to vote by mail.",
      yes=["No-excuse absentee voting"], no=["Mailing ballots to everyone", "Requiring an excuse"]),
    S("Only voters with a reason, like illness or travel, should vote by mail.",
      yes=["Excuse-required absentee voting"], no=["No-excuse mail voting"]),
    S("Almost no one should vote by mail; vote in person.",
      yes=["In-person voting with rare exceptions"], no=["Widespread mail voting"]),
]

T["mail_ballot_deadline"] = [
    S("Count mail ballots postmarked by Election Day that arrive within a week or more.",
      yes=["A grace period of a week or longer"], no=["Election Day receipt deadlines"]),
    S("Count postmarked mail ballots that arrive within 3 days.",
      yes=["A 3-day grace period"], no=["Longer grace periods", "No grace period"]),
    S("Count only mail ballots received by Election Day.",
      yes=["Election Day receipt deadlines"], no=["Counting ballots that arrive later"]),
]

T["auto_registration"] = [
    S("Register eligible citizens automatically at agencies like the DMV, unless they opt out.",
      yes=["Automatic voter registration"], no=["Requiring people to sign up themselves"]),
    S("Offer registration at agencies, but people must choose to sign up.",
      yes=["Opt-in registration at the DMV"], no=["Automatic registration"]),
    S("People should register to vote on their own.",
      yes=["Ending registration at government agencies"], no=["Automatic or agency registration"]),
]

T["felony_voting"] = [
    S("People with felony convictions should always be able to vote, even in prison.",
      yes=["Voting from prison, as in Maine and Vermont"], no=["Taking away voting rights for felonies"]),
    S("People with felony convictions should vote once released from prison.",
      yes=["Restoring the vote on release"], no=["Voting from prison", "Waiting until parole ends"]),
    S("People with felony convictions should vote after finishing parole or probation.",
      yes=["Restoring the vote after the full sentence"], no=["Restoring it on release"]),
    S("Voting rights only after a waiting period or individual review.",
      yes=["Case-by-case restoration"], no=["Automatic restoration"]),
    S("People convicted of a felony should never vote again.",
      yes=["Permanent loss of voting rights"], no=["Restoring voting rights"]),
]

T["electoral_college"] = [
    S("Elect the president by national popular vote, ending the Electoral College.",
      yes=["A national popular vote"], no=["The Electoral College"]),
    S("Keep the Electoral College, but split each state's votes by its vote share.",
      yes=["Proportional allocation of electoral votes"], no=["Winner-take-all states", "A national popular vote"]),
    S("Keep the Electoral College as it is.",
      yes=["Today's winner-take-all Electoral College"], no=["A national popular vote"]),
]

T["popular_vote_loser"] = [
    S("Winning the presidency while losing the national vote should be impossible.",
      yes=["Changing the system so the vote winner always wins"], no=["Today's system as it stands"]),
    S("It's acceptable, but the system should change to make it rarer.",
      yes=["Reforms that make it less likely"], no=["Abolishing state-based selection"]),
    S("It's acceptable; it reflects the role of states in choosing the president.",
      yes=["Keeping the state-based system"], no=["Changing the system to prevent it"]),
]

T["redistricting"] = [
    S("Independent commissions with no politicians should draw congressional districts.",
      yes=["Independent redistricting commissions"], no=["Legislatures drawing their own maps"]),
    S("Commissions with equal members from both parties should draw districts.",
      yes=["Bipartisan commissions"], no=["Legislatures drawing maps"]),
    S("State legislatures should draw districts once every 10 years after the census.",
      yes=["Legislative maps once a decade"], no=["Redistricting commissions", "Mid-decade redrawing"]),
    S("State legislatures should draw districts whenever they choose, including mid-decade.",
      yes=["Mid-decade redistricting by legislatures, for either party"], no=["Limits on when maps are redrawn"]),
]

T["campaign_spending"] = [
    S("Strict limits on election spending by corporations, unions and the wealthy, with a constitutional amendment if needed.",
      yes=["Overturning Citizens United", "Limits on outside spending"], no=["Unlimited outside spending"]),
    S("No spending limits, but full disclosure of who pays for political ads.",
      yes=["Disclosure of donors behind political ads"], no=["Spending limits", "Anonymous spending"]),
    S("No limits or disclosure rules; spending on politics is free speech.",
      yes=["Unlimited and anonymous political spending"], no=["Limits or disclosure rules"]),
]

T["public_financing"] = [
    S("Candidates who accept spending limits should get public money matching small donations several times over.",
      yes=["Multiple matching of small donations"], no=["No public financing"]),
    S("Candidates who accept limits should get a modest amount of public money.",
      yes=["Modest public financing"], no=["Large matching programs", "No public money"]),
    S("No public money for campaigns.",
      yes=["Ending public campaign financing"], no=["Any taxpayer money for campaigns"]),
]

T["congress_term_limits"] = [
    S("Members of Congress should be limited to 12 years or less.", yes=["Term limits of 12 years or less"], no=["Unlimited terms"]),
    S("Members of Congress should be limited to about 18 to 24 years.", yes=["Long term limits"], no=["Short limits", "Unlimited terms"]),
    S("No term limits for Congress; voters can remove members.", yes=["Unlimited terms"], no=["Congressional term limits"]),
]

T["court_term_limits"] = [
    S("Future Supreme Court justices should serve 18-year terms.", yes=["18-year terms"], no=["Life tenure"]),
    S("Future justices should serve fixed terms of about 25 years.", yes=["Terms of about 25 years"], no=["18-year terms", "Life tenure"]),
    S("Keep life terms for Supreme Court justices.", yes=["Life tenure"], no=["Term limits for justices"]),
]

T["ranked_choice"] = [
    S("All elections should use ranked-choice voting.", yes=["Ranked-choice voting everywhere"], no=["Banning ranked-choice voting"]),
    S("Each state or city should decide on ranked-choice voting.", yes=["Letting each place choose its voting method"], no=["Requiring ranked-choice everywhere", "Banning ranked-choice voting"]),
    S("Ban ranked-choice voting.", yes=["State bans on ranked-choice voting"], no=["Ranked-choice elections"]),
]
T["statehood"] = existing("D20", "statehood")

T["voting_age"] = [
    S("The voting age should be 16.", yes=["Lowering the voting age to 16"], no=["Keeping it at 18"]),
    S("17-year-olds should vote if they'll be 18 by the next general election.", yes=["Letting 17-year-olds vote in primaries"], no=["Lowering it to 16"]),
    S("The voting age should stay 18.", yes=["Today's voting age"], no=["Lowering or raising it"]),
    S("The voting age should be 21.", yes=["Raising the voting age to 21"], no=["Voting at 18"]),
]

T["noncitizen_local_voting"] = [
    S("Legal permanent residents should vote in local elections like school board races.",
      yes=["Noncitizen voting in local elections"], no=["Bans on noncitizen local voting"]),
    S("Each city should decide whether green card holders vote locally.",
      yes=["Letting each city decide"], no=["State bans on noncitizen voting", "Requiring cities to allow it"]),
    S("Ban noncitizen voting in local elections everywhere.",
      yes=["Citizens-only voting at every level"], no=["Noncitizens voting locally"]),
]

if __name__ == "__main__":
    write("D20", T)
    write_clarity("D20", C)
