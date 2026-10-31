# Hand codes for the 200-obligation pilot (data/rules_standards/pilot_sample.jsonl), Kaplow (1992) test: can the addressee know,
# before acting, what complies, without a later decision by an authority or court?
# R rule | S standard | M mixed (a bright-line duty with an open-ended element) | L standard to be specified later by a delegated/
# implementing act, technical standard or guidelines named in the provision | D content left to member states (transposition choice,
# not ex post) | N not an obligation (constitutive, competence, footnote, case-law quote, truncated)
CODES = (
 "R L S R S R N R S R S R R R R S R S S R R R R S R R S S R S R R R M L S R S R R R S S R R S R D R S"   # 0-49
 " R R R R S R S R S S R R R R R R S R R R R R R R R D M R R S R R R R R R S R R R R R R R R S S R M S" # 50-99
 " R R R S R S R S R R N N R R R R R S R S M R R S R R R R R R R R R R R R R R N R R R S R D R S R R R" # 100-149
 " R R S N R R R N R N S R R S R R R R N R R R R R S M S R R M R R R R R R R M R R S R R S R R R R R R" # 150-199
).split()
assert len(CODES) == 200
