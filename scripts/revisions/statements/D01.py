"""Taxes and redistribution."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["income_tax_structure"] = [
    S("Income tax should rise much more steeply with income than today.",
      yes=["A top income tax rate above 50% on the highest incomes", "New brackets above today's 37% rate"],
      no=["Keeping the top rate at 37%", "A flat tax or fewer brackets"]),
    S("The highest incomes should be taxed more; middle incomes no more than now.",
      yes=["Raising rates on the highest incomes above 37%", "Keeping or cutting rates on middle incomes"],
      no=["A top rate above 50%", "Flattening the rates"]),
    S("Keep today's seven rates, from 10% to 37%.",
      yes=["Today's brackets and top rate of 37%"],
      no=["Raising the top rate", "Cutting to two or three rates or a flat tax"]),
    S("Simplify to a few rates with a lower top rate.",
      yes=["Two or three rates between about 10% and 30%", "Cutting the top rate below 37%"],
      no=["Raising rates on high incomes", "Keeping seven brackets"]),
    S("Everyone should pay one flat rate on income above a tax-free amount.",
      yes=["A single income tax rate for everyone", "A basic tax-free amount so the lowest earners pay nothing"],
      no=["Higher rates for higher incomes", "Today's seven brackets"]),
    S("Abolish the federal income tax and raise the money another way.",
      yes=["Ending the federal income tax", "Replacing it with something like a national sales tax"],
      no=["Any federal tax on income, flat or graduated"]),
]

T["low_income_tax"] = [
    S("Low-income households should owe no income tax and get bigger credits.",
      yes=["Larger refundable credits like the Earned Income Tax Credit", "No federal income tax for low-income households"],
      no=["Any minimum income tax for the lowest earners"]),
    S("Keep today's setup: low-income households owe no income tax and keep today's credits.",
      yes=["No federal income tax for low-income households", "Refundable credits at about today's size"],
      no=["Bigger credits", "Cutting credits or adding a minimum tax"]),
    S("Low-income households should owe no income tax, but credits paid out as refunds should shrink.",
      yes=["Smaller refundable credits than today", "Still no income tax owed for low-income households"],
      no=["Larger credits", "A minimum tax on the lowest earners"]),
    S("Everyone should pay at least a small income tax.",
      yes=["A minimum income tax of about $100 a year, even for the lowest earners"],
      no=["Households paying no income tax at all", "Refund payouts beyond what a household owes"]),
    S("Low-income households should pay the same flat rate as everyone, with no tax-free amount.",
      yes=["One rate on every dollar of income, starting with the first"],
      no=["Tax-free amounts and refundable credits for low earners"]),
]

T["tax_burden_principle"] = [
    S("High earners should pay a much larger share of their income in taxes.",
      yes=["Tax rates that climb steeply with income", "Higher taxes on top earners' investment income too"],
      no=["A flat tax", "Cutting top rates"]),
    S("High earners should pay a somewhat larger share of their income.",
      yes=["Rates that rise moderately with income"],
      no=["Steep rates on top earners", "A flat tax"]),
    S("Everyone should pay the same share of income above a basic tax-free amount.",
      yes=["A flat tax with a tax-free allowance"],
      no=["Higher rates for higher incomes", "Taxing the first dollar of income"]),
    S("Everyone should pay the same share of every dollar they earn.",
      yes=["One flat rate starting with the first dollar, for everyone"],
      no=["Tax-free amounts", "Higher rates for higher incomes"]),
]

C["top_income_tax"] = {
    "why": "'A lot' and 'somewhat' had no numbers.",
    "scope": "Today the top rate is 37%. Raising or lowering a lot means by about 10 percentage points or more; somewhat means by a few points. Assume the money raised or lost changes the federal budget, not your own taxes.",
}
T["top_income_tax"] = [
    S("Raise income taxes on people earning over $1 million a year a lot.",
      yes=["A top rate around 47% or higher on income over $1 million"],
      no=["Keeping 37%", "Cutting taxes on million-dollar earners"]),
    S("Raise income taxes on people earning over $1 million a year somewhat.",
      yes=["A top rate a few points above 37%, around 40%"],
      no=["A top rate near 50% or more", "Cutting taxes on million-dollar earners"]),
    S("Keep income taxes on people earning over $1 million a year about where they are.",
      yes=["A top rate of about 37%"],
      no=["Raising or cutting the top rate"]),
    S("Lower income taxes on people earning over $1 million a year somewhat.",
      yes=["A top rate a few points below 37%, around 33%"],
      no=["Raising taxes on top earners", "A top rate below 30%"]),
    S("Lower income taxes on people earning over $1 million a year a lot.",
      yes=["A top rate around 27% or lower"],
      no=["Keeping 37%", "Raising taxes on top earners"]),
]

T["top_rate_number"] = [
    S("Income above $1 million a year should be taxed at 70% or more.",
      yes=["A 70%+ rate on each dollar above $1 million, like the top rates of the 1950s to 1970s"],
      no=["Any top rate near today's 37%"]),
    S("Income above $1 million a year should be taxed at about 50% to 60%.",
      yes=["A new top rate of 50% to 60% on income over $1 million"],
      no=["Keeping 37%", "Going to 70% or more"]),
    S("Income above $1 million a year should be taxed at about 40% to 45%.",
      yes=["A modest increase from 37% to 40–45% on income over $1 million"],
      no=["A rate of 50% or more", "Cutting the top rate"]),
    S("Keep the top rate at 37%.",
      yes=["Today's 37% top rate"],
      no=["Raising or lowering it"]),
    S("Cut the top rate to about 25% to 30%.",
      yes=["A top rate of 25–30% on income over $1 million"],
      no=["Keeping 37%", "Raising rates on top earners"]),
    S("Cut the top rate to 20% or lower.",
      yes=["A top rate of 20% or less, even for the highest earners"],
      no=["Keeping 37%", "Any rate above about 20%"]),
]

T["corporate_rate"] = [
    S("Raise the corporate tax rate back to 35% or higher.",
      yes=["Undoing the 2017 cut from 35% to 21%"],
      no=["Keeping 21%", "Cutting the corporate rate below 21%"]),
    S("Raise the corporate tax rate to about 28%.",
      yes=["A partial increase, from 21% to about 28%"],
      no=["Going back to 35%", "Keeping 21% or cutting it"]),
    S("Keep the corporate tax rate at 21%.",
      yes=["The 21% rate set in 2018"],
      no=["Raising the corporate rate", "Cutting the corporate rate"]),
    S("Cut the corporate tax rate to about 15%.",
      yes=["Lowering the rate from 21% to about 15%"],
      no=["Keeping 21%", "Raising the corporate rate"]),
]

T["wealth_tax"] = [
    S("Tax wealth above $50 million at 3% or more every year.",
      yes=["A yearly tax of 3%+ on stocks, businesses, property and savings above $50 million"],
      no=["Taxing only income, not wealth"]),
    S("Tax wealth above $50 million at about 1% to 2% every year.",
      yes=["A yearly 1–2% tax on fortunes above $50 million"],
      no=["A rate of 3% or more", "No yearly wealth tax"]),
    S("No yearly wealth tax, but tax big gains in value when the owner dies.",
      yes=["Taxing untaxed investment gains on large estates at death"],
      no=["A yearly tax on total wealth"]),
    S("Tax income, not wealth.",
      yes=["Taxing money only when it's earned or an investment is sold"],
      no=["Any yearly tax on total wealth", "Taxing gains at death"]),
]

C["large_fortunes"] = {
    "why": "'Much more' and 'somewhat more' had no scale.",
    "scope": "Think about taxes, not any particular person. “Much more” means something like a wealth tax or top rates near 50%; “somewhat more” means closing a few tax breaks or raising rates a few points.",
}
T["large_fortunes"] = [
    S("Billion-dollar fortunes are a problem in themselves, and taxes should shrink them over time.",
      yes=["Taxes designed to break up fortunes of $1 billion or more", "A steep yearly wealth tax or a heavy tax on large inheritances"],
      no=["Leaving very large fortunes alone"]),
    S("Billionaires should pay much more in taxes than now.",
      yes=["A wealth tax or top rates near 50% or more", "Taxing investment gains like wages for the richest"],
      no=["Today's tax levels for the richest"]),
    S("Billionaires should pay somewhat more than now.",
      yes=["Closing tax breaks the richest use", "Raising their rates a few points"],
      no=["A wealth tax aimed at shrinking fortunes", "Leaving their taxes as they are"]),
    S("The richest pay about the right amount now.",
      yes=["Today's taxes on the richest"],
      no=["New taxes aimed at billionaires", "Tax cuts for them"]),
    S("Taxes on the richest are already too high and discourage investment.",
      yes=["Cutting taxes on top incomes, investment gains and estates"],
      no=["Wealth taxes or higher rates on billionaires"]),
]

T["estate_tax_level"] = [
    S("Tax estates above about $1 million, at 50% or more on the largest.",
      yes=["Lowering the exemption from $15 million to about $1 million", "Rates of 50% or more on the biggest estates"],
      no=["Today's $15 million exemption", "Ending the estate tax"]),
    S("Tax estates above about $3.5 million, at about 45%.",
      yes=["Returning to the 2009 rules: a $3.5 million exemption and a 45% rate"],
      no=["Today's $15 million exemption", "Going down to $1 million"]),
    S("Keep today's estate tax: 40% on the part above $15 million.",
      yes=["Today's exemption and 40% rate"],
      no=["Taxing more estates", "Exempting more or ending the tax"]),
    S("Raise the threshold so even fewer estates pay.",
      yes=["An exemption above $15 million per person"],
      no=["Taxing more estates", "Ending the tax outright"]),
    S("Eliminate the estate tax.",
      yes=["No federal tax on estates of any size"],
      no=["Any estate tax, even on the largest fortunes"]),
]

T["inheritance_principle"] = [
    S("A large share of very big inheritances should go to the public.",
      yes=["Heavy taxes on inheritances of several million dollars or more", "Stopping fortunes from building up across generations"],
      no=["Letting heirs keep most of a large inheritance"]),
    S("A moderate tax on very large inheritances is fair.",
      yes=["A tax on inheritances of several million dollars or more at moderate rates"],
      no=["Taking most of a large inheritance", "No inheritance tax"]),
    S("Only a small tax, and only on the very largest inheritances.",
      yes=["A low tax rate that applies only to the biggest inheritances"],
      no=["Moderate or heavy taxes on inheritances"]),
    S("Inheritances shouldn't be taxed at all; the money was already taxed when it was earned.",
      yes=["Ending taxes on inheritances and estates"],
      no=["Any tax on what heirs receive"]),
]

T["capital_gains_rate"] = [
    S("Profits from selling investments should be taxed at the same rates as wages, for everyone.",
      yes=["Taxing stock sale profits at up to 37%, like wages"],
      no=["Today's lower 20% top rate on investment profits"]),
    S("High earners should pay wage rates on investment profits; others should keep lower rates.",
      yes=["Up to 37% on investment profits for people with high incomes", "Lower rates for middle-income investors"],
      no=["Today's 20% top rate for the wealthy", "Raising rates on middle-income investors"]),
    S("Keep investment profits taxed at lower rates than wages, as today.",
      yes=["Today's top rate of 20% (plus the 3.8% surtax)"],
      no=["Taxing them like wages", "Cutting investment tax rates further"]),
    S("Tax investment profits at lower rates than today.",
      yes=["A top rate below 20% on profits from selling stocks and other investments"],
      no=["Raising those rates"]),
    S("Don't tax profits from selling investments at all.",
      yes=["Ending the tax on gains from selling stocks, property and businesses"],
      no=["Any tax on investment profits"]),
]

T["gains_at_death"] = [
    S("Tax the untaxed gains at death, above about $1 million.",
      yes=["Taxing the $900,000 gain in the example when the owner dies"],
      no=["Letting gains like that go untaxed forever"]),
    S("Don't tax at death, but heirs should pay tax on the whole gain when they sell.",
      yes=["Heirs paying tax on the full $900,000 when they sell"],
      no=["Taxing at death", "Wiping the gain off the books at death, as today"]),
    S("Keep today's rule: the gain before death is never taxed.",
      yes=["Heirs paying tax only on gains after they inherit"],
      no=["Taxing the $900,000 at death or when heirs sell"]),
]

C["cash_aid_level"] = {
    "why": "'Enough to stay above the poverty line' had no figure.",
    "context": "The federal poverty line is about $32,000 a year for a family of four.",
}
T["cash_aid_level"] = [
    S("Guarantee every household enough to stay above the poverty line.",
      yes=["Cash and food aid topping up any household below about $32,000 a year for a family of four"],
      no=["Leaving any household below the poverty line", "Cutting today's aid"]),
    S("Spend more on cash and food aid, mainly for families with children and people who can't work.",
      yes=["Larger food stamps, Earned Income Tax Credit and cash welfare for these groups"],
      no=["A guaranteed income for all", "Cutting aid"]),
    S("Keep cash and food aid at about today's level.",
      yes=["Today's SNAP, Earned Income Tax Credit and cash welfare"],
      no=["Expanding food and cash aid", "Cutting food and cash aid"]),
    S("Spend less on cash and food aid, with charities, churches and families doing more.",
      yes=["Smaller food stamps and welfare budgets", "More help from charities, churches and families"],
      no=["Expanding aid"]),
    S("End most federal cash and food aid.",
      yes=["Ending most federal food stamps and cash welfare", "Leaving it to states, charities and families"],
      no=["Keeping today's federal aid"]),
]

T["aid_form"] = [
    S("Aid should be mostly cash that people spend as they choose.",
      yes=["Replacing food and housing benefits with cash"],
      no=["Limits on what aid can buy"]),
    S("Keep today's mix of cash and benefits for specific needs.",
      yes=["Cash aid alongside food stamps and housing vouchers"],
      no=["All cash", "More restrictions on what aid can buy"]),
    S("Aid should mostly be for specific needs like food and rent.",
      yes=["Food stamps and housing vouchers rather than cash"],
      no=["Turning benefits into cash", "Banning specific foods"]),
    S("Aid should be for specific needs, with limits on what can be bought.",
      yes=["Banning soda and candy purchases with food aid", "Benefits that can only be spent on essentials"],
      no=["Cash aid people can spend freely"]),
]

T["work_req_rule"] = [
    S("Cash and food aid shouldn't depend on working.",
      yes=["Aid for adults who can work but aren't working"],
      no=["Any work, job search or training requirement"]),
    S("No work requirement, but offer job training and help finding work.",
      yes=["Voluntary job training and job search help"],
      no=["Cutting off aid for not working"]),
    S("Require about 20 hours a week of work, job search or training after about 3 months.",
      yes=["A 20-hour weekly requirement for adults 18 to 54 with no disability or children at home", "A grace period of about 3 months"],
      no=["No requirement", "Requiring 30+ hours from day one"]),
    S("Require 30 or more hours a week from the start, and cut off anyone who doesn't comply.",
      yes=["A 30-hour weekly requirement with no grace period", "Ending benefits for those who don't meet it"],
      no=["Grace periods", "Aid without work"]),
]
T["work_req_cases"] = existing("D01", "work_req_cases")

T["ubi"] = [
    S("Every adult should get about $1,500 a month or more, enough to live on.",
      yes=["A universal basic income for every adult, working or not", "Higher taxes to pay for it"],
      no=["Means-tested aid only"]),
    S("Every adult should get about $500 a month.",
      yes=["A smaller universal payment to every adult", "Higher taxes to pay for it"],
      no=["A full living income for all", "No universal payment"]),
    S("No payment to everyone, but a guaranteed minimum income for anyone below a set level.",
      yes=["Topping up incomes below a set floor"],
      no=["Sending checks to every adult regardless of income"]),
    S("No guaranteed income of any kind.",
      yes=["Ending or avoiding any guaranteed income"],
      no=["Universal payments", "A guaranteed minimum income"]),
]

T["child_benefit_level"] = [
    S("Every child should bring about $300 a month, whatever the parents earn.",
      yes=["A monthly payment of about $300 per child, for all families"],
      no=["Linking child support to parents' income or taxes"]),
    S("A bigger child credit than today, with the full amount for low-income families.",
      yes=["Raising the $2,200 credit", "Paying the full credit to families with low earnings"],
      no=["Keeping or cutting today's credit"]),
    S("Keep about today's child tax credit of up to $2,200.",
      yes=["Today's credit and rules"],
      no=["Expanding the child credit", "Cutting the child credit"]),
    S("A smaller child credit, and only for families who owe income tax.",
      yes=["Shrinking the credit", "Ending refunds to families who owe no income tax"],
      no=["Expanding the credit"]),
    S("No federal child credit.",
      yes=["Ending the child tax credit"],
      no=["Any federal child benefit"]),
]

T["child_benefit_work"] = [
    S("Parents with no earnings should get the full child tax credit.",
      yes=["The full credit for every child, whether or not parents work"],
      no=["Requiring earnings to get the credit"]),
    S("Parents with no earnings should get part of the child tax credit.",
      yes=["A partial credit for non-working parents, the rest tied to earnings"],
      no=["The full credit without work", "Nothing for non-working parents"]),
    S("Only parents with earnings from work should get the child tax credit.",
      yes=["Tying the credit to earnings from work"],
      no=["Paying the credit to parents who don't work"]),
]

C["inequality_tradeoff"] = {
    "why": "'The gap' and the ways to reduce it were abstract.",
    "scope": "Today the top 10% of earners take home nearly half of all income. Reducing the gap would mean things like higher taxes on top earners and more aid for low earners.",
}
T["inequality_tradeoff"] = trade(
    S("Government should act to narrow the gap between rich and poor, even at the cost of higher taxes and slower growth.",
      yes=["Higher taxes on top earners and large fortunes", "More aid and services for low earners"],
      no=["Tax cuts aimed at growth that widen the gap"]),
    S("Government should focus on growth and leave the gap alone, even if it widens.",
      yes=["Lower taxes and fewer rules aimed at growth", "Judging policy by overall growth, not by the gap"],
      no=["Higher taxes or new programs mainly to narrow the gap"]),
    S("You weigh narrowing the gap and growth about equally.",
      means=["You'd back steps to narrow the gap only when they cost little growth"]))

T["deficit_approach"] = [
    S("Borrowing is fine for now; the deficit isn't the priority.",
      yes=["Running deficits to pay for other priorities"],
      no=["Spending cuts or tax increases aimed at the deficit"]),
    S("Close the deficit mainly by raising taxes on high earners and corporations.",
      yes=["Higher taxes on top earners and corporations to close the gap"],
      no=["Closing it mainly with spending cuts"]),
    S("Close the deficit with an even mix of tax increases and spending cuts.",
      yes=["A deal with tax increases and spending cuts in about equal parts"],
      no=["Closing it with taxes alone or cuts alone"]),
    S("Close the deficit mainly by cutting spending.",
      yes=["Spending cuts as most of the fix", "Only small tax increases, if any"],
      no=["Large tax increases"]),
    S("Close the deficit entirely with spending cuts, no tax increases.",
      yes=["Cutting about $1.8 trillion a year in spending over time"],
      no=["Any tax increase"]),
]

T["balanced_budget_amendment"] = [
    S("No balanced-budget amendment; the government needs to be able to borrow.",
      yes=["Leaving borrowing decisions to Congress each year"],
      no=["A constitutional balanced-budget rule"]),
    S("Require a balanced budget in normal times, with exceptions for wars and recessions.",
      yes=["A balanced-budget amendment with war and recession exceptions"],
      no=["No rule at all", "A rule with no exceptions"]),
    S("Require a balanced budget every year, no exceptions.",
      yes=["A strict balanced-budget amendment, even in wars and recessions"],
      no=["Exceptions that allow borrowing"]),
]

C["poverty_cause"] = {
    "why": "'An unfair economic system' and 'circumstances' had no examples.",
    "options": {
        "0": "An economic system that is unfair to them, such as low wages, too few good jobs, or discrimination",
        "1": "Circumstances they didn't choose, such as where they grew up, illness in the family, or bad luck",
    },
}
T["poverty_cause"] = [
    S("Poverty is mainly caused by an unfair economic system.",
      means=["Low wages, too few good jobs and discrimination keep most poor adults poor, more than their own choices"]),
    S("Poverty is mainly caused by circumstances people didn't choose.",
      means=["Where people grew up, family illness or bad luck explain most poverty, more than their own choices"]),
    S("Poverty comes from a mix of circumstances and choices.",
      means=["Both what happens to people and what they decide, like schooling and work, matter about equally"]),
    S("Poverty is mainly caused by people's own choices.",
      means=["Choices like dropping out of school, not working or having children early explain most poverty among able adults"]),
    S("Poverty is mainly caused by lack of effort.",
      means=["Most able adults who are poor could get out of poverty if they tried harder"]),
]

T["job_guarantee"] = [
    S("The federal government should guarantee a job to anyone who wants one.",
      yes=["Public jobs in care work or infrastructure for anyone who can't find work, paid at least minimum wage"],
      no=["Leaving job creation to private employers"]),
    S("Guarantee jobs only where unemployment is high.",
      yes=["Public jobs programs in high-unemployment areas"],
      no=["A nationwide job guarantee", "No public jobs"]),
    S("No job guarantee, but help with job searches and training.",
      yes=["Job training and placement help"],
      no=["Government-created jobs for the unemployed"]),
    S("Jobs should come from the private sector.",
      yes=["Leaving job creation to businesses"],
      no=["Government jobs programs", "Federal job training programs"]),
]

T["tips_overtime_tax"] = [
    S("Tips and overtime should be taxed like any other pay.",
      yes=["Taxing all pay the same way"],
      no=["Special tax breaks for tips or overtime"]),
    S("Exempt tips and overtime from income tax for low- and middle-income workers only.",
      yes=["A tax break on tips and overtime with an income limit"],
      no=["The break for high earners", "Taxing them like other wages for everyone"]),
    S("Exempt tips and overtime from income tax for everyone.",
      yes=["No income tax on tips or overtime, at any income"],
      no=["Income limits on the break"]),
]

if __name__ == "__main__":
    write("D01", T)
    write_clarity("D01", C)
