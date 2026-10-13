"""Democratic norms and the presidency."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["exec_orders_scope"] = [
    S("When Congress won't act, a president should wait, acting alone only on how the executive branch runs.",
      yes=["Executive orders limited to managing federal agencies"], no=["Presidents making new policy without Congress"]),
    S("A president should act alone only in emergencies.",
      yes=["Unilateral action in true emergencies"], no=["Executive orders to get around Congress in normal times"]),
    S("A president can act alone where existing laws leave room to decide.",
      yes=["Executive orders that use discretion existing laws give"], no=["Orders beyond what laws allow"]),
    S("A president can act alone through executive orders whenever it seems necessary.",
      yes=["Broad use of executive orders when Congress won't act, by any president"], no=["Waiting for Congress"]),
]

T["refuse_to_spend"] = [
    S("A president must spend money as Congress directed.",
      yes=["No delays or refusals to spend approved funds"], no=["Withholding funds Congress approved"]),
    S("A president can briefly delay spending while asking Congress to cancel it, as current law allows.",
      yes=["The 1974 law's 45-day process"], no=["Refusing outright", "Allowing no delay"]),
    S("A president can refuse to spend money on programs the president considers wasteful.",
      yes=["Presidents withholding approved money, for any president"], no=["Requiring presidents to spend as directed"]),
]
T["refuse_to_spend_cases"] = existing("D19", "refuse_to_spend_cases")

T["emergency_duration"] = [
    S("No special emergency powers until Congress votes to approve.",
      yes=["Requiring a vote of Congress before emergency powers start"], no=["Open-ended presidential emergencies"]),
    S("Emergencies should last 30 days, then need Congress's approval.",
      yes=["A 30-day limit without a vote"], no=["Longer emergencies without a vote"]),
    S("Emergencies should last 6 months, then need Congress's approval.",
      yes=["A 6-month limit without a vote"], no=["Open-ended emergencies", "Shorter limits"]),
    S("Emergencies should last as long as the president decides, as today.",
      yes=["Today's open-ended emergency powers"], no=["Time limits on emergencies"]),
]

T["emergency_funding"] = [
    S("A president should never use an emergency to spend money Congress refused.",
      yes=["Keeping spending decisions with Congress"], no=["Emergency declarations to fund rejected projects"]),
    S("Only for a sudden threat, like an attack, until Congress can act.",
      yes=["Short-term emergency spending after an attack"], no=["Using emergencies for projects Congress rejected"]),
    S("A president can declare an emergency to fund projects whenever the need seems urgent.",
      yes=["Emergency spending on projects Congress refused, by any president"], no=["Leaving funding to Congress alone"]),
]
T["emergency_funding_cases"] = existing("D19", "emergency_funding_cases")

T["civil_service"] = [
    S("Career government employees should be protected from firing over policy disagreements.",
      yes=["Civil service protections for scientists and analysts"], no=["Firing staff for disagreeing with the president"]),
    S("Only senior employees who help make policy should be fireable over disagreements.",
      yes=["Fewer protections for senior policy staff"], no=["Firing regular staff over policy"]),
    S("Most federal employees should be fireable at will.",
      yes=["Ending most civil service protections"], no=["Job protections for career staff"]),
]

T["independent_agencies"] = [
    S("Keep independent agencies and make more agencies independent.",
      yes=["Protecting agency leaders from firing over policy", "Adding more independent agencies"], no=["Presidents firing agency heads at will"]),
    S("Keep the independent agencies we have.",
      yes=["Today's protections for the Fed, FTC and similar agencies"], no=["Adding or removing protections"]),
    S("Keep only the Federal Reserve independent.",
      yes=["Letting the president fire leaders of the FTC, SEC and others"], no=["Presidents firing the Fed chair"]),
    S("The president should be able to fire any agency leader.",
      yes=["Ending independence for all agencies, including the Fed"], no=["Agencies shielded from the president"]),
]

T["prosecute_opponents"] = [
    S("A president should never be involved in deciding whom the Justice Department investigates.",
      yes=["Leaving investigations to career prosecutors"], no=["Presidents directing investigations of critics"]),
    S("A president can raise concerns, but career prosecutors decide.",
      yes=["Presidents flagging concerns without ordering investigations"], no=["Presidents ordering investigations"]),
    S("A president can order investigations of specific people the president believes broke the law.",
      yes=["Presidents directing investigations, including of opponents, for any president"], no=["Keeping presidents out of these decisions"]),
]

T["pardon_allies"] = [
    S("Presidents should never pardon family, associates or allies; amend the Constitution to forbid it.",
      yes=["A constitutional ban on self-serving pardons"], no=["Pardons of family or allies"]),
    S("Pardoning family or allies is legal, but presidents should almost never do it.",
      yes=["Keeping the power while strongly discouraging its use"], no=["A ban", "Routine pardons of allies"]),
    S("It's acceptable for a president to pardon family or allies treated unfairly.",
      yes=["Pardons of allies the president believes were treated unfairly"], no=["Limits on these pardons"]),
]

T["accept_results"] = [
    S("A candidate who lost should concede once courts and officials confirm the result.",
      yes=["Conceding after results are confirmed"], no=["Continuing to claim fraud"]),
    S("A candidate can accept the result but keep saying publicly it was stolen.",
      yes=["Accepting the outcome while disputing it in public"], no=["Overturning the result", "Staying quiet about fraud claims"]),
    S("A candidate should keep fighting, including asking legislators to overturn the result.",
      yes=["Pressing legislators to overturn confirmed results"], no=["Conceding the election"]),
    S("A candidate should refuse to accept the result and urge supporters to resist.",
      yes=["Refusing to concede and calling on supporters to resist"], no=["Accepting confirmed results"]),
]

C["checks_vs_action"] = {
    "why": "'Checks' and 'act quickly' had no examples.",
    "scope": "The federal government in general, whichever party is in charge. Checks include Congress approving laws and spending, courts reviewing actions, and the Senate confirming appointments.",
}
T["checks_vs_action"] = trade(
    S("No single leader should be able to act without others agreeing, even if needed changes take years.",
      yes=["Requiring Congress, courts and the Senate to sign off on major moves"], no=["Presidents acting alone to speed things up"]),
    S("An elected leader should be able to act quickly, even with fewer checks on mistakes or abuse.",
      yes=["Presidents acting without waiting for Congress or courts"], no=["Checks that delay what voters chose"]),
    S("You weigh checks and quick action about equally.",
      means=["You'd let leaders act fast in a crisis but keep checks in normal times"]))

C["courts_vs_majority"] = {
    "why": "'Takes away some people's rights' had no examples.",
    "scope": "Laws in general, including ones you like and dislike: for example, popular laws on gun limits, school prayer, policing powers or speech that courts say violate the Constitution.",
}
T["courts_vs_majority"] = trade(
    S("Courts should strike down unconstitutional laws even when most voters support them.",
      yes=["Courts overturning popular laws that violate rights"], no=["Courts deferring to majorities on rights"]),
    S("Courts should rarely overrule laws most voters clearly support, even if some people's rights are limited.",
      yes=["Letting popular laws stand", "Narrower court review"], no=["Courts overturning laws with majority support"]),
    S("You weigh court review and majority rule about equally.",
      means=["You'd want courts to step in only when rights are clearly violated"]))

T["filibuster"] = [
    S("Expand the 60-vote rule to nominations for judges and cabinet posts.",
      yes=["Requiring 60 votes to confirm judges and cabinet members"], no=["Majority-vote confirmations"]),
    S("Keep the 60-vote rule as it is.",
      yes=["Today's filibuster"], no=["Expanding, reforming or ending it"]),
    S("Keep the 60-vote rule, but make senators who block a bill stay and speak on the floor.",
      yes=["A talking filibuster"], no=["Silent filibusters", "Ending the filibuster"]),
    S("End the 60-vote rule for some bills, like voting rights or budget bills.",
      yes=["Majority votes for selected kinds of bills"], no=["Keeping 60 votes for everything"]),
    S("End the 60-vote rule; a simple majority should pass bills.",
      yes=["Abolishing the filibuster, whichever party is in charge"], no=["Requiring 60 votes"]),
]
T["filibuster_cases"] = existing("D19", "filibuster_cases")

T["rule_bending_leader"] = [
    S("It's never acceptable for a president to bend or work around laws, court rulings or official procedures.",
      yes=["Presidents following laws and rulings even when they block their agenda"], no=["Working around rules to deliver for voters"]),
    S("Bending the rules is acceptable only in a real emergency.",
      yes=["Bending rules in true emergencies"], no=["Bending rules to get policies through"]),
    S("Bending the rules is acceptable when they clearly stand in the way of what voters chose.",
      yes=["Working around laws or rulings that block an elected agenda"], no=["Letting rules stop a mandate"]),
    S("The country needs a leader willing to bend the rules.",
      yes=["A president who works around laws, rulings and procedures"], no=["Leaders bound by every rule"]),
]

T["political_violence"] = [
    S("Political violence is never justified in the US today.",
      means=["No cause justifies violence, whoever is in power"]),
    S("Violence is justified only against a government that has seized power illegally.",
      means=["Violence is acceptable only if the constitutional order has been overthrown"]),
    S("Violence is sometimes justified when peaceful methods have failed.",
      means=["After peaceful efforts fail, violence for a political cause can be acceptable"]),
]

T["court_expansion"] = [
    S("Congress should add justices when the party in power wants different rulings.",
      yes=["Adding justices to change the Court's majority, for either party"], no=["Keeping 9 justices"]),
    S("Change the Court's size only as part of a bipartisan reform.",
      yes=["Bipartisan changes to the Court"], no=["One party adding justices on its own"]),
    S("Keep the Supreme Court at 9 justices.",
      yes=["Keeping 9 justices"], no=["Adding justices"]),
]

T["presidential_immunity"] = [
    S("Former presidents can be prosecuted like anyone else.",
      yes=["Overturning broad presidential immunity"], no=["Immunity for official acts"]),
    S("Former presidents are immune only for core constitutional duties.",
      yes=["Immunity for duties like pardons and commanding the military only"], no=["Immunity for all official acts"]),
    S("Former presidents are immune for all official acts.",
      yes=["The 2024 ruling's broad immunity"], no=["Prosecuting former presidents for official acts"]),
]

T["press_retaliation"] = [
    S("A president should never punish news outlets for their coverage.",
      yes=["Protecting outlets' licenses and press access regardless of coverage"], no=["Pulling access or licenses over coverage"]),
    S("A president can limit outlets' access to events like briefings, not licenses.",
      yes=["Restricting access to briefings"], no=["Pulling broadcast licenses"]),
    S("A president can punish outlets the president believes spread falsehoods.",
      yes=["Pulling licenses or access from outlets, for any president"], no=["Protecting outlets from presidential punishment"]),
]

T["agency_deference"] = [
    S("Courts should usually defer to agency experts when a law is unclear.",
      yes=["Restoring deference to agencies"], no=["Judges deciding unclear laws themselves"]),
    S("Courts should defer to agencies only on technical or scientific questions.",
      yes=["Deference on scientific and technical matters"], no=["Deference on all questions", "No deference"]),
    S("Judges should decide what unclear laws mean themselves.",
      yes=["The 2024 ruling ending deference"], no=["Courts deferring to agencies"]),
]

T["president_court_ruling"] = [
    S("A president should comply fully with a court ruling while appealing, and avoid attacking the judge.",
      yes=["Complying and appealing quietly"], no=["Attacking judges", "Ignoring rulings"]),
    S("A president should comply while appealing, but can criticize the judge publicly.",
      yes=["Complying while criticizing the judge"], no=["Ignoring rulings"]),
    S("A president should comply only if a higher court agrees.",
      yes=["Waiting for appeals before complying"], no=["Complying with lower court rulings"]),
    S("A president can ignore a ruling the president believes is wrong.",
      yes=["Presidents disregarding court rulings, for any president"], no=["Requiring compliance with rulings"]),
]

if __name__ == "__main__":
    write("D19", T)
    write_clarity("D19", C)
