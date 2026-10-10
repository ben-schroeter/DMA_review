# Website outline (revision 2)

Changes from revision 1:
- The home page is now a long, scrolling overview with most of the headline data.
- A new section explains why tech regulation matters, linking it to the EU's productivity and competitiveness gap.
- The US comparison has its own page.

```
/                         Home: long-form overview (sections 1–8 below)
/why-it-matters/          Full version of section 2, with sources
/findings/rules/          The rulebook in detail
/findings/evidence/       What we know about impact
/findings/us-comparison/  EU vs US (draft: site/us_comparison.md)
/instruments/             Index of all 115, plus one page each
/studies/                 Library of all sources
/data/                    Downloads, citation, licence
/methodology/
/about/
```

---

## Home page

Each section is one screen or less: a heading that states the finding, two or three sentences, then figures or one chart. Every section ends with a "More" link to the detailed page.

### 1. Opening *(your introduction)*
- Title and a one-sentence thesis, followed by your introduction text.
- Five headline figures in one row:

| Figure | Value |
|---|---|
| EU digital instruments | **115** (105 adopted, 10 pending) |
| Legal restrictions in their texts | **≈24,700** |
| Implementing and delegated acts adopted under them | **690** |
| Proposal promises never checked | **half** (218 of 440) |
| EU vs US, restrictions per act | **≈2.4×** |

### 2. Why tech regulation matters *(new; draft text below)*
Draft:

> Europe's growth problem is largely a technology problem. The EU's economy has fallen behind the United States over the past two decades: the gap in GDP at constant prices widened from slightly more than 15% in 2002 to 30% in 2023. Around 70% of the gap in GDP per head is explained by lower productivity, and, as the Draghi report on European competitiveness put it, "the productivity gap between the EU and the US is largely explained by the tech sector." Only four of the world's top 50 tech companies are European, and the EU's share of global tech revenues fell from 22% to 18% between 2013 and 2023 while the US share rose from 30% to 38%.
>
> Regulation is one reason the report gives. It counts "around 100 tech-focused laws and over 270 regulators active in digital networks", and notes that more than 60% of EU companies see regulation as an obstacle to investment. Our dataset, built from the CEPS inventory, has 115 instruments.
>
> Not everyone agrees regulation is the main cause. Anu Bradford argues the gap owes more to Europe's fragmented single market, shallow capital markets and other features of the US ecosystem than to strict rules. The EU's own simplification agenda now treats the volume of rules as a problem in itself.
>
> That debate is usually conducted without numbers: how many rules are there, how fast are they growing, and did they deliver what was promised? This site provides them.

- Figure strip from the Draghi report: GDP gap 15% → 30%; 4 of top 50 tech firms; tech revenue share 22% → 18% against the US 30% → 38%; more than 60% of firms see regulation as an obstacle.
- Each figure links to its source page. All Draghi figures were checked against Part A of the report. Before publishing, add one line on the Commission's simplification and omnibus agenda with checked figures.

### 3. The rulebook has grown fast
- Chart: cumulative instruments and cumulative restrictions since 1987.
- Figures:
  - 55 of the 105 adopted acts date from 2020 or later
  - about 2.8 million words of legal text
  - about 24,700 restrictions in the original texts
- Chart: average restrictions per act by decade: 25 (before 2000), 140 (2000s), 177 (2010s), 256 (2020s).

### 4. New laws are bigger and get bigger in negotiation
- Texts grow between the Commission proposal and the adopted act: median +45% words, +28% restrictions (99 acts compared).
- Chart: proposal against adopted act (chart 08).

### 5. Who the rules bind, and how
- Addressees: private parties 22%, member states 23%, EU institutions 25%, unclear 30%. Flag as approximate (74% addressee accuracy).
- Types:
  - about 21,200 obligations ("shall", "must")
  - 1,600 prohibitions
  - 1,500 duties of result ("shall ensure")
  - smaller numbers of restricted permissions and explicit requirements
- Chart: the 12 policy areas, sorted by restrictions.

### 6. The second layer: implementing acts and guidance
- 690 implementing and delegated acts, containing about 11,200 further restrictions. That is close to half again on top of the main acts.
- 138 pieces of guidance:
  - Commission guidance: 52 (EUR-Lex) and 6 (web)
  - EDPB: 52
  - EBA: 20
  - ESMA: 8
- About 48,000 national measures transposing the directives.
- Chart: main acts against implementing acts (chart 04).

### 7. Do the rules work? We mostly don't know
- 299 studies and evaluations, of which 42 are causal.
- Evidence level:
  - strong for 2 instruments (GDPR, roaming)
  - moderate for 12
  - thin for 60
  - forecasts only for 40
- Promises in the proposals: 218 of 440 never measured, 67 reported only as activity, 64 measured, 64 partly measured, 27 mixed.
- Charts: evidence levels; promise outcomes.
- Two or three short examples with links, e.g. the Data Act's €270bn GDP forecast, roaming as a success that was measured, the DMA's early evidence.

### 8. How the EU compares with the US
- 10 matched pairs: the EU act has more restrictions in every one, ×2.4 at the median, and is denser in 8 of the 10 (14.1 against 8.8 per 1,000 words).
- Chart 10.
- A link to the full explainer.

### 9. Explore and caveats
- Three entry points: instruments, studies, data.
- A caveats strip of one line each:
  - counts are not costs
  - automated counts are approximate
  - "not measured" means not found
  - the method page has the full detail

---

## Other pages

The other pages are unchanged from revision 1 except for these additions:
- **/why-it-matters/:** the long version of section 2.
  - The Draghi diagnosis and the productivity figures.
  - The regulation-as-obstacle evidence (EIB Investment Survey, SME surveys).
  - Counter-views (Bradford, and critiques of the productivity-gap measure).
  - The EU's 2025–26 simplification agenda (Competitiveness Compass, omnibus packages), with figures checked before publishing.
  - How this project's data can test these claims.
- **/findings/us-comparison/:** the explainer already drafted (`site/us_comparison.md`).
- **About and Methodology:** as before. The Methodology page gains the US comparison and the source-category rules (impact assessments grouped with promises; enforcement excluded).

## Sources for section 2
- M. Draghi, *The future of European competitiveness*, Part A (September 2024). All quoted figures were checked against the report text: GDP gap, 70% productivity share, tech-sector attribution, 4 of top 50, tech revenue shares, ~100 laws and >270 regulators, >60% of firms.
- A. Bradford, "The False Choice Between Digital Regulation and Innovation", *Northwestern University Law Review* (2024). Confirm the volume number before citing; sources disagree between vol. 118 and vol. 119.
- Still to verify before use: Competitiveness Compass burden-reduction targets, and the scope of the Digital Omnibus.
