import sys; sys.path.insert(0, ".")
from impact_record import write
from psd3_common import indicators, literature, IA
write("52023PC0367", "Payment Services Regulation (PSR)", "52023PC0367", IA,
      "ex-ante only: joint impact assessment with PSD3; fraud baseline statistics; not yet applied",
      "The Payment Services Regulation (shared impact assessment with PSD3) is meant to cut payment scams through payee name checks, fraud data sharing and refunds in some impersonation cases, and to improve open banking; the Commission put the targeted scam losses at about EUR 323 million a year (2020). A political agreement was reached in November 2025 but the rules do not yet apply; reported payment fraud in Europe has since risen to EUR 4.2 billion in 2024.",
      indicators(), literature())
