"""Race and equity."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["gap_cause_wealth"] = [
    S("The Black–white wealth gap is mostly caused by discrimination that continues today.",
      means=["Bias in hiring, pay, lending and housing today explains most of the gap"]),
    S("The gap is mostly the lasting effect of past discrimination, like slavery and segregation.",
      means=["Wealth that Black families were barred from building generations ago explains most of the gap"]),
    S("The gap comes from a mix of past discrimination and differences in choices, families and culture.",
      means=["History and present-day choices both matter about equally"]),
    S("The gap is mostly differences in choices, families and culture, not discrimination.",
      means=["Things like saving, marriage rates and family structure explain most of the gap"]),
]

T["gap_cause_arrests"] = [
    S("Higher arrest rates for Black Americans mostly reflect bias in policing and courts.",
      means=["Police stop, search and arrest Black people more for the same behavior"]),
    S("Higher arrest rates reflect bias and differences in crime rates about equally.",
      means=["Both biased policing and more crime in some areas matter"]),
    S("Higher arrest rates mostly reflect higher crime rates driven by poverty and neighborhood conditions.",
      means=["Poor, high-crime neighborhoods explain most of the gap, more than police bias"]),
    S("Higher arrest rates mostly reflect higher crime rates driven by family and culture.",
      means=["Family structure and culture explain most of the gap, more than police bias or poverty"]),
]

T["gap_cause_tests"] = [
    S("Racial gaps in test scores mostly reflect biased tests.",
      means=["The tests measure background more than ability or learning"]),
    S("Racial gaps in test scores mostly reflect unequal schools and resources.",
      means=["Underfunded schools, weaker teachers and fewer resources explain most of the gap"]),
    S("Racial gaps in test scores mostly reflect family income and neighborhood conditions.",
      means=["Poverty and the neighborhoods children grow up in explain most of the gap"]),
    S("Racial gaps in test scores mostly reflect family structure and culture.",
      means=["Differences in family life and attitudes toward school explain most of the gap"]),
]

T["hiring_race"] = [
    S("Employers should consider race as one important factor among qualified applicants, to increase diversity.",
      yes=["Weighing race meaningfully in hiring decisions"],
      no=["Race-blind hiring"]),
    S("Employers should use race only as a tie-breaker between equally qualified applicants.",
      yes=["Race as a tie-breaker"],
      no=["Race as a major factor", "Ignoring race entirely"]),
    S("Employers shouldn't consider race, but should recruit in many different communities.",
      yes=["Outreach to a wide range of communities", "Race-blind decisions"],
      no=["Using race in hiring decisions"]),
    S("Race should play no part in hiring at all.",
      yes=["Race-blind hiring and recruiting"],
      no=["Race-based outreach or preferences"]),
]

T["contract_set_asides"] = [
    S("Government should set aside a share of contracts for minority-owned businesses.",
      yes=["Set percentages of contracts for minority-owned firms"],
      no=["Race-neutral contracting only"]),
    S("No racial set-asides, but help small or disadvantaged businesses of any race.",
      yes=["Programs for small or low-income-owned firms of any race"],
      no=["Racial set-asides", "No help for small firms"]),
    S("No special contracting programs for any group.",
      yes=["Awarding contracts on bids alone"],
      no=["Set-asides by race or business size"]),
]

T["workplace_diversity"] = [
    S("Large employers should have racial diversity programs with hiring targets and required training.",
      yes=["Racial hiring targets", "Required diversity training"],
      no=["Leaving it to each company"]),
    S("Large employers should do outreach and mentoring for minorities, without targets.",
      yes=["Recruiting and mentoring programs"],
      no=["Hiring targets", "No programs"]),
    S("Large employers should run only general training on treating everyone equally.",
      yes=["Equal-treatment training for all"],
      no=["Programs aimed at particular races"]),
    S("No such programs, but leave the choice to each company.",
      yes=["Letting companies decide"],
      no=["Required programs", "Government bans"]),
    S("No such programs, and government should bar them at federal contractors.",
      yes=["Barring race-targeted programs at companies with federal contracts"],
      no=["Programs aimed at hiring or promoting minorities"]),
]

T["dei_offices"] = [
    S("Public universities should keep and expand diversity, equity and inclusion offices.",
      yes=["More DEI staff and programs at public universities"],
      no=["Closing DEI offices"]),
    S("Keep DEI offices, but focus them on equal treatment for everyone.",
      yes=["Offices that serve all students rather than particular groups"],
      no=["Expanding group-focused programs", "Closing the offices"]),
    S("Public universities should close DEI offices.",
      yes=["State laws closing DEI offices, as Texas and Florida have done"],
      no=["Keeping DEI offices"]),
]

T["reparations"] = [
    S("The federal government should make cash reparations payments to descendants of enslaved people.",
      yes=["Cash payments to each eligible Black American descended from enslaved people"],
      no=["An apology or study alone"]),
    S("Reparations should come as programs like housing, education and business grants rather than cash.",
      yes=["Targeted grants for housing, education and business"],
      no=["Cash payments", "No reparations"]),
    S("No reparations payments, but a formal apology and an official study.",
      yes=["A government apology", "A federal commission to study reparations"],
      no=["Payments or programs"]),
    S("Nothing beyond today's laws.",
      yes=["No reparations, apology or study"],
      no=["Any reparations"]),
]

T["local_redlining_compensation"] = [
    S("Cities that enforced housing segregation should compensate those harmed and their descendants.",
      yes=["Payments to victims and descendants, like Evanston's housing grants"],
      no=["Limiting compensation to living victims"]),
    S("Compensate only people personally harmed who are still living.",
      yes=["Payments to surviving victims"],
      no=["Payments to descendants", "No compensation"]),
    S("Cities shouldn't compensate families for past housing segregation.",
      yes=["No redlining compensation"],
      no=["Payments to victims or descendants"]),
]

C["hate_crime_sentences"] = {
    "why": "'Much longer' and 'somewhat longer' had no scale.",
    "scope": "Crimes like assault or vandalism, compared with the same crime without that motive. “Much longer” means something like double; “somewhat longer” means a modest addition.",
}
T["hate_crime_sentences"] = [
    S("Hate-motivated crimes should carry much longer sentences.",
      yes=["Roughly doubling sentences for crimes motivated by hatred of a group"],
      no=["Treating the motive as irrelevant"]),
    S("Hate-motivated crimes should carry somewhat longer sentences.",
      yes=["Modest sentence increases for hate crimes"],
      no=["Doubling sentences", "No added penalty"]),
    S("Longer sentences for hate crimes against people, not property.",
      yes=["Added time for assaults motivated by hate"],
      no=["Added time for hate-motivated vandalism"]),
    S("Punish the crime the same whatever the motive.",
      yes=["Repealing hate crime sentence enhancements"],
      no=["Longer sentences based on motive"]),
]

T["race_districts"] = [
    S("States should create majority-minority districts whenever a group is large and close together enough.",
      yes=["Required majority-Black or majority-Hispanic districts where possible"],
      no=["Race-blind districting"]),
    S("Create majority-minority districts only where there's evidence of past voting discrimination.",
      yes=["Such districts where discrimination is shown"],
      no=["Requiring such districts everywhere", "Banning such districts"]),
    S("Draw districts without considering race.",
      yes=["Race-blind redistricting"],
      no=["Districts drawn to give a racial group a majority"]),
]

T["teach_racism_history"] = [
    S("Schools should teach racism as central to the American story, including how it shapes society today.",
      yes=["Making slavery and segregation central themes, tied to present-day issues"],
      no=["Treating racism as one chapter among many"]),
    S("Schools should teach racism as an important part of history, alongside the nation's progress.",
      yes=["Teaching slavery and segregation with civil rights gains and other progress"],
      no=["Making it the central story", "Downplaying slavery and segregation"]),
    S("Schools should teach slavery and segregation fully, but not as the defining story of the country.",
      yes=["Full facts of slavery and segregation"],
      no=["Framing American history mainly around racism"]),
]

C["teach_institutional_racism"] = {
    "why": "'Built into laws and institutions' had no examples.",
    "scope": "High school classes. For example, the claim that lending, policing, school funding or hiring practices disadvantage Black Americans today even when no one intends it.",
}
T["teach_institutional_racism"] = [
    S("Schools should teach as established fact that racism is built into US laws and institutions today.",
      yes=["Teaching that lending, policing, school funding and hiring disadvantage Black Americans by design or effect"],
      no=["Presenting it as one view among several"]),
    S("Schools should teach it as one view among several.",
      yes=["Presenting it alongside opposing views"],
      no=["Teaching it as fact", "Banning the topic in schools"]),
    S("Public schools shouldn't teach that racism is built into US institutions today.",
      yes=["State laws keeping it out of public school lessons"],
      no=["Teaching it as fact or as one view"]),
]

T["discrimination_black"] = [
    S("Black job applicants face racial discrimination almost always.", means=["Out of 10 job searches by Black Americans, 9 or more run into discrimination because of race"]),
    S("Black job applicants face racial discrimination most of the time.", means=["Out of 10 job searches by Black Americans, about 7 run into discrimination because of race"]),
    S("Black job applicants face racial discrimination about half the time.", means=["Out of 10 job searches by Black Americans, about 5 run into discrimination because of race"]),
    S("Black job applicants sometimes face racial discrimination.", means=["Out of 10 job searches by Black Americans, about 3 run into discrimination because of race"]),
    S("Black job applicants rarely face racial discrimination.", means=["Out of 10 job searches by Black Americans, 1 or fewer run into discrimination because of race"]),
]
T["discrimination_white"] = [
    S("White applicants rarely face racial discrimination.", means=["Out of 10 job or college applications by white Americans, 1 or fewer run into discrimination because of race"]),
    S("White applicants sometimes face racial discrimination.", means=["Out of 10 job or college applications by white Americans, about 3 run into discrimination because of race"]),
    S("White applicants face racial discrimination about half the time.", means=["Out of 10 job or college applications by white Americans, about 5 run into discrimination because of race"]),
    S("White applicants face racial discrimination most of the time.", means=["Out of 10 job or college applications by white Americans, about 7 run into discrimination because of race"]),
    S("White applicants face racial discrimination almost always.", means=["Out of 10 job or college applications by white Americans, 9 or more run into discrimination because of race"]),
]
T["discrimination_groups"] = existing("D13", "discrimination_groups")

T["tribal_sovereignty"] = [
    S("Tribes should have full self-government, including over non-Native people on tribal land.",
      yes=["Tribal courts and laws applying to everyone on tribal land"],
      no=["State or federal control over tribal lands"]),
    S("Tribes should govern their members, with limited authority over others.",
      yes=["Tribal self-government over members", "Limited tribal power over non-members"],
      no=["Full tribal power over non-members", "More outside control"]),
    S("States and the federal government should have more control over tribal lands than today.",
      yes=["Expanding state and federal authority on reservations"],
      no=["Expanding tribal self-government"]),
]

T["disparate_impact"] = [
    S("Tests or rules that screen out far more of one race should be illegal unless clearly necessary.",
      yes=["Disparate-impact liability for employers, landlords and lenders"],
      no=["Allowing any test without intent to discriminate"]),
    S("They should be illegal only if a fairer test would work as well and the employer refused it.",
      yes=["Liability only when a fair alternative was refused"],
      no=["Broad disparate-impact rules", "Ignoring impact entirely"]),
    S("Only intentional discrimination should be illegal.",
      yes=["Ending disparate-impact liability"],
      no=["Penalizing tests for uneven results alone"]),
]

T["confederate_monuments"] = [
    S("Remove public monuments honoring Confederate leaders.",
      yes=["Taking down Confederate statues and renaming places named for Confederate leaders"],
      no=["Keeping them on public land"]),
    S("Move Confederate monuments to museums with historical context.",
      yes=["Relocating statues to museums"],
      no=["Leaving them in public squares", "Destroying the monuments"]),
    S("Keep Confederate monuments, but add historical context.",
      yes=["Plaques explaining the history"],
      no=["Removing or relocating them"]),
    S("Keep Confederate monuments as they are.",
      yes=["Leaving statues and names unchanged"],
      no=["Removing, moving or adding context to them"]),
]

T["college_admissions_race"] = [
    S("Colleges should consider race as one important factor, to increase diversity.",
      yes=["Race-conscious admissions, overturning the 2023 ruling"],
      no=["Race-blind admissions"]),
    S("Colleges should consider race only as a minor factor, like a tie-breaker.",
      yes=["Race as a tie-breaker"],
      no=["Race as a major factor", "Race-blind admissions"]),
    S("Colleges shouldn't consider race, but can consider economic hardship.",
      yes=["Preferences for low-income applicants of any race"],
      no=["Considering race"]),
    S("Colleges shouldn't consider race or any other group characteristic.",
      yes=["Admissions based only on individual records"],
      no=["Race or group-based preferences of any kind"]),
]

if __name__ == "__main__":
    write("D13", T)
    write_clarity("D13", C)
