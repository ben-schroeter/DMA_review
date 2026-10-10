import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 1987 proposal predates financial statements with indicators; no monitoring indicators or review clause were set"),
 ind("objective (recitals)", "Coordinated pan-European digital mobile service", "Reserve 890-915/935-960 MHz for a single pan-European digital system (GSM) so terminals and networks work across borders", "",
     "GSM became the dominant world standard; cross-country econometric work finds the analogue-to-digital switch (with more spectrum) had a major effect on EU mobile diffusion, but a single mandated digital standard had no significant extra effect on diffusion compared with competing standards elsewhere.", "mixed evidence", "Gruber & Verboven 2001a, 2001b"),
 ind("expected impact (2009 amendment)", "Spectrum flexibility", "Opening the 900 MHz band to UMTS and later technologies (Directive 2009/114/EC)", "Industry capital savings up to EUR 1.6bn (Commission estimate)",
     "Not evaluated ex post; the figure is a Commission forecast reported in the trade press.", "not measured", "telecoms.com 2009"),
]
literature = [
 lit("gruber-verboven-2001-standards", "Gruber & Verboven", 2001, "The evolution of markets under entry and standards regulation - the case of global mobile telecommunications", "International Journal of Industrial Organization 19(7) (CEPR DP 2440)", "https://doi.org/10.1016/S0167-7187(01)00069-8",
     "peer-reviewed", "econometric diffusion model, panel of countries 1981-1997 (not a clean causal design)", "mobile diffusion; standards; entry", "mixed",
     "Setting a single standard significantly sped up diffusion for analogue mobile, but not for digital; network benefits of one standard appear offset by gains from competition between digital systems; adding competitors had a strong immediate effect",
     "A worldwide study found that imposing one standard helped analogue mobile spread, but the single digital standard (as with GSM in Europe) brought no measurable extra boost.",
     "global, 1981-1997", "established authors; correlational panel", "abstract read", pdf_url="https://repec.cepr.org/repec/cpr/ceprdp/Dp2440.pdf"),
 lit("gruber-verboven-2001-eu-diffusion", "Gruber & Verboven", 2001, "The diffusion of mobile telecommunications services in the European Union", "European Economic Review 45(3)", "https://doi.org/10.1016/S0014-2921(00)00068-4",
     "peer-reviewed", "logistic diffusion model, EU countries", "mobile diffusion", "positive",
     "Transition from analogue to digital in the early 1990s, with the increase in spectrum capacity, had a major impact on diffusion; competition also significant; late-licensing countries catch up",
     "Across the EU, the switch to digital mobile (GSM) and the extra spectrum it brought were the main drivers of mobile phone take-up in the 1990s.",
     "EU, 1980s-1990s", "correlational; cannot separate the Directive from the technology", "abstract read"),
 lit("ec-2007-gsm-repeal-proposal", "European Commission", 2007, "Proposal for a Directive repealing Council Directive 87/372/EEC (GSM Directive)", "COM(2007) 367", EU + "52007PC0367",
     "Commission proposal (impact statement)", "ex-ante (CEPT technical studies; no quantified IA in the text)", "spectrum flexibility; rural coverage", "positive (forecast)",
     "Reserving 900 MHz exclusively for GSM blocks more advanced systems such as UMTS; the band's propagation allows cheaper coverage of rural areas; CEPT found UMTS can coexist with GSM",
     "By 2007 the Commission saw the GSM-only rule as a barrier and proposed opening the band to 3G, citing cheaper rural coverage.",
     "EU, forecast", "forecast; qualitative", "full text read"),
 lit("telecoms-2009-umts900", "Telecoms.com", 2009, "EU move lends helping hand to UMTS900", "trade press", "https://www.telecoms.com/wireless-networking/eu-move-lends-helping-hand-to-umts900",
     "press report of Commission estimate", "secondary report", "capital cost savings", "positive (forecast)",
     "Commission expected industry savings of up to EUR 1.6 billion from reforming the GSM Directive (amended by Directive 2009/114/EC)",
     "The Commission expected opening the GSM band to 3G to save operators up to EUR 1.6 billion in network costs.",
     "EU, forecast", "secondary; forecast", "page summary via search"),
]
write("31987L0372", "Frequency Bands Directive (GSM)", "51987PC0035(02)", "none (pre-dates impact assessments); 2007 repeal proposal COM(2007) 367",
      "thin: two older econometric diffusion studies (mixed on the value of a single mandated standard); no ex-post evaluation",
      "The 1987 GSM Directive reserved the 900 MHz band for one pan-European digital mobile system. Research shows the move to digital mobile drove rapid phone take-up in Europe, but a worldwide study found no extra diffusion boost from mandating a single digital standard. The rule was relaxed in 2009 to allow 3G, with forecast savings of up to EUR 1.6 billion that were never checked.",
      indicators, literature)
