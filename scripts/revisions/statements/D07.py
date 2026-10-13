"""Technology and AI."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, write, write_clarity  # noqa: E402

C, T = {}, {}

T["ai_regulation_level"] = [
    S("Pause the most advanced AI until safety rules are in place.",
      yes=["A halt on training the most powerful AI systems", "Safety rules before work resumes"],
      no=["Letting the industry set its own pace"]),
    S("Strict AI rules: testing and approval before major new systems are released.",
      yes=["Government testing and approval of major AI releases"],
      no=["A pause", "Few or no new rules"]),
    S("Targeted AI rules for specific harms, like fraud and discrimination, through existing agencies.",
      yes=["Using agencies like the FTC to police AI fraud and bias"],
      no=["Pre-approval of AI systems", "No new rules"]),
    S("Few or no new AI rules; fix problems as they arise.",
      yes=["Letting AI companies develop freely"],
      no=["New AI regulations or approvals"]),
]

T["ai_state_laws"] = [
    S("States should be free to set stricter AI rules than federal law.",
      yes=["State AI laws stricter than any federal law"],
      no=["A federal law overriding state AI rules"]),
    S("States should regulate AI until there's a federal law.",
      yes=["State AI laws for now", "A federal standard replacing them later"],
      no=["Banning state AI laws now", "States going beyond a future federal law"]),
    S("One national AI standard should override state AI laws.",
      yes=["Federal preemption of state AI laws"],
      no=["Separate AI laws in each state"]),
]

T["ai_china_race"] = [
    S("AI safety rules come first, whatever China does.",
      yes=["Safety rules even if they slow US companies"],
      no=["Dropping safety rules to keep ahead of China"]),
    S("Avoid AI rules that would put US companies far behind China.",
      yes=["Safety rules that don't badly slow US firms"],
      no=["Rules that hand China a big lead", "Dropping most safety rules"]),
    S("Staying ahead of China matters more than most AI safety concerns.",
      yes=["Loosening safety rules that slow US AI companies"],
      no=["Rules that could let China pull ahead"]),
]

T["ai_licensing"] = [
    S("The most powerful AI systems should need government approval after safety testing.",
      yes=["A government license for frontier AI releases"],
      no=["Releasing them without approval"]),
    S("The most powerful AI systems should be licensed by an independent safety body.",
      yes=["Licensing by an independent body, not a government agency"],
      no=["Government licensing", "No approval"]),
    S("No approval, but companies must test for dangers and report to the government.",
      yes=["Required safety testing and reporting"],
      no=["Licensing before release", "No reporting"]),
    S("No AI requirements beyond existing laws.",
      yes=["Leaving frontier AI to existing law"],
      no=["Testing, reporting or licensing requirements"]),
]

T["ai_open_release"] = [
    S("The most powerful AI models shouldn't be published for anyone to download.",
      yes=["Barring open release of the most capable models"],
      no=["Publishing top models freely"]),
    S("The most powerful models can be published after safety testing.",
      yes=["Open release once a model passes safety tests"],
      no=["A ban", "Publishing without testing"]),
    S("Companies should be free to publish their most powerful models.",
      yes=["Open release without restrictions"],
      no=["Limits on publishing AI models"]),
]

T["ai_job_loss"] = [
    S("Government should slow the use of AI to replace workers.",
      yes=["Limits on replacing people with AI"],
      no=["Letting companies automate freely"]),
    S("Government should mainly expand income support for people who lose work to AI.",
      yes=["Cash payments to displaced workers"],
      no=["Leaving displaced workers to the market"]),
    S("Government should mainly fund retraining and help workers find new jobs.",
      yes=["Retraining programs and job placement help"],
      no=["Slowing AI use", "Cash support as the main answer"]),
    S("Government should do little; new jobs will appear.",
      yes=["Leaving the job market to adjust"],
      no=["New programs or limits on AI"]),
]

T["ai_layoff_limits"] = [
    S("Require notice and severance, and ban replacing people with AI in some jobs, like teaching and nursing.",
      yes=["Advance notice and severance for AI layoffs", "Bans on AI replacing teachers and nurses"],
      no=["Letting employers automate any job"]),
    S("Require advance notice and severance for AI layoffs, but no bans.",
      yes=["Notice and severance pay when replacing workers with AI"],
      no=["Job-specific bans", "No requirements"]),
    S("No limits on employers replacing workers with AI.",
      yes=["Leaving technology choices to employers"],
      no=["Notice, severance or bans"]),
]

T["moderation_false"] = [
    S("Social media companies should remove much more legal-but-false content.",
      yes=["Removing more false posts about health, elections and news"],
      no=["Leaving most false posts up"]),
    S("Social media companies should remove about as much false content as now.",
      yes=["Today's moderation of false posts"],
      no=["Removing more or less"]),
    S("Social media companies should remove less false content.",
      yes=["Leaving most false posts up", "Labels or replies instead of removal"],
      no=["Removing more false posts"]),
    S("Social media companies should remove only illegal content.",
      yes=["Leaving every legal post up, false or not"],
      no=["Removing legal posts for being false"]),
]

T["moderation_offensive"] = [
    S("Social media companies should remove much more legal-but-offensive content.",
      yes=["Removing more insults aimed at races, religions and other groups"],
      no=["Leaving most offensive posts up"]),
    S("Social media companies should remove about as much offensive content as now.",
      yes=["Today's moderation of offensive posts"],
      no=["Removing more or less"]),
    S("Social media companies should remove less offensive content.",
      yes=["Leaving most offensive posts up"],
      no=["Removing more offensive posts"]),
    S("Social media companies should remove only illegal content.",
      yes=["Leaving every legal post up, however offensive"],
      no=["Removing legal posts for being offensive"]),
]

T["moderation_law"] = [
    S("Social media companies should decide what they host.",
      yes=["Leaving removals and bans to the companies"],
      no=["Laws limiting what platforms can remove"]),
    S("Require large platforms to explain removals and let users appeal.",
      yes=["Required explanations and appeals for removals and bans"],
      no=["Banning removals of political posts", "No requirements"]),
    S("Ban the largest platforms from removing legal political posts.",
      yes=["Laws like Texas's and Florida's barring political viewpoint removals"],
      no=["Letting platforms remove legal political posts"]),
]

T["platform_liability"] = [
    S("Platforms should be liable for harmful content their systems recommend or promote.",
      yes=["Lawsuits over posts that algorithms push to users"],
      no=["Today's broad Section 230 shield"]),
    S("Platforms should be liable only if told about clearly illegal content and they don't remove it.",
      yes=["Notice-and-takedown liability"],
      no=["Liability for recommendations", "Today's full shield"]),
    S("Keep today's protection: users, not platforms, are responsible for posts.",
      yes=["Keeping Section 230 as it is"],
      no=["Making platforms liable for user posts"]),
]

T["social_media_min_age"] = [
    S("No legal minimum age for social media; parents decide.",
      yes=["Leaving social media age to parents"],
      no=["Age limits set by law"]),
    S("A legal minimum age of 13 for social media.",
      yes=["Making 13 the legal minimum"],
      no=["Raising it to 16 or 18"]),
    S("A legal minimum age of 16 for social media.",
      yes=["Barring under-16s from Instagram, TikTok and Snapchat accounts, as Australia does"],
      no=["Letting 13- to 15-year-olds have accounts"]),
    S("A legal minimum age of 18 for social media.",
      yes=["Barring all minors from social media accounts"],
      no=["Accounts for anyone under 18"]),
]

T["age_verification"] = [
    S("Adult websites shouldn't have to check ages; parents should use controls at home.",
      yes=["Parental controls instead of age checks"],
      no=["Required age checks for adult sites"]),
    S("Adult websites should check ages by methods that don't need ID.",
      yes=["Age estimates from face scans or similar methods"],
      no=["Requiring ID uploads", "No checks"]),
    S("Adult websites should check ages with a government ID or similar.",
      yes=["ID-based age checks for porn and gambling sites"],
      no=["Letting adult sites skip age checks"]),
]

T["algorithm_bias_testing"] = [
    S("AI used to screen job or loan applicants should face independent bias audits with public results.",
      yes=["Independent audits for bias against women and minorities", "Publishing the results"],
      no=["Relying on existing law alone"]),
    S("Companies should test their screening AI for bias and keep records.",
      yes=["Required internal bias testing and records"],
      no=["Public audits", "No testing requirement"]),
    S("Existing anti-discrimination laws are enough for screening AI.",
      yes=["No new testing rules"],
      no=["Required bias testing or audits"]),
]

T["data_centers"] = [
    S("Limit new AI data centers until there's enough clean power.",
      yes=["Pausing new data centers until clean power catches up"],
      no=["Fast-tracking data centers and power plants"]),
    S("Allow data centers, but make them pay the full cost of new power plants and lines.",
      yes=["Data centers paying for the power they need, not other customers"],
      no=["Limits on new data centers", "Spreading their power costs to households"]),
    S("Speed up approval of data centers and power plants to keep the US ahead in AI.",
      yes=["Faster permits for data centers and the plants that power them"],
      no=["Limits or extra charges on data centers"]),
]

T["election_deepfakes"] = [
    S("It should be illegal for anyone to share unlabeled AI fakes of candidates in the months before an election.",
      yes=["Penalties for individuals and campaigns who share unlabeled deepfakes"],
      no=["Relying only on fraud and defamation laws"]),
    S("Only campaigns and paid advertisers must label AI fakes; no penalties for individuals.",
      yes=["Labeling rules for campaigns and ads"],
      no=["Penalizing ordinary people who share fakes", "No new rules"]),
    S("Existing fraud and defamation laws are enough for AI fakes.",
      yes=["No new deepfake laws"],
      no=["Labeling rules or penalties for deepfakes"]),
]

T["automation_tax"] = [
    S("Companies should pay a special tax when robots or AI replace workers, used to support those workers.",
      yes=["A tax on replacing workers with machines", "Using it to support displaced workers"],
      no=["Leaving automation untaxed"]),
    S("No special automation tax, but end tax breaks that favor machines over workers.",
      yes=["Ending write-offs that make machines cheaper than people"],
      no=["A robot tax", "Keeping those tax breaks"]),
    S("No automation tax; it would slow productivity growth.",
      yes=["Leaving automation decisions untaxed"],
      no=["Any tax on replacing workers with machines"]),
]

T["crypto_rules"] = [
    S("Ban most cryptocurrencies.",
      yes=["Banning most crypto sales and trading"],
      no=["Letting crypto trade under light rules"]),
    S("Regulate crypto like stocks and banks.",
      yes=["Securities- and banking-style rules for crypto companies"],
      no=["A ban", "Light or no rules"]),
    S("Light crypto rules focused on fraud.",
      yes=["Anti-fraud rules only"],
      no=["Bank- or stock-style regulation", "A ban"]),
    S("No special rules for crypto.",
      yes=["Treating crypto companies like any other business"],
      no=["Crypto-specific regulation"]),
]

T["digital_dollar"] = [
    S("The Federal Reserve should create a digital dollar people can hold directly.",
      yes=["A Fed-issued digital currency for the public"],
      no=["Banning a digital dollar"]),
    S("A digital dollar only with strict privacy protections.",
      yes=["A digital dollar with legal limits on government tracking"],
      no=["One without privacy rules", "A ban"]),
    S("Ban a Federal Reserve digital dollar.",
      yes=["Prohibiting a government digital currency"],
      no=["Any Fed digital dollar"]),
]

T["ai_copyright"] = [
    S("AI companies should need permission and pay to train on copyrighted work.",
      yes=["Licensing deals with authors, artists and publishers before training"],
      no=["Training on published work without consent"]),
    S("AI companies should pay for copyrighted work they train on, but don't need permission.",
      yes=["A required fee or royalty system for training"],
      no=["Letting creators refuse", "Free use"]),
    S("Training AI on published work should be allowed freely.",
      yes=["Treating training as fair use"],
      no=["Fees or permission for training"]),
]

T["ai_companions_minors"] = [
    S("AI friend or romantic-partner chatbots should be banned for minors.",
      yes=["Barring under-18s from companion chatbot apps"],
      no=["Letting minors use them with parental consent"]),
    S("Allow companion chatbots for minors with parental consent and safety limits.",
      yes=["Parental consent and built-in safety limits"],
      no=["A ban", "No consent or limits"]),
    S("Allow companion chatbots for minors; parents can decide at home.",
      yes=["No legal limits on minors' use"],
      no=["Bans or required consent"]),
]

if __name__ == "__main__":
    write("D07", T)
    write_clarity("D07", C)
