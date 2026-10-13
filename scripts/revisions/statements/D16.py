"""Guns."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["handgun_purchase"] = [
    S("Ban handgun sales to most civilians.",
      yes=["Ending handgun sales to ordinary adults"], no=["Licensed handgun ownership"]),
    S("Require a license with safety training, plus a background check for every handgun sale.",
      yes=["A permit-to-purchase with training", "Background checks on private sales too"], no=["Buying without a license"]),
    S("Require a background check for every handgun sale, including private sales, but no license.",
      yes=["Universal background checks"], no=["A license requirement", "Exempting private sales"]),
    S("Keep current federal handgun law.",
      yes=["Checks at licensed dealers only"], no=["Universal checks or licenses", "Ending dealer checks"]),
    S("Fewer federal rules on buying handguns, such as ending required background checks.",
      yes=["Ending federal background check requirements"], no=["Checks or licenses"]),
]

T["private_sale_checks"] = [
    S("Require a background check for every private gun sale or transfer, even between family.",
      yes=["Checks on all transfers, including family gifts and loans"], no=["Exemptions for family"]),
    S("Require checks for all private sales, but not gifts or loans to family and close friends.",
      yes=["Universal checks with family and friend exemptions"], no=["Checking family transfers", "Exempting private sales"]),
    S("Require checks only for private sales at gun shows and online.",
      yes=["Closing the gun show and online sale gap"], no=["Checks on every private sale"]),
    S("Private gun sales shouldn't require a background check.",
      yes=["Leaving private sales unchecked"], no=["Any private-sale check"]),
]

T["semi_auto_rifles"] = [
    S("Ban new sales of rifles like the AR-15 and buy back the ones people own.",
      yes=["A sales ban plus a buyback"], no=["Letting owners keep them"]),
    S("Ban new sales of rifles like the AR-15; owners keep the ones they have.",
      yes=["A ban on new sales, like the 1994–2004 federal ban"], no=["A buyback", "Continued sales"]),
    S("Sell rifles like the AR-15 only to people 21+ with a license and training.",
      yes=["Age 21, license and training for these rifles"], no=["A ban", "Sales at 18 with only a background check"]),
    S("Sell rifles like the AR-15 with a background check, as most states do now.",
      yes=["Today's rules"], no=["Bans, licenses or higher age limits"]),
    S("Sell rifles like the AR-15 with no federal background check.",
      yes=["Ending federal checks for these rifles"], no=["Any federal check or ban"]),
]

T["magazine_limit"] = [
    S("Limit magazines to 10 rounds or fewer.",
      yes=["Banning magazines over 10 rounds"], no=["Standard 15–30 round magazines"]),
    S("Limit magazines to about 15 to 20 rounds.",
      yes=["A cap around 15–20 rounds"], no=["A 10-round cap", "No limit"]),
    S("No limit on magazine size.",
      yes=["Magazines of any size"], no=["Any magazine limit"]),
]

T["concealed_carry"] = [
    S("Concealed carry should generally not be allowed, except for police and security guards.",
      yes=["Ending concealed carry for ordinary civilians"], no=["Carry permits for the public"]),
    S("Concealed carry should require a permit with training and a background check.",
      yes=["Permits with required training"], no=["Permitless carry"]),
    S("Concealed carry should require a permit with a background check only.",
      yes=["Permits without required training"], no=["Training requirements", "Permitless carry"]),
    S("No permit should be needed to carry a concealed handgun.",
      yes=["Permitless carry for anyone who can legally own a gun"], no=["Permit requirements"]),
]
T["carry_locations"] = existing("D16", "carry_locations")

T["red_flag"] = [
    S("Courts should be able to temporarily take guns from someone dangerous, at the request of police or family.",
      yes=["Red flag laws letting family or police petition"], no=["Requiring a conviction first"]),
    S("Courts can take guns at police request only, with a quick hearing.",
      yes=["Police-only petitions with prompt hearings"], no=["Family petitions", "No red flag law"]),
    S("Guns should be taken only after a criminal conviction or formal mental health commitment.",
      yes=["Repealing red flag laws"], no=["Taking guns before a conviction or commitment"]),
]
T["red_flag_cases"] = existing("D16", "red_flag_cases")

T["gun_purchase_age"] = [
    S("21 to buy any gun.", yes=["Raising the minimum age for rifles and shotguns to 21"], no=["Gun purchases at 18"]),
    S("21 for handguns and semi-automatic rifles; 18 for hunting rifles and shotguns.",
      yes=["Raising the age for AR-15-style rifles to 21"], no=["21 for all guns", "18 for semi-automatic rifles"]),
    S("21 for handguns from dealers; 18 for rifles and shotguns, as today.", yes=["Today's federal age rules"], no=["Raising or lowering them"]),
    S("18 to buy any gun.", yes=["Letting 18-year-olds buy handguns from dealers"], no=["Age-21 limits"]),
]

T["second_amendment_meaning"] = [
    S("The Second Amendment protects only states' right to maintain militias.",
      means=["It gives individuals no personal right to own guns"]),
    S("It protects an individual right to own guns, subject to broad regulation.",
      means=["Licensing, bans on some weapons and similar rules fit within it"]),
    S("It protects an individual right to own guns, with only narrow limits.",
      means=["Only limited rules, like barring felons, fit within it"]),
    S("It protects an individual right with almost no limits.",
      means=["Almost any gun law, including licenses and weapon bans, violates it"]),
]

T["self_defense_law"] = [
    S("People attacked in public should retreat first if they safely can before using deadly force.",
      yes=["A duty to retreat in public"], no=["Stand-your-ground laws"]),
    S("Only someone who started the conflict should have to retreat.",
      yes=["A duty to retreat for the person who started it"], no=["A general duty to retreat"]),
    S("People can stand their ground anywhere they have a right to be.",
      yes=["Stand-your-ground laws"], no=["A duty to retreat"]),
]

T["gun_maker_liability"] = [
    S("Gun makers and sellers should be suable like makers of other dangerous products.",
      yes=["Repealing the 2005 shield law"], no=["Today's protection"]),
    S("Gun makers and sellers should be suable only if they broke the law or marketed irresponsibly.",
      yes=["Suits over illegal sales or reckless marketing"], no=["Full repeal", "Full protection"]),
    S("Keep today's legal protection for gun makers and sellers.",
      yes=["The 2005 shield law as it is"], no=["Opening them to lawsuits"]),
]

T["gun_registry"] = [
    S("A national registry of who owns every gun.", yes=["Registering all guns"], no=["Today's ban on a registry"]),
    S("A national registry for handguns and semi-automatic rifles only.", yes=["Registering those guns"], no=["Registering all guns", "No registry"]),
    S("No national gun registry.", yes=["Keeping the ban on a federal registry"], no=["Any gun registry"]),
]

T["suppressors"] = [
    S("Ban suppressors for civilians.", yes=["Ending civilian suppressor sales"], no=["Legal suppressor ownership"]),
    S("Keep today's suppressor rules.", yes=["Federal registration and approval"], no=["A ban", "Dropping suppressor registration"]),
    S("Treat suppressors like ordinary gun parts.", yes=["Ending federal registration for suppressors"], no=["Registration or bans"]),
]

if __name__ == "__main__":
    write("D16", T)
    write_clarity("D16", C)
