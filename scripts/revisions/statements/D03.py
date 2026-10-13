"""Health care and social insurance."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["coverage_guarantee"] = [
    S("The federal government should make sure everyone is insured, through one government plan.",
      yes=["A single government health plan covering every American"],
      no=["Leaving coverage to individuals and employers"]),
    S("The federal government should make sure everyone is insured, through whatever mix of public and private coverage works.",
      yes=["A guarantee of coverage for every American", "Private plans and government programs side by side"],
      no=["Leaving some people uninsured", "Requiring one government plan only"]),
    S("No guarantee for everyone, but help people with low incomes or serious health conditions get covered.",
      yes=["Programs like Medicaid and subsidies for people with low incomes or serious illnesses"],
      no=["Guaranteed coverage for everyone", "Ending help for low-income and sick people"]),
    S("Health coverage is each person's own responsibility.",
      yes=["Leaving insurance to individuals and their employers"],
      no=["Government guarantees or subsidies for coverage"]),
]

T["medicare_age"] = [
    S("Everyone of any age should be in Medicare automatically.",
      yes=["Medicare for all ages, paid with taxes or premiums"],
      no=["Keeping Medicare mainly for people 65 and older"]),
    S("Anyone of any age should be able to buy into Medicare.",
      yes=["A Medicare buy-in for people under 65"],
      no=["Enrolling everyone automatically", "Keeping it for 65+ only"]),
    S("Lower the Medicare age to 60.",
      yes=["Opening Medicare to people 60 to 64"],
      no=["Opening it to all ages", "Keeping it at 65"]),
    S("Keep Medicare at 65 and older.",
      yes=["Today's Medicare age of 65"],
      no=["Lowering or raising the age"]),
    S("Raise the Medicare age gradually to 67.",
      yes=["Phasing the eligibility age up from 65 to 67"],
      no=["Keeping it at 65", "Lowering the Medicare age"]),
]

T["private_insurance_role"] = [
    S("Private insurance should only cover extras a government plan doesn't.",
      yes=["A government plan as everyone's main coverage", "Private plans only for extras like private rooms"],
      no=["Private insurance as a full alternative"]),
    S("Private insurance should compete with a government plan, and people choose.",
      yes=["A public option alongside private insurance"],
      no=["Pushing private insurance out", "Limiting the public plan to people private insurers won't cover"]),
    S("Private insurance should stay the main system, with a government plan only for those who can't get covered.",
      yes=["Private insurance for most people", "A public plan as a backstop"],
      no=["A public plan anyone can choose"]),
]

T["drug_prices"] = [
    S("Government should set prices for all brand-name drugs, for everyone.",
      yes=["Federal price-setting for every brand-name drug, for all buyers"],
      no=["Leaving most drug prices to drugmakers"]),
    S("Government should negotiate prices for many more drugs, for Medicare and private insurance.",
      yes=["Expanding negotiation beyond today's limited list", "Applying negotiated prices to private insurance too"],
      no=["Setting all prices", "Keeping negotiation as limited as today"]),
    S("Keep Medicare's negotiation for a limited number of drugs, as today.",
      yes=["Today's Medicare negotiation program"],
      no=["Expanding negotiation to more drugs", "Ending Medicare negotiation"]),
    S("End government drug price negotiation; let competition set prices.",
      yes=["Repealing Medicare drug price negotiation"],
      no=["Any government role in setting drug prices"]),
]

T["drug_import"] = [
    S("People should be able to buy cheaper drugs imported from any country with safety standards like ours.",
      yes=["Imports from Canada, Europe and similar countries through licensed pharmacies"],
      no=["Limiting imports to small state programs"]),
    S("Allow imported drugs only through limited state programs approved by the FDA.",
      yes=["FDA-approved state import programs, like Florida's"],
      no=["Open imports from any safe country", "Banning imports"]),
    S("Don't allow drug imports; they're too hard to keep safe.",
      yes=["Keeping the ban on importing prescription drugs"],
      no=["State or national import programs"]),
]

T["medicaid_scope"] = [
    S("Medicaid should cover all low-income adults in every state, mostly paid by the federal government.",
      yes=["Requiring every state to expand Medicaid", "Federal money paying most of the cost"],
      no=["Letting states skip expansion", "Capping federal Medicaid money"]),
    S("Keep Medicaid as it is: each state chooses whether to cover all low-income adults.",
      yes=["Today's optional expansion"],
      no=["Requiring expansion", "Capping federal money"]),
    S("Limit federal Medicaid money per person and give states more control.",
      yes=["Per-person caps on federal Medicaid spending", "More state say over who's covered"],
      no=["Requiring states to expand Medicaid"]),
    S("Give each state a fixed amount for Medicaid and let it decide everything.",
      yes=["Block grants with full state control"],
      no=["Federal rules on who must be covered"]),
]

T["medicaid_work"] = [
    S("Medicaid coverage shouldn't depend on work.",
      yes=["Repealing the 2025 work requirement"],
      no=["Any work, volunteer or school requirement for Medicaid"]),
    S("Require about 80 hours a month of work, volunteering or school, with exemptions.",
      yes=["The 2025 law's 80-hour requirement", "Exemptions for parents, caregivers and students"],
      no=["No requirement", "Stricter rules"]),
    S("Require more hours or allow fewer exemptions than the 2025 law.",
      yes=["A stricter Medicaid work requirement than 80 hours a month"],
      no=["Today's exemptions for parents, caregivers and students as they stand"]),
]

T["ss_shortfall"] = [
    S("Close Social Security's gap only with taxes, mainly on high earners, and keep or raise benefits.",
      yes=["Higher Social Security taxes on high earners", "Keeping or raising benefits"],
      no=["Raising the retirement age", "Any benefit cuts"]),
    S("Close the gap mostly with taxes, plus small benefit changes.",
      yes=["Tax increases as most of the fix", "Minor benefit adjustments"],
      no=["Large benefit cuts", "Taxes alone"]),
    S("Close the gap with an even mix of tax increases and benefit cuts.",
      yes=["A deal that splits the fix about evenly"],
      no=["Taxes alone", "Benefit cuts alone"]),
    S("Close the gap mostly by slowing benefit growth, with small tax increases.",
      yes=["Raising the retirement age or slowing benefit growth", "Small tax increases"],
      no=["Large tax increases"]),
    S("Close the gap only by slowing benefit growth; no tax increases.",
      yes=["Raising the retirement age and trimming future benefits"],
      no=["Any Social Security tax increase"]),
]

T["ss_retirement_age"] = [
    S("Lower the full retirement age to 65.",
      yes=["Full benefits at 65 instead of 67"],
      no=["Keeping 67", "Raising the age"]),
    S("Keep the full retirement age at 67.",
      yes=["Today's age of 67"],
      no=["Raising or lowering it"]),
    S("Raise the full retirement age to 68 or 69.",
      yes=["Gradually raising it to 68–69 for people now under 50"],
      no=["Keeping 67", "Going to 70 or higher"]),
    S("Raise the full retirement age to 70 or higher.",
      yes=["Gradually raising it to 70+ for people now under 50"],
      no=["Keeping 67"]),
]

T["ss_payroll_cap"] = [
    S("Apply Social Security tax to all wages, with no cap.",
      yes=["Taxing wages above $184,500 at the full 12.4%"],
      no=["Keeping the cap"]),
    S("Apply Social Security tax to wages above $400,000, leaving a gap in between.",
      yes=["Taxing wages over $400,000", "No new tax on wages between $184,500 and $400,000"],
      no=["Taxing all wages", "Keeping today's cap"]),
    S("Raise the Social Security wage cap somewhat, but keep one.",
      yes=["A higher cap than $184,500"],
      no=["Removing the cap", "Leaving it as is"]),
    S("Keep the Social Security wage cap as it is.",
      yes=["Today's $184,500 cap"],
      no=["Raising or removing the cap"]),
    S("Lower the Social Security tax rate, even if future benefits shrink.",
      yes=["A rate below 12.4%", "Smaller future benefits"],
      no=["Raising the cap or the rate"]),
]

T["medicare_structure"] = [
    S("Expand Medicare to cover dental, vision and hearing, paid with higher taxes.",
      yes=["Adding dental, vision and hearing coverage", "Higher taxes to pay for it"],
      no=["Vouchers or private accounts"]),
    S("Keep Medicare as it is, adding taxes or savings to pay for it.",
      yes=["Today's Medicare, with new funding or savings"],
      no=["Major expansion", "Turning it into vouchers or accounts"]),
    S("Give future retirees a set amount to choose between traditional Medicare and private plans.",
      yes=["A fixed payment per retiree (premium support)"],
      no=["Open-ended traditional Medicare", "Adding new benefits"]),
    S("Gradually replace Medicare with personal health savings accounts.",
      yes=["Phasing Medicare out in favor of individual accounts"],
      no=["Traditional Medicare for future retirees"]),
]

C["medicare_means_test"] = {
    "why": "Didn't say how much more higher-income retirees pay today.",
    "scope": "Today single retirees with incomes over about $100,000 pay higher premiums for doctor visits, rising to about three times the standard premium at the top.",
}
T["medicare_means_test"] = [
    S("Higher-income retirees should pay much more for Medicare than today.",
      yes=["Much steeper Medicare premiums for retirees with high incomes", "Lowering the income level where higher premiums start"],
      no=["Today's premium scale"]),
    S("Higher-income retirees should pay somewhat more for Medicare than today.",
      yes=["Modestly higher premiums for high-income retirees"],
      no=["Much steeper premiums", "Equal premiums for all"]),
    S("Keep today's income-based Medicare premiums.",
      yes=["Today's higher premiums above about $100,000"],
      no=["Raising or removing them"]),
    S("Everyone paid in and should pay the same for Medicare.",
      yes=["One Medicare premium for all retirees"],
      no=["Income-based Medicare premiums"]),
]

T["ss_private_accounts"] = [
    S("Social Security should stay a guaranteed benefit, with no personal accounts.",
      yes=["Keeping Social Security fully as a guaranteed benefit"],
      no=["Diverting Social Security taxes into investment accounts"]),
    S("Personal accounts only as an extra on top of Social Security.",
      yes=["Add-on retirement accounts that don't take money from Social Security"],
      no=["Carving accounts out of Social Security taxes"]),
    S("Workers should be able to put part of their Social Security tax into personal accounts.",
      yes=["Optional personal accounts funded from Social Security taxes"],
      no=["Keeping the whole tax in the traditional system", "Replacing Social Security outright"]),
    S("Gradually replace Social Security with personal accounts.",
      yes=["Phasing out the guaranteed benefit for personal investment accounts"],
      no=["Social Security as a guaranteed benefit for future retirees"]),
]

T["insurance_mandate"] = [
    S("People should be required to have health insurance, with a penalty if they don't.",
      yes=["Bringing back a penalty for going uninsured"],
      no=["Leaving insurance as a personal choice"]),
    S("No penalty, but sign uninsured people up automatically for a free basic plan.",
      yes=["Automatic enrollment in a free basic plan"],
      no=["A penalty for going uninsured", "Leaving people uninsured"]),
    S("Whether to buy health insurance is a personal choice.",
      yes=["Keeping the penalty at $0"],
      no=["Mandates or automatic enrollment"]),
]

T["preexisting_conditions"] = [
    S("Insurers should never charge more or refuse coverage over past health problems, as today.",
      yes=["Keeping the ban on pre-existing condition pricing and denials"],
      no=["Letting insurers charge more for conditions like diabetes or cancer"]),
    S("Insurers can charge somewhat more for past health problems, but not refuse coverage.",
      yes=["Higher premiums for people with conditions like diabetes or cancer", "A ban on refusing them"],
      no=["Today's full ban", "Letting insurers refuse coverage"]),
    S("Insurers can charge more or refuse coverage, with a separate government plan for those turned down.",
      yes=["Letting insurers price or deny based on health history", "Government-funded high-risk pools"],
      no=["Today's ban on denials and higher prices"]),
]

T["school_vaccines"] = [
    S("Children should need vaccines like measles and polio for public and private schools.",
      yes=["School vaccine requirements covering every school"],
      no=["Leaving vaccines up to parents"]),
    S("Require vaccines for public schools only.",
      yes=["Vaccine requirements at public schools", "Letting private schools set their own rules"],
      no=["Requiring them at private schools", "No requirement anywhere"]),
    S("Recommend vaccines, but parents decide.",
      yes=["Ending school vaccine requirements"],
      no=["Requiring vaccines to attend school"]),
]
T["vaccine_exemptions"] = existing("D03", "vaccine_exemptions")

T["outbreak_gov_mandate"] = [
    S("During a serious outbreak, government should require most workers to be vaccinated.",
      yes=["Vaccine mandates for most workers in a serious outbreak"],
      no=["Leaving it to workers and employers"]),
    S("Require vaccination only for health care and other close-contact jobs.",
      yes=["Mandates for nurses, doctors and similar workers"],
      no=["Mandates for most workers", "No mandate at all"]),
    S("No government vaccine requirement for workers.",
      yes=["Leaving vaccination to each worker"],
      no=["Any government vaccine mandate for jobs"]),
]

T["outbreak_employer"] = [
    S("Any employer should be able to require its workers to be vaccinated during an outbreak.",
      yes=["Employer vaccine requirements at any workplace"],
      no=["Laws barring employer mandates"]),
    S("Only health care employers should be able to require vaccination.",
      yes=["Hospitals and clinics requiring vaccines", "Barring other employers from requiring them"],
      no=["Mandates at other workplaces"]),
    S("No employer should be able to require vaccination.",
      yes=["Laws banning employer vaccine mandates"],
      no=["Any employer requiring vaccines, even hospitals"]),
]

T["immigrant_health_benefits"] = [
    S("Everyone living here with a low enough income should be able to get Medicaid, whatever their status.",
      yes=["Medicaid for low-income people without legal status"],
      no=["Waiting periods for legal immigrants"]),
    S("Legal immigrants should get Medicaid right away, plus children whatever their status.",
      yes=["Ending the 5-year wait", "Coverage for children without legal status"],
      no=["Coverage for adults without legal status", "Keeping the wait"]),
    S("Most legal immigrants should get Medicaid after 5 years, as today.",
      yes=["Today's 5-year wait"],
      no=["Covering people without legal status", "Longer waits"]),
    S("Legal immigrants should wait 10 years or more for Medicaid.",
      yes=["Lengthening the wait from 5 years to 10+"],
      no=["Today's 5-year wait"]),
    S("Medicaid should be for citizens only.",
      yes=["Ending Medicaid eligibility for green card holders"],
      no=["Medicaid for any non-citizen"]),
]

T["water_fluoride"] = [
    S("Cities should add fluoride to drinking water, as health agencies recommend.",
      yes=["Fluoridating public water"],
      no=["State bans on fluoride"]),
    S("Each city should decide on fluoride.",
      yes=["Local choice on fluoridation"],
      no=["State or federal bans", "Requiring fluoride everywhere"]),
    S("Fluoride in drinking water should be banned.",
      yes=["Banning fluoride in public water, as Utah and Florida did in 2025"],
      no=["Cities adding fluoride"]),
]

T["food_additives"] = [
    S("Ban food additives allowed in the US but banned elsewhere.",
      yes=["Banning certain artificial dyes and additives other countries ban"],
      no=["Leaving them on the market"]),
    S("Require warning labels on those additives instead of banning them.",
      yes=["Clear warning labels on additives banned abroad"],
      no=["Banning those additives", "No labels"]),
    S("Trust US regulators' approval of food additives.",
      yes=["Leaving approved additives on the market without new labels"],
      no=["Bans or warning labels"]),
]

T["long_term_care"] = [
    S("Create a new government insurance program for nursing home and home care for everyone.",
      yes=["Universal long-term care insurance"],
      no=["Requiring people to spend down savings first"]),
    S("Government should help middle-income families with long-term care too, not only the poor.",
      yes=["Aid for nursing home and home care for middle-income families"],
      no=["A universal program", "Keeping aid for the poor only"]),
    S("Keep today's long-term care system.",
      yes=["Medicaid paying after people spend down their savings"],
      no=["New programs", "Cutting help"]),
    S("Families and private insurance should pay for long-term care, with less government help.",
      yes=["Relying on families and private insurance", "Cutting Medicaid long-term care spending"],
      no=["New government long-term care programs"]),
]

T["health_coverage"] = [
    S("One government plan should cover everyone.",
      yes=["A single-payer system like Medicare for All", "Little or no role for private insurance"],
      no=["Today's mix of private and public coverage"]),
    S("Everyone should be able to choose a government plan or private insurance.",
      yes=["A public option alongside private insurance"],
      no=["Ending private insurance", "Keeping today's system unchanged"]),
    S("Keep roughly today's system: mostly private, with government programs for older, low-income and hard-to-insure people.",
      yes=["Today's Medicare, Medicaid and marketplace subsidies"],
      no=["A public option or single payer", "Cutting those programs"]),
    S("Mostly private insurance, with smaller government programs than today.",
      yes=["Shrinking Medicaid and marketplace subsidies"],
      no=["A public option", "Expanding government coverage"]),
    S("Government shouldn't provide health coverage; private insurance or paying directly.",
      yes=["Ending government health programs"],
      no=["Medicare, Medicaid or any public plan"]),
]

if __name__ == "__main__":
    write("D03", T)
    write_clarity("D03", C)
