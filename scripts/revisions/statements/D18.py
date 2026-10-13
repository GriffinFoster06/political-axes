"""Speech and civil liberties."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["hate_speech_law"] = [
    S("Government shouldn't punish speech, however hateful, unless it threatens or incites violence, as today.",
      yes=["Protecting hateful speech under the First Amendment"], no=["Fines or jail for hateful speech"]),
    S("Only the most extreme public hateful speech should be a crime, such as calling a group subhuman.",
      yes=["Narrow hate speech laws for the most extreme speech"], no=["Broad hate speech laws", "Protecting all non-threatening speech"]),
    S("Hateful public speech about race, religion, sexual orientation or gender identity should bring fines or jail.",
      yes=["Hate speech laws like those in much of Europe"], no=["Protecting hateful speech"]),
]

T["hateful_speaker_response"] = [
    S("Answer hateful speech with more speech; don't try to silence the speaker.",
      yes=["Rebutting and debating"], no=["Boycotts, firings or deplatforming"]),
    S("Criticism and boycotts are fair, but the speaker shouldn't lose their job or platform.",
      yes=["Public criticism and boycotts"], no=["Firing or deplatforming", "Legal penalties"]),
    S("Platforms, venues and employers should drop the speaker.",
      yes=["Deplatforming, canceled events and firings"], no=["Legal penalties", "Leaving them in place"]),
    S("The law should punish hateful speech.",
      yes=["Legal penalties for hateful speech"], no=["Leaving it to public response alone"]),
]
T["campus_speakers"] = existing("D18", "campus_speakers")

T["flag_burning"] = [
    S("Burning the flag in protest should stay legal as protected speech.",
      yes=["The 1989 Supreme Court ruling as it stands"], no=["A flag-burning ban"]),
    S("Flag burning should be legal, but cities can ban open fires in some places for safety.",
      yes=["Fire-safety rules that apply to all fires"], no=["Bans aimed at flag burning itself"]),
    S("Amend the Constitution to allow a flag-burning ban.",
      yes=["A constitutional amendment banning flag burning"], no=["Treating flag burning as protected speech"]),
]

T["protest_masks"] = [
    S("Masks at protests should be legal; anonymity protects protesters from retaliation.",
      yes=["Allowing masked protest"], no=["Mask bans at protests"]),
    S("Masks at protests should be illegal only while committing a crime.",
      yes=["Added penalties for masked crimes"], no=["Banning masks at all protests"]),
    S("Wearing a mask to hide your identity at any protest should be illegal.",
      yes=["Protest mask bans"], no=["Anonymous protest"]),
]

T["campus_encampments"] = [
    S("Public universities should allow protest camps as long as they stay peaceful.",
      yes=["Letting peaceful camps stay"], no=["Removing peaceful camps"]),
    S("Allow protest camps only for a limited time in designated areas.",
      yes=["Time and place limits on camps"], no=["Unlimited camps", "Immediate removal"]),
    S("Remove protest camps right away.",
      yes=["Clearing encampments immediately"], no=["Allowing campus encampments"]),
]

T["gov_misinformation"] = [
    S("Government shouldn't judge what's true online.",
      yes=["No government role on false claims"], no=["Government corrections, flags or removal demands"]),
    S("Government should only publish its own corrections.",
      yes=["Official corrections on health and election claims"], no=["Flagging or removing posts"]),
    S("Government should flag false posts, but not require removal.",
      yes=["Government flags on false health and election posts"], no=["Required removal", "Staying silent"]),
    S("Government should require platforms to remove posts its agencies find false on topics like health and elections.",
      yes=["Required removal of posts agencies judge false"], no=["Leaving false posts up"]),
]

T["misinfo_penalty"] = [
    S("No new penalties for spreading false information beyond fraud and defamation law.",
      yes=["Relying on existing law"], no=["New fines or jail for false claims"]),
    S("Penalties only for knowingly false claims about when, where or how to vote.",
      yes=["Laws against false voting information"], no=["Penalties for other false claims"]),
    S("Fines or jail for knowingly spreading harmful false claims.",
      yes=["Penalties for false claims about medicines, disasters and similar topics"], no=["Leaving harmful false claims unpunished"]),
]

T["jawboning"] = [
    S("Officials should never pressure social media companies over legal speech.",
      yes=["Barring officials from takedown requests over legal posts"], no=["Officials asking for removals"]),
    S("Officials can ask for takedowns only for clear legal violations, like threats.",
      yes=["Requests limited to illegal content"], no=["Requests about legal posts"]),
    S("Officials can ask for takedowns, but every request must be public.",
      yes=["Public logs of every government takedown request"], no=["Secret requests", "Banning requests"]),
    S("Officials can ask for takedowns, and companies decide.",
      yes=["Officials flagging posts they consider harmful"], no=["Limits on officials' requests"]),
]

T["library_book_decisions"] = [
    S("School librarians should decide on challenged books, using professional standards.",
      yes=["Leaving challenges to librarians"], no=["Board votes or automatic removal"]),
    S("A committee of librarians, teachers and parents should decide.",
      yes=["Mixed review committees"], no=["Librarians alone", "Automatic removal"]),
    S("The elected school board should decide.",
      yes=["School board votes on challenged books"], no=["Leaving it to librarians"]),
    S("A challenged book should come off the shelves during review; one objection is enough.",
      yes=["Pulling books on a single objection pending review"], no=["Keeping books available during review"]),
]

T["library_explicit"] = [
    S("High school libraries should carry literary novels with explicit sex, freely available.",
      yes=["Open access to these books"], no=["Permission slips or removal"]),
    S("Students should need parent permission to check out novels with explicit sex.",
      yes=["Parental permission for these books"], no=["Open access", "Removing these novels"]),
    S("High school libraries shouldn't carry novels with explicit sex.",
      yes=["Removing these books"], no=["Keeping them on shelves"]),
]

T["employer_speech"] = [
    S("The law should protect workers from being fired for political views expressed outside work.",
      yes=["Laws protecting off-duty political speech"], no=["Firing over personal posts or views"]),
    S("Employers can fire over outside political speech only if it directly harms the business.",
      yes=["Firing only when the business is harmed"], no=["Firing for views alone", "Full protection"]),
    S("Employers should be free to fire workers for political views.",
      yes=["At-will firing over political speech"], no=["Laws protecting off-duty speech"]),
]
T["employer_speech_cases"] = existing("D18", "employer_speech_cases")

T["defamation_public_figures"] = [
    S("Keep today's high bar for public figures suing news outlets.",
      yes=["The actual-malice standard"], no=["Easier defamation suits"]),
    S("Make it somewhat easier for public figures to sue news outlets.",
      yes=["Lowering the bar somewhat"], no=["Today's high bar", "Liability for any false story"]),
    S("Make it much easier: proving a story was false and harmful should be enough.",
      yes=["Dropping the actual-malice standard"], no=["Today's high bar"]),
]

T["public_broadcasting"] = [
    S("Fund public radio and TV more than in the past.", yes=["Increased federal funding for public broadcasting"], no=["Ending federal funding"]),
    S("Fund public radio and TV about as in the past.", yes=["Restoring past federal funding levels"], no=["Ending or increasing funding"]),
    S("No federal funding for public broadcasting.", yes=["Ending federal money for public radio and TV"], no=["Any federal funding"]),
]

T["campus_speech_codes"] = [
    S("Public universities should be able to discipline students for offensive speech.",
      yes=["Speech codes covering offensive remarks"], no=["Protecting offensive speech on campus"]),
    S("Discipline only for repeated offensive speech aimed at a specific person.",
      yes=["Rules against targeted, repeated remarks"], no=["Broad speech codes", "No limits at all"]),
    S("Public universities shouldn't discipline students for offensive speech.",
      yes=["Protecting all non-threatening speech"], no=["Campus speech codes"]),
]

if __name__ == "__main__":
    write("D18", T)
    write_clarity("D18", C)
