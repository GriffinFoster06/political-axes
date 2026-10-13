"""Crime and policing."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

C["police_spending"] = {
    "why": "'A lot' and 'somewhat' had no scale.",
    "scope": "Think about cities in general, not only your own. “A lot” means a quarter or more; “somewhat” means about 5% to 10%. Social services means things like mental health crisis teams, addiction treatment and youth programs.",
}
T["police_spending"] = [
    S("Replace police departments with other public-safety services.",
      yes=["Abolishing police departments", "Crisis teams, violence interrupters and social services in their place"],
      no=["Keeping police departments"]),
    S("Cut police budgets a lot and move the money to social services.",
      yes=["Cutting police budgets by a quarter or more", "Funding crisis teams, treatment and youth programs"],
      no=["Keeping or raising police budgets"]),
    S("Cut police budgets somewhat and move some money to social services.",
      yes=["Cuts of about 5–10% shifted to social services"],
      no=["Deep cuts", "Raising police budgets"]),
    S("Keep police spending about the same.",
      yes=["Today's police budgets"],
      no=["Cutting or raising them"]),
    S("Raise police spending somewhat, to hire and train more officers.",
      yes=["About 5–10% more for hiring and training"],
      no=["Cutting police budgets"]),
    S("Raise police spending a lot, to hire and train many more officers.",
      yes=["A quarter or more added to police budgets", "Many more officers on the streets"],
      no=["Cutting police budgets"]),
]

T["crisis_responders"] = [
    S("Trained mental health workers, without police, should answer non-violent mental health 911 calls.",
      yes=["Civilian crisis teams sent instead of police"],
      no=["Police as first responders to these calls"]),
    S("Mental health workers and police should respond together.",
      yes=["Co-responder teams"],
      no=["Sending either one alone"]),
    S("Police officers with mental health training should respond.",
      yes=["Crisis-trained officers handling these calls"],
      no=["Civilian-only response"]),
]

T["qualified_immunity"] = [
    S("End qualified immunity so people can sue officers who violate their rights.",
      yes=["Letting people sue officers for money damages over rights violations"],
      no=["Today's protection for officers"]),
    S("Narrow qualified immunity so officers can be sued for serious violations.",
      yes=["Suits for serious violations even without an identical earlier case"],
      no=["Ending qualified immunity", "Keeping it as is"]),
    S("Keep qualified immunity as it is.",
      yes=["Today's rule blocking most suits"],
      no=["Narrowing or ending it"]),
    S("Expand legal protections for police officers.",
      yes=["Stronger shields against lawsuits for officers"],
      no=["Narrowing or ending qualified immunity"]),
]

T["misconduct_records"] = [
    S("All police misconduct complaints should be public, including unproven ones.",
      yes=["Public access to every complaint about force or dishonesty"],
      no=["Keeping complaints confidential"]),
    S("Only police misconduct complaints found to be true should be public.",
      yes=["Publishing sustained complaints"],
      no=["Publishing unproven complaints", "Keeping all secret"]),
    S("Police misconduct records should stay confidential.",
      yes=["Keeping complaint records private"],
      no=["Public misconduct records"]),
]

T["mandatory_minimums"] = [
    S("End mandatory minimum sentences and let judges decide.",
      yes=["Repealing mandatory minimums, including for drug dealing"],
      no=["Sentences judges can't go below"]),
    S("Keep mandatory minimums only for violent crimes.",
      yes=["Minimums for violent crimes", "Ending them for drug and other nonviolent crimes"],
      no=["Minimums for drug dealing"]),
    S("Keep mandatory minimums as they are.",
      yes=["Today's mandatory minimums"],
      no=["Ending or expanding them"]),
    S("Add more mandatory minimums and make them longer.",
      yes=["New and longer mandatory sentences"],
      no=["Giving judges more leeway"]),
]

T["violent_sentences"] = [
    S("Sentences for violent crimes like armed robbery are much too long.",
      yes=["Substantially shorter sentences for violent crimes"], no=["Longer sentences"]),
    S("Sentences for violent crimes are somewhat too long.",
      yes=["Modestly shorter sentences"], no=["Longer sentences"]),
    S("Sentences for violent crimes are about right.",
      yes=["Keeping today's sentences"], no=["Shortening or lengthening them"]),
    S("Sentences for violent crimes are somewhat too short.",
      yes=["Modestly longer sentences"], no=["Shorter sentences"]),
    S("Sentences for violent crimes are much too short.",
      yes=["Substantially longer sentences for violent crimes"], no=["Shorter sentences"]),
]

T["death_penalty"] = [
    S("The death penalty should never be used for murder.",
      yes=["Abolishing the death penalty"], no=["Executions for any murder"]),
    S("The death penalty only for the most extreme murders, like killing several people or a child.",
      yes=["Executions limited to the worst murders"], no=["Abolishing the death penalty", "Using it for most planned murders"]),
    S("The death penalty for most planned murders.",
      yes=["Wide use of the death penalty for premeditated murder"], no=["Abolishing or narrowly limiting it"]),
]
T["death_penalty_cases"] = existing("D15", "death_penalty_cases")

T["cash_bail"] = [
    S("End cash bail and release almost everyone before trial, except clear dangers.",
      yes=["Ending cash bail", "Holding only people judged clearly dangerous"],
      no=["Bail amounts set by judges"]),
    S("Release most people charged with nonviolent crimes without bail; judges set bail for others.",
      yes=["No bail for nonviolent charges", "Bail for violent charges"],
      no=["Ending bail entirely", "Bail for everyone"]),
    S("Keep cash bail, with amounts set by judges.",
      yes=["Today's cash bail system"],
      no=["Ending bail", "Automatic detention"]),
    S("Keep everyone charged with violent or repeat crimes in jail until trial.",
      yes=["Automatic pretrial detention for violent and repeat charges"],
      no=["Releasing these defendants on bail or without it"]),
]

C["prison_purpose"] = {
    "why": "'Rehabilitation' and 'punishment' had no examples.",
    "sides": {
        "0": {"text": "Education, job training, and drug and mental health treatment to prepare people for release, even if it costs more."},
        "1": {"text": "Punishing crime and keeping offenders away from the public, with fewer programs and comforts, even if fewer people change their ways."},
    },
}
T["prison_purpose"] = trade(
    S("Prisons should focus on rehabilitation, even if it costs more.",
      yes=["Education, job training and treatment programs in prison"],
      no=["Cutting programs to save money"]),
    S("Prisons should focus on punishment and protecting the public.",
      yes=["Prisons focused on punishment, with fewer programs and comforts"],
      no=["Spending more on prison education and treatment"]),
    S("You weigh rehabilitation and punishment about equally.",
      means=["You'd want programs for those likely to change while keeping prison tough"]))

T["second_chance"] = trade(
    S("Limit how employers and landlords use criminal records for people who've served nonviolent sentences.",
      yes=["“Ban the box” rules on job applications", "Sealing old nonviolent records"],
      no=["Letting employers and landlords reject anyone with a record"]),
    S("Employers and landlords should be free to consider criminal records.",
      yes=["Asking about records on job and rental applications"],
      no=["Laws hiding or limiting the use of records"]),
    S("You weigh second chances and freedom to consider records about equally.",
      means=["You'd seal old records but let employers see recent ones"]))

T["juveniles_adult_court"] = [
    S("Teens 15 to 17 should never be tried as adults.",
      yes=["Juvenile court for all under-18 cases"], no=["Transfers to adult court"]),
    S("Teens should be tried as adults only for murder.",
      yes=["Adult trials for murder"], no=["Adult trials for robbery or assault"]),
    S("Teens can be tried as adults for serious violent crimes if a judge decides.",
      yes=["Judge-decided transfers to adult court"], no=["Automatic transfers", "Never transferring"]),
    S("Teens should be tried as adults automatically for serious violent crimes.",
      yes=["Automatic adult trials for armed robbery and similar crimes"], no=["Keeping these cases in juvenile court"]),
]

T["private_prisons"] = [
    S("Ban private prisons and private immigration detention centers.",
      yes=["Ending government contracts with private prison companies"], no=["Private prisons"]),
    S("Use private prisons only under strict oversight.",
      yes=["Private prisons with strict inspections and rules"], no=["A ban", "Loose oversight"]),
    S("Use private prisons if they save money.",
      yes=["Contracting with private prisons to cut costs"], no=["Banning private prisons"]),
]

T["road_blocking"] = [
    S("Allow protesters to block roads if it's brief and peaceful.",
      yes=["Tolerating short, peaceful road blockades"], no=["Arrests for peaceful road blocking"]),
    S("Ask road-blocking protesters to move, and arrest only those who refuse.",
      yes=["Warnings first, then arrests"], no=["Immediate arrests", "Letting blockades stay"]),
    S("Arrest road-blocking protesters right away.",
      yes=["Immediate arrests for blocking roads"], no=["Tolerating blockades"]),
    S("Arrest road-blocking protesters and treat it as a serious crime, with possible jail.",
      yes=["Felony-level charges and jail for blocking highways"], no=["Warnings or minor fines"]),
]

T["riot_response"] = [
    S("When a protest turns into rioting, use as little force as possible and focus on calming tensions.",
      yes=["De-escalation, with minimal force"], no=["Sending in the National Guard"]),
    S("Arrest people damaging property, but avoid force against peaceful protesters.",
      yes=["Targeted arrests of looters"], no=["Force against peaceful protesters", "Letting looting go"]),
    S("Use whatever force is needed to stop rioting quickly, including the National Guard.",
      yes=["Heavy force and the National Guard to end riots fast"], no=["Holding back to calm tensions"]),
]

T["troops_in_cities"] = [
    S("A president should never send troops into a city over a governor's objection.",
      yes=["Requiring governors' consent for troops"], no=["Federal troops over a governor's objection"]),
    S("Only during a riot or uprising local police can't control.",
      yes=["Troops for true uprisings, under the Insurrection Act"], no=["Troops for ordinary crime"]),
    S("Yes, whenever the president judges crime is out of control, for any president.",
      yes=["Sending troops to fight crime over a governor's objection"], no=["Requiring a governor's consent"]),
]

T["victims_voice"] = [
    S("Victims' views shouldn't affect sentences or parole.",
      yes=["Decisions based on the law and the offender only"], no=["Victim statements shaping sentences"]),
    S("Victims can speak, but their wishes get no special weight.",
      yes=["Victim statements at hearings"], no=["Giving them significant weight"]),
    S("Victims' views should carry significant weight in sentencing and parole.",
      yes=["Victims' wishes shaping sentences and parole decisions"], no=["Ignoring victims' wishes"]),
]

T["asset_forfeiture"] = [
    S("Police should take cash or property only after a criminal conviction.",
      yes=["Ending civil asset forfeiture"], no=["Seizures without a conviction"]),
    S("Seizure without conviction only with strong evidence the government must prove.",
      yes=["A high burden of proof on the government"], no=["Today's looser rules", "Requiring a conviction"]),
    S("Police should be able to seize property linked to crime without a conviction, as most states allow.",
      yes=["Today's civil forfeiture"], no=["Requiring a conviction"]),
]

T["stop_and_frisk"] = [
    S("Police shouldn't stop and frisk people they find suspicious.",
      yes=["Ending stop-and-frisk"], no=["Pat-downs based on suspicion"]),
    S("Stop-and-frisk only with specific reasons, recorded and reviewed for bias.",
      yes=["Documented, reviewed stops"], no=["Stops on hunches", "A total ban"]),
    S("Police should stop and frisk suspicious people in high-crime areas.",
      yes=["Wide use of stop-and-frisk"], no=["Limits that discourage stops"]),
]

if __name__ == "__main__":
    write("D15", T)
    write_clarity("D15", C)
