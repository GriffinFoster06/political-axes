"""Values: concrete wording for each question and what each answer means."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, agree_item, trade, write, write_clarity  # noqa: E402

C = {}  # clarity edits
T = {}  # statements

# ---------- fairness and wealth ----------
C["fair_small_gaps"] = {
    "why": "'Small' and the means of keeping gaps small were undefined.",
    "scope": "The richest 1% of US households own about 30% of all wealth; the bottom half own about 2.5%. Small gaps would take much higher taxes on large incomes, fortunes and inheritances, spent on everyone else.",
}
T["fair_small_gaps"] = agree_item("fair_small_gaps",
    S("A fair society keeps wealth gaps small, using taxes and benefits to do it.",
      yes=["Much higher taxes on top incomes, large fortunes and big inheritances",
           "Spending that money on benefits and services for people with less",
           "Treating today's gap (the top 1% owning about 30% of wealth) as unfair in itself"],
      no=["Leaving the gap alone as long as people at the bottom are getting richer",
          "Cutting taxes on high earners or large estates"]),
    S("A fair society doesn't need small wealth gaps; how the money was gained matters more than the size of the gap.",
      yes=["Judging a fortune by how it was made, not by how big it is",
           "Leaving large gaps alone when they come from work, saving or building a business"],
      no=["New taxes aimed mainly at shrinking the gap, like a tax on large fortunes",
          "Treating the top 1%'s share of wealth as unfair in itself"]),
    S("You see this both ways about equally.",
      means=["You'd judge ideas like a tax on large fortunes or cutting estate taxes one at a time, rather than by a rule about gaps"]))

C["fair_keep_earnings"] = {
    "why": "'Keep what they earn' didn't say what earnings or what keeping means.",
    "scope": "“What they earn” means pay, business profits and investment gains. Keeping it means low taxes on it, even for the highest earners, such as a founder whose company makes them a billionaire.",
}
T["fair_keep_earnings"] = agree_item("fair_keep_earnings",
    S("People should keep what they earn through pay, profits and investments, even if a few become far richer than everyone else.",
      yes=["Low taxes on income and investment gains, including for the highest earners",
           "Letting founders and investors keep most of what they make, even billions"],
      no=["Raising taxes on top earners mainly to narrow the gap between rich and poor",
          "Caps or special taxes on very large fortunes"]),
    S("Fairness can require taking a larger share from those who end up far richer than others.",
      yes=["Higher tax rates on very high incomes and investment gains",
           "Using that money to help people who earn far less"],
      no=["Cutting taxes for top earners on the grounds that they earned it"]),
    S("You see this both ways about equally.",
      means=["You'd judge each tax on high earners on its own merits rather than by a rule about keeping earnings"]))

C["security_vs_choice"] = {
    "why": "'Basic needs' and 'fewer choices' were undefined.",
    "sides": {
        "0": {"text": "Everyone is guaranteed health care, enough food, a place to live and a basic income, even if taxes are high for most workers and people have less say over their doctor, health plan or pension."},
        "1": {"text": "People keep more of what they earn and choose their own health plan, savings and housing, even if some can't afford health care or a home and go without."},
    },
}
T["security_vs_choice"] = trade(
    S("Everyone should be guaranteed health care, food, housing and a basic income, paid for with high taxes.",
      yes=["Government health coverage, food aid, housing help and a guaranteed income for everyone",
           "Higher taxes on most workers, not only the rich, to pay for it",
           "Less individual choice of health plan or pension in exchange"],
      no=["Cutting guaranteed benefits to lower taxes",
          "Leaving health care and retirement mainly to each person's own choices"]),
    S("People should keep more of their pay and make their own choices, even if some go without.",
      yes=["Lower taxes, with people choosing and paying for their own health plans and savings",
           "Accepting that some people will go without health care or housing"],
      no=["Guaranteed health care, housing or income for everyone paid for with high taxes"]),
    S("You value guaranteed needs and freedom to choose about equally.",
      means=["You'd judge each program, like government health care or a guaranteed income, by its cost and what it gives up"]))

C["equal_treatment_vs_association"] = {
    "why": "'Turned away unfairly' and the kinds of businesses were undefined.",
    "scope": "Businesses open to the public, such as shops, restaurants, hotels, landlords and wedding vendors.",
    "sides": {
        "0": {"text": "Laws that bar them from turning people away over race, religion, sex, sexual orientation, disability or similar traits, even if owners must serve people or events they object to."},
        "1": {"text": "Owners' freedom to choose whom they serve or rent to, even if some people are turned away over traits like these."},
    },
}
T["equal_treatment_vs_association"] = trade(
    S("Businesses open to the public shouldn't be allowed to turn people away over traits like race, religion, sex or sexual orientation.",
      yes=["Anti-discrimination laws covering shops, restaurants, hotels, landlords and wedding vendors",
           "Requiring a baker or photographer who serves weddings to serve same-sex weddings too"],
      no=["Letting owners refuse customers or tenants over their race, religion, sex or sexual orientation",
          "Religious exemptions that let businesses refuse some customers"]),
    S("Owners should be free to choose whom they serve or rent to, even if some people are turned away.",
      yes=["Letting a wedding vendor turn down an event they object to",
           "Narrower anti-discrimination laws for private businesses"],
      no=["Fining or suing owners for refusing to serve someone"]),
    S("You weigh equal treatment and owners' freedom about equally.",
      means=["You'd decide case by case, for example treating a hotel turning guests away differently from a photographer turning down a wedding"]))

C["liberty_vs_order"] = {
    "why": "'Freedoms' and 'order' were abstract.",
    "scope": "Think of things like police stopping and searching people in high-crime areas, curfews during riots, clearing homeless camps from parks, cameras in public places, and limits on protests that block roads.",
    "sides": {
        "0": {"text": "Protecting rights like not being stopped and searched without cause, protesting, and living as you choose in public, even if crime and disorder are harder to control."},
        "1": {"text": "Keeping streets safe and orderly with steps like stop-and-search, curfews, public cameras and clearing camps, even if some people's freedoms are limited."},
    },
}
T["liberty_vs_order"] = trade(
    S("Individual freedoms should win when they clash with keeping order.",
      yes=["Strict limits on police stopping and searching people without cause",
           "Letting protests go ahead even when they block roads",
           "Fewer cameras and less monitoring of public places"],
      no=["Curfews and sweeps of homeless camps", "Stop-and-search in high-crime areas"]),
    S("Public order and safety should win when they clash with individual freedoms.",
      yes=["Stop-and-search in high-crime areas", "Curfews during riots",
           "Clearing homeless camps from parks and sidewalks", "Cameras in public places"],
      no=["Letting protests block roads", "Tight limits on police that make disorder harder to control"]),
    S("You weigh freedom and order about equally.",
      means=["You'd judge each measure, like curfews, camp sweeps or stop-and-search, by how much safety it buys and how much freedom it costs"]))

C["conscience_vs_law"] = {
    "why": "No examples of what breaking a law out of conscience looks like.",
    "scope": "Examples: refusing to fight in a war you think is unjust, hiding someone from deportation, a clerk refusing marriage licenses they object to, blocking a road in protest. Think about laws in general.",
}
T["conscience_vs_law"] = trade(
    S("People should follow their conscience even if it means breaking the law.",
      yes=["Refusing to fight in a war you believe is unjust",
           "Hiding someone from deportation if you believe it's wrong",
           "Officials refusing to carry out laws they find immoral, like a clerk refusing licenses"],
      no=["Obeying a law you believe is wrong while waiting for it to change"]),
    S("People should obey the law and work to change it, even when they think it's wrong.",
      yes=["Following laws you disagree with while you vote, petition or sue to change them",
           "Officials carrying out laws they personally object to, or resigning"],
      no=["Breaking laws in protest, like blocking roads",
          "Hiding people from deportation or refusing a draft"]),
    S("You weigh conscience and obeying the law about equally.",
      means=["Whether to break a law would depend for you on how serious the wrong is"]))

# ---------- tradition and change ----------
C["tradition_wisdom"] = {
    "why": "No examples of which customs and traditions.",
    "scope": "Customs such as marriage before having children, regular religious worship, respect for elders, family meals, traditional roles for men and women, and national rituals like the Pledge of Allegiance.",
}
T["tradition_wisdom"] = agree_item("tradition_wisdom",
    S("Long-standing customs usually hold wisdom worth keeping, even when no one can spell out exactly why.",
      yes=["Keeping customs like marriage before children, regular worship and respect for elders",
           "Making those who want to change a long-standing custom show why it should change"],
      no=["Dropping a custom just because it seems old-fashioned"]),
    S("A custom being old isn't a reason to keep it; each should be judged on its own merits.",
      yes=["Dropping customs that no longer make sense, such as fixed roles for men and women if they limit people",
           "Judging marriage, religious practice or family customs by how well they work today"],
      no=["Keeping a custom mainly because it has lasted a long time"]),
    S("You see this both ways about equally.",
      means=["Some customs on the list seem worth keeping to you and others don't, and age alone doesn't settle it"]))

C["progress_by_questioning"] = {
    "why": "No examples of progress or of traditional ways.",
    "scope": "Changes such as ending slavery, women voting and working outside the home, modern medicine replacing folk remedies, same-sex marriage, and new industries replacing old ones.",
}
T["progress_by_questioning"] = agree_item("progress_by_questioning",
    S("Progress comes mainly from people challenging the way things have always been done.",
      yes=["Encouraging people to challenge long-standing customs and institutions",
           "Changing laws and practices that rest mostly on tradition"],
      no=["Treating long-standing customs as settled"]),
    S("Progress comes mainly from building on what already works, more than from challenging tradition.",
      yes=["Improving existing institutions step by step",
           "Keeping traditional practices unless there's clear evidence they fail"],
      no=["Treating tradition as something to be overcome"]),
    S("You see this both ways about equally.",
      means=["You'd credit some progress on the list to challenging tradition and some to building on it"]))

C["pace_of_change"] = {
    "why": "Didn't say what kind of change.",
    "scope": "Changes of any kind and in any direction, such as legalizing or banning drugs, changing who can marry, raising or cutting taxes and programs, new rules on immigration or guns, and new technology at school and work.",
}
T["pace_of_change"] = [
    S("Big changes should happen fast and all at once.",
      yes=["Overhauling a whole system, like health care or immigration, in one law",
           "Acting while there's a majority for it rather than waiting"],
      no=["Phasing changes in over many years", "Trying changes in a few places first"]),
    S("Change should come at a steady pace, in clear steps.",
      yes=["Changes phased in over a few years with set steps"],
      no=["Overhauls all at once", "Holding off change mainly to keep things as they are"]),
    S("Change should be slow and careful.",
      yes=["Trying changes in a few states or cities first, then expanding",
           "Phasing changes in over many years, with time to undo them"],
      no=["Overhauling whole systems at once"]),
    S("Change as little as possible and keep what works.",
      yes=["Keeping laws and institutions that work, even if imperfect",
           "Changing things only when they have clearly failed"],
      no=["Big reforms in any direction"]),
]

C["moral_rules"] = {
    "why": "No examples of basic moral questions.",
    "scope": "Basic moral questions, like whether lying, stealing, killing or breaking a promise is wrong; not matters of taste.",
}
T["moral_rules"] = [
    S("Whether lying, stealing or even killing is wrong depends entirely on the culture and the situation.",
      means=["No moral rule holds for everyone everywhere",
             "A practice one culture condemns can be right in another"]),
    S("Right and wrong mostly depend on the situation, with a few fixed rules.",
      means=["A handful of acts, like murdering an innocent person, are always wrong",
             "Most others, like lying or breaking a promise, can be right in some situations"]),
    S("Many moral rules are fixed, though some depend on the situation.",
      means=["Acts like murder, theft and betrayal are wrong for everyone",
             "Some questions, like when a lie is acceptable, depend on circumstances"]),
    S("Right and wrong are the same for all people at all times.",
      means=["Acts like murder, theft, lying and adultery are wrong everywhere, in every era, whatever a culture says"]),
]

# ---------- groups ----------
GROUPS = "Groups such as races, religions, social classes or regions. “Power and status” means wealth, top jobs, seats in Congress and on company boards, influence and respect."
C["group_status_natural"] = {"why": "'Power and status' was undefined.", "scope": GROUPS}
C["group_status_equalize"] = {"why": "'Power and status' was undefined.", "scope": GROUPS}
T["group_status_natural"] = agree_item("group_status_natural",
    S("It's natural and acceptable for some groups to end up with more wealth, top jobs and influence than others.",
      yes=["Accepting that groups will differ in wealth, top jobs and political seats",
           "Treating people as individuals rather than measuring groups against each other"],
      no=["Policies designed to make every group equal in wealth or representation",
          "Targets for how many of each group hold top jobs or board seats"]),
    S("It isn't acceptable for some groups to have more wealth, top jobs and influence than others.",
      yes=["Policies that narrow gaps between groups in wealth, top jobs and political seats",
           "Treating a large gap between groups as a problem to fix"],
      no=["Accepting such gaps as natural"]),
    S("You see this both ways about equally.",
      means=["Some gaps between groups seem acceptable to you and others don't"]))
T["group_status_equalize"] = agree_item("group_status_equalize",
    S("Society should actively work to make groups equal in wealth, top jobs and influence.",
      yes=["Policies to close gaps between groups, such as targeted aid, recruitment or outreach",
           "Tracking how each group is represented in top jobs, colleges and government"],
      no=["Accepting large gaps between groups as natural"]),
    S("Society shouldn't try to make groups equal in wealth, top jobs and influence.",
      yes=["Equal rights for every person, without trying to equalize outcomes for groups"],
      no=["Programs aimed at making groups equal in wealth or representation",
          "Targets for group representation in jobs, colleges or government"]),
    S("You see this both ways about equally.",
      means=["You'd back some efforts to close gaps between groups but not others"]))

C["zero_sum"] = {
    "why": "No examples of groups or of getting ahead.",
    "scope": "Groups such as rich and poor, workers and owners, races, men and women, immigrants and people born here, cities and rural areas. Getting ahead means more income, jobs, college seats or political power.",
}
C["positive_sum"] = {
    "why": "No examples of groups or of getting ahead.",
    "scope": C["zero_sum"]["scope"],
}
T["zero_sum"] = agree_item("zero_sum",
    S("When one group gains, another usually loses.",
      means=["When the rich get richer, you'd expect workers or the poor to be losing out",
             "When immigrants gain jobs, or one group gains college seats, you'd expect others to lose them"]),
    S("One group's gains don't usually come at another's expense.",
      means=["Higher profits, more immigrants working or more women in top jobs can leave room for others to gain too"]),
    S("You see this both ways about equally.",
      means=["Some gains on the list look like one group's loss to you, others don't"]))
T["positive_sum"] = agree_item("positive_sum",
    S("Different groups can usually all get ahead together.",
      means=["Owners and workers, immigrants and people born here, cities and rural areas can all gain from the same growth"]),
    S("Groups usually can't all get ahead together; gains for one tend to mean losses for another.",
      means=["Higher profits tend to come out of workers' pay, and more jobs for one group mean fewer for another"]),
    S("You see this both ways about equally.",
      means=["Some groups can rise together in your view, others are in real competition"]))

C["proportional_vs_need"] = {
    "why": "'Something valuable', 'need' and 'contribution' were abstract.",
    "scope": "Things like pay raises at work, public benefits, college aid and help after a disaster.",
    "sides": {
        "0": {"text": "Those who need it most get more, like a struggling single parent or the family hit hardest, even if they worked less or paid less in taxes."},
        "1": {"text": "Those who contributed more get more, like the hardest workers or those who paid more in taxes, even if some in greater need get less."},
    },
}
T["proportional_vs_need"] = trade(
    S("Those who need it most should get more, even if they contributed less.",
      yes=["College aid based on family income rather than grades",
           "Benefits and disaster aid aimed at those hit hardest"],
      no=["Linking benefits mainly to what people paid in taxes", "Merit-only scholarships"]),
    S("Those who contributed more should get more, even if some in greater need get less.",
      yes=["Merit-based pay raises and scholarships",
           "Benefits like Social Security tied to what you paid in"],
      no=["Aid that gives the most to those who contributed least"]),
    S("You weigh need and contribution about equally.",
      means=["You'd want a mix, such as aid that's partly based on need and partly on what people put in"]))

C["get_ahead"] = {
    "why": "'Gets ahead' was undefined.",
    "scope": "Getting ahead means earning a good income, owning a home, or doing better than your parents. Think about people in general, not any one person.",
}
T["get_ahead"] = [
    S("Family background and connections mostly decide who gets ahead.",
      means=["Children of well-off or well-connected parents mostly stay ahead",
             "Most people born poor stay poor, however hard they work"]),
    S("Luck and circumstances mostly decide who gets ahead.",
      means=["Things outside people's control, like health, the economy or where they grew up, matter more than effort or talent"]),
    S("Background, luck and effort all matter about equally.",
      means=["Hard work raises your chances, but where you start and what happens to you count about as much"]),
    S("Talent and skills mostly decide who gets ahead.",
      means=["People with ability, education and in-demand skills mostly rise, wherever they start"]),
    S("Hard work mostly decides who gets ahead.",
      means=["Most people who work hard and keep at it can get ahead in the US today, wherever they start"]),
]

# ---------- children ----------
C["child_independence"] = {
    "why": "'Question rules' and 'respect authority' had no concrete behavior.",
    "scope": "Children of elementary and middle school age, at home and at school.",
    "sides": {
        "0": {"text": "To ask why a rule exists, say when they disagree with a parent or teacher, and make some choices of their own, even if they argue more and are harder to manage."},
        "1": {"text": "To follow rules from parents, teachers and other adults without arguing, and accept “because I said so,” even if they question things less."},
    },
}
T["child_independence"] = trade(
    S("Children should learn to question rules and think for themselves.",
      yes=["Children asking why a rule exists and arguing their side",
           "Letting children make some choices, like their activities or how to spend free time"],
      no=["Expecting children to obey adults without asking why"]),
    S("Children should learn to respect rules and authority.",
      yes=["Children doing what parents and teachers say without arguing",
           "“Because I said so” as a good enough reason"],
      no=["Children openly challenging adults' rules"]),
    S("You value both about equally.",
      means=["You'd want children to obey most rules but feel free to ask why"]))

C["child_discipline"] = {
    "why": "'Express themselves', 'behave badly', 'discipline' and 'good manners' were undefined.",
    "scope": "Children of elementary school age, about 5 to 11.",
    "sides": {
        "0": {"text": "Let children show strong feelings, speak up, dress and play as they like, and handle misbehavior by talking it through, even if they're sometimes loud, rude or defiant."},
        "1": {"text": "Expect please and thank you, sitting still at meals and in class, and obeying the first time, with time-outs or lost privileges when they don't, even if that means stricter parenting."},
    },
}
T["child_discipline"] = trade(
    S("Children should have room to express themselves, even if they sometimes misbehave.",
      yes=["Letting children show strong feelings and speak up",
           "Handling misbehavior by talking it through rather than punishing",
           "Letting children choose how they dress and play"],
      no=["Time-outs or lost privileges as the main response to misbehavior",
          "Expecting children to sit still and stay quiet"]),
    S("Children should be held to discipline and good manners, even if that means stricter parenting.",
      yes=["Expecting please and thank you, sitting still at meals and in class, and obeying the first time",
           "Consequences like time-outs or lost privileges for misbehaving"],
      no=["Letting rudeness or defiance slide so children can express themselves"]),
    S("You value both about equally.",
      means=["You'd set firm rules on manners but leave children room to show their feelings"]))

# ---------- country and world ----------
C["weigh_foreigners"] = {
    "why": "No examples of the decisions or tradeoffs involved.",
    "scope": "Decisions like trade deals that cost some US jobs but raise incomes abroad, aid for disease and famine, how many refugees to take in, and climate rules that mostly help other countries.",
}
T["weigh_foreigners"] = trade(
    S("The US should weigh people abroad about as much as Americans, even if Americans sometimes lose out.",
      yes=["A trade deal that costs some US jobs if it lifts far more people abroad out of poverty",
           "Spending on vaccines and famine relief abroad even when the money could go to Americans",
           "Taking in more refugees even at some cost to Americans"],
      no=["Turning down help abroad mainly because Americans don't gain from it"]),
    S("The US should put Americans' interests first, even if people elsewhere are worse off.",
      yes=["Turning down trade deals that cost US jobs, even if they'd help poorer countries more",
           "Cutting aid abroad when the money could be spent on Americans",
           "Setting refugee and immigration numbers by what's good for Americans"],
      no=["Accepting costs to Americans to help people abroad"]),
    S("You weigh Americans' interests and people abroad about equally.",
      means=["You'd accept small costs to Americans for big gains abroad, but not large ones"]))

C["loyalty_humanity_country"] = {
    "why": "Abstract; no example of what each loyalty looks like.",
    "scope": "Your own sense of loyalty: for example, whether you'd sooner call yourself a citizen of the world or an American first.",
}
T["loyalty_humanity_country"] = trade(
    S("Your strongest loyalty is to humanity as a whole.",
      means=["You think of yourself as a citizen of the world before an American",
             "When the interests of the US and the rest of the world clash, you'd feel pulled toward the world"]),
    S("Your strongest loyalty is to your country.",
      means=["You think of yourself as an American first",
             "When the interests of the US and the rest of the world clash, you'd feel pulled toward the US"]),
    S("Your loyalty to humanity and to your country are about equal.",
      means=["You'd feel pulled both ways when US interests clash with the rest of the world's"]))

# ---------- human nature and morality ----------
EVERYDAY = "Everyday situations such as returning a lost wallet, paying taxes honestly, not littering, telling the truth on a form, and waiting your turn."
C["people_trustworthy"] = {"why": "'The right thing' had no examples.", "scope": EVERYDAY}
C["people_selfish"] = {"why": "'Act selfishly' had no examples.", "scope": EVERYDAY}
T["people_trustworthy"] = agree_item("people_trustworthy",
    S("Most people will do the right thing without rules forcing them to.",
      means=["You'd expect most people to return a lost wallet, pay their taxes honestly and wait their turn even without fines, audits or police"]),
    S("Most people won't do the right thing unless rules make them.",
      means=["Without fines, audits or police, you'd expect many people to keep a lost wallet, cheat on taxes or cut in line"]),
    S("You see this both ways about equally.",
      means=["You'd trust people on some things on the list but not others"]))
T["people_selfish"] = agree_item("people_selfish",
    S("Without strong rules and consequences, most people will act selfishly.",
      means=["Without fines, audits or police, you'd expect most people to cheat on taxes, litter, cut in line or keep a lost wallet"]),
    S("Most people won't act selfishly even without strong rules and consequences.",
      means=["You'd expect most people to return a lost wallet, pay taxes honestly and wait their turn even if no one were checking"]),
    S("You see this both ways about equally.",
      means=["You'd expect people to behave on some things on the list but not others"]))

SACRED = "Examples people point to: burning a national flag in private, dishonoring a dead body, cloning a human, selling your own kidney, or mocking a holy book where no one sees."
SACRED_DEF = [
    {"term": "sacred", "text": "Treated as holy or as deserving reverence, such as God, a holy book, the flag, or the dead."},
    {"term": "natural", "text": "In keeping with how things are meant to be, such as human biology or the family."},
]
C["sacred_limits"] = {"why": "'Sacred or natural' had no examples or definition.", "scope": SACRED, "definitions": SACRED_DEF}
C["harm_only"] = {"why": "No examples of acts that harm nobody.", "scope": SACRED}
T["sacred_limits"] = agree_item("sacred_limits",
    S("Some acts are wrong even when no one is harmed, because they violate what's sacred or natural.",
      yes=["Calling acts like dishonoring the dead, cloning a human or desecrating a holy book wrong, even in private"],
      no=["The view that only harm to others makes an act wrong"]),
    S("An act isn't wrong just because it goes against what's sacred or natural; what matters is whether it harms someone.",
      yes=["Judging acts only by whether they hurt someone",
           "Seeing private acts like burning your own flag or mocking a holy book as not wrong"],
      no=["Calling harmless acts wrong because they offend religious or natural order"]),
    S("You see this both ways about equally.",
      means=["Some acts on the list seem wrong to you even though no one is hurt; others don't"]))
T["harm_only"] = agree_item("harm_only",
    S("If an act harms nobody, it isn't wrong.",
      yes=["Seeing private acts like burning your own flag or mocking a holy book as not wrong",
           "Judging acts only by whether they hurt someone"],
      no=["Calling harmless acts wrong because they offend religious or natural order"]),
    S("An act can be wrong even if it harms nobody.",
      yes=["Calling acts like dishonoring the dead, cloning a human or desecrating a holy book wrong, even in private"],
      no=["The view that only harm to others makes an act wrong"]),
    S("You see this both ways about equally.",
      means=["Some harmless acts on the list seem wrong to you; others don't"]))

# ---------- government and social problems ----------
C["gov_role_values"] = {
    "why": "'Social problem' and 'makes things worse' had no examples.",
    "scope": "Social problems such as poverty, homelessness, drug addiction, failing schools and people without health insurance. Government efforts such as cash and food aid, public housing, federal school programs, addiction treatment and Medicaid.",
    "definitions": [{"term": "makes things worse", "text": "The problem ends up as bad or worse than before, or the side effects, such as cost, dependence on aid, or pushing out families, charities and businesses, outweigh what was gained."}],
}
T["gov_role_values"] = agree_item("gov_role_values",
    S("Government programs aimed at problems like poverty, homelessness and addiction usually backfire.",
      yes=["Shrinking or ending programs like public housing and long-term cash aid",
           "Leaving problems like homelessness and addiction mostly to families, charities, churches and local groups"],
      no=["New government programs to tackle these problems",
          "Expanding programs like public housing or Medicaid"]),
    S("Government efforts on problems like poverty, homelessness and addiction usually help more than they hurt.",
      yes=["Keeping or expanding programs like food aid, Medicaid, public housing and addiction treatment",
           "New government programs when a problem is going unsolved"],
      no=["Cutting these programs on the grounds that they backfire"]),
    S("You see this both ways about equally.",
      means=["Some programs on the list seem to work to you and others seem to backfire"]))

C["gov_role_values_rev"] = {
    "why": "No examples of problems or of what solving them without the federal government means.",
    "scope": "Problems such as poverty among older people, people without health insurance, polluted air and rivers, recovering from big disasters, and worn-out highways. “Without the federal government” means left to states, cities, charities, churches, businesses and families.",
}
T["gov_role_values_rev"] = agree_item("gov_role_values_rev",
    S("Some problems, like old-age poverty, pollution and disaster recovery, are too big to solve without the federal government.",
      yes=["Federal programs like Social Security, Medicare, disaster aid and national pollution limits",
           "Federal money for highways and other large projects"],
      no=["Handing these problems to states, charities and businesses alone"]),
    S("Problems like old-age poverty, pollution and disaster recovery can be solved without the federal government.",
      yes=["Shifting programs and money from Washington to states and cities",
           "Relying on charities, churches, businesses and families for problems like these"],
      no=["New or larger federal programs for these problems"]),
    S("You see this both ways about equally.",
      means=["Some problems on the list need the federal government in your view and others don't"]))

if __name__ == "__main__":
    write("D25", T)
    write_clarity("D25", C)
