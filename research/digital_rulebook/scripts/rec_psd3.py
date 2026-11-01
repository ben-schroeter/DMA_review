import sys; sys.path.insert(0, ".")
from impact_record import write
from psd3_common import indicators, literature, IA
write("52023PC0366", "Payment Services Directive 3 (PSD3)", "52023PC0366", IA,
      "ex-ante only: joint impact assessment with PSR; fraud baseline statistics; not yet applied",
      "PSD3 (licensing and supervision of payment and e-money institutions) shares its impact assessment with the Payment Services Regulation; the Commission expected them to cut payment scams and strengthen open banking and competition from non-bank firms, at one-off costs of a few hundred million euros. A political agreement was reached in November 2025 but the rules are not yet applied, so there is no evidence of effect; meanwhile payment fraud in Europe rose to EUR 4.2 billion in 2024.",
      indicators(), literature())
