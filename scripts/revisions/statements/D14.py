"""Immigration and national identity."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["legal_immigration_level"] = [
    S("Raise green cards to 2 million or more a year.",
      yes=["Doubling or more permanent legal immigration"], no=["Keeping it at about 1 million", "Cutting legal immigration"]),
    S("Raise green cards to about 1.5 million a year.",
      yes=["A 50% increase in permanent legal immigration"], no=["Doubling legal immigration", "Keeping or cutting it"]),
    S("Keep green cards at about 1 million a year.",
      yes=["Today's level of permanent legal immigration"], no=["Raising or cutting it"]),
    S("Cut green cards to about 500,000 a year.",
      yes=["Halving permanent legal immigration"], no=["Keeping today's level", "Deeper cuts below 250,000"]),
    S("Cut green cards to fewer than 250,000 a year.",
      yes=["Cutting permanent legal immigration by three-quarters or more"], no=["Today's level"]),
]

C["temp_workers_seasonal"] = {
    "why": "'More' and 'fewer' had no baseline.",
    "context": "Today roughly 400,000 seasonal farm jobs and about 66,000 or more seasonal non-farm jobs a year are filled through these visas.",
}
C["temp_workers_skilled"] = {
    "why": "'More' and 'fewer' had no baseline.",
    "context": "Today 85,000 new skilled-worker (H-1B) visas a year are issued under the main cap, with more at universities and research groups.",
}
for iid, what in (("temp_workers_seasonal", "seasonal farm and service"), ("temp_workers_skilled", "skilled")):
    T[iid] = [
        S(f"Admit many more temporary foreign workers for {what} jobs.",
          yes=["Raising these visa numbers well above today's"], no=["Keeping or cutting them"]),
        S(f"Admit somewhat more temporary foreign workers for {what} jobs.",
          yes=["A modest increase in these visas"], no=["Large increases in these visas", "Cutting these visas"]),
        S(f"Keep temporary visas for {what} jobs about the same.",
          yes=["Today's visa numbers"], no=["Raising or cutting them"]),
        S(f"Admit somewhat fewer temporary foreign workers for {what} jobs.",
          yes=["A modest cut in these visas"], no=["Raising these visa numbers", "Deep cuts in these visas"]),
        S(f"Admit many fewer temporary foreign workers for {what} jobs.",
          yes=["Deep cuts in these visas"], no=["Keeping or raising them"]),
    ]

T["skills_vs_family"] = [
    S("Green cards should mostly go by family ties, as now.",
      yes=["Keeping about two-thirds of green cards for relatives"], no=["Shifting to a skills-based system"]),
    S("Green cards should be split evenly between family ties and job skills.",
      yes=["Moving toward half family, half skills"], no=["Today's family-heavy mix", "A mostly skills-based system"]),
    S("Green cards should mostly go by job skills and education, as in Canada and Australia.",
      yes=["A points system for skills, education and English"], no=["Family ties as the main path"]),
]

T["sponsor_relatives"] = [
    S("Citizens should be able to sponsor spouses, children, parents and siblings, with shorter waits.",
      yes=["Clearing family visa backlogs"], no=["Ending sibling or parent sponsorship"]),
    S("Citizens should be able to sponsor spouses, children, parents and siblings, as today.",
      yes=["Today's family categories"], no=["Expanding or narrowing them"]),
    S("Citizens should sponsor only spouses, minor children and parents.",
      yes=["Ending sponsorship of siblings and adult children"], no=["Sibling sponsorship"]),
    S("Citizens should sponsor only spouses and minor children.",
      yes=["Ending sponsorship of parents, siblings and adult children"], no=["Sponsoring parents or siblings"]),
]

T["border_security"] = [
    S("Fewer agents and barriers at the southern border.",
      yes=["Cutting Border Patrol and removing some barriers"], no=["More agents or wall"]),
    S("Keep about current enforcement at the southern border.",
      yes=["Today's agents and barriers"], no=["Cutting or adding enforcement"]),
    S("More agents and technology at the border, but no new wall.",
      yes=["More Border Patrol agents, sensors, drones and cameras"], no=["New physical wall", "Cutting enforcement"]),
    S("A wall along most of the southern border, plus more agents.",
      yes=["Building wall along most of the 1,950-mile border", "More agents"], no=["Cutting enforcement"]),
]

T["military_border"] = [
    S("The military shouldn't be used at the border; leave it to civilian agencies.",
      yes=["Border control by Border Patrol only"], no=["Troops at the border"]),
    S("Troops can support border agents with transport and surveillance, but not stop people.",
      yes=["Troops in support roles"], no=["Troops stopping crossers", "No military role"]),
    S("Troops should stop people crossing and turn them back.",
      yes=["Soldiers stopping and turning back crossers"], no=["Limiting troops to support roles"]),
]

T["everify"] = [
    S("Employers shouldn't be required to use E-Verify.",
      yes=["Keeping E-Verify voluntary"], no=["A nationwide E-Verify mandate"]),
    S("Only large employers should have to use E-Verify.",
      yes=["E-Verify for big companies"], no=["Requiring it of small businesses", "No requirement"]),
    S("All employers should use E-Verify, with heavy fines for hiring people without legal status.",
      yes=["Mandatory E-Verify", "Heavy fines on employers"], no=["Voluntary checks"]),
]

T["local_police_cooperation"] = [
    S("Local police shouldn't help federal immigration agents at all.",
      yes=["Sanctuary policies barring cooperation"], no=["Holding people for immigration agents"]),
    S("Local police should help only with people convicted of serious crimes.",
      yes=["Handing over people convicted of serious crimes"], no=["Helping in other cases", "Refusing all help"]),
    S("Local police should help whenever federal agents ask.",
      yes=["Holding people in jail for immigration agents", "Joint enforcement programs"], no=["Sanctuary policies"]),
]

T["asylum_rules"] = [
    S("Make asylum easier to apply for, and let applicants live and work here while they wait.",
      yes=["Work permits for asylum seekers", "Releasing applicants while cases proceed"], no=["Limits on applying at the border"]),
    S("Keep the right to apply for asylum here, but decide cases much faster.",
      yes=["More asylum judges and faster rulings"], no=["Ending asylum at the border", "Years-long waits"]),
    S("People should apply for asylum from outside the US or in the first safe country they reach.",
      yes=["Applying from abroad or in Mexico first"], no=["Applying after crossing the border"]),
    S("End or sharply limit asylum at the southern border.",
      yes=["Closing the border to asylum claims"], no=["Allowing claims at the border"]),
]

T["asylum_grounds"] = [
    S("People fleeing gang violence or domestic abuse should qualify for asylum, whether or not their government could protect them.",
      yes=["Asylum for victims of gangs and domestic abuse"], no=["Limiting asylum to the traditional grounds"]),
    S("They should qualify only if their own government can't or won't protect them.",
      yes=["Asylum when the home government fails to protect them"], no=["Asylum whatever the government could do", "No asylum for these cases"]),
    S("Asylum should be only for people targeted for race, religion, politics or similar reasons.",
      yes=["Excluding gang and domestic violence claims"], no=["Asylum for gang or abuse victims"]),
]

T["refugee_cap"] = [
    S("Resettle 125,000 or more refugees a year.", yes=["A refugee cap of 125,000+"], no=["Caps below 50,000"]),
    S("Resettle about 50,000 to 100,000 refugees a year.", yes=["A middle-sized refugee program"], no=["A cap of 125,000 or more", "Under 30,000"]),
    S("Resettle about 15,000 to 30,000 refugees a year.", yes=["A small refugee program"], no=["50,000 or more", "Ending refugee resettlement"]),
    S("Resettle fewer than 10,000 refugees a year.", yes=["A very small refugee program"], no=["Caps of 15,000 or more"]),
    S("Resettle no refugees.", yes=["Ending refugee resettlement"], no=["Any refugee admissions"]),
]

T["birthright_citizenship"] = [
    S("All children born in the US should be citizens automatically.",
      yes=["Birthright citizenship for every child born here"], no=["Limits based on parents' status"]),
    S("Children born here should be citizens only if a parent is a citizen or green card holder.",
      yes=["Ending citizenship for children of parents without legal status or on temporary visas"], no=["Citizenship for every child born here"]),
    S("Children born here should be citizens only if a parent is a citizen.",
      yes=["Ending citizenship for children of green card holders and others"], no=["Citizenship based on birthplace alone"]),
]

T["assimilation"] = [
    S("Immigrants shouldn't be expected to adopt American customs at all.",
      means=["Keeping their language, customs and way of life is entirely up to them"]),
    S("Immigrants should learn English and follow the law, but keep their own culture freely.",
      means=["Beyond English and the law, no pressure to change customs, dress, food or holidays"]),
    S("Immigrants should learn English and adopt most American customs.",
      means=["They can keep some traditions, but should take on most American ways of life"]),
    S("Immigrants should fully blend in and leave their old customs behind.",
      means=["Over time they should stop keeping the language and customs of their home country"]),
]
T["american_criteria"] = existing("D14", "american_criteria")

T["american_basis"] = [
    S("Believing in ideals like freedom and equality makes someone American; anyone can become American.",
      means=["An immigrant who embraces those ideals is as American as someone born here"]),
    S("Those ideals plus learning English and sharing the culture make someone American.",
      means=["Ideals aren't enough on their own; language and culture matter too"]),
    S("Being born here or raised in the culture from childhood makes someone American.",
      means=["Someone who arrives as an adult isn't fully American, even with citizenship"]),
]

T["patriotic_education"] = [
    S("Schools should give the country's failures and injustices at least as much attention as its achievements.",
      yes=["History lessons that focus on slavery, the treatment of Native Americans and other injustices as much as on achievements"],
      no=["Lessons centered on national pride"]),
    S("Schools should teach failures and achievements in balance.",
      yes=["Even-handed coverage of both"], no=["Leaning heavily either way"]),
    S("Schools should emphasize achievements and ideals so students take pride in the country.",
      yes=["Lessons that build pride in the founding and the country's achievements"],
      no=["Lessons focused mainly on failures"]),
]

T["anthem_kneeling"] = [
    S("Kneeling during the anthem is always an acceptable protest.",
      yes=["Athletes kneeling for any cause"], no=["Punishing or banning it"]),
    S("Kneeling is acceptable, but not at official government or military events.",
      yes=["Kneeling at games", "Expecting standing at official events"], no=["Kneeling at military ceremonies"]),
    S("Kneeling during the anthem isn't acceptable; it disrespects the country.",
      yes=["Expecting everyone to stand"], no=["Kneeling as protest"]),
]

C["culture_tradeoff"] = {
    "why": "'Keep their own cultures' and 'one shared culture' had no examples.",
    "sides": {
        "0": {"text": "Groups keep their own languages, holidays, foods and religious practices, even if people share less in common."},
        "1": {"text": "People adopt one shared culture, with English, the same national holidays and common customs, even if some traditions fade."},
    },
}
T["culture_tradeoff"] = trade(
    S("America is stronger when groups keep their own cultures.",
      yes=["Bilingual schools and services", "Public support for many cultures' holidays and traditions"],
      no=["Pressure on immigrants to drop their language or customs"]),
    S("America is stronger when people adopt one shared culture.",
      yes=["English as the common language", "Shared national holidays and customs"],
      no=["Government support for keeping separate languages and cultures"]),
    S("You value many cultures and one shared culture about equally.",
      means=["You'd want a common language and civic culture while groups keep their own traditions"]))

T["dual_citizenship"] = [
    S("US citizens should be able to hold another citizenship, as today.",
      yes=["Allowing dual citizenship"], no=["Requiring people to give up other citizenship"]),
    S("Allow dual citizenship, except for people in high government office.",
      yes=["Barring dual citizens from high office"], no=["Banning dual citizenship for everyone"]),
    S("Citizens should hold only US citizenship.",
      yes=["Requiring people to give up any other citizenship"], no=["Dual citizenship"]),
]

T["us_exceptional"] = [
    S("Many countries are better than the US.", means=["On the whole, a number of countries do better than the US"]),
    S("The US is no better or worse than many other countries.", means=["It's roughly on a par with many other countries"]),
    S("The US is one of the greatest countries, along with some others.", means=["It ranks near the top, alongside a few others"]),
    S("The US stands above all other countries.", means=["No other country matches it"]),
]

T["english_official"] = [
    S("No official language; government should offer services in many languages.",
      yes=["Multilingual ballots, forms and services"], no=["English-only government"]),
    S("Make English official, but keep ballots and health information in other languages.",
      yes=["English as the official language", "Translated ballots and health information"], no=["English-only for everything"]),
    S("Government business should be in English only.",
      yes=["English-only ballots, forms and services"], no=["Government services in other languages"]),
]

T["citizens_first"] = [
    S("Legal immigrants should be treated the same as citizens for jobs and benefits.",
      yes=["Equal access to jobs and benefits for green card holders"], no=["Citizen preferences"]),
    S("Citizens should get preference only for government jobs.",
      yes=["Citizenship preference in government hiring"], no=["Preference for benefits or private jobs"]),
    S("Citizens should get preference for government jobs and benefits.",
      yes=["Limiting benefits and government jobs to citizens first"], no=["Equal treatment of legal immigrants"]),
    S("Citizens should get preference, and private employers should show no citizen is available before hiring a non-citizen.",
      yes=["Citizens-first rules for government jobs, benefits and private hiring"], no=["Hiring non-citizens freely"]),
]

T["immigrant_selection_culture"] = [
    S("Culture and religion should never count in deciding who may immigrate.",
      yes=["Selection without regard to culture or religion"], no=["Tests or bans by culture or religion"]),
    S("Only knowledge of English and US civics should count.",
      yes=["English and civics requirements"], no=["Preferences by culture or country", "Religious bans"]),
    S("Give some preference to people from countries with cultures closer to America's.",
      yes=["Favoring immigrants from culturally similar countries"], no=["Ignoring culture", "Religious bans"]),
    S("Consider culture and religion, and bar people from some religions or cultures.",
      yes=["Barring immigrants from some religions or cultures"], no=["Selection blind to religion"]),
]
T["enforcement_limits"] = existing("D14", "enforcement_limits")

T["status_policy"] = [
    S("Let most people without legal status stay and apply for citizenship without major penalties.",
      yes=["A path to citizenship with few conditions"], no=["Fines or waiting periods", "Deporting people who have built lives here"]),
    S("Let them stay and apply for citizenship after requirements like a fine and a background check.",
      yes=["Earned citizenship with fines and checks"], no=["Citizenship with no conditions", "Legal status without citizenship"]),
    S("Let them stay and work legally, but not become citizens.",
      yes=["Permanent work permits without citizenship"], no=["A path to citizenship", "Deporting people who have built lives here"]),
    S("Let them work here for a limited time, then require them to leave.",
      yes=["Temporary work permits ending in departure"], no=["Permanent status", "Immediate removal"]),
    S("Require them to leave, starting with people with criminal records.",
      yes=["Deporting most people without legal status, criminals first"], no=["Legal status for those here"]),
    S("Remove all people without legal status as quickly as possible.",
      yes=["Mass deportation, as fast as possible"], no=["Any legal status or delay"]),
]
T["status_groups"] = existing("D14", "status_groups")

if __name__ == "__main__":
    write("D14", T)
    write_clarity("D14", C)
