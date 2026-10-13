"""Sexuality and gender identity."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["same_sex_marriage"] = [
    S("Same-sex couples should be able to marry in every state, as today.",
      yes=["Keeping legal same-sex marriage nationwide"],
      no=["Replacing it with civil unions", "Ending legal recognition"]),
    S("Same-sex couples should get civil unions with the same rights, but not marriage.",
      yes=["Civil unions with equal legal rights"],
      no=["Calling same-sex unions marriage", "No legal recognition"]),
    S("Same-sex couples shouldn't get any legal recognition.",
      yes=["Ending legal recognition of same-sex couples"],
      no=["Same-sex marriage or civil unions"]),
]

T["same_sex_adoption"] = [
    S("Same-sex couples should be able to adopt on the same terms, through every agency.",
      yes=["Requiring all state-funded agencies to place children with same-sex couples"],
      no=["Letting religious agencies decline them"]),
    S("Same-sex couples can adopt, but religious agencies can decline to place children with them.",
      yes=["Religious exemptions for state-funded adoption agencies"],
      no=["Requiring every agency to serve them", "Barring same-sex adoption"]),
    S("Same-sex couples shouldn't be able to adopt.",
      yes=["Barring same-sex couples from adoption and foster care"],
      no=["Same-sex adoption"]),
]

T["wedding_vendors"] = [
    S("Businesses must serve same-sex weddings like any other.",
      yes=["Requiring bakeries, florists and photographers to serve same-sex weddings"],
      no=["Religious exemptions for wedding vendors"]),
    S("Only businesses making custom expressive work, like a designed cake or photographs, can refuse.",
      yes=["Letting a custom cake designer or photographer decline", "Requiring other businesses to serve"],
      no=["Letting any business refuse", "No exemption at all"]),
    S("Any business should be able to refuse to serve a same-sex wedding for religious reasons.",
      yes=["Religious exemptions for all wedding businesses"],
      no=["Requiring vendors to serve same-sex weddings"]),
]
T["religious_refusal_cases"] = existing("D10", "religious_refusal_cases")

T["minors_transition"] = [
    S("Gender transition treatments for minors should be allowed when the young person, parents and doctors agree.",
      yes=["Access to puberty blockers, hormones and, in some cases, surgery under 18"],
      no=["State bans on these treatments"]),
    S("Allow treatments for minors only after extended evaluation by specialists, and no surgery before 18.",
      yes=["Blockers or hormones after long specialist evaluation", "No surgery under 18"],
      no=["Treatment on agreement alone", "Full bans"]),
    S("Ban these treatments under 18, except in research studies.",
      yes=["Bans outside clinical research"],
      no=["Routine treatment for minors", "Banning research too"]),
    S("Ban gender transition treatments under 18.",
      yes=["Bans like the Tennessee law the Supreme Court upheld in 2025"],
      no=["Any blockers, hormones or surgery for minors"]),
]
T["minors_transition_cases"] = existing("D10", "minors_transition_cases")

T["trans_adult_sports"] = [
    S("Transgender women should compete in women's college events.",
      yes=["Open eligibility in women's college sports"],
      no=["Hormone rules or bans"]),
    S("Transgender women can compete in women's college events if they meet hormone-level rules.",
      yes=["Eligibility based on testosterone limits"],
      no=["Open eligibility", "Barring transgender women outright"]),
    S("Transgender women can compete in women's events only if they didn't go through male puberty.",
      yes=["Eligibility only for those who transitioned before male puberty"],
      no=["Hormone rules alone", "Full bans"]),
    S("Transgender women should compete in men's or open categories, not women's.",
      yes=["Limiting women's college events to those born female"],
      no=["Transgender women in women's events"]),
]

T["bathrooms"] = [
    S("Transgender people should use restrooms and locker rooms matching their gender identity.",
      yes=["Access by gender identity in schools and government buildings"],
      no=["Rules based on sex at birth"]),
    S("Transgender people should use private single-person facilities or those matching their sex at birth.",
      yes=["Single-person options", "Shared facilities by sex at birth"],
      no=["Shared facilities by gender identity"]),
    S("People should use only facilities matching their sex at birth.",
      yes=["Laws requiring restroom and locker room use by sex at birth"],
      no=["Access by gender identity"]),
]

T["id_sex_marker"] = [
    S("ID sex should be based on gender identity, including an “X” option.",
      yes=["Self-chosen sex markers on passports and licenses", "An X marker"],
      no=["Markers fixed at sex at birth"]),
    S("ID sex should be based on gender identity, male or female only.",
      yes=["Changing markers to match identity"],
      no=["An X option", "Markers fixed at sex at birth"]),
    S("ID sex should be sex at birth, with changes allowed after medical transition.",
      yes=["Changes only after medical transition"],
      no=["Changes on request", "Never allowing changes"]),
    S("ID sex should be sex at birth only.",
      yes=["Passports and licenses showing sex at birth"],
      no=["Any change to the sex marker"]),
]

T["school_pronouns"] = [
    S("Teachers should use a student's chosen name and pronouns whenever the student asks.",
      yes=["Requiring teachers to use chosen names and pronouns"],
      no=["Requiring parental consent first"]),
    S("Teachers should use chosen names and pronouns only with a parent's consent.",
      yes=["Parental consent before school uses new names or pronouns"],
      no=["Using them without parents' consent", "Banning chosen pronouns at school"]),
    S("Teachers may use chosen names and pronouns, but none can be required to.",
      yes=["Letting each teacher decide"],
      no=["Requiring or banning their use"]),
    S("Schools should use names and pronouns matching sex at birth.",
      yes=["Policies requiring birth names and pronouns"],
      no=["Using chosen names or pronouns"]),
]

T["parent_notification"] = [
    S("Schools should tell parents about a student's gender identity only if the student agrees.",
      yes=["Student privacy unless the student consents"],
      no=["Required parental notification"]),
    S("Schools should tell parents of students under 16; older students decide.",
      yes=["Notification for younger students", "Privacy for students 16 and up"],
      no=["Always notifying", "Never notifying without consent"]),
    S("Schools should tell parents unless staff believe the student would be at risk of abuse.",
      yes=["Notification with an abuse-risk exception"],
      no=["Student consent rules", "Notification with no exceptions"]),
    S("Schools should always tell parents.",
      yes=["Mandatory parental notification"],
      no=["Withholding this from parents for any reason"]),
]

T["lgbt_nondiscrimination"] = [
    S("Federal law should ban discrimination over sexual orientation and gender identity in housing, services and businesses.",
      yes=["A federal law like the Equality Act covering both"],
      no=["Leaving protections to states"]),
    S("Federal law should ban discrimination over sexual orientation, but not gender identity.",
      yes=["Federal protections for gay, lesbian and bisexual people"],
      no=["Including gender identity", "No federal law"]),
    S("No federal law; leave LGBT discrimination protections to states.",
      yes=["State-by-state protections"],
      no=["A federal anti-discrimination law"]),
    S("No discrimination protections for sexual orientation or gender identity at any level.",
      yes=["Repealing state and local protections"],
      no=["Any such protections"]),
]
T["nondiscrimination_exemptions"] = existing("D10", "nondiscrimination_exemptions")

T["gender_belief"] = [
    S("Gender identity alone determines whether someone is a man or a woman.",
      means=["A person who identifies as a woman is a woman, whatever their sex at birth"]),
    S("Gender identity mostly determines whether someone is a man or a woman.",
      means=["Identity counts more than sex at birth, though both play some part"]),
    S("Both sex at birth and gender identity determine it.",
      means=["Neither alone settles whether someone is a man or a woman"]),
    S("Sex at birth mostly determines whether someone is a man or a woman.",
      means=["Sex at birth counts more than identity, though identity plays some part"]),
    S("Sex at birth alone determines whether someone is a man or a woman.",
      means=["A person born male is a man, whatever their gender identity"]),
]

T["trans_school_sports"] = [
    S("Transgender girls should be able to play on high school girls' teams.",
      yes=["Open eligibility for girls' teams"],
      no=["Hormone rules or bans"]),
    S("Transgender girls can play on girls' teams if they meet medical criteria like hormone levels.",
      yes=["Eligibility based on hormone levels"],
      no=["Open eligibility", "Barring transgender girls outright"]),
    S("Transgender girls should play on boys' teams or in an open category.",
      yes=["Limiting girls' teams to those born female"],
      no=["Transgender girls on girls' teams"]),
]

if __name__ == "__main__":
    write("D10", T)
    write_clarity("D10", C)
