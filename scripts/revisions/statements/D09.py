"""Abortion and reproduction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

T["abortion_rule"] = [
    S("Abortion should be legal for any reason at any point in pregnancy.",
      yes=["No legal limit on abortion at any stage"],
      no=["Bans after viability or after 15 weeks", "Limiting abortion to specific circumstances"]),
    S("Abortion should be legal for any reason until about 24 weeks; after that, only for serious health risks.",
      yes=["Abortion on request through about viability", "Later abortions for serious risks to the woman's health"],
      no=["Limits at 12–15 weeks", "No limits at all"]),
    S("Abortion should be legal for any reason in about the first 12 to 15 weeks; after that, only in specific circumstances.",
      yes=["Abortion on request in the first trimester or so", "Limits after about 15 weeks"],
      no=["Abortion on request up to viability", "Bans in early pregnancy"]),
    S("Abortion should be legal only in specific circumstances, like rape, incest or a threat to the woman's life or health.",
      yes=["Abortion for rape, incest, and risks to the woman's life or health"],
      no=["Abortion on request at any stage"]),
    S("Abortion should be legal only to save the woman's life.",
      yes=["A ban with a life-of-the-woman exception"],
      no=["Exceptions for rape, incest or health", "Abortion on request"]),
    S("Abortion should never be legal.",
      yes=["A total ban, with no exceptions"],
      no=["Any legal abortion"]),
]
T["abortion_exceptions"] = existing("D09", "abortion_exceptions")

T["abortion_who_decides"] = [
    S("Abortion law should be the same nationwide, set by Congress.",
      yes=["A national abortion law that overrides state laws"],
      no=["Each state setting its own law"]),
    S("Congress should mostly set abortion law, with room for states to adjust details.",
      yes=["A national baseline with state adjustments"],
      no=["Leaving it fully to states", "No state role at all"]),
    S("Each state should decide its abortion law, as today.",
      yes=["State-by-state abortion laws"],
      no=["A national abortion law, either protecting or banning it"]),
]

T["abortion_pills_mail"] = [
    S("Doctors should be able to prescribe abortion pills online and mail them anywhere, including states with bans.",
      yes=["Telehealth prescriptions and mail delivery to any state"],
      no=["Requiring in-person visits"]),
    S("Doctors can prescribe abortion pills online and mail them, but only to states where abortion is legal.",
      yes=["Telehealth abortion in states where it's legal"],
      no=["Mailing pills into states with bans", "Requiring in-person visits"]),
    S("Abortion pills should require an in-person doctor visit.",
      yes=["In-person dispensing only"],
      no=["Telehealth prescriptions and mail delivery"]),
    S("Abortion pills shouldn't be available at all.",
      yes=["Pulling abortion pills from the market"],
      no=["Any legal access to abortion pills"]),
]

T["abortion_shield_laws"] = [
    S("States should fully protect their doctors from other states' prosecution for mailing abortion pills.",
      yes=["Shield laws blocking extradition and out-of-state lawsuits"],
      no=["Doctors facing the patient's state's laws"]),
    S("Protect doctors only for care given in person in their own state.",
      yes=["Shielding in-person care", "No protection for mailing pills into ban states"],
      no=["Full shield laws", "No protection at all"]),
    S("Doctors should face the laws of the patient's state.",
      yes=["Letting ban states prosecute or sue out-of-state doctors who mail pills"],
      no=["Shield laws"]),
]

T["abortion_public_funding"] = [
    S("Medicaid and other government health programs should pay for abortions like other care.",
      yes=["Repealing the Hyde Amendment's limits"],
      no=["Limiting coverage to rape, incest and life"]),
    S("Government health programs should pay for abortions only for rape, incest or a threat to life, as now.",
      yes=["Today's Hyde Amendment rules"],
      no=["Full coverage", "No coverage at all"]),
    S("Government health programs should never pay for abortions.",
      yes=["Ending even the rape, incest and life exceptions"],
      no=["Any public funding for abortion"]),
]

T["ivf_embryos"] = [
    S("IVF should be legal and insurance should have to cover it.",
      yes=["Required insurance coverage of IVF", "Freezing or discarding unused embryos as patients choose"],
      no=["Limits on what happens to unused embryos"]),
    S("IVF should be legal under today's rules.",
      yes=["Today's IVF rules"],
      no=["Required coverage", "Limits on discarding embryos"]),
    S("IVF should be legal, with limits so unused embryos aren't destroyed.",
      yes=["Rules against discarding embryos, such as creating fewer or requiring them to be kept or donated"],
      no=["Discarding unused embryos"]),
    S("IVF should be banned because it destroys embryos.",
      yes=["A ban on IVF"],
      no=["Legal IVF"]),
]

T["contraception_access"] = [
    S("Birth control should be free to anyone, with no prescription needed.",
      yes=["Free, over-the-counter birth control for adults"],
      no=["Prescription requirements or cost barriers"]),
    S("Insurance must cover birth control at no extra cost, as today.",
      yes=["Today's no-cost coverage requirement"],
      no=["Dropping the requirement", "Restricting any type"]),
    S("Birth control should be legal, but employers and insurers shouldn't have to cover it.",
      yes=["Ending the coverage requirement"],
      no=["Required no-cost coverage", "Restrictions on legal methods"]),
    S("Some types of birth control, such as emergency contraception, should be restricted.",
      yes=["Limits on emergency contraception and some other methods"],
      no=["Unrestricted access to all methods"]),
]

T["minors_abortion_parents"] = [
    S("A girl under 18 should decide on abortion with her doctor, without parents.",
      yes=["No parental notice or consent laws"],
      no=["Requiring parents to be told or to agree"]),
    S("A parent must be told before a minor's abortion, but needn't give permission.",
      yes=["Parental notification laws"],
      no=["Parental consent requirements", "No notice at all"]),
    S("A parent must give permission for a minor's abortion, but a judge can make an exception.",
      yes=["Parental consent with a court bypass"],
      no=["Notice only", "Consent with no exceptions"]),
    S("A parent must give permission for a minor's abortion, with no exceptions.",
      yes=["Parental consent with no court bypass"],
      no=["Letting a judge waive consent"]),
]

T["life_begins"] = [
    S("A developing human gets the same right to life as a born person only at birth.",
      means=["Before birth, a fetus doesn't have the right to life a born baby has"]),
    S("A developing human gets the same right to life around viability, about 22 to 24 weeks.",
      means=["After it could survive outside the womb, a fetus has the same right to life as a born person"]),
    S("A developing human gets the same right to life once cardiac activity can be detected, about 6 weeks.",
      means=["From about 6 weeks on, a developing human has the same right to life as a born person"]),
    S("A developing human has the same right to life from conception.",
      means=["A fertilized egg has the same right to life as a born person"]),
]

T["surrogacy"] = [
    S("Paid surrogacy should be legal and regulated.",
      yes=["Paid surrogacy contracts with legal rules"],
      no=["Banning paid surrogacy"]),
    S("Only unpaid surrogacy should be allowed, with expenses covered.",
      yes=["Covering a surrogate's expenses", "Banning payment beyond expenses"],
      no=["Paid surrogacy", "A total ban"]),
    S("Surrogacy should be banned.",
      yes=["Banning paid and unpaid surrogacy"],
      no=["Any legal surrogacy"]),
]

if __name__ == "__main__":
    write("D09", T)
    write_clarity("D09", C)
