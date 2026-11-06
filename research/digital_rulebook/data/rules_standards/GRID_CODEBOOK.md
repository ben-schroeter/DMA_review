# Codebook: regulatory design grid (Coglianese)

Replaces the rules/standards (Kaplow) codes for the main analysis from November 2026. Source: Cary Coglianese, "Rule Design:
Defining the Regulator-Regulatee Relationship" (2024; SSRN 4734545), and the National Academies report on safety regulation in
high-hazard industries that adopted it. Two questions classify every obligation:

- **Means or ends?** Does the provision tell the addressee *what to do* (an action, procedure, design feature, content, format,
  or a specific act that is banned)? That is **means**. Or does it tell the addressee *what to achieve or avoid* (a result,
  state of affairs, level of performance or harm), leaving how to the addressee? That is **ends**.
- **Micro or macro?** Is the required action or result *specific*: a named act, number, deadline, closed list, feature or a
  concrete, checkable result? That is **micro**. Or is it *general*: the addressee must design its own plan, system or
  process (macro-means), or bring about an open-ended result judged by terms such as appropriate, adequate, effective, fair,
  safe, secure, not misleading, without risk (macro-ends)? That is **macro**.

## Codes

| Code | Cell | Meaning | Examples |
|---|---|---|---|
| MM | Micro-means | A specific action, content, format, procedure step or specific banned act. | "Roaming providers shall charge … on a per-kilobyte basis." "The white paper shall contain the following information:" "Providers of online platforms shall not present advertisements based on profiling using special categories of personal data." "The application shall be filed in one of the official languages." "Importers shall keep a copy of the EU declaration of conformity for 10 years." |
| ME | Micro-ends | A specific, checkable result or state; the addressee chooses how to achieve it. | "The payment service provider shall ensure that the payee receives the full amount." "The amount is made available and value dated immediately after receipt of the funds." "Toys shall not contain [listed] substances." "By default personal data are not made accessible to an indefinite number of persons." "Noise shall not exceed 85 dB(A)." |
| XM | Macro-means | Management-based: the addressee must set up and run a plan, policy, procedure, system, framework, risk assessment, governance or control arrangement whose content it designs. | "Financial entities shall have a sound, comprehensive and well-documented ICT risk management framework." "shall implement and maintain effective policies and procedures to identify, prevent, manage and disclose conflicts of interest." "shall establish … a clear and detailed strategy for winding down." "Providers of very large online platforms shall diligently identify, analyse and assess any systemic risks." |
| XE | Macro-ends | A general duty: an open-ended result or level judged after the fact. | "take appropriate and proportionate measures to ensure a high level of privacy, safety and security of minors." "implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk." "Machinery shall be designed and constructed so that it can be operated without putting persons at risk." "shall negotiate in good faith." "shall not engage in unfair commercial practices." |
| L | Specified later | The provision says its content will be set by a delegated or implementing act, technical standards, harmonised standards, common specifications or guidelines. Code the duty that waits for the specification. | "When specified in the delegated act adopted pursuant to Article 4, supply chain actors shall:" |
| D | Left to member states | The content is chosen by the member state when it transposes or implements. | "Member States shall lay down the rules on penalties …" "Member States shall determine how such reference is to be made." |
| N | Not a duty | No one is required to do or achieve anything: definitions, scope or transitional clauses, presumptions and rules of evidence, statements of when a period starts or how long it lasts, allocations of competence or lists of tasks, entitlements and rights phrased as such, programme objectives, footnotes, quoted case law, truncated fragments. | "The period of withdrawal shall begin from the date of the agreement." "Products placed on the market before 11 December 2027 shall be subject to the requirements only if …" "The burden shall be on the provider to prove …" "Each supervisory authority shall be competent for …" "The bodies of the Joint Undertaking shall be:" |

## Decision rules

1. **First test N.** Ask: is a person or body required to do, refrain from, or bring about something? If not, N. Time limits
   that bind an authority's own procedure ("the total duration of any extension shall not exceed 20 working days") are N unless
   they require a named body to act by a date ("ESMA shall submit the draft RTS by 30 June 2024" is MM).
2. **Judge the core duty**, as before. A loose qualifier on *how or when* a specific act is done stays micro: "notify without
   undue delay", "publish in an easily accessible manner", "a brief summary" are MM. But when an open term decides *what* must
   be done or *whether* the act is allowed, the duty is macro: "include the information necessary to demonstrate compliance",
   "preserve the content only if and for as long as necessary", "extend the period only where, having regard to the rights and
   interests of all parties …" are XE.
3. **"Shall ensure that …"**: MM if what follows is a specified act by someone ("ensure that agents inform users of this fact");
   ME if it is a specified state or result ("ensure that the payee receives the full amount"); XE if the state is open-ended
   ("ensure an appropriate level of security", "ensure that the processing is fair").
4. **Prohibitions**: a specific act banned is MM ("shall not present advertisements based on profiling of minors"); a specific
   result banned is ME ("shall not exceed", "shall not contain [listed substances]"); an open-ended result banned is XE
   ("shall not mislead", "shall not cause harm", "shall not compromise security").
5. **Product requirements**: a named feature, marking or document is MM ("bears a serial number"); a measurable performance
   or the absence of a named hazard is ME; an essential requirement framed as safety, fitness or absence of risk in general
   terms is XE.
6. **Plans, systems and assessments** are XM even when the list of their elements is fixed. A duty to assess or evaluate
   that must "consider" or "take into account" listed factors is XM. If a list item is coded as its own
   obligation, code that item on its own wording.
7. **Information duties** (inform, notify, report, publish, register, keep records, submit, label) are MM when what, to whom
   or when is fixed; XE only if the content is entirely open ("provide all appropriate information").
8. **"Take appropriate measures to [goal]"** is XE (an open result). **"Take the following measures:" with a list** is MM.
   **"Adopt measures / take all necessary measures"** with no stated goal is XE.
9. **Duties of member states and EU bodies** are coded on the same tests. A member state duty that leaves the content to the
   state is D; one that fixes it is coded on the grid ("Member States shall ensure that providers offer a free switching
   service" is ME or MM by rule 3).
10. **Mixed cases**: pick the element that decides compliance. If a specific floor and an open-ended duty matter equally,
    choose the macro code.
11. **Comitology and procedure references** ("That implementing act shall be adopted in accordance with the examination
    procedure referred to in Article X") are N.
12. **Cross-references**: "in accordance with Article X" takes the code that Article X's duty would get if clear from the
    clause; otherwise MM.

## Relation to the earlier codes

Kaplow's rule/standard test (data/rules_standards/CODEBOOK.md) roughly corresponds to micro/macro, but not exactly: a micro-ends
duty ("ensure the payee receives the full amount") was a rule under Kaplow; under the grid it is an ends-based duty that leaves
the means to the addressee. The earlier codes stay in data/rules_standards/batches/*_coded.json for comparison; the new codes are
in data/rules_standards/grid/*_coded.json.
