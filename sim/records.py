"""Record-in-office answer sets for past presidents (fix 7 of the simulation report).

The roster answers give each politician's views today. For three past presidents
those differ from what they did in office, and the president comparison groups
are meant to describe the presidency. Each record set starts from the person's
views-today answers and changes only the questions where their record in office
clearly points elsewhere. Questions their presidency never touched (most
transgender policy, AI, crypto) keep their views-today answer.

Values are answer codes (0 = first option). Case ids work the same way.
"""

RECORDS = {
    "bclinton_rec": {
        "base": "bclinton", "years": "1993–2001",
        "set": {
            # DOMA, Don't Ask Don't Tell, ENDA for sexual orientation only
            "same_sex_marriage": 1, "same_sex_adoption": 1, "lgbt_nondiscrimination": 1,
            # welfare reform; "the era of big government is over"
            "work_req_rule": 3, "cash_aid_level": 3, "federal_size": 3,
            # 1994 crime bill: more mandatory minimums, federal death penalty, 100,000 police
            "mandatory_minimums": 3, "death_penalty": 2, "violent_sentences": 4, "police_spending": 5, "cash_bail": 2,
            "marijuana_law": 4, "drug_possession": 3,
            # Brady Act, assault weapons and magazine ban, gun-show checks, HUD suits against gun makers
            "semi_auto_rifles": 1, "magazine_limit": 0, "private_sale_checks": 1, "handgun_purchase": 2,
            "concealed_carry": 1, "gun_maker_liability": 0, "second_amendment_meaning": 1,
            "cl_k12": 0, "cl_gov": 0, "cl_worship": 0,
            # NAFTA, WTO, permanent normal trade with China, "strategic partnership"
            "trade_agreements": 0, "tariff_level": 0, "china_trade": 0, "china_posture": 0, "export_controls": 0,
            # 1996 immigration law, Operation Gatekeeper
            "status_policy": 3, "border_security": 2, "everify": 2,
            # bank deregulation, balanced budgets without an amendment
            "bank_rules": 3, "deficit_approach": 2, "balanced_budget_amendment": 0,
            # post-Cold War defense cuts; Bosnia and Kosovo; NATO expansion
            "defense_spending": 1, "nato": 0, "ally_attacked": 0,
            # executive orders late in the term; Marc Rich and Roger Clinton pardons
            "exec_orders_scope": 2, "pardon_allies": 2,
            # Kyoto signed but never sent to the Senate; BTU tax dropped
            "climate_action": 1,
            # language-access order (EO 13166)
            "english_official": 0,
        },
    },
    "obama_rec": {
        "base": "obama", "years": "2009–2017",
        "set": {
            # the ACA: mostly private insurance with subsidies and Medicaid expansion; the mandate
            "health_coverage": 2, "insurance_mandate": 0,
            # did not back legalization in office; let states proceed
            "marijuana_law": 3,
            # sentencing reform and clemency, short of ending mandatory minimums
            "mandatory_minimums": 1,
            # TPP; tire tariffs
            "trade_agreements": 1, "tariff_level": 1,
            # NSA programs until 2015, Apple v. FBI, drone campaign, Libya
            "surveillance_tradeoff": 2, "warrant_tradeoff": 2, "encryption_access": 2, "border_device_search": 2,
            "gov_buys_data": 1, "strikes_on_terrorists": 2,
            # "pen and phone"; DACA and DAPA
            "exec_orders_scope": 3,
            # kept the filibuster in office
            "filibuster": 1,
            # opposed same-sex marriage until May 2012, then endorsed it
            "same_sex_marriage": 0,
            # record deportations alongside DACA; refugee cap 70,000-110,000
            "status_policy": 1, "border_security": 2, "refugee_cap": 1,
        },
    },
    "gwbush_rec": {
        "base": "gwbush", "years": "2001–2009",
        "set": {
            # Federal Marriage Amendment; abstinence-only funding; stem-cell limits
            "same_sex_marriage": 2, "same_sex_adoption": 2, "sex_education": 2, "ivf_embryos": 2,
            "evolution_class": 2, "school_prayer": 2,
            # faith-based initiative; Healthy Marriage Initiative
            "faith_charities": 2, "promote_marriage": 2,
            # Patriot Act, warrantless wiretapping, signing statements, enemy-combatant claims,
            # US attorney firings; he complied with court rulings and accepted results
            "surveillance_tradeoff": 3, "warrant_tradeoff": 3, "exec_orders_scope": 2, "emergency_duration": 2,
            "rule_bending_leader": 2, "checks_vs_action": 2, "presidential_immunity": 1, "refuse_to_spend": 1,
            "civil_service": 1, "prosecute_opponents": 1, "independent_agencies": 1,
            # Medicare Part D and No Child Left Behind grew federal programs and standards
            "education_department": 0, "sd_marriage": 0,
            # 2002 steel tariffs alongside new trade deals
            "tariff_level": 1,
            # comprehensive immigration reform with a path to legal status
            "status_policy": 1,
            # Iraq, the surge, a bigger military
            "defense_spending": 4, "troops_abroad": 3, "iran_nuclear": 2,
        },
    },
}
