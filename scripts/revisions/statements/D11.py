"""Religion and public life."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

C["church_state_tradeoff"] = {
    "why": "'Separate' and 'support and reflect religion' had no examples.",
    "scope": "Government at every level, in things like prayers before city council meetings, nativity scenes or the Ten Commandments on public property, “In God We Trust” on money, and public money for religious schools and charities.",
}
T["church_state_tradeoff"] = trade(
    S("Keep religion and government strictly separate, even if public life has less room for religious expression.",
      yes=["No official prayers at government meetings", "No religious displays on public property", "No public money for religious schools"],
      no=["Government-sponsored religious displays or prayers"]),
    S("Let government support and reflect religion, even if people of other faiths or none feel left out.",
      yes=["Prayers before government meetings", "Nativity scenes and Ten Commandments displays on public property", "Public money for religious schools and charities"],
      no=["Removing religion from public settings"]),
    S("You weigh separation and room for religion about equally.",
      means=["You'd allow some things, like “In God We Trust,” but not others, like school-led prayer"]))

C["faith_based_laws"] = {
    "why": "No example of a law based on religious teaching.",
    "scope": "Lawmakers of any faith, voting on issues like abortion, marriage, the death penalty, immigration or aid to the poor.",
}
T["faith_based_laws"] = trade(
    S("Laws should rest on reasons everyone can share, not religious teaching.",
      yes=["Lawmakers explaining votes on abortion, marriage or immigration in non-religious terms"],
      no=["Passing laws because a religion teaches them"]),
    S("Lawmakers should be free to base laws on their religious beliefs.",
      yes=["Votes on abortion, marriage, the death penalty or aid to the poor guided by faith"],
      no=["Requiring non-religious reasons for laws"]),
    S("You weigh shared reasons and faith-based reasons about equally.",
      means=["Faith can shape a lawmaker's view, but you'd want laws to have reasons beyond it too"]))

T["school_prayer"] = [
    S("Public schools shouldn't sponsor prayer in any form.",
      yes=["Banning school-organized prayer and moments of silence meant for prayer"],
      no=["Teacher-led prayer"]),
    S("A moment of silence in public schools, but no led prayer.",
      yes=["A daily moment of silence"],
      no=["Teacher- or school-led prayer"]),
    S("Teacher-led prayer in public schools that students can skip.",
      yes=["Classroom prayer led by teachers, with opt-outs"],
      no=["Banning school prayer"]),
    S("Daily prayer led by public schools.",
      yes=["School-led prayer every day"],
      no=["Keeping prayer out of public schools"]),
]

T["ten_commandments"] = [
    S("The Ten Commandments shouldn't be displayed in public school classrooms.",
      yes=["Striking down state display laws"],
      no=["Classroom displays, even historical ones"]),
    S("Display the Ten Commandments only as part of a history-of-law display.",
      yes=["Showing them alongside documents like the Magna Carta and the Constitution"],
      no=["Posting them alone in every classroom"]),
    S("Display the Ten Commandments in every public school classroom.",
      yes=["Laws like Louisiana's and Texas's requiring classroom displays"],
      no=["Keeping them out of classrooms"]),
]

T["vouchers_religious_schools"] = [
    S("Public tuition money should go only to non-religious private schools.",
      yes=["Barring vouchers at religious schools"],
      no=["Using public money at Catholic, Christian, Jewish or Muslim schools"]),
    S("Public tuition money can go to religious schools if religious classes are optional for those students.",
      yes=["Vouchers at religious schools with an opt-out from religious instruction"],
      no=["Religion classes required for voucher students", "Barring religious schools"]),
    S("Public tuition money should go to religious schools on equal terms.",
      yes=["Vouchers usable at any religious school"],
      no=["Excluding religious schools"]),
]

T["religious_charter"] = [
    S("Religious groups shouldn't run publicly funded charter schools that teach their faith.",
      yes=["Keeping charter schools non-religious"],
      no=["Religious charter schools"]),
    S("Religious charter schools are fine if students can opt out of religious instruction.",
      yes=["Religious charters with opt-outs"],
      no=["Required religious instruction in charters", "Barring religious charters"]),
    S("Religious groups should run charter schools like anyone else.",
      yes=["Publicly funded charters that teach a faith"],
      no=["Barring religious groups from running charters"]),
]

T["religious_exemptions"] = [
    S("Religious exemptions from general laws should be rare; everyone should follow the same laws.",
      yes=["Applying laws equally regardless of belief"],
      no=["Broad religious exemptions"]),
    S("Grant religious exemptions only when they don't harm anyone else.",
      yes=["Exemptions that affect only the believer"],
      no=["Exemptions that burden others", "Refusing harmless exemptions"]),
    S("Grant religious exemptions in most cases unless government has a very strong reason.",
      yes=["A strong presumption for exemptions, as in the Religious Freedom Restoration Act"],
      no=["Requiring believers to follow laws that conflict with their faith"]),
]
T["religious_exemption_cases"] = existing("D11", "religious_exemption_cases")

T["christian_nation"] = [
    S("Government should favor no religion.",
      yes=["Strict government neutrality on religion"],
      no=["Official recognition of Christianity"]),
    S("No official declaration, but government can recognize the nation's Christian heritage.",
      yes=["Official mentions of Christian heritage in ceremonies and proclamations"],
      no=["A legal declaration", "Removing all religious references"]),
    S("The US government should officially declare the US a Christian nation.",
      yes=["A law declaring the US a Christian nation"],
      no=["Government neutrality toward all religions"]),
]

T["religious_country"] = [
    S("It isn't important for the country that most Americans are religious.",
      means=["The country would do just as well if most people weren't religious"]),
    S("It's somewhat important for the country that most Americans are religious.",
      means=["Widespread religion helps the country, but isn't vital"]),
    S("It's very important for the country that most Americans are religious.",
      means=["A decline in religion would seriously harm the country"]),
    S("The country's success depends on most Americans being religious.",
      means=["Without widespread faith, the country would fail"]),
]

T["evolution_class"] = [
    S("Science classes should teach evolution only.",
      yes=["Evolution as the scientific explanation"],
      no=["Mentioning creation in science class"]),
    S("Teach evolution and mention that many people hold religious beliefs about creation.",
      yes=["Evolution, with a note that religious views exist"],
      no=["Teaching creation as an alternative explanation"]),
    S("Teach evolution alongside creation or intelligent design as alternatives.",
      yes=["Both presented as explanations in science class"],
      no=["Evolution only"]),
    S("Teach creation or intelligent design instead of evolution.",
      yes=["Replacing evolution in science classes"],
      no=["Teaching evolution"]),
]

T["faith_charities"] = [
    S("Keep public money away from religious charities.",
      yes=["Funding only secular groups for shelters and addiction programs"],
      no=["Grants to church-run programs"]),
    S("Religious charities can get public money if they keep religion out of the services.",
      yes=["Funding church-run shelters with no religious content"],
      no=["Funding programs with faith content", "Barring religious groups"]),
    S("Religious charities should get public money on equal terms, including faith content people can opt out of.",
      yes=["Grants to faith-based programs with optional religious content"],
      no=["Excluding religious charities from funding"]),
]

if __name__ == "__main__":
    write("D11", T)
    write_clarity("D11", C)
