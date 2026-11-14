# Pending corrections

Items to fix in the next data update. Each line: what, why, source, date flagged.

- **[source records done 14 Nov; data regenerates in the next rebuild] Technology Transfer Block Exemption (row 25)**: our record measures Regulation (EU) 316/2014, which expired on 30 April 2026. The CEPS dataset (Zenner & Marcus, 5th edition, November 2026, Table 1 "Antitrust Block Exemptions") lists Regulation (EU) 2026/877 instead, probably the replacement TTBER. To do: confirm 2026/877 on EUR-Lex, then switch the record (identifier, CELEX, dates, measured text, obligations, secondary acts, page). Flagged 14 Nov 2026.
- **ViDA (row 90)**: identifier corrected to Directive (EU) 2025/516 (it was already measured on the adopted act). Its low count (14 obligations, 0 on firms) is a method effect: it is an amending act and the method skips text inserted by amendments; its rules are counted in the consolidated VAT Directive. Flagged 14 Nov 2026.
- **DAC (row 19)**: only 2 obligations coded as binding firms. Method effect: the directive tells member states to require reporting by intermediaries (DAC6) and platforms (DAC7), so the grammatical subject is the member state. Same for other directives that oblige firms through national law; the 'ultimate addressee' field only partly corrects this. Consider a re-coding rule for "Member States shall require [firms] to". Flagged 14 Nov 2026.

- **[flagged 14 Nov 2026] Anti-Money Laundering Regulation (row 68): timing gap.** Regulation (EU) 2024/1624 applies only from
  10 July 2027. Until then companies' AML duties come from Directive (EU) 2015/849 as amended by Directive (EU) 2018/843, through
  national law; that directive is not in the database. Our 295 company obligations for AML therefore describe the rules from 2027.
  To do with the next rebuild: say so on the AMLR law page (and in the company-type and finance text where AML counts are cited);
  decide whether to add Directive 2015/849 as the act in force until July 2027. The Transfer of Funds Regulation (row 127) has
  applied since 30 December 2024 and is current.
