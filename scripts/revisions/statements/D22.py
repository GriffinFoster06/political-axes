"""Foreign policy and defense."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

C["engagement_tradeoff"] = {
    "why": "'Active role' and 'world affairs' had no examples.",
    "scope": "Think about the long run, not one conflict. An active role means things like military alliances, bases abroad, foreign aid, and pressing other countries on trade and security.",
}
T["engagement_tradeoff"] = trade(
    S("The US should take an active role in world affairs, even if it's costly and risks war.",
      yes=["Keeping alliances like NATO and bases abroad", "Foreign aid and diplomacy to shape events"],
      no=["Pulling back from alliances and bases"]),
    S("The US should focus on problems at home and stay out of other countries' affairs, even if rivals gain influence.",
      yes=["Bringing troops home", "Cutting foreign aid and commitments abroad"],
      no=["New military commitments abroad"]),
    S("You weigh an active role abroad and focusing at home about equally.",
      means=["You'd keep core alliances but avoid new commitments"]))

C["allies_tradeoff"] = {
    "why": "No examples of working with allies versus acting alone.",
    "scope": "Think about trade, security and diplomacy: for example, sanctions, military action, tariffs and climate or trade agreements.",
}
T["allies_tradeoff"] = trade(
    S("The US should work through alliances and agreements, even if it means compromising.",
      yes=["Joint sanctions and military action with allies", "Trade and security agreements"],
      no=["Acting alone over allies' objections"]),
    S("The US should act on its own to pursue its interests, even if allies object.",
      yes=["Unilateral tariffs, sanctions or strikes when they serve US interests"],
      no=["Watering down US goals to keep allies on board"]),
    S("You weigh working with allies and acting alone about equally.",
      means=["You'd work with allies by default but act alone on vital interests"]))

T["ally_attacked"] = [
    S("If a treaty ally like a NATO member is attacked, the US should send troops to help defend it.",
      yes=["US troops defending an attacked ally"], no=["Limiting help to weapons or sanctions"]),
    S("The US should send weapons and money to an attacked ally, but not troops.",
      yes=["Arms and money for the ally"], no=["Sending US troops", "Staying out"]),
    S("The US should sanction the attacker and send humanitarian aid, but not weapons or troops.",
      yes=["Sanctions and humanitarian aid"], no=["Weapons or troops"]),
    S("The US should stay out, even when a treaty ally is attacked.",
      yes=["No US involvement"], no=["Sanctions, weapons or troops"]),
]

T["nato"] = [
    S("Stay in NATO and strengthen the US commitment.",
      yes=["More US forces and support for NATO"], no=["Reducing the US role"]),
    S("Stay in NATO, but require allies to spend much more on defense.",
      yes=["Pressing allies to raise military spending"], no=["Leaving NATO", "Accepting today's ally spending"]),
    S("Stay in NATO, but reduce US forces in Europe.",
      yes=["Bringing some troops home from Europe"], no=["Leaving NATO", "Adding forces"]),
    S("Leave NATO and bring US forces home from Europe.",
      yes=["Withdrawing from NATO"], no=["US defense promises to European allies"]),
]

C["defense_spending"] = {
    "why": "'Somewhat' and 'a lot' had no scale.",
    "scope": "Today it is roughly $900 billion to $1 trillion a year, more than the next several countries combined. “Somewhat” means about 5% to 10%; “a lot” means a quarter or more.",
}
T["defense_spending"] = [
    S("Cut military spending by a quarter or more.", yes=["Cutting $200 billion or more a year"], no=["Keeping or raising spending"]),
    S("Cut military spending somewhat.", yes=["Trimming about 5–10%"], no=["Deep cuts", "Raising military spending"]),
    S("Keep military spending about the same.", yes=["Today's military budget"], no=["Cutting or raising it"]),
    S("Raise military spending somewhat.", yes=["Adding about 5–10%"], no=["Cutting military spending", "A huge military buildup"]),
    S("Raise military spending a lot.", yes=["Adding a quarter or more, roughly $250 billion a year"], no=["Cutting military spending"]),
]

T["troops_abroad"] = [
    S("Bring most US troops home from bases in Germany, Japan, South Korea and elsewhere.",
      yes=["Closing most permanent bases abroad"], no=["Keeping troops stationed abroad"]),
    S("Reduce US troops abroad gradually.", yes=["Drawing down bases over time"], no=["Rapid withdrawal", "Keeping or adding troops"]),
    S("Keep about today's level of US troops abroad.", yes=["Today's bases and troop levels"], no=["Cutting or adding troops"]),
    S("Station more US troops abroad.", yes=["More bases and troops in allied countries"], no=["Bringing troops home"]),
]
T["use_force_cases"] = existing("D22", "use_force_cases")

C["foreign_aid_level"] = {
    "why": "'A lot' and 'somewhat' had no scale.",
    "scope": "Economic, health and humanitarian aid, not military aid. It has usually been about 1% of the federal budget. “A lot” means half again or more; “somewhat” means about 10% to 20%.",
}
T["foreign_aid_level"] = [
    S("Raise US foreign aid a lot.", yes=["Raising economic, health and humanitarian aid by half or more"], no=["Cutting foreign aid"]),
    S("Raise US foreign aid somewhat.", yes=["Raising aid about 10–20%"], no=["Cutting foreign aid", "Large increases"]),
    S("Keep US foreign aid about the same.", yes=["Aid at about 1% of the budget"], no=["Raising or cutting it"]),
    S("Cut US foreign aid somewhat.", yes=["Trimming aid about 10–20%"], no=["Raising aid", "Ending most aid"]),
    S("End most US foreign aid.", yes=["Ending most economic, health and humanitarian aid"], no=["Keeping aid programs"]),
]

T["global_health_aid"] = [
    S("Increase US funding to fight diseases like HIV and malaria abroad.", yes=["More money for programs like PEPFAR and malaria nets"], no=["Cutting global health aid"]),
    S("Keep US global health funding about the same.", yes=["Today's global health programs"], no=["Raising or cutting them"]),
    S("Reduce US global health funding.", yes=["Cuts to global health programs"], no=["Raising funding"]),
    S("End US global health funding; that's for other countries to handle.", yes=["Ending programs like PEPFAR"], no=["Any US global health funding"]),
]

T["israel_military_aid"] = [
    S("Give Israel military aid without conditions.", yes=["Unconditional military aid to Israel"], no=["Limits on how weapons are used"]),
    S("Give Israel military aid with conditions on how weapons are used.", yes=["Aid tied to rules on weapons use"], no=["Unconditional aid", "Ending aid"]),
    S("Give Israel only defensive military aid, like missile defense.", yes=["Funding Iron Dome and similar defenses"], no=["Offensive weapons for Israel"]),
    S("Give Israel no military aid.", yes=["Ending US military aid to Israel"], no=["Any military aid to Israel"]),
]

T["palestinian_state"] = [
    S("The US should push hard now for an independent Palestinian state alongside Israel.", yes=["Recognizing a Palestinian state now", "Pressing Israel to accept it"], no=["Waiting for a negotiated peace"]),
    S("The US should support a Palestinian state only after a negotiated peace with security guarantees for Israel.", yes=["A two-state outcome through negotiation"], no=["Recognizing a state now", "Opposing any Palestinian state"]),
    S("The US shouldn't support a Palestinian state.", yes=["Opposing Palestinian statehood"], no=["US support for a two-state solution"]),
]

T["ukraine_support"] = [
    S("Send more military aid to help Ukraine win back its territory.", yes=["More weapons and money for Ukraine"], no=["Pressing Ukraine to give up territory"]),
    S("Give Ukraine enough aid to defend itself while pushing for talks.", yes=["Continued defensive aid plus diplomacy"], no=["Aid for retaking all territory", "Cutting aid"]),
    S("End most aid and press Ukraine to accept a settlement.", yes=["Cutting aid to push a deal"], no=["Continued military aid"]),
    S("End all aid to Ukraine and stay out.", yes=["Ending all US aid to Ukraine"], no=["Any US aid or involvement"]),
]

T["taiwan_defense"] = [
    S("If China invaded Taiwan, the US should stay out.", yes=["No US response to an invasion"], no=["Sanctions, weapons or troops"]),
    S("If China invaded Taiwan, the US should impose sanctions only.", yes=["Sanctions on China"], no=["Sending weapons or troops"]),
    S("If China invaded Taiwan, the US should send weapons and impose sanctions, but not troops.", yes=["Arms for Taiwan and sanctions on China"], no=["US forces fighting China"]),
    S("If China invaded Taiwan, the US should send its own forces to defend Taiwan.", yes=["US military defense of Taiwan"], no=["Staying out of the fight"]),
]

T["china_posture"] = [
    S("Cooperate with China on shared problems and avoid confrontation.", yes=["Working with China on climate, health and trade"], no=["Treating China as an enemy"]),
    S("Compete with China economically, but keep talking and cooperate where possible.", yes=["Tech and trade limits plus ongoing diplomacy"], no=["Confrontation on every front", "Avoiding competition"]),
    S("Treat China as the main adversary and confront it on every front.", yes=["Broad pressure on China in trade, tech and the military"], no=["Cooperating with China"]),
]

T["united_nations"] = [
    S("Give the UN more power and US funding.", yes=["More US money and authority for the UN"], no=["Cutting UN funding"]),
    S("Stay in the UN and pay the full US share.", yes=["Paying full UN dues"], no=["Cutting funding", "Leaving the UN"]),
    S("Stay in the UN, but cut funding and take part less.", yes=["Lower UN dues and less participation"], no=["Paying the full share", "Leaving the UN"]),
    S("Leave the UN.", yes=["Withdrawing from the United Nations"], no=["UN membership"]),
]

T["international_courts"] = [
    S("Join the International Criminal Court and accept its authority, including over Americans.", yes=["US membership in the ICC"], no=["Shielding Americans from the court"]),
    S("Cooperate with the court case by case, without joining.", yes=["Helping with some ICC cases"], no=["Joining the ICC", "Refusing all cooperation"]),
    S("Don't join or cooperate with the International Criminal Court.", yes=["No US cooperation with the ICC"], no=["Membership or cooperation"]),
    S("Don't join, and punish the court when it targets Americans or US allies.", yes=["Sanctions on ICC officials"], no=["Cooperating with the ICC"]),
]

C["human_rights_tradeoff"] = {
    "why": "'Press on human rights' had no examples.",
    "scope": "Countries that jail critics or persecute minorities. Pressing could mean sanctions, cutting arms sales or limiting trade.",
}
T["human_rights_tradeoff"] = trade(
    S("The US should press countries on human rights, even if it hurts trade or security ties.",
      yes=["Sanctions and arms-sale cuts over human rights abuses"], no=["Overlooking abuses for trade or security"]),
    S("The US should work with countries when it serves US interests, whatever their record.",
      yes=["Trade and security deals with abusive governments"], no=["Sanctions that cost US interests"]),
    S("You weigh human rights and US interests about equally.",
      means=["You'd press on the worst abuses but keep vital ties"]))

T["nuclear_arms_control"] = [
    S("Negotiate sharp nuclear cuts with Russia and China, aiming eventually for none.", yes=["Deep mutual cuts toward zero"], no=["Building up the arsenal"]),
    S("Negotiate mutual limits while keeping a strong nuclear arsenal.", yes=["Arms control treaties with a strong deterrent"], no=["Aiming for zero", "Building up without limits"]),
    S("Don't negotiate limits; build up nuclear forces without limits.", yes=["An unlimited nuclear buildup"], no=["Arms control treaties"]),
]

T["national_service"] = [
    S("Service should stay fully voluntary for young Americans.", yes=["Volunteer military and service programs"], no=["Required service"]),
    S("No requirement, but strong rewards like college aid for those who serve.", yes=["College aid and other rewards for service"], no=["Required service"]),
    S("Every young American should do a year of military or civilian service.", yes=["A national service requirement for ages 18–25"], no=["Voluntary-only service"]),
    S("Every young American should do required military service.", yes=["A peacetime military draft for everyone"], no=["Voluntary or civilian options instead"]),
]

T["strikes_on_terrorists"] = [
    S("The US should never use drone strikes against terrorist leaders abroad.", yes=["Ending drone strikes"], no=["Targeted killings abroad"]),
    S("Drone strikes only with the other country's permission.", yes=["Strikes with host-country consent"], no=["Strikes without permission"]),
    S("Strike terrorist leaders wherever they are, with or without permission.", yes=["Drone strikes anywhere"], no=["Limits based on host-country consent"]),
]

T["arms_sales"] = [
    S("US companies shouldn't sell weapons to any other country.", yes=["Banning arms exports"], no=["Arms sales even to allies"]),
    S("Allow weapons sales only to close allies that are democracies.", yes=["Arms sales to allies like the UK and Japan"], no=["Sales to non-democracies"]),
    S("Allow weapons sales to friendly countries, except those with poor human rights records.", yes=["Sales to friendly governments with decent records"], no=["Sales to abusive governments"]),
    S("Allow weapons sales to any friendly government.", yes=["Arms sales to friendly governments whatever their record"], no=["Human rights limits on arms sales"]),
]

T["iran_nuclear"] = [
    S("If Iran moved to build a nuclear weapon, the US should negotiate and accept some risk.", yes=["Diplomacy without military threats"], no=["Military strikes on Iran"]),
    S("The US should negotiate, backed by tough sanctions, but not strike.", yes=["Talks plus heavy sanctions"], no=["Military strikes"]),
    S("The US should strike Iran's nuclear sites if talks fail.", yes=["Strikes as a last resort"], no=["Ruling out strikes", "Striking before talks"]),
    S("The US should strike Iran's nuclear sites right away.", yes=["Immediate military strikes"], no=["Waiting on negotiations"]),
]

T["acquire_territory"] = [
    S("The US shouldn't try to gain new territory like Greenland.", yes=["No new US territory"], no=["Buying or pressuring for territory"]),
    S("The US should gain territory only if the people living there vote for it.", yes=["Territory by local vote"], no=["Acquiring land over residents' objections"]),
    S("The US should buy or negotiate for new territory, even if the people there object.", yes=["Purchasing territory like Greenland over local objection"], no=["Military or economic coercion"]),
    S("The US should gain new territory by any means, including economic or military pressure.", yes=["Pressure or force to acquire territory"], no=["Limiting acquisition to consent"]),
]

if __name__ == "__main__":
    write("D22", T)
    write_clarity("D22", C)
