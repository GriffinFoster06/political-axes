"""Environment and energy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, write, write_clarity  # noqa: E402

C, T = {}, {}

T["net_zero_target"] = [
    S("The US should reach net-zero greenhouse gas emissions by 2035.",
      yes=["Cutting emissions to net zero within about ten years", "Fast changes to power plants, cars and buildings"],
      no=["Waiting until 2050 or later"]),
    S("The US should reach net zero by 2050.",
      yes=["A 2050 net-zero target, as most rich countries have set"],
      no=["A 2035 deadline", "No target"]),
    S("The US should reach net zero, but later than 2050.",
      yes=["A slower timeline past 2050"],
      no=["2035 or 2050 deadlines", "Dropping a target"]),
    S("The US shouldn't set a net-zero target.",
      yes=["No national emissions goal"],
      no=["Any net-zero deadline"]),
]

T["climate_willing_to_pay"] = [
    S("You'd pay $50 or more a month in higher energy costs for climate policies.",
      means=["Your household would accept about $600+ a year more on electricity and fuel"]),
    S("You'd pay about $20 a month more for climate policies.",
      means=["Your household would accept about $240 a year more on electricity and fuel, but not much beyond that"]),
    S("You'd pay about $5 a month more for climate policies.",
      means=["Your household would accept about $60 a year more, but not more"]),
    S("You wouldn't pay anything more for climate policies.",
      means=["Climate policies shouldn't raise your household's energy bills at all"]),
]

T["carbon_tax"] = [
    S("A high and rising federal carbon tax, around $100 a ton.",
      yes=["A carbon tax adding about 90 cents a gallon to gasoline", "Raising it over time"],
      no=["A small carbon tax", "No carbon tax"]),
    S("A moderate carbon tax, around $25 to $50 a ton.",
      yes=["A carbon tax adding about 20 to 45 cents a gallon to gasoline"],
      no=["A $100 tax", "No carbon tax"]),
    S("No federal carbon tax.",
      yes=["Keeping fossil fuels free of a carbon tax"],
      no=["Any carbon tax"]),
]

T["carbon_tax_use"] = [
    S("Carbon tax money should go to clean energy and climate programs.",
      yes=["Spending it on clean energy, transit and climate programs"],
      no=["Rebating the money to households", "Cutting other taxes with it"]),
    S("Carbon tax money should go back to households as equal rebates.",
      yes=["The same check to every household"],
      no=["Spending it on programs", "Using it for tax cuts"]),
    S("Carbon tax money should cut other taxes, like income or payroll taxes.",
      yes=["Lower income or payroll tax rates paid for by the carbon tax"],
      no=["New spending", "Rebate checks"]),
]

T["carbon_border_fee"] = [
    S("Imports from countries with weaker pollution rules should pay a carbon fee.",
      yes=["A carbon fee on imported steel, cement and aluminum"],
      no=["Letting high-pollution imports in fee-free"]),
    S("Charge a carbon fee on imports only if US producers pay for their carbon too.",
      yes=["A border fee paired with a US carbon price"],
      no=["A fee on imports alone"]),
    S("No carbon fee on imports.",
      yes=["Leaving imports free of carbon fees"],
      no=["Any carbon border fee"]),
]

T["drilling_public_lands"] = [
    S("No new oil and gas drilling on federal land and waters, and phase out existing leases.",
      yes=["Ending new leases", "Winding down current federal drilling"],
      no=["Any new federal drilling"]),
    S("No new federal oil and gas leases, but existing ones can continue.",
      yes=["A halt to new leasing", "Letting current wells keep producing"],
      no=["New leases", "Ending existing ones"]),
    S("Allow new federal drilling with strict environmental review.",
      yes=["New leases after full environmental review"],
      no=["A leasing ban", "Fast-tracked approvals"]),
    S("Expand federal drilling and speed up approvals.",
      yes=["More leases on federal land and offshore", "Faster permits"],
      no=["Limits on new federal drilling"]),
]

T["coal_plants"] = [
    S("Close all coal plants by about 2035.",
      yes=["A deadline to shut down coal power"],
      no=["Letting coal plants run until they age out"]),
    S("Phase coal plants out gradually as they age.",
      yes=["Retiring coal plants over time without building new ones"],
      no=["A fixed 2035 shutdown", "Government help to keep them open"]),
    S("Keep coal plants running as long as they make economic sense.",
      yes=["Letting the market decide when coal plants close"],
      no=["Forced closures", "Subsidies to keep them open"]),
    S("Use government help to keep coal plants open.",
      yes=["Subsidies or orders to keep coal plants running"],
      no=["Closing coal plants"]),
]

T["nuclear_power"] = [
    S("Phase out nuclear power.",
      yes=["Closing existing nuclear plants over time"],
      no=["Building new plants"]),
    S("No new nuclear plants, but keep existing ones running.",
      yes=["Keeping today's plants open"],
      no=["New plants", "Closing existing ones"]),
    S("Build some new nuclear plants under current safety rules.",
      yes=["New plants with today's approval process"],
      no=["Phasing out nuclear", "Loosening safety approvals"]),
    S("Build many new nuclear plants, with faster approvals.",
      yes=["A large nuclear build-out", "Speeding up licensing"],
      no=["Phasing out nuclear"]),
]

T["nuclear_funding"] = [
    S("No government money for new nuclear plants.",
      yes=["Leaving nuclear financing to private companies"],
      no=["Federal loans, guarantees or tax credits for nuclear"]),
    S("Government loan guarantees only for new nuclear plants.",
      yes=["Federal loan guarantees for nuclear projects"],
      no=["Direct grants or large tax credits", "No support at all"]),
    S("Large direct government support for new nuclear plants.",
      yes=["Federal money, loans and tax credits to build plants"],
      no=["Leaving nuclear to the private market"]),
]

T["ev_requirement"] = [
    S("Require most new cars sold to be electric by 2035.",
      yes=["A 2035 electric-vehicle sales requirement"],
      no=["Leaving the car mix to buyers"]),
    S("No electric-car requirement, but keep tightening pollution limits for new cars.",
      yes=["Stricter tailpipe limits over time"],
      no=["An EV mandate", "Freezing pollution limits"]),
    S("No electric-car requirement and no tighter pollution limits.",
      yes=["Freezing or loosening car pollution rules"],
      no=["EV mandates", "Tighter tailpipe limits"]),
]

T["ev_tax_credit"] = [
    S("Bring back a federal EV tax credit of $7,500 or more.",
      yes=["A credit of $7,500+ for buyers of new electric cars"],
      no=["No federal EV credit"]),
    S("A smaller EV credit, only for lower- and middle-income buyers.",
      yes=["An income-limited EV credit"],
      no=["A $7,500 credit for anyone", "No credit"]),
    S("No federal EV tax credit, as now.",
      yes=["Keeping the EV credit repealed"],
      no=["Any federal EV credit"]),
]

C["env_jobs_tradeoff"] = {
    "why": "No examples of the rules or jobs at stake.",
    "scope": "Industries like coal and metal mining, oil and gas, and manufacturing. Rules like limits on mine runoff, smokestack emissions and drilling near water supplies.",
}
T["env_jobs_tradeoff"] = trade(
    S("Stricter environmental rules, even if some mining, oil and factory jobs are lost.",
      yes=["Tighter limits on mine runoff, smokestack emissions and drilling near water", "Accepting some lost jobs in those industries"],
      no=["Weakening rules to save jobs"]),
    S("Keep mining, oil and factory jobs, even if the environment is less protected.",
      yes=["Easing environmental rules that threaten those jobs"],
      no=["New rules that would cost jobs in those industries"]),
    S("You weigh the environment and those jobs about equally.",
      means=["You'd judge each rule by how much protection it buys and how many jobs it costs"]))

C["permitting_tradeoff"] = {
    "why": "'Thorough review' and 'harms' were undefined.",
    "scope": "Projects of any kind of energy. Reviews study effects on wildlife, water, air and nearby residents, and today can take 4 years or more for major projects.",
}
T["permitting_tradeoff"] = trade(
    S("Keep thorough environmental reviews, even if pipelines, power lines and solar farms take many years.",
      yes=["Full studies of effects on wildlife, water, air and neighbors", "Neighbors' right to challenge projects in court"],
      no=["Deadlines that cut reviews short"]),
    S("Speed up approvals for pipelines, power lines and solar farms, even if some harms are missed.",
      yes=["Hard deadlines on reviews", "Limits on lawsuits that delay projects"],
      no=["Multi-year reviews for every major project"]),
    S("You weigh thorough review and speed about equally.",
      means=["You'd want faster reviews for small projects and full reviews for big ones"]))

T["land_protection"] = [
    S("Protect much more US land and water from mining, drilling and logging, such as 30% by 2030.",
      yes=["New national monuments, wilderness areas and marine reserves"],
      no=["Opening protected land to development"]),
    S("Protect somewhat more land than today.",
      yes=["Some new protected areas"],
      no=["A 30% target", "Opening protected land"]),
    S("Protect about as much land as today.",
      yes=["Today's protected areas"],
      no=["Adding or removing protections"]),
    S("Protect less land; open more to development.",
      yes=["Opening protected land to mining, drilling and logging", "Shrinking some national monuments"],
      no=["New protected areas"]),
]

T["sell_public_land"] = [
    S("Keep all federal land public.",
      yes=["No sales of national forests or grazing land"],
      no=["Selling federal land, even for housing"]),
    S("Sell only small parcels near towns, for housing.",
      yes=["Selling small federal parcels for homes"],
      no=["Large sales", "Keeping every acre"]),
    S("Sell large amounts of federal land to states or private owners.",
      yes=["Transferring national forests and grazing land to states or buyers"],
      no=["Keeping it all federal"]),
]

T["climate_agreements"] = [
    S("The US should join climate agreements with binding targets for each country.",
      yes=["Rejoining international climate deals", "Enforceable emission targets for every country"],
      no=["Voluntary targets", "Staying out"]),
    S("The US should join climate agreements with voluntary targets, like Paris.",
      yes=["Rejoining the Paris Agreement"],
      no=["Binding targets", "Staying out"]),
    S("The US shouldn't take part in international climate agreements.",
      yes=["Staying out of the Paris Agreement"],
      no=["Joining any international climate deal"]),
]

T["climate_belief"] = [
    S("Climate change is mostly caused by humans and is a serious threat.",
      means=["Burning fossil fuels is the main cause of recent warming", "The effects will be severe without major action"]),
    S("Climate change is mostly caused by humans, but manageable.",
      means=["Burning fossil fuels is the main cause", "People can adapt to most of the effects"]),
    S("Climate change is partly human and partly natural, with uncertain effects.",
      means=["Human activity is one cause among several", "How serious it will be is unclear"]),
    S("Climate change is mostly natural, not caused by humans.",
      means=["The climate is changing, but human activity isn't the main reason"]),
    S("Climate change isn't happening.",
      means=["Earth's average temperature hasn't really risen in recent decades"]),
]

T["environmental_justice"] = [
    S("Pollution cleanup should set aside a share of money for low-income and minority neighborhoods.",
      yes=["A fixed share of federal cleanup money for those areas"],
      no=["Ranking cleanup by pollution levels alone"]),
    S("Pollution cleanup should go to the most polluted areas, whoever lives there.",
      yes=["Ranking cleanup by how polluted a place is"],
      no=["Set-asides by income or race"]),
    S("No special priority for any neighborhood in pollution cleanup.",
      yes=["Treating all areas alike"],
      no=["Priority by pollution level or by who lives there"]),
]

T["adaptation_tradeoff"] = trade(
    S("Climate money should go mainly to cutting emissions, even if less protects communities from floods and heat.",
      yes=["Spending on clean power, efficiency and emission cuts first"],
      no=["Putting most money into sea walls, cooling centers and flood defenses"]),
    S("Climate money should go mainly to protecting communities from floods and heat, even if emissions fall more slowly.",
      yes=["Sea walls, flood defenses, cooling centers and stronger buildings"],
      no=["Putting most money into emission cuts"]),
    S("You weigh cutting emissions and preparing for effects about equally.",
      means=["You'd split climate money roughly evenly between the two"]))

T["plastic_bags"] = [
    S("Ban single-use plastic checkout bags.",
      yes=["Plastic bag bans in stores"],
      no=["Letting stores hand out plastic bags"]),
    S("Allow plastic bags, with a fee per bag.",
      yes=["A required per-bag charge"],
      no=["A ban", "Free bags"]),
    S("Allow free plastic bags, as each store chooses.",
      yes=["Leaving bags to stores"],
      no=["Bans or bag fees"]),
]

C["climate_action"] = {
    "why": "'Fast, deep' and 'noticeably' had no scale.",
    "options": {
        "0": "Require fast, deep cuts in greenhouse gas emissions, such as halving them within 10 years, even if energy prices rise noticeably",
    },
}
T["climate_action"] = [
    S("Require fast, deep cuts in emissions, even if energy prices rise noticeably.",
      yes=["Rules to roughly halve US emissions within 10 years", "Accepting noticeably higher energy bills"],
      no=["Voluntary approaches", "Slower phase-ins"]),
    S("Require gradual cuts in emissions, accepting small increases in energy prices.",
      yes=["Steadily tightening emission limits", "Small increases in energy bills"],
      no=["Fast, costly cuts", "No required cuts"]),
    S("Fund clean energy research and tax credits, but don't require emission cuts.",
      yes=["Clean energy research and tax credits"],
      no=["Required emission cuts"]),
    S("Take no specific action on climate change.",
      yes=["No climate-specific spending or rules"],
      no=["Clean energy credits", "Emission limits"]),
    S("Repeal existing climate rules and expand fossil fuel production.",
      yes=["Repealing emission rules", "More oil, gas and coal production"],
      no=["Any climate rules or clean energy credits"]),
]

if __name__ == "__main__":
    write("D05", T)
    write_clarity("D05", C)
