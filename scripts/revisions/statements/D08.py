"""Privacy and surveillance."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

C["surveillance_tradeoff"] = {
    "why": "'Monitoring' and 'broad' were undefined.",
    "scope": "Monitoring to find terrorists and spies, under any administration: for example, collecting records of who calls or emails whom, when and for how long, for millions of Americans at once.",
}
T["surveillance_tradeoff"] = trade(
    S("Limit government monitoring of phone and internet records, even if some attacks are harder to stop.",
      yes=["Collecting records only on specific suspects", "Ending bulk collection of Americans' call and email records"],
      no=["Programs that sweep up millions of innocent people's records"]),
    S("Allow broad monitoring of phone and internet records, even if many innocent people's records are collected.",
      yes=["Bulk collection of call and email records to search for terrorists and spies"],
      no=["Limiting collection to named suspects"]),
    S("You weigh privacy and security about equally.",
      means=["You'd accept some bulk collection with strict limits on who can search it and why"]))

T["warrant_tradeoff"] = trade(
    S("Intelligence agencies should get a judge's warrant before reading Americans' messages, even if it slows investigations.",
      yes=["A warrant requirement for searching Americans' messages"],
      no=["Reading messages first and getting approval later"]),
    S("Agencies should be able to collect Americans' messages first and get approval later, so threats aren't missed.",
      yes=["Collecting and reading first, with after-the-fact review"],
      no=["Requiring a warrant up front"]),
    S("You weigh warrants and speed about equally.",
      means=["You'd allow collecting first only in urgent cases, with a warrant required soon after"]))

T["cameras_tradeoff"] = trade(
    S("Limit city and police cameras and license plate readers, even if some crimes go unsolved.",
      yes=["Fewer public cameras and plate readers", "Short limits on how long footage is kept"],
      no=["Camera networks recording everyone's movements"]),
    S("Use cameras and license plate readers widely, even if everyone's movements are recorded.",
      yes=["More cameras on streets and in parks", "Plate readers tracking cars citywide"],
      no=["Limits that leave crimes unsolved"]),
    S("You weigh privacy and solving crimes about equally.",
      means=["You'd allow cameras in high-crime spots with limits on how long footage is kept"]))

T["encryption_access"] = [
    S("Tech companies shouldn't build a way to unlock encrypted phones and messages, even with a court order.",
      yes=["Strong encryption that no one, including the company, can unlock"],
      no=["Required back doors for police"]),
    S("Require a way to unlock encrypted data only in the most serious cases, like terrorism or child exploitation.",
      yes=["Court-ordered access for terrorism and child exploitation cases"],
      no=["Access in ordinary criminal cases", "No access at all"]),
    S("Tech companies should give police a way to unlock encrypted data in any criminal case with a court order.",
      yes=["Required unlock methods for any court order"],
      no=["Encryption no one can unlock"]),
]

T["facial_recognition"] = [
    S("Ban police from using facial recognition.",
      yes=["A ban on facial recognition by police"],
      no=["Using it even for serious crimes"]),
    S("Allow police facial recognition only for serious crimes, with a warrant.",
      yes=["Warrant-based use to identify suspects in serious crimes"],
      no=["Use in any investigation", "Live crowd scanning"]),
    S("Allow police facial recognition in any criminal investigation.",
      yes=["Running suspects' photos against image databases"],
      no=["A warrant requirement", "Live scanning of crowds"]),
    S("Allow police facial recognition, including live scanning of crowds.",
      yes=["Real-time face scanning in public places"],
      no=["Limits on police use of facial recognition"]),
]
T["facial_recognition_cases"] = existing("D08", "facial_recognition_cases")

T["data_privacy_law"] = [
    S("A strict federal privacy law: companies need your permission before collecting or selling your data.",
      yes=["Opt-in consent for collecting location, browsing and purchase data"],
      no=["Collecting data by default"]),
    S("A moderate federal privacy law: you can tell companies not to sell your data.",
      yes=["A national right to opt out of data sales"],
      no=["Opt-in consent", "No federal law"]),
    S("No federal privacy law; leave it to states.",
      yes=["State privacy laws like California's"],
      no=["A national privacy law"]),
    S("No new privacy laws; people can choose which services to use.",
      yes=["Leaving data practices to companies and customers"],
      no=["Federal or state privacy rules"]),
]

T["gov_buys_data"] = [
    S("Government should never buy Americans' personal data without a warrant.",
      yes=["A warrant requirement for buying location and other data"],
      no=["Agencies buying data from brokers"]),
    S("Government can buy personal data without a warrant only for national security.",
      yes=["Purchases for intelligence and terrorism cases"],
      no=["Purchases for ordinary police work", "A total ban"]),
    S("Government can buy any personal data that's for sale to anyone.",
      yes=["Agencies buying phone location histories from data brokers"],
      no=["A warrant requirement for purchased data"]),
]

T["digital_id"] = [
    S("No national digital ID; keep state IDs and passports.",
      yes=["Sticking with driver's licenses and passports"],
      no=["A federal digital ID"]),
    S("A voluntary national digital ID.",
      yes=["A federal phone-based ID people can choose to use"],
      no=["Requiring a digital ID", "No digital ID"]),
    S("A national digital ID required for everyone.",
      yes=["A mandatory federal digital ID"],
      no=["Relying on state IDs"]),
]

T["border_device_search"] = [
    S("Border agents should need a warrant to search travelers' phones and laptops.",
      yes=["A warrant requirement for device searches, including for citizens"],
      no=["Suspicionless searches"]),
    S("Border agents should need reasonable suspicion of a crime to search devices.",
      yes=["Requiring suspicion before any device search"],
      no=["Suspicionless searches", "A full warrant requirement"]),
    S("Border agents should be able to search any traveler's devices, as current rules mostly allow.",
      yes=["Searches without suspicion at the border"],
      no=["Warrant or suspicion requirements"]),
]

T["dna_databases"] = [
    S("Police should never search consumer DNA databases for suspects.",
      yes=["Barring police from ancestry-site DNA"],
      no=["Using relatives' DNA to find suspects"]),
    S("Police can search consumer DNA databases only with a warrant, for violent crimes.",
      yes=["Warrant-based searches in murder and rape cases"],
      no=["Searches without a warrant", "Searches for lesser crimes"]),
    S("Police can search consumer DNA databases for violent crimes.",
      yes=["DNA database searches in violent cases, without a warrant"],
      no=["Searches for nonviolent crimes", "A ban"]),
    S("Police can search consumer DNA databases for any crime.",
      yes=["DNA searches in any case, including property crimes"],
      no=["Limits on police DNA searches"]),
]

T["workplace_monitoring"] = [
    S("Employers shouldn't monitor workers' computers, keystrokes or locations without agreement for specific reasons.",
      yes=["Monitoring only with worker consent and a stated reason"],
      no=["Routine keystroke and location tracking"]),
    S("Employers can monitor workers, but must say exactly what is monitored.",
      yes=["Disclosure of what's tracked"],
      no=["Secret monitoring", "Banning monitoring"]),
    S("Employers can monitor freely; it's their equipment and time.",
      yes=["Keystroke, screen and location tracking on work devices and time"],
      no=["Limits or notice rules on workplace monitoring"]),
]

if __name__ == "__main__":
    write("D08", T)
    write_clarity("D08", C)
