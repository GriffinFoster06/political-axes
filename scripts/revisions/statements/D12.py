"""Family and gender roles."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, write, write_clarity  # noqa: E402

C, T = {}, {}

T["work_arrangement"] = [
    S("For a married couple with young children, both parents working full time and sharing childcare is usually best.",
      means=["Two full-time jobs plus shared childcare or daycare beats having a parent at home"]),
    S("Both parents working, with one part time, is usually best.",
      means=["One parent cuts back hours while children are young, but neither stops working"]),
    S("One parent staying home while the children are young is usually best.",
      means=["Even when two incomes are affordable, a parent at home full time is better for young children"]),
]

T["caregiver_parent"] = [
    S("Which parent stays home should depend on who wants to or who earns less, not on sex.",
      means=["A father staying home is just as good as a mother doing it"]),
    S("Usually the mother should stay home, but either is fine.",
      means=["Mothers are a slightly better default, though fathers can do it well"]),
    S("The mother should stay home; young children need their mother.",
      means=["A father at home isn't an equal substitute for a mother at home"]),
]

T["marriage_decisions"] = [
    S("Major family decisions should be made equally by both spouses.",
      means=["Neither spouse gets the final say on where to live or big spending"]),
    S("Major decisions are equal, but each spouse leads in different areas.",
      means=["Spouses divide up who takes the lead on, say, money, the house or the children"]),
    S("The husband should have the final say on major family decisions.",
      means=["When spouses disagree on where to live or big spending, the husband decides"]),
]

T["promote_marriage"] = [
    S("Government shouldn't favor married people over unmarried people.",
      yes=["Treating married and unmarried people alike in taxes and benefits"],
      no=["Marriage bonuses or pro-marriage campaigns"]),
    S("Government should only remove tax and benefit rules that penalize marriage.",
      yes=["Fixing marriage penalties in taxes and aid"],
      no=["Active bonuses for marrying", "Leaving penalties in place"]),
    S("Government should actively encourage marriage.",
      yes=["Bonuses or tax breaks for married couples", "Public campaigns promoting marriage"],
      no=["Treating marriage as a private matter"]),
]

T["unmarried_partner_rights"] = [
    S("Unmarried couples who live together should have the same legal rights as married couples.",
      yes=["Inheritance, hospital visits and similar rights for cohabiting couples"],
      no=["Reserving those rights for marriage"]),
    S("Unmarried couples should get some rights after living together several years.",
      yes=["Limited rights after years together"],
      no=["Equal rights right away", "No rights without marriage"]),
    S("Those rights should come with marriage.",
      yes=["Reserving inheritance and hospital rights for married couples"],
      no=["Granting them to unmarried partners"]),
]

T["childcare_spending"] = [
    S("Government should make childcare free for every family with children under 5.",
      yes=["Free childcare for all families, whatever their income"],
      no=["Help for low-income families only"]),
    S("No family should pay more than about 7% of its income for childcare.",
      yes=["Subsidies capping childcare costs at about 7% of income"],
      no=["Free childcare for all", "Help for the poor only"]),
    S("Childcare help should go to low-income families only, as today.",
      yes=["Today's subsidies for low-income families"],
      no=["Help for middle-income families"]),
    S("No government help with childcare costs.",
      yes=["Ending childcare subsidies"],
      no=["Any public childcare aid"]),
]

T["childcare_form"] = [
    S("Help for families with young children should go mainly to childcare programs, so parents can work.",
      yes=["Funding daycare and preschool programs"],
      no=["Cash to parents as the main form of help"]),
    S("Help should be split between childcare programs and cash to parents.",
      yes=["Both childcare funding and cash payments"],
      no=["Putting it all into one or the other"]),
    S("Help should go mainly to parents as cash, whether they use childcare or stay home.",
      yes=["Cash payments that parents spend as they choose"],
      no=["Aid tied to paid childcare"]),
]

T["stay_home_support"] = [
    S("Support should go to childcare so parents can work, not to parents who stay home.",
      yes=["Childcare subsidies for working parents"],
      no=["Equal support for stay-at-home parents"]),
    S("Some support for both, but more for childcare.",
      yes=["Larger childcare subsidies plus some help for stay-at-home parents"],
      no=["Equal support", "Nothing for stay-at-home parents"]),
    S("Parents who stay home should get the same support as parents who pay for childcare.",
      yes=["Equal credits or payments either way"],
      no=["Favoring paid childcare"]),
]

T["no_fault_divorce"] = [
    S("One spouse should be able to divorce without the other's agreement or proof of wrongdoing, as today.",
      yes=["Keeping no-fault divorce"],
      no=["Requiring proof of fault"]),
    S("Keep no-fault divorce, but with a longer waiting period when there are children.",
      yes=["Longer waiting periods for parents"],
      no=["Ending no-fault divorce", "Today's waiting periods"]),
    S("Divorce should require agreement or proof of fault, like abuse or adultery.",
      yes=["Ending no-fault divorce"],
      no=["Divorce over one spouse's objection without fault"]),
]

T["pay_transparency"] = [
    S("Large employers should post pay ranges and report pay by gender.",
      yes=["Pay ranges in job ads", "Reporting pay by gender to the government"],
      no=["Leaving pay information private"]),
    S("Large employers should post pay ranges only.",
      yes=["Pay ranges in job ads"],
      no=["Gender pay reporting"]),
    S("Neither: no pay posting or reporting rules.",
      yes=["Leaving pay disclosure to employers"],
      no=["Pay range or pay-by-gender rules"]),
]

T["board_gender_rules"] = [
    S("Large public companies should have at least 40% women on their boards.",
      yes=["A legal minimum of 40% women on boards"],
      no=["Leaving board makeup to companies"]),
    S("No board quota, but companies must report how many women serve.",
      yes=["Required reporting of board gender"],
      no=["Board gender quotas", "No reporting"]),
    S("No board gender requirement or reporting.",
      yes=["Leaving board makeup to shareholders"],
      no=["Quotas or reporting"]),
]

T["birth_rate_policy"] = [
    S("Birth rates are a personal choice, not a government concern.",
      yes=["No policies aimed at birth rates"],
      no=["Baby bonuses"]),
    S("Make raising children more affordable, but don't aim at raising birth rates.",
      yes=["Help with child costs for families who have children"],
      no=["Payments designed to get people to have more children"]),
    S("Government should aim to raise birth rates with large payments or tax breaks for each child.",
      yes=["Large baby bonuses or tax breaks per child"],
      no=["Treating birth rates as none of government's business"]),
]

T["workplace_gender_programs"] = [
    S("Large employers should run programs to bring more women into jobs where they're few, with hiring targets and required training.",
      yes=["Hiring targets for women", "Required training"],
      no=["Leaving it to each company"]),
    S("Large employers should run outreach and mentoring for women, without targets.",
      yes=["Recruiting and mentoring programs for women"],
      no=["Hiring targets", "No programs"]),
    S("Large employers should run only general training on treating everyone equally.",
      yes=["Equal-treatment training for all"],
      no=["Programs aimed at women specifically"]),
    S("No such programs, but leave the choice to each company.",
      yes=["Letting companies decide"],
      no=["Required programs", "Government bans"]),
    S("No such programs, and government should bar them at federal contractors.",
      yes=["Barring gender-targeted programs at companies with federal contracts"],
      no=["Programs aimed at hiring or promoting women"]),
]

T["women_draft"] = [
    S("If there's a draft, women should be drafted on the same terms as men.",
      yes=["Women registering and serving in any role, including combat"],
      no=["A men-only draft"]),
    S("Women should be drafted, but only for non-combat roles.",
      yes=["Drafting women for support roles"],
      no=["Drafting women for combat", "A men-only draft"]),
    S("Only men should be drafted.",
      yes=["Keeping draft registration for men only"],
      no=["Drafting women"]),
]

T["natural_roles"] = [
    S("Differences in men's and women's family roles come almost entirely from upbringing and culture.",
      means=["If children were raised differently, mothers and fathers would take on the same roles"]),
    S("They come mostly from culture, partly from nature.",
      means=["Biology plays a small part, but upbringing explains most of the difference"]),
    S("They come about equally from culture and nature.",
      means=["Upbringing and biology matter about the same"]),
    S("They come mostly from natural differences between the sexes.",
      means=["Biology explains most of why mothers and fathers take on different roles"]),
    S("They come almost entirely from nature; men and women are suited to different roles.",
      means=["Mothers and fathers take different roles mainly because of biology, not upbringing"]),
]

if __name__ == "__main__":
    write("D12", T)
    write_clarity("D12", C)
