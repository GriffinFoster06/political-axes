"""Drugs and personal liberty."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["marijuana_law"] = [
    S("Marijuana should be legal to grow and sell to adults, regulated like alcohol.",
      yes=["Licensed marijuana stores in every state", "Ending the federal ban"], no=["Fines or jail for adult use"]),
    S("Adults should be able to have small amounts of marijuana, but not buy it in stores.",
      yes=["Legal possession and home growing"], no=["Commercial marijuana stores", "Penalties for small amounts"]),
    S("Marijuana should be legal only for medical use with a doctor's recommendation.",
      yes=["Medical marijuana programs"], no=["Recreational marijuana sales or possession"]),
    S("Marijuana should be illegal, with fines but no jail for small amounts.",
      yes=["Civil fines for possession"], no=["Legal recreational use", "Jail for small amounts"]),
    S("Marijuana should be illegal, with jail possible for having it.",
      yes=["Criminal penalties, including jail, for possession"], no=["Legal or decriminalized marijuana"]),
]

T["marijuana_records"] = [
    S("Clear past convictions for small amounts of marijuana automatically.",
      yes=["Automatic expungement"], no=["Making people apply"]),
    S("Clear past marijuana possession convictions if the person applies.",
      yes=["Expungement on application"], no=["Automatic clearing", "Keeping all records"]),
    S("Keep past marijuana possession convictions on record.",
      yes=["Leaving old convictions in place"], no=["Expunging old marijuana convictions"]),
]

T["drug_possession"] = [
    S("Having small amounts of drugs like cocaine or heroin should be legal and regulated.",
      yes=["Legal, regulated sale of hard drugs to adults"], no=["Fines or arrests for possession"]),
    S("Possession of small amounts should get a civil fine or a referral to treatment, not a criminal charge.",
      yes=["Decriminalization with fines or treatment referrals"], no=["Legal sales", "Criminal charges"]),
    S("Possession should be a crime, but first offenses get treatment instead of jail.",
      yes=["Drug courts and diversion for first offenses"], no=["Decriminalizing possession", "Jail for first offenses"]),
    S("Possession should be a crime, with jail possible even for first offenses.",
      yes=["Jail as an option for any possession charge"], no=["Treatment-only or decriminalized approaches"]),
]

T["psychedelics"] = [
    S("Psilocybin should be legal for any adult.",
      yes=["Legal sales of magic mushrooms to adults"], no=["Limiting it to clinics or prescriptions"]),
    S("Psilocybin should be legal only in supervised settings, like a licensed center.",
      yes=["Licensed centers, as in Oregon and Colorado"], no=["Open sales", "A total ban"]),
    S("Psilocybin should be legal only as a prescribed treatment, if approved as a medicine.",
      yes=["FDA-approved psilocybin therapy"], no=["Recreational or center-based use"]),
    S("Psilocybin should be illegal.",
      yes=["Keeping psilocybin banned"], no=["Any legal psilocybin use"]),
]

T["supervised_sites"] = [
    S("Cities should be able to run supervised drug use sites, with federal funding.",
      yes=["Overdose prevention sites", "Federal money for them"], no=["Banning these sites"]),
    S("Cities can run supervised drug use sites if they choose, without federal funding.",
      yes=["Local choice on overdose prevention sites"], no=["Federal funding", "A federal ban"]),
    S("Supervised drug use sites should be illegal.",
      yes=["Shutting down sites like New York's"], no=["Any supervised use sites"]),
]

T["sports_betting"] = [
    S("Phone sports betting should be legal everywhere, with few limits.",
      yes=["Nationwide legal betting apps"], no=["Limits on ads or bet sizes"]),
    S("Phone sports betting should be legal where states choose, with limits on ads and bet sizes.",
      yes=["State-legalized betting apps", "Ad and bet-size limits"], no=["Few limits", "Banning apps"]),
    S("Sports betting should be legal only in person, not on phones.",
      yes=["Betting at casinos and licensed locations"], no=["Phone betting apps"]),
    S("Sports betting should be illegal.",
      yes=["Banning sports betting"], no=["Any legal sports betting"]),
]

T["sex_work_law"] = [
    S("No criminal penalties for paying or being paid for sex between adults.",
      yes=["Decriminalizing sex work for both sides"], no=["Arresting buyers or sellers"]),
    S("Paid sex should be legal only in licensed, regulated businesses, as in some Nevada counties.",
      yes=["Licensed brothels"], no=["Unlicensed sex work", "Full criminal bans"]),
    S("Paying for sex should be illegal, but selling it shouldn't be.",
      yes=["Penalties for buyers only, as in Sweden"], no=["Arresting sellers", "Legal paid sex"]),
    S("Paying and selling sex should both be illegal, as in most states.",
      yes=["Penalties for buyers and sellers"], no=["Legal or decriminalized sex work"]),
]

T["adult_content"] = [
    S("Explicit content made by consenting adults should be legal with no special limits.",
      yes=["No age checks or special rules for porn sites"], no=["Bans or verification laws"]),
    S("Explicit content should be legal, but websites must verify viewers are adults.",
      yes=["Age-verification laws for porn sites"], no=["No checks", "Banning pornography"]),
    S("Explicit content should be legal but banned from most websites and sold only through restricted channels.",
      yes=["Restricting porn to limited, controlled outlets"], no=["Open access online"]),
    S("Making or selling explicit content should be illegal.",
      yes=["Banning pornography"], no=["Any legal pornography"]),
]

T["aid_in_dying"] = [
    S("Doctors should be able to prescribe life-ending medicine to a dying, mentally capable adult, with a short wait.",
      yes=["Medical aid in dying with a brief waiting period"], no=["Banning medical aid in dying"]),
    S("Allow medical aid in dying only with strict safeguards, like two doctors' approval and a longer wait.",
      yes=["Strict safeguards and longer waits"], no=["Short waits", "A ban"]),
    S("Doctors shouldn't be allowed to prescribe life-ending medicine.",
      yes=["Banning medical aid in dying"], no=["Any legal aid in dying"]),
]
T["aid_in_dying_cases"] = existing("D17", "aid_in_dying_cases")

T["sin_taxes"] = [
    S("No extra taxes to discourage use; adults should make their own choices.",
      yes=["Ending extra taxes on tobacco and alcohol"], no=["Soda or junk food taxes"]),
    S("Extra taxes only on tobacco and alcohol, as today.",
      yes=["Today's tobacco and alcohol taxes"], no=["Soda and junk food taxes", "Ending these taxes"]),
    S("Extra taxes on sugary drinks and junk food as well as tobacco and alcohol.",
      yes=["Soda and junk food taxes"], no=["Leaving those products untaxed"]),
]

T["helmet_law"] = [
    S("Adults should decide for themselves whether to wear a motorcycle helmet.",
      yes=["Repealing adult helmet laws"], no=["Required helmets for adults"]),
    S("Require helmets only for riders under 21 or without health insurance.",
      yes=["Helmet rules for young or uninsured riders"], no=["Requiring all riders", "No requirement"]),
    S("All motorcycle riders should have to wear helmets.",
      yes=["Universal helmet laws"], no=["Exemptions for adult riders"]),
]

T["drinking_age"] = [
    S("The drinking age should be 18.", yes=["Lowering the drinking age to 18"], no=["Keeping it at 21"]),
    S("18 for beer and wine, 21 for liquor.", yes=["Beer and wine at 18"], no=["Liquor at 18", "21 for everything"]),
    S("The drinking age should stay 21.", yes=["Today's drinking age of 21"], no=["Lowering or raising it"]),
    S("The drinking age should be older than 21.", yes=["Raising the drinking age above 21"], no=["Drinking at 21"]),
]

T["vape_flavors"] = [
    S("Adults should be able to buy flavored vapes and cigarettes.", yes=["Legal flavored products for adults"], no=["Flavor bans"]),
    S("Allow flavored vapes and cigarettes, with higher taxes.", yes=["Extra taxes on flavored products"], no=["Flavor bans", "No extra tax"]),
    S("Flavored vapes and cigarettes should be banned.", yes=["Bans on flavored vapes and menthol cigarettes"], no=["Sales to adults"]),
]

T["kidney_payment"] = [
    S("People should be able to be paid for donating a kidney, in a regulated market.",
      yes=["A legal, regulated market for kidneys"], no=["Today's ban on payment"]),
    S("Kidney donors should get only a fixed government payment, not a market price.",
      yes=["A set government payment to living donors"], no=["A market for kidneys", "Keeping the ban"]),
    S("Keep the ban on paying for kidneys.",
      yes=["Today's federal ban"], no=["Any payment for organs"]),
]

T["right_to_try"] = [
    S("Seriously ill patients should be able to use any treatment that passed early safety testing.",
      yes=["Access to unapproved drugs after early trials"], no=["Requiring FDA programs or full approval"]),
    S("Unapproved treatments only through FDA-supervised programs.",
      yes=["FDA expanded-access programs"], no=["Access outside FDA supervision", "No access before approval"]),
    S("Patients should wait for full FDA approval.",
      yes=["Requiring full approval first"], no=["Early access to unapproved drugs"]),
]

T["raw_milk"] = [
    S("Stores should be able to sell raw milk anywhere, with a warning label.",
      yes=["Raw milk sales in stores"], no=["Bans on raw milk"]),
    S("Raw milk should be sold only directly from farms.",
      yes=["Farm-direct raw milk sales"], no=["Raw milk in stores", "A total ban"]),
    S("Raw milk sales should be banned.",
      yes=["Banning unpasteurized milk sales"], no=["Any legal raw milk sales"]),
]

if __name__ == "__main__":
    write("D17", T)
    write_clarity("D17", C)
