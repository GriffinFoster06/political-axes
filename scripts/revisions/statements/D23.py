"""Education."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, write, write_clarity  # noqa: E402

C, T = {}, {}

T["school_choice"] = [
    S("Public education money should go only to public schools.",
      yes=["Keeping tax money in district public schools"], no=["Vouchers or education savings accounts for private schools"]),
    S("Public money can follow students to public charter schools, but not private schools.",
      yes=["Funding charter schools"], no=["Vouchers for private schools"]),
    S("Public money should follow low-income students to any school, including private schools.",
      yes=["Vouchers for low-income families"], no=["Vouchers for every family", "No private school vouchers"]),
    S("Public money should follow every student to any school their family chooses.",
      yes=["Universal vouchers or education savings accounts, as in Arizona and Florida"], no=["Limiting public money to public schools"]),
]

T["charter_schools"] = [
    S("There should be fewer charter schools; limit or close them.", yes=["Caps on new charters", "Closing some charter schools"], no=["New charter schools"]),
    S("There should be about as many charter schools as today.", yes=["Today's number of charters"], no=["Expanding or closing charters"]),
    S("There should be more charter schools.", yes=["Opening more charter schools"], no=["Caps on charters"]),
    S("There should be many more charter schools; any qualified group should be able to open one.", yes=["Lifting caps on charters entirely"], no=["Limits on new charters"]),
]

T["curriculum_control"] = [
    S("Teachers and education experts should have the most say over what public schools teach.", yes=["Curriculum set by educators"], no=["Parents or boards overriding teachers on content"]),
    S("State education boards should have the most say over what public schools teach.", yes=["Statewide curriculum standards"], no=["District-by-district or parent control"]),
    S("Local elected school boards should have the most say over what public schools teach.", yes=["Local boards choosing curriculum"], no=["State mandates on content"]),
    S("Parents should have the most say, with the right to review all teaching materials.", yes=["Parents' bill of rights laws", "Posting all lesson materials for parents"], no=["Educators deciding content alone"]),
]

T["lesson_opt_out"] = [
    S("Parents shouldn't be able to pull children out of lessons.", yes=["The same curriculum for all students"], no=["Opt-outs, even from sex education"]),
    S("Parents should be able to pull children out of sex education only.", yes=["Sex ed opt-outs"], no=["Opt-outs from other lessons"]),
    S("Parents should be able to pull children out of any lesson that conflicts with their values.", yes=["Opt-outs from any lesson parents object to on values or religious grounds"], no=["Required participation in objectionable lessons"]),
]

T["teach_gender_identity"] = [
    S("Public schools should teach about gender identity starting in elementary school.", yes=["Lessons on gender identity from early grades"], no=["Bans on the topic"]),
    S("Public schools should teach about gender identity only in middle and high school.", yes=["Lessons from middle school on"], no=["Elementary lessons", "Banning the topic"]),
    S("Teach about gender identity only in high school, and only if parents opt in.", yes=["Opt-in high school lessons"], no=["Lessons in younger grades", "Opt-out instead of opt-in"]),
    S("Public schools shouldn't teach about gender identity at any grade.", yes=["Laws barring the topic in public schools"], no=["Lessons on gender identity"]),
]

T["sex_education"] = [
    S("High school sex ed should fully cover contraception, consent and sexual orientation.", yes=["Comprehensive sex education"], no=["Abstinence-only classes"]),
    S("Sex ed should cover contraception and consent while encouraging teens to wait.", yes=["Contraception and consent lessons, stressing waiting"], no=["Abstinence-only classes", "Covering sexual orientation"]),
    S("High school sex ed should teach abstinence only.", yes=["Abstinence-only education"], no=["Teaching contraception"]),
    S("High schools shouldn't teach sex ed; parents should.", yes=["Ending school sex education"], no=["Any sex ed in schools"]),
]

T["student_loan_cancel"] = [
    S("Cancel all existing federal student loan debt.", yes=["Wiping out all federal student loans"], no=["Requiring borrowers to repay"]),
    S("Cancel about $10,000 to $20,000 per borrower.", yes=["Partial cancellation for each borrower"], no=["Full cancellation", "No broad cancellation"]),
    S("Cancel student debt only for people misled by their schools, or after years of public service.", yes=["Fraud relief and Public Service Loan Forgiveness"], no=["Broad cancellation"]),
    S("Don't cancel federal student loan debt.", yes=["Requiring full repayment"], no=["Any cancellation programs"]),
]

T["loan_repayment"] = [
    S("Cap student loan payments at 5% of income or less, forgiving the rest after 10 years.", yes=["Low income-based caps and fast forgiveness"], no=["Standard repayment"]),
    S("Cap payments at about 10% of income, forgiving the rest after 20 to 25 years.", yes=["Income-driven repayment like today's plans"], no=["5% caps", "No caps"]),
    S("Borrowers should repay what they borrowed on standard terms, without income caps.", yes=["Ending income-driven repayment and forgiveness"], no=["Income-based caps"]),
]

T["free_college"] = [
    S("Public college tuition should be free for everyone, paid by taxes.", yes=["Tuition-free public colleges for all"], no=["Charging tuition at public colleges"]),
    S("Public college should be tuition-free for families earning under about $125,000.", yes=["Free tuition below $125,000 income"], no=["Free college for wealthier families", "No free college"]),
    S("Only community college should be tuition-free.", yes=["Free community college"], no=["Free four-year public college"]),
    S("Public college shouldn't be tuition-free.", yes=["Students paying tuition"], no=["Tax-funded free tuition"]),
]

T["education_department"] = [
    S("Expand the Department of Education, with more federal school funding.", yes=["More federal money and staff for schools"], no=["Cutting or closing the department"]),
    S("Keep the Department of Education about as it is.", yes=["Today's department"], no=["Expanding or closing it"]),
    S("Shrink the Department of Education, sending money and control to states.", yes=["Block grants to states", "Fewer federal staff"], no=["Expanding federal school funding"]),
    S("Close the Department of Education.", yes=["Abolishing the department"], no=["A federal education department"]),
]

T["school_discipline"] = [
    S("Handle repeatedly disruptive or violent students with counseling and repairing harm; suspend only as a last resort.", yes=["Restorative justice and counseling"], no=["Routine suspensions and expulsions"]),
    S("Use a mix of counseling and suspension.", yes=["Counseling first, suspension when needed"], no=["Suspension as the default", "Never suspending"]),
    S("Suspend or expel repeatedly disruptive or violent students to protect others.", yes=["Suspensions and expulsions"], no=["Keeping violent students in class"]),
]

T["selective_admissions"] = [
    S("Selective public high schools should admit by lottery among qualified applicants.", yes=["Lotteries for specialized schools"], no=["Admissions by test score"]),
    S("Use grades and tests, plus seats for the top students from every middle school.", yes=["Test-based admission with seats for each middle school"], no=["Tests alone", "A lottery"]),
    S("Admit students by test and grades only.", yes=["Merit-only admissions"], no=["Lotteries or set-asides"]),
]

T["legacy_admissions"] = [
    S("Colleges that get federal money should be banned from favoring children of graduates or donors.", yes=["Legacy admissions bans"], no=["Legacy and donor preferences"]),
    S("Colleges can favor children of graduates or donors, but must say so publicly.", yes=["Disclosure of legacy preferences"], no=["A ban", "Secret preferences"]),
    S("Colleges should decide for themselves whether to favor children of graduates or donors.", yes=["Leaving legacy policies to colleges"], no=["Government bans or rules"]),
]

if __name__ == "__main__":
    write("D23", T)
    write_clarity("D23", C)
