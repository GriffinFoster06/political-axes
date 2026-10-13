"""Housing and land use."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, write, write_clarity  # noqa: E402

C, T = {}, {}

T["zoning_density"] = [
    S("Cities should be required to allow apartment buildings in most neighborhoods.",
      yes=["Ending single-family-only zoning in high-cost cities and suburbs", "Apartment buildings on most residential streets"],
      no=["Keeping neighborhoods limited to single houses"]),
    S("Allow duplexes and townhomes in single-family neighborhoods, but not large apartment buildings.",
      yes=["Two- to four-unit homes and townhomes on single-family lots"],
      no=["Large apartment buildings in those neighborhoods", "Keeping single-family-only zoning"]),
    S("Each neighborhood should decide what can be built.",
      yes=["Neighborhood votes or local boards deciding on new housing types"],
      no=["City or state rules requiring more housing types"]),
    S("Keep single-family zoning.",
      yes=["Neighborhoods limited to one house per lot"],
      no=["Duplexes, townhomes or apartments in those neighborhoods"]),
]

T["zoning_state_override"] = [
    S("States should override local zoning whenever cities fall short of housing goals.",
      yes=["State laws forcing cities to allow more homes when they miss targets"],
      no=["Leaving zoning entirely to cities"]),
    S("States should override local zoning only near transit and job centers.",
      yes=["State-required apartments near train stations and job hubs"],
      no=["Statewide overrides everywhere", "No state role"]),
    S("Zoning should stay local.",
      yes=["Cities and towns setting their own zoning"],
      no=["State laws overriding local zoning"]),
]

T["housing_approval"] = [
    S("Housing that meets every rule should be approved automatically.",
      yes=["By-right approval with no hearings", "Ending lawsuits that delay rule-following projects"],
      no=["Public hearings for projects that already follow the rules"]),
    S("Approve rule-following housing after a short public comment period.",
      yes=["A brief comment period, then approval"],
      no=["Long hearings and lawsuits", "Approval with no public input"]),
    S("Neighbors should have a say through hearings and the right to sue.",
      yes=["Public hearings and lawsuits over new housing, even if it meets the rules"],
      no=["Automatic approval"]),
]

T["rent_control"] = [
    S("Cities should strictly limit rent increases, such as to inflation.",
      yes=["Capping yearly rent increases for existing tenants at inflation"],
      no=["Exempting new buildings", "No limits"]),
    S("Moderate limits on rent increases, with new buildings exempt.",
      yes=["Caps of about inflation plus a few percent", "Exempting newly built housing"],
      no=["Strict inflation-only caps", "No limits"]),
    S("Limit rent increases only temporarily during emergencies.",
      yes=["Emergency caps after disasters"],
      no=["Permanent rent control"]),
    S("No limits on rent increases.",
      yes=["Letting landlords set rents freely", "State bans on local rent control"],
      no=["Any rent control"]),
]

T["eviction_cause"] = [
    S("Landlords should need a specific reason to evict or not renew any tenant.",
      yes=["Just-cause eviction rules for all tenants"],
      no=["Ending a lease just because its term is up"]),
    S("Landlords should need a reason only for tenants who've lived there a year or more.",
      yes=["Just-cause protection after a year"],
      no=["Protection from day one", "No protection at all"]),
    S("Landlords can end a lease when its term ends.",
      yes=["Non-renewal without giving a reason"],
      no=["Just-cause eviction laws"]),
]

T["rent_vouchers"] = [
    S("Every eligible low-income family should get federal rent help.",
      yes=["Funding vouchers for all eligible households, up from about 1 in 4"],
      no=["Keeping help limited by funding"]),
    S("Help more families with rent vouchers than today.",
      yes=["Expanding voucher funding"],
      no=["Covering every eligible family", "Cutting vouchers"]),
    S("Keep rent help at about today's level.",
      yes=["Today's voucher funding"],
      no=["Expanding or cutting it"]),
    S("Help fewer families with rent; rely more on the private market.",
      yes=["Cutting federal rental help"],
      no=["Expanding vouchers"]),
]

T["public_housing"] = [
    S("Government should build and own a large amount of housing for people of all incomes.",
      yes=["Large-scale public housing open to all incomes, like Vienna's"],
      no=["Leaving housing to private builders"]),
    S("Government should build and own housing for low-income people.",
      yes=["More public housing for low-income families"],
      no=["Public housing for all incomes", "Leaving it all to the market"]),
    S("Government should pay private builders through tax credits instead of owning housing.",
      yes=["Tax credits for private affordable housing"],
      no=["Government-owned housing"]),
    S("Leave housing to the market.",
      yes=["No government building or subsidizing of housing"],
      no=["Public housing", "Affordable-housing tax credits"]),
]

T["encampments"] = [
    S("Allow people to camp in public until there's enough shelter or housing.",
      yes=["Letting people stay on sidewalks and in parks when they have nowhere else"],
      no=["Clearing camps without a place to go", "Fines or jail for camping"]),
    S("Clear camps only after offering each person a shelter bed.",
      yes=["Clearing camps once a bed is offered"],
      no=["Clearing without an offer", "Letting camps stay when beds are available"]),
    S("Ban camping and clear camps, even without enough shelter beds.",
      yes=["Clearing camps whether or not shelter is available"],
      no=["Letting people camp on sidewalks or in parks"]),
    S("Ban camping, with fines or jail for people who don't move.",
      yes=["Fines or jail for refusing to leave a camp"],
      no=["Tolerating public camping"]),
]

T["housing_first"] = [
    S("House homeless people first, with no requirement to be sober or in treatment.",
      yes=["Giving housing without conditions on drug use or treatment"],
      no=["Requiring sobriety or treatment first"]),
    S("House people first, but require treatment to keep the housing.",
      yes=["Housing tied to staying in treatment"],
      no=["Housing with no conditions", "Requiring sobriety before housing"]),
    S("Treatment or sobriety should come first, before housing.",
      yes=["Making sobriety or treatment a condition for getting housing"],
      no=["Housing with no conditions"]),
]

T["involuntary_treatment"] = [
    S("Keep treatment voluntary except when someone is an immediate danger.",
      yes=["Today's immediate-danger standard"],
      no=["Committing people who can't meet basic needs"]),
    S("Also require treatment when people can't meet basic needs like food and shelter.",
      yes=["Widening involuntary treatment to people who can't care for themselves"],
      no=["Keeping the narrow danger standard", "Long required hospital stays"]),
    S("Make it much easier to require treatment, including longer hospital stays.",
      yes=["Broader involuntary commitment", "Longer required hospital stays"],
      no=["Today's narrow standard"]),
]

T["investor_homes"] = [
    S("Ban large investment firms from buying single-family homes to rent out.",
      yes=["Barring firms with hundreds of homes from buying more"],
      no=["Letting large investors buy houses"]),
    S("Allow large investors to buy homes, but with limits or extra taxes.",
      yes=["Caps or extra taxes on large investors' home purchases"],
      no=["An outright ban", "No limits"]),
    S("Let large investment firms buy homes to rent; they add rental housing.",
      yes=["No limits on investor purchases"],
      no=["Bans or extra taxes on investors"]),
]

T["short_term_rentals"] = [
    S("Ban short-term rentals like Airbnb in most neighborhoods.",
      yes=["Banning whole-home nightly rentals in residential areas"],
      no=["Allowing them with registration"]),
    S("Allow short-term rentals only in the owner's own home.",
      yes=["Renting your own home or a room in it", "Banning investor-owned nightly rentals"],
      no=["Allowing any whole home to be rented nightly"]),
    S("Allow short-term rentals with registration and taxes.",
      yes=["Registration and hotel-style taxes for short-term rentals"],
      no=["Banning short-term rentals", "No rules"]),
    S("No limits on short-term rentals.",
      yes=["Letting owners rent their homes by the night freely"],
      no=["Bans or registration rules"]),
]

T["mortgage_deduction"] = [
    S("End the mortgage interest deduction and use the money for renters or first-time buyers.",
      yes=["Repealing the deduction", "Aid for renters or first-time buyers"],
      no=["Keeping the deduction"]),
    S("Keep the mortgage interest deduction only for smaller mortgages.",
      yes=["Lowering the cap on mortgages that qualify"],
      no=["Repealing the deduction", "Keeping it as is"]),
    S("Keep the mortgage interest deduction as it is.",
      yes=["Today's deduction"],
      no=["Cutting or expanding it"]),
    S("Expand the mortgage interest deduction to help more homeowners.",
      yes=["Letting homeowners who don't itemize claim it", "A higher cap"],
      no=["Limiting or repealing it"]),
]

C["transit_vs_roads"] = {
    "why": "Didn't say what kinds of spending are in play.",
    "scope": "Federal and state transportation spending. Transit means buses, subways, light rail and commuter trains; roads means highways, new lanes and bridges.",
}
T["transit_vs_roads"] = [
    S("Shift much more transportation money to transit and away from new roads.",
      yes=["Large increases for buses, subways and trains", "Fewer new highways and lanes"],
      no=["Today's split"]),
    S("Shift somewhat more transportation money to transit.",
      yes=["Modest increases for buses and trains"],
      no=["Cutting highway building sharply", "More for roads"]),
    S("Keep about today's split between transit and roads.",
      yes=["Today's transportation budgets"],
      no=["Shifting money either way"]),
    S("Put more transportation money into roads and highways.",
      yes=["More highways, lanes and bridges", "Less for transit"],
      no=["Shifting money to transit"]),
]

if __name__ == "__main__":
    write("D04", T)
    write_clarity("D04", C)
