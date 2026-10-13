"""Federalism and the size of government."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, trade, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

C["national_vs_state_tradeoff"] = {
    "why": "'Major policies' had no examples.",
    "scope": "Major policies like abortion, guns, the minimum wage, school standards and marijuana, whichever party is in power.",
}
T["national_vs_state_tradeoff"] = trade(
    S("Major policies should be set nationally so rules are the same everywhere, even if some states disagree.",
      yes=["National laws on issues like abortion, guns and the minimum wage"], no=["Rules that change at each state line"]),
    S("States should decide most policies, even if rules differ from state to state.",
      yes=["Each state setting its own rules on abortion, guns, wages and schools"], no=["National rules overriding states"]),
    S("You weigh national standards and state control about equally.",
      means=["You'd set some issues nationally and leave others to states"]))

T["closer_government_tradeoff"] = trade(
    S("The federal government solves problems like roads, schools and public health better.",
      yes=["Federal money and rules for roads, schools and public health"], no=["Shifting these jobs to states and cities"]),
    S("State and local governments solve these problems better, even if some lack money or expertise.",
      yes=["Handing roads, schools and public health to states and cities"], no=["Federal control of these jobs"]),
    S("You'd trust federal and state or local government about equally.",
      means=["Which level is better depends on the problem"]))
T["states_differ"] = existing("D24", "states_differ")

T["state_preemption"] = [
    S("States should be able to stop cities from passing their own laws on things like minimum wage, guns or plastic bags.",
      yes=["State laws overriding city ordinances"], no=["Cities setting their own rules"]),
    S("States should override city laws only where one statewide rule is clearly needed.",
      yes=["Limited state overrides"], no=["Blanket preemption", "No state overrides"]),
    S("Cities should set their own rules on these things without states overriding them.",
      yes=["Local control over wages, guns and bags"], no=["State preemption laws"]),
]

T["grant_conditions"] = [
    S("The federal government should be able to withhold money from states over any policy it chooses.",
      yes=["Cutting funds to states that don't follow federal policy, under any administration"], no=["Limits on funding conditions"]),
    S("The federal government can attach conditions only about how that money is spent.",
      yes=["Conditions tied to the program being funded"], no=["Cutting funds over unrelated policies"]),
    S("Federal money to states should come with no conditions.",
      yes=["No-strings federal grants"], no=["Any funding conditions"]),
]
T["grant_conditions_cases"] = existing("D24", "grant_conditions_cases")

T["state_refusal"] = [
    S("States must help enforce federal laws, even ones they disagree with.",
      yes=["Requiring state police to help with federal laws"], no=["States refusing to cooperate"]),
    S("States can decline to use their own police and resources on federal laws, but can't block federal agents.",
      yes=["States declining to help", "Federal agents still enforcing"], no=["States blocking federal agents"]),
    S("States can refuse to help and pass laws blocking federal enforcement within their borders.",
      yes=["State laws blocking federal enforcement"], no=["Federal enforcement over state objections"]),
]
T["state_refusal_cases"] = existing("D24", "state_refusal_cases")

C["federal_size"] = {
    "why": "'Bigger' and 'smaller' didn't say in what way.",
    "scope": "Think about what it does and spends, not about any particular administration. Today federal spending is about $7 trillion a year, a little under a quarter of the economy. Bigger means more spending and more programs; smaller means fewer.",
}
T["federal_size"] = [
    S("The federal government should be much bigger, doing much more.",
      yes=["Large new federal programs in areas like health care, childcare and housing", "Federal spending well above today's level"],
      no=["Cutting federal programs or agencies"]),
    S("The federal government should be somewhat bigger.",
      yes=["Some new or expanded federal programs"], no=["Large new programs", "Cutting programs"]),
    S("The federal government should stay about the size it is now.",
      yes=["Federal spending and programs at about today's level"], no=["Major expansion", "Major cuts"]),
    S("The federal government should be somewhat smaller.",
      yes=["Trimming federal spending and some programs"], no=["New federal programs", "Closing major agencies"]),
    S("The federal government should be much smaller, doing far less.",
      yes=["Closing agencies and ending many programs", "Leaving more to states, charities and markets"],
      no=["New or expanded federal programs"]),
]

C["experimentation_tradeoff"] = {
    "why": "No examples of state experiments.",
    "scope": "Policies on things like health care, schools or welfare: for example, a state trying single-payer health care, school vouchers, or work requirements for aid.",
}
T["experimentation_tradeoff"] = trade(
    S("When it's unclear what works, pick one national approach based on the best evidence.",
      yes=["One national health, school or welfare policy"], no=["Each state trying its own approach"]),
    S("Let states try different approaches, even if some get it wrong.",
      yes=["States testing ideas like single-payer, vouchers or work requirements"], no=["One national approach for everyone"]),
    S("You weigh one national approach and state experiments about equally.",
      means=["You'd let states experiment, then adopt what works nationally"]))

if __name__ == "__main__":
    write("D24", T)
    write_clarity("D24", C)
