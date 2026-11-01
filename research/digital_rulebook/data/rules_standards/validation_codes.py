# Hand codes for the fresh validation sample (data/rules_standards/validation_sample.json), coded before seeing the reader codes.
CODES = (
 "R S N R R R R R R R S R R S R R R R S R R R S R R M R S S R S S N R R S S S R M S S S R R R R L R S"   # 0-49
 " S R N R S R R S S M R R S S R R R S M R S R S R R R S S S R R R S R R R S R R R R R R R S R R R R R" # 50-99
 " S R S R R R R R S R S M R R S R R R R R R R R S R N R S R S S N R R R R R R R R R R R N R R R S R R" # 100-149
 " R R S R R R R R N S R R R R R R S R M R R S R R R R R R R R R R R N R S R R S R R S R R R R S R R R" # 150-199
).split()
assert len(CODES) == 200
