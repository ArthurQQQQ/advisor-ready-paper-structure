---
name: advisor-ready-paper-structure
description: "Review the structure of a paper or outline, especially empirical ML/AI. Use when the author wants to check section order, map claims to supplied evidence, locate gaps in the argument, or get a prioritized section-by-section revision plan."
---

# Advisor-Ready Paper Structure · 不烧心的论文结构审阅

Review how the draft or outline makes its argument from the supplied material. Identify where the paper makes its central claim, where the reader finds its evidence, and which changes would make that sequence clearer. Respect the author's research question, scientific scope, and target format. Work on the requested sections, using wider context only when it changes their role.

## 1. Establish what the evidence supports

- Read the supplied notes, draft, figures, tables, protocol and results in scope. Give each distinct evidence item an ID such as `E01` and a source locator such as a filename and heading, table row, or figure panel. Record what it directly shows, relevant population/split, comparison and protocol, and where it can support a claim. Classify it as usable, limited, conflicting, or unavailable. A draft assertion, recollection, or analysis plan stays so labeled. Separate direct observation from interpretation.
- State the strongest defensible conclusion in one or two sentences. Link it to evidence IDs and state its scope. Identify the intended claim if it exceeds the evidence. When a source is ambiguous or contradictory, say what remains open and how it affects the proposed placement or wording of the claim. Report conflicting, null, or unfavorable evidence that changes the conclusion.
- Mark missing evidence or reasoning with gap IDs such as `G01`. Distinguish edits the author can make from the current draft from checks that affect a structural choice or a claim's scope. For each check, name the material, the comparison or verification, and what finding would change the recommendation. Prioritize provenance and comparability when they determine which results belong together. If a check is blocked, give a defensible fallback the author can use now.

## 2. Outline the paper section by section

Read [the section playbook](references/section-playbook.md) for empirical papers. Adapt to the actual contribution and venue. Each proposed section or subsection has a job and a logical handoff. Describe what belongs there, in what order, and which evidence IDs support it. For existing drafts, anchor feedback to a section and specific heading, paragraph, or display. For a move or split, name both the current location and the destination. For a new outline, name where the recommendation belongs.

The introduction leads from a concrete problem to the key idea and a bounded evidence preview. The method explains the key idea and follows the actual flow. Each experiment connects its purpose, comparison and reading guide, observation, interpretation, and implication for a design or claim. The conclusion returns to the opening question, states supported findings and limits, and draws future work from those limits. Other paper types may organize the argument around a proof, dataset, synthesis, or case.

## 3. Leave visible gaps and plan the displays

Write the working outline in the manuscript language. For bilingual guidance, give each section's job and writing sequence in both requested languages. Give each claim and gap a single shared ID across the two languages.

At the exact location of a substantive gap, leave the missing prose blank and show a short editor note with its gap ID. Write the note in the author's preferred second language. If unspecified, use Chinese notes for an English manuscript and English notes for a Chinese or other non-English manuscript. Notes say what to add or verify and why. Use smaller gray sans-serif notes and darker serif draft text in HTML, with an explicit text label for gaps so they are distinguishable without color. In Markdown, use visibly labeled italic blockquotes and retain the same IDs.

Plan only figures and tables needed for an argument. Reserve each at its intended section with a provisional title, the claim it would support, source or gap IDs, and enough specification to build it. For a figure give panels, axes/units or diagram components and the intended comparison. For a table give rows, columns, metric, analysis set, and uncertainty where applicable. Leave missing data cells and plot regions empty. Mark them with an adjacent note, never with dummy numbers, fabricated panels, or a claim that assumes the result.

## 4. Deliver the review

Return these components in order, combining them into one document when practical.

1. **Review summary** with the main structural finding, the strongest conclusion supported by the supplied evidence, and the highest-impact uncertainty or conflict.
2. **Evidence map** with IDs, source locators, present support, and boundaries.
3. **Priority checks** with the evidence or gap to start from, the action and its completion check, and what the outcome would change. For blocked actions, give the dependency and a defensible fallback.
4. **Suggested structure and annotated outline**, including blank figure/table slots where required. If file output is available, use [the HTML scaffold](assets/annotated-outline.html) for the styled working copy. Otherwise use the Markdown conventions above. Honor requests for a different document format.
5. **Section-by-section review table**, last. Give one row per proposed section and substantive subsection, including those ready to write. Multiple rows may cover a section with independent gaps. Use the following columns, translated as needed.

| Section | Job in the argument | Evidence and location | Logic or evidence gap | Recommended revision | Priority and completion check |
|---|---|---|---|---|---|
| Section or subsection | What the reader should understand | E IDs and exact draft location when present | G ID and concrete issue, or ready | Specific edit or check and where it belongs | Order or dependency and an observable check |

Before delivery, check that each substantive claim in the review points to supplied evidence, every open gap has a row and a next action, every planned display is linked to a claim or gap, and the table agrees with the outline and priority checks. Mark missing material in the review and keep notes with their original locations. A structure review uses the supplied draft and evidence.
