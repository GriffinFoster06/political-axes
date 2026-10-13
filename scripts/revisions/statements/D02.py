"""Labor and business."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, write, write_clarity  # noqa: E402

C, T = {}, {}

T["min_wage_jobs"] = [
    S("Raise the minimum wage to $15 quickly; higher pay for many is worth some lost jobs.",
      yes=["Going from $7.25 to $15 within a year or two", "Accepting that some low-wage jobs disappear"],
      no=["A slow phase-in", "Leaving the minimum where it is"]),
    S("Raise the minimum wage to $15 over several years to limit job losses.",
      yes=["Phasing in $15 step by step over several years"],
      no=["Jumping straight to $15", "Leaving the minimum at $7.25"]),
    S("Raise the minimum wage only part of the way, or only where living costs are high.",
      yes=["A smaller raise, such as $10–12", "Higher minimums only in high-cost areas"],
      no=["$15 nationwide", "No raise at all"]),
    S("Don't raise the minimum wage; lost jobs would hurt the least experienced workers most.",
      yes=["Keeping the federal minimum at $7.25"],
      no=["Raising it to $15, quickly or slowly"]),
]

T["right_to_work"] = [
    S("Union contracts should be able to require fees in every state.",
      yes=["Overriding the 26 state right-to-work laws", "Letting contracts require covered workers to pay the union"],
      no=["State right-to-work laws"]),
    S("Each state should decide whether union contracts can require fees, as today.",
      yes=["Keeping today's state-by-state right-to-work laws"],
      no=["A national right-to-work law", "Overriding state right-to-work laws"]),
    S("No union contract anywhere should be able to require fees.",
      yes=["A national right-to-work law covering every state"],
      no=["Contracts that require covered workers to pay the union"]),
]

T["union_organizing"] = [
    S("Make forming a union much easier.",
      yes=["Recognizing a union once most workers sign cards, without a separate vote", "Large fines for employers who interfere"],
      no=["Keeping today's election process", "Requiring unions to win new votes regularly"]),
    S("Make forming a union somewhat easier.",
      yes=["Faster union votes", "Larger fines for illegal interference by employers"],
      no=["Recognition by signed cards alone", "Making it harder to form or keep a union"]),
    S("Keep today's rules for forming a union.",
      yes=["Today's election process and penalties"],
      no=["Making it easier or harder"]),
    S("Make it harder to keep a union.",
      yes=["New votes every few years for workers to keep their union"],
      no=["Card-check recognition", "Faster union elections"]),
]

T["public_unions"] = [
    S("Teachers and other government workers should bargain through unions and be able to strike.",
      yes=["Collective bargaining over pay, benefits and work rules", "The right to strike for most government workers"],
      no=["Banning strikes by teachers and state workers", "Limiting what unions can bargain over"]),
    S("Government workers should bargain through unions, but not strike.",
      yes=["Collective bargaining for teachers and state workers", "Banning strikes by government workers"],
      no=["The right to strike", "Ending public-sector bargaining"]),
    S("Government workers' unions should bargain over wages only.",
      yes=["Limiting bargaining to pay, as Wisconsin did in 2011"],
      no=["Bargaining over pensions, health benefits or work rules"]),
    S("Government workers shouldn't bargain through unions at all.",
      yes=["Ending collective bargaining for teachers and state workers"],
      no=["Any union bargaining for government workers"]),
]

T["paid_leave"] = [
    S("Federal law should guarantee 12 weeks or more of paid leave, funded by a payroll tax.",
      yes=["A national paid leave program for a new child or serious illness", "A payroll tax on workers and employers to fund it"],
      no=["Leaving paid leave to employers and states"]),
    S("Federal law should guarantee a shorter paid leave, such as 4 to 6 weeks.",
      yes=["A national paid leave of 4–6 weeks"],
      no=["12+ weeks of paid leave", "No federal paid leave"]),
    S("No requirement, but tax credits for employers who offer paid leave.",
      yes=["Tax credits to encourage employers to offer paid leave"],
      no=["A national paid leave requirement"]),
    S("No federal role in paid leave.",
      yes=["Leaving paid leave to employers and states"],
      no=["A federal paid leave program", "Federal tax credits for it"]),
]

T["sick_days"] = [
    S("All employers should give at least 7 paid sick days a year.",
      yes=["A national paid sick day requirement covering every employer, including small ones"],
      no=["Exempting small businesses"]),
    S("Employers with more than 50 workers should give paid sick days.",
      yes=["A paid sick day requirement for larger employers", "Exempting small businesses"],
      no=["Requiring it of all employers", "No requirement"]),
    S("No federal requirement for paid sick days.",
      yes=["Leaving sick days to states and employers"],
      no=["A national paid sick day law"]),
]

T["gig_workers"] = [
    S("App-based drivers and delivery workers should be employees.",
      yes=["Minimum wage, overtime and benefits for full-time app drivers"],
      no=["Treating them as independent contractors"]),
    S("Create a new middle category for app-based workers.",
      yes=["Pay floors and some benefits", "Keeping flexible, set-your-own hours"],
      no=["Full employee status", "Leaving them as contractors with no floor"]),
    S("Keep app-based workers as independent contractors.",
      yes=["Today's contractor status, with no required minimum wage or benefits"],
      no=["Making app drivers employees", "Required pay floors or benefits"]),
]

C["regulation_tradeoff"] = {
    "why": "'Rules' and 'unsafe practices' had no examples.",
    "scope": "Rules like workplace safety standards, food and drug inspections, limits on pollution, overdraft and hidden-fee rules, and licensing and paperwork for new businesses.",
}
T["regulation_tradeoff"] = trade(
    S("Business rules protecting workers, consumers and the environment should be stronger, even if prices rise and fewer businesses start.",
      yes=["Tougher workplace safety, food inspection and pollution rules", "Rules against hidden fees and overdraft charges"],
      no=["Rolling back safety or pollution rules to lower costs"]),
    S("There should be fewer rules on business so it grows and prices stay low, even if more people are harmed by unsafe practices.",
      yes=["Cutting paperwork and licensing for new businesses", "Rolling back safety, fee and pollution rules that raise costs"],
      no=["New rules that raise prices or slow business growth"]),
    S("You weigh protections and fewer rules about equally.",
      means=["You'd judge each rule, like a safety standard or fee limit, by whether its protection is worth its cost"]))

C["precaution_tradeoff"] = {
    "why": "No examples of products or harms.",
    "scope": "New products in general, such as new chemicals in household goods, new food additives, medical devices, e-cigarettes and self-driving cars.",
}
T["precaution_tradeoff"] = trade(
    S("Companies should prove new products are safe before selling them, even if useful products are delayed for years.",
      yes=["Safety testing and approval before new chemicals, additives, devices or self-driving cars go on sale"],
      no=["Selling first and pulling products only after harm shows up"]),
    S("New products should be allowed on sale and problems fixed as they appear, even if some people are harmed first.",
      yes=["Letting new chemicals, devices and self-driving cars on the market without long pre-approval", "Recalls and lawsuits after problems appear"],
      no=["Long approval processes before sale"]),
    S("You weigh caution and speed about equally.",
      means=["You'd want pre-approval for products with serious risks and fast approval for the rest"]))

T["big_company_breakup"] = [
    S("Break up companies that control most of their market, even if their prices are low.",
      yes=["Splitting up dominant firms in fields like online search or meatpacking"],
      no=["Leaving dominant firms alone because prices are low"]),
    S("Break up dominant companies only if they're proven to hurt consumers, workers or competitors.",
      yes=["Antitrust cases against firms shown to cause harm"],
      no=["Breaking up firms just for being big", "Leaving harmful monopolies alone"]),
    S("Leave dominant companies as they are, but block them from buying rivals.",
      yes=["Blocking acquisitions by the biggest firms"],
      no=["Breaking up existing companies"]),
    S("Leave dominant companies alone; size usually reflects success.",
      yes=["Leaving market leaders and their acquisitions alone"],
      no=["Antitrust break-ups", "Blocking their mergers"]),
]

T["merger_rules"] = [
    S("Block most large mergers unless the companies prove they'll help customers and workers.",
      yes=["Making merging companies prove the benefits first"],
      no=["Approving mergers unless the government proves harm"]),
    S("Review each merger and block those likely to raise prices or cut wages.",
      yes=["Case-by-case review that weighs prices and wages"],
      no=["Blocking most mergers by default", "Waving most mergers through"]),
    S("Approve most mergers unless they'd clearly raise prices.",
      yes=["A high bar for blocking a merger"],
      no=["Blocking mergers over wages or size alone"]),
    S("Rarely interfere with mergers.",
      yes=["Letting companies merge as they choose"],
      no=["Most government merger reviews and challenges"]),
]

T["bank_rules"] = [
    S("Break up the largest banks.",
      yes=["Splitting up banks with more than $100 billion in assets"],
      no=["Leaving the largest banks intact"]),
    S("Make large banks hold more of their own money as a cushion against losses.",
      yes=["Higher capital requirements for the largest banks"],
      no=["Breaking banks up", "Loosening today's rules"]),
    S("Keep rules on large banks about as strict as today.",
      yes=["Today's capital and oversight rules"],
      no=["Tightening or loosening them"]),
    S("Loosen rules on large banks so they can lend more.",
      yes=["Lower capital requirements and lighter oversight"],
      no=["Stricter rules on big banks"]),
]

T["bailouts"] = [
    S("Government should take over a failing giant and run it until it can be sold or wound down.",
      yes=["Temporary government ownership of a failing bank or company"],
      no=["Letting the company collapse", "Loans with no government control"]),
    S("Government should lend a failing giant money to survive, with strict conditions.",
      yes=["Rescue loans like those in 2008, with conditions"],
      no=["Letting the company fail", "Taking it over outright"]),
    S("Protect insured deposits only and let the company fail.",
      yes=["Covering insured bank deposits", "Letting shareholders and lenders take the losses"],
      no=["Rescue loans or takeovers"]),
    S("Let a failing giant collapse with no government help.",
      yes=["No bailout, even if it causes a recession"],
      no=["Any rescue, loan or takeover"]),
]

T["licensing"] = [
    S("Require a government license for more jobs, to protect customers.",
      yes=["New licensing requirements for more occupations"],
      no=["Removing license requirements"]),
    S("Keep about today's licensing requirements.",
      yes=["Today's licenses for jobs like barbers and electricians"],
      no=["Adding or removing license requirements"]),
    S("Require licenses only where health or safety is clearly at risk.",
      yes=["Licenses for jobs like electricians", "Dropping licenses for jobs like interior designers"],
      no=["Licensing jobs with little safety risk"]),
    S("Remove most license requirements.",
      yes=["Relying on reviews and private certifications instead of government licenses"],
      no=["Most government licensing for jobs"]),
]

T["price_controls"] = [
    S("Government should cap prices on essentials like food, water and gas when inflation is high.",
      yes=["Price caps on essentials during high inflation", "Bans on price gouging after disasters"],
      no=["Letting prices rise freely"]),
    S("Ban sharp price hikes only during declared emergencies.",
      yes=["Anti-gouging laws after disasters"],
      no=["Price caps during ordinary inflation", "Letting prices spike after disasters"]),
    S("Don't limit prices for essentials, even after disasters.",
      yes=["Letting high prices draw in more supply"],
      no=["Price caps", "Anti-gouging laws"]),
]

C["economic_system"] = {
    "why": "'Strong rules', 'large safety net' and 'modest rules' had no reference points.",
    "options": {
        "2": "Private businesses and markets, with strong government rules and a large safety net, as in much of Western Europe",
        "3": "Private businesses and markets, with modest rules and a basic safety net, roughly like the US today",
    },
}
T["economic_system"] = [
    S("Most major industries should be owned by the public or by their workers.",
      yes=["Public or worker ownership of most big industries"],
      no=["An economy run mainly by private companies"]),
    S("Private businesses, but government should run key industries like energy and health care.",
      yes=["Government-run energy and health care", "Private businesses elsewhere"],
      no=["Public ownership of most industries", "Private energy and health care"]),
    S("Markets with strong rules and a large safety net, as in much of Western Europe.",
      yes=["Strong labor, consumer and environmental rules", "Universal health care and generous benefits"],
      no=["Government running whole industries", "Shrinking rules and benefits to US levels or below"]),
    S("Markets with modest rules and a basic safety net, roughly like the US today.",
      yes=["Today's mix of regulation and safety-net programs"],
      no=["European-style benefits and rules", "Cutting government to the minimum"]),
    S("Free markets with as little government as possible.",
      yes=["Cutting business rules and safety-net programs to a minimum"],
      no=["Government-run industries", "A large safety net"]),
]

T["public_ownership"] = [
    S("Government should own and run most utilities like electricity, railroads and internet service.",
      yes=["Public ownership of most power, rail and internet systems"],
      no=["Leaving them mostly to private companies"]),
    S("Government should run some of them, where private companies haven't served people well.",
      yes=["City-owned power or internet where private service is poor or costly"],
      no=["Public ownership of most utilities", "Barring public ownership"]),
    S("Government should run them only where there's no private provider.",
      yes=["Public utilities only as a last resort"],
      no=["Public ownership competing with private companies"]),
    S("Private companies should run them.",
      yes=["Leaving electricity, rail and internet to private companies"],
      no=["Government-owned utilities"]),
]

T["workers_on_boards"] = [
    S("Workers should elect about half the board at large companies.",
      yes=["Requiring companies with 1,000+ workers to give employees half the board seats, as Germany does for its largest firms"],
      no=["Boards elected only by shareholders"]),
    S("Workers should elect about a third of the board at large companies.",
      yes=["Requiring a third of board seats be elected by employees"],
      no=["Half the board", "No requirement"]),
    S("Allow worker board seats if companies choose, but don't require them.",
      yes=["Voluntary worker representation"],
      no=["Requiring worker-elected board members"]),
    S("Workers shouldn't elect board members.",
      yes=["Boards chosen by shareholders only"],
      no=["Any worker-elected board seats"]),
]

T["noncompetes"] = [
    S("Ban noncompete agreements for all workers.",
      yes=["Letting any worker take a job with a competitor"],
      no=["Noncompetes, even for executives"]),
    S("Allow noncompetes only for top executives.",
      yes=["Banning noncompetes for ordinary workers"],
      no=["Noncompetes for ordinary workers", "Banning them for executives"]),
    S("Allow noncompetes, but limit them to a year or less.",
      yes=["Noncompetes capped at one year"],
      no=["Banning noncompetes outright", "Noncompetes longer than a year"]),
    S("Allow noncompetes; both sides agreed to the contract.",
      yes=["Enforcing noncompetes as written"],
      no=["Bans or limits on noncompetes"]),
]

T["right_to_repair"] = [
    S("Companies should make parts, tools and manuals available for most products.",
      yes=["Right-to-repair laws for phones, cars, farm equipment and more"],
      no=["Letting companies restrict who can repair their products"]),
    S("Require repair access only where it matters most, like cars and farm equipment.",
      yes=["Right-to-repair for cars and farm equipment"],
      no=["Requiring it for phones and most products", "No requirement"]),
    S("Companies should decide whether to share parts and manuals.",
      yes=["Letting manufacturers control repairs"],
      no=["Right-to-repair laws"]),
]

T["farm_subsidies"] = [
    S("Expand farm payments and subsidized crop insurance.",
      yes=["More federal support when prices or harvests fall"],
      no=["Cutting or capping farm programs"]),
    S("Keep farm payments and crop insurance about as they are.",
      yes=["Today's farm programs"],
      no=["Expanding or cutting them"]),
    S("Limit farm payments to small and mid-size farms.",
      yes=["Cutting off large farms and agribusiness"],
      no=["Payments to the biggest farms"]),
    S("Phase out farm payments and subsidized insurance.",
      yes=["Ending federal farm subsidies over time"],
      no=["Keeping them for any farm size"]),
]

T["business_incentives"] = [
    S("States and cities should offer tax breaks to attract factories and offices.",
      yes=["Tax-break deals to bring jobs"],
      no=["Banning these deals"]),
    S("Allow these tax breaks only with strict job guarantees and repayment if the company leaves.",
      yes=["Clawbacks if promised jobs don't appear"],
      no=["Deals with no guarantees", "Banning deals outright"]),
    S("Ban tax-break deals for individual companies.",
      yes=["Ending special tax deals to lure companies"],
      no=["Any company-specific incentives"]),
]

T["fed_independence"] = [
    S("The Federal Reserve alone should set interest rates, free of pressure from elected officials.",
      yes=["Fed independence from the president and Congress"],
      no=["Presidents or Congress pressuring the Fed"]),
    S("The Fed should set rates, but Congress should review its decisions more closely.",
      yes=["More congressional oversight and audits of the Fed"],
      no=["Presidential control of rates", "Leaving the Fed unchecked"]),
    S("The president should be able to direct the Federal Reserve.",
      yes=["Letting the president tell the Fed where to set rates, under either party"],
      no=["Fed independence"]),
]

C["infrastructure"] = {
    "why": "'Much more' and 'somewhat more' had no scale.",
    "scope": "Compared with today. “Much more” means about half again or more; “somewhat more” means a modest increase. Assume the money is borrowed or comes from taxes.",
}
T["infrastructure"] = [
    S("Spend much more on roads, bridges, water systems and the power grid.",
      yes=["Raising federal infrastructure spending by about half or more", "Borrowing or taxing to pay for it"],
      no=["Keeping spending flat", "Shifting it to states"]),
    S("Spend somewhat more on infrastructure.",
      yes=["A modest increase in federal infrastructure spending"],
      no=["A large increase", "Cutting infrastructure spending"]),
    S("Keep infrastructure spending about the same.",
      yes=["Today's federal infrastructure budget"],
      no=["Raising or cutting it"]),
    S("Spend less on infrastructure; leave more to states and private companies.",
      yes=["Cutting federal infrastructure spending", "More toll roads and private investment"],
      no=["New federal infrastructure spending"]),
]

T["min_wage"] = [
    S("A federal minimum wage of $20 an hour or more, rising with inflation.",
      yes=["Raising the federal minimum from $7.25 to $20+", "Automatic yearly raises tied to inflation"],
      no=["A $15 minimum", "Keeping $7.25"]),
    S("A federal minimum wage of about $15 an hour, rising with inflation.",
      yes=["Raising the federal minimum from $7.25 to about $15", "Automatic yearly raises tied to inflation"],
      no=["Going as high as $20", "Keeping $7.25", "Ending the federal minimum"]),
    S("A federal minimum wage of about $10 to $12 an hour.",
      yes=["A modest raise from $7.25"],
      no=["$15 or more", "Keeping $7.25"]),
    S("Keep the federal minimum wage at $7.25 an hour.",
      yes=["Leaving it where it's been since 2009", "Letting states set higher minimums"],
      no=["Any federal increase", "Ending the federal minimum"]),
    S("No federal minimum wage; leave it to states and employers.",
      yes=["Repealing the federal minimum wage"],
      no=["Any national wage floor"]),
]

if __name__ == "__main__":
    write("D02", T)
    write_clarity("D02", C)
