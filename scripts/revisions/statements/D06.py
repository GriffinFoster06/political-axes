"""Trade."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from statement_kit import S, existing, write, write_clarity  # noqa: E402

C, T = {}, {}

C["tariff_level"] = {
    "why": "'Low', 'moderate' and 'high' tariffs had no numbers.",
    "scope": "Think about trade policy in general, not one country. Roughly: low means 5% or less on most goods, moderate means about 10% to 25% on many goods, high means 25% or more on most imports.",
}
T["tariff_level"] = [
    S("Few or no tariffs; free trade benefits most people.",
      yes=["Removing most tariffs on imports"],
      no=["Tariffs to protect US industries"]),
    S("Low tariffs, used mainly against countries that break trade rules.",
      yes=["Tariffs of about 5% or less on most goods", "Targeted tariffs on rule-breakers, like countries dumping cheap steel"],
      no=["Broad tariffs to protect industries"]),
    S("Moderate tariffs on many goods to protect key US industries.",
      yes=["Tariffs of about 10–25% on goods like steel, cars and electronics"],
      no=["Free trade", "High tariffs on most imports"]),
    S("High tariffs on most imports to bring manufacturing back, even if prices rise.",
      yes=["Tariffs of 25% or more on most imports", "Accepting higher prices for US-made goods"],
      no=["Lowering tariffs to keep prices down"]),
]

T["tariff_price_tradeoff"] = [
    S("Lower prices matter more than protecting factory jobs with tariffs.",
      yes=["Keeping tariffs low so cars and appliances stay cheaper"],
      no=["Tariffs that raise those prices by 10%"]),
    S("Tariffs to protect factory jobs are worth it only if prices rise about 2% to 3%.",
      yes=["Small tariffs with a small price effect"],
      no=["Tariffs that raise prices by 10%"]),
    S("Protecting factory jobs is worth prices about 10% higher on goods like cars and appliances.",
      yes=["Tariffs that add about 10% to cars and appliances to keep factory jobs here"],
      no=["Dropping tariffs to lower prices"]),
]

T["tariff_authority"] = [
    S("Only Congress should set tariffs, by passing laws.",
      yes=["Requiring a vote of Congress for any tariff"],
      no=["Presidents setting tariffs on their own"]),
    S("Congress sets tariffs, but the president can add them in a true emergency.",
      yes=["Emergency tariffs by a president, with Congress setting the rest"],
      no=["Presidents setting tariffs whenever they choose", "No emergency power"]),
    S("The president should set tariffs whenever the president judges it's in the national interest.",
      yes=["Broad presidential power over tariffs, for any president"],
      no=["Requiring Congress to approve tariffs"]),
]
T["tariff_authority_cases"] = existing("D06", "tariff_authority_cases")

T["trade_agreements"] = [
    S("The US should sign tariff-cutting deals with as many countries as possible.",
      yes=["New free trade agreements with many countries"],
      no=["Withdrawing from existing deals"]),
    S("Sign more trade deals, but only with strong labor and environmental rules.",
      yes=["Trade deals with enforceable labor and environmental standards"],
      no=["Deals without those rules", "Pulling out of deals"]),
    S("Sign trade deals only with close allies.",
      yes=["Deals with countries like Canada, Japan and European nations"],
      no=["Deals with non-allies"]),
    S("No more trade deals; pull out of existing ones where possible.",
      yes=["Withdrawing from trade agreements like the one with Canada and Mexico"],
      no=["New tariff-cutting deals"]),
]

T["trade_jobs_tradeoff"] = [
    S("Make trade deals that help the country overall, even if some regions lose jobs.",
      yes=["Trade deals with overall gains despite local job losses"],
      no=["Blocking deals to protect existing jobs"]),
    S("Make those trade deals only with major help for workers who lose jobs.",
      yes=["Large retraining, wage insurance and relocation aid for affected workers"],
      no=["Deals with no help for workers", "Blocking deals outright"]),
    S("Protecting existing US jobs comes first.",
      yes=["Turning down deals that would cost US industries jobs"],
      no=["Trade deals that shift jobs abroad, even with overall gains"]),
]

T["china_trade"] = [
    S("Trade freely with China, as with other countries.",
      yes=["Normal trade in goods and technology with China"],
      no=["Special limits on China trade"]),
    S("Limit trade with China only in sensitive technology.",
      yes=["Restrictions on advanced chips and military goods"],
      no=["Moving other production out of China", "Cutting off trade"]),
    S("Limit sensitive technology and move production of essentials out of China.",
      yes=["Chip limits", "Moving medicine and electronics production out of China"],
      no=["Free trade with China", "Cutting off most trade"]),
    S("Cut off most trade with China.",
      yes=["Ending most imports from and exports to China"],
      no=["Ordinary trade with China"]),
]

T["china_ownership"] = [
    S("Chinese companies should be able to own US businesses, farmland and apps like any foreign company.",
      yes=["Treating Chinese buyers like other foreign investors"],
      no=["Special bans on Chinese ownership"]),
    S("Chinese companies can own US businesses, except in defense and personal data.",
      yes=["Blocking Chinese ownership in defense and data-heavy businesses"],
      no=["Broader bans", "No limits"]),
    S("No Chinese ownership of farmland, key technology or popular apps; other businesses are fine.",
      yes=["Banning Chinese purchases of farmland", "Forcing sale of apps like TikTok"],
      no=["A total ban", "No limits"]),
    S("Ban Chinese ownership of US businesses entirely.",
      yes=["Barring any China-based company from owning US businesses"],
      no=["Any Chinese ownership in the US"]),
]

T["industrial_policy"] = [
    S("Government should pay companies to build factories in many industries.",
      yes=["Subsidies and tax credits for chips, batteries and many other industries"],
      no=["Leaving investment to the market"]),
    S("Pay companies to build factories only in industries vital to national security.",
      yes=["Subsidies for chips and defense-related production"],
      no=["Subsidies for many industries", "No subsidies"]),
    S("The market should decide where investment goes.",
      yes=["Ending industry-specific subsidies like the chip program"],
      no=["Government payments to build factories"]),
]

T["buy_american"] = [
    S("Federal agencies should buy the best value, wherever it's made.",
      yes=["Ending Buy American rules for most purchases"],
      no=["Paying more for US-made goods"]),
    S("Buy American only for military and security needs.",
      yes=["US-made requirements for defense purchases"],
      no=["Requiring it for everyday purchases"]),
    S("Buy American if it costs no more than about 25% extra.",
      yes=["Paying up to a 25% premium for US-made vehicles, steel and equipment"],
      no=["Paying any price", "Ignoring where goods are made"]),
    S("Always buy American, even at much higher cost.",
      yes=["US-made requirements regardless of price"],
      no=["Buying foreign goods to save money"]),
]

T["offshoring_penalty"] = [
    S("Companies that move US jobs abroad should face penalties.",
      yes=["Higher taxes and losing government contracts for offshoring"],
      no=["Letting companies move jobs freely"]),
    S("No penalty, but end tax breaks that make moving jobs abroad cheaper.",
      yes=["Closing tax breaks for overseas operations"],
      no=["Penalties for moving jobs abroad", "Keeping those tax breaks"]),
    S("Companies should decide where to operate.",
      yes=["No penalties or special taxes for offshoring"],
      no=["Penalizing companies that move jobs abroad"]),
]

T["export_controls"] = [
    S("Companies should be free to sell advanced technology to anyone.",
      yes=["Ending chip export limits on China and Russia"],
      no=["Export controls"]),
    S("Block sales of technology with clear military uses only.",
      yes=["Blocking military-use technology"],
      no=["Blocking most advanced chips", "No limits at all"]),
    S("Block sales of most advanced technology to rivals, even if US companies lose sales.",
      yes=["Broad limits on selling top chips and tech to China and Russia"],
      no=["Letting companies sell advanced chips to rivals"]),
]

T["friend_shoring"] = [
    S("Allies should get clearly lower tariffs than other countries.",
      yes=["Much lower tariffs for Canada, Japan and European countries"],
      no=["Treating allies like everyone else"]),
    S("Allies should get somewhat lower tariffs.",
      yes=["Modest tariff preferences for allies"],
      no=["Large preferences", "No preference"]),
    S("Treat all trading partners the same.",
      yes=["The same tariffs for allies and others"],
      no=["Tariff breaks for allies"]),
    S("Allies should face tariffs too if they sell more to us than they buy.",
      yes=["Tariffs on allies with trade surpluses with the US"],
      no=["Tariff breaks for allies"]),
]

if __name__ == "__main__":
    write("D06", T)
    write_clarity("D06", C)
