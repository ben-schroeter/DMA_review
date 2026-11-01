"""Shared content for PSD3 (52023PC0366) and PSR (52023PC0367): one joint impact assessment SWD(2023) 231."""
import sys; sys.path.insert(0, ".")
from impact_record import ind, lit
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
IA = "SWD(2023) 231 (executive summary SWD(2023) 232) - joint impact assessment for PSD3 and PSR"

def indicators():
    return [
 ind("note", "Neither PSD3 nor PSR has LFS indicators; the memorandum provides only for a review five years after application (PSR: focus on open banking, fees, fraud liability). PSD3 and PSR share one impact assessment"),
 ind("expected impact (impact assessment)", "Fraud protection", "Reduce authorised push payment (social engineering) fraud via IBAN/name check, fraud data sharing, conditional refund liability", "Baseline: APP fraud on SEPA credit transfers est. EUR 323m (2020)",
     "Baseline worsening, pre-application: EBA-ECB report EEA payment fraud EUR 3.4bn (2022), 3.5bn (2023), 4.2bn (2024); credit transfer fraud EUR 2.2bn in 2024 (+16%), ~85% of losses borne by users. Rules not yet applied (provisional agreement Nov 2025).", "not measured", "SWD(2023) 231; EBA-ECB 2025"),
 ind("expected impact (impact assessment)", "Open banking", "Better data access interfaces, permission dashboards", "One-off cost ~EUR 185-190m (net) for interfaces; up to EUR 47m for dashboards",
     "Forecast only.", "not measured", "SWD(2023) 231"),
 ind("expected impact (impact assessment)", "Competition / level playing field", "Non-bank PSP access to payment systems and bank accounts; downward pressure on prices", "",
     "Not measured; Settlement Finality Directive access change partly delivered via the Instant Payments Regulation (2024).", "not measured", "SWD(2023) 231"),
    ]

def literature():
    return [
 lit("ec-2023-psd3-psr-ia", "European Commission", 2023, "Impact Assessment accompanying the proposals for a Payment Services Regulation and a Payment Services Directive (PSD3)", IA, EU + "52023SC0231",
     "Commission impact assessment", "ex-ante", "fraud; open banking; competition; compliance costs", "positive (forecast)",
     "Main benefit: reduction of social engineering fraud (APP fraud on SEPA credit transfers estimated at EUR 323m a year in 2020); more open banking innovation, more bank/non-bank competition. Costs: IBAN/name check for 1,200-1,300 PSPs (~EUR 50m one-off), permission dashboards up to EUR 47m, interface upgrades ~EUR 185m one-off offset by savings",
     "The Commission expected the payments package to cut fraud in which customers are tricked into paying scammers (put at about EUR 323 million a year) and to boost open banking, at one-off costs of a few hundred million euros.",
     "EU, forecast", "forecast", "executive summary read; full text searched"),
 lit("ec-2023-psd2-review", "European Commission", 2023, "Report on the review of Directive 2015/2366/EU on payment services (PSD2)", "COM(2023) 365", EU + "52023DC0365",
     "Commission review report", "evaluation (ex-post, of PSD2)", "fraud; open banking; competition", "mixed",
     "PSD2 objectives only partly achieved: strong customer authentication cut fraud on authenticated payments, but social engineering fraud persists and open banking is hampered by inadequate interfaces",
     "The Commission's review of the previous payments directive found that strong authentication cut card fraud but scams and poor bank data interfaces remained problems.",
     "EU, 2018-2022", "Commission self-assessment", "page summary via search"),
 lit("eba-ecb-2025-payment-fraud", "European Banking Authority & European Central Bank", 2025, "2025 Report on payment fraud", "EBA-ECB joint report, 15 December 2025",
     "https://www.eba.europa.eu/publications-and-media/press-releases/joint-eba-ecb-report-payment-fraud-strong-authentication-remains-effective-fraudsters-are-adapting",
     "supervisory statistics", "descriptive (reported fraud data, EEA)", "payment fraud", "n/a (baseline)",
     "EEA payment fraud EUR 3.4bn (2022), 3.5bn (2023), 4.2bn (2024); credit transfer fraud EUR 2.2bn in 2024 (+16%), ~85% borne by users, mainly manipulation scams; SCA still effective against fraud it targets",
     "Payment fraud in Europe rose to EUR 4.2 billion in 2024, with customers bearing most losses from scams - the baseline the new rules aim to improve.",
     "EEA, 2022-2024", "official statistics; pre-application baseline", "page summary via search"),
    ]
