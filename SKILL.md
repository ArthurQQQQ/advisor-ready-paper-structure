---
name: advisor-ready-paper-structure
description: "Review and restructure a paper or outline, especially empirical ML/AI. Lead with a short verdict and a clickable whole-paper argument map. Each node gives one or two concrete revisions grounded in evidence and baseline checks."
---

# Advisor-Ready Paper Structure · 不烧心的论文结构审阅

Review how the draft or outline makes its argument from the supplied material. Identify where the paper makes its central claim, where the reader finds its evidence, and which changes would make that sequence clearer. Respect the author's research question, scientific scope, and target format. Work on the requested sections, using wider context only when it changes their role.

Start with the topic or research question and a draft or outline. Use experiment notes, results, baseline descriptions, figures, and tables when supplied. A target venue is optional. Review what the author has and record material gaps in the review.

## 1. Establish what the evidence supports

- Read the supplied notes, draft, figures, tables, protocol and results in scope. Give each distinct evidence item an ID such as `E01` and a source locator such as a filename and heading, table row, or figure panel. Record what it directly shows, relevant population/split, comparison and protocol, and where it can support a claim. Classify it as usable, limited, conflicting, or unavailable. A draft assertion, recollection, or analysis plan stays so labeled. Separate direct observation from interpretation.
- For each material comparative claim, identify which baseline tests it and whether the draft explains why that comparison matters. Use the supplied sources to identify the closest or strongest relevant alternatives. Check whether the comparison uses compatible datasets, splits, metrics, and training or inference budgets where those affect the claim. Record the exact source and comparison limits in the relevant node. A missing explanation may call for a revision using existing evidence. A comparison whose support cannot be verified calls for a source check or a narrower claim. A comparison confirmed missing and needed for the claim calls for a new experiment or a narrower claim. Leave completeness open when the supplied sources cannot establish it. Do not invent baselines, results, or literature claims.
- State the strongest defensible conclusion in one or two sentences. Link it to evidence IDs and state its scope. Identify the intended claim if it exceeds the evidence. When a source is ambiguous or contradictory, say what remains open and how it affects the proposed placement or wording of the claim. Report conflicting, null, or unfavorable evidence that changes the conclusion.
- Mark missing evidence or reasoning with gap IDs such as `G01`. Distinguish edits the author can make from the current draft from checks that affect a structural choice or a claim's scope. For each check, name the material, the comparison or verification, and what finding would change the recommendation. Prioritize provenance and comparability when they determine which results belong together. If a check is blocked, give a defensible fallback the author can use now.

## 2. Map the whole argument

Use [the section playbook](references/section-playbook.md) to adapt the map to the manuscript's topic, contribution, and venue. For a whole-paper review, cover the title and abstract, introduction, related work where relevant, method, experimental setup, substantive results in the proposed order, discussion, conclusion, and appendices as applicable. Use the paper's actual section names or concrete proposed headings. Group minor subsections under the node where their material belongs. For narrower reviews, map the requested sections and include adjacent context where a handoff depends on it.

Label each node with a short section or result name. Show the reading order and use connections only where a section hands an assumption, design choice, result, or limitation to another. Keep parallel experiments and supporting analyses distinct, especially when they test different populations, outcomes, or claims.

On selection, show one or two concrete edits for the node. Use direct verbs and name the affected heading, paragraph, figure, or table. For a move or split, name the current location and the destination. Include evidence, comparison boundaries, or a fallback in the edit when they affect what the author should do. Keep exact source locations traceable through the relevant edit text.

The introduction leads from a concrete problem to the key idea and a bounded evidence preview. The method explains the key idea and follows the actual flow. Each experiment connects its purpose, comparison and reading guide, observation, interpretation, and implication for a design or claim. The conclusion returns to the opening question, states supported findings and limits, and draws future work from those limits. Other paper types may organize the argument around a proof, dataset, synthesis, or case.

## 3. Leave visible gaps and plan the displays

Write the outline in the manuscript language. For bilingual guidance, give the edit in both requested languages when needed. Use the same evidence and gap IDs across languages.

At a substantive gap, say what to add or verify as one of the node's edits. For a separate annotated draft, put the note at the exact location in the author's preferred second language. Keep all visible report text at a comfortably readable size.

Plan only figures and tables needed for an argument. Reserve each at its intended section with a provisional title, the claim it would support, source or gap IDs, and enough specification to build it. For a figure give panels, axes/units or diagram components and the intended comparison. For a table give rows, columns, metric, analysis set, and uncertainty where applicable. Leave missing data cells and plot regions empty. Mark them with an adjacent note, never with dummy numbers, fabricated panels, or a claim that assumes the result.

## 4. Deliver a compact review

1. **Verdict.** Lead with one short sentence that states the most consequential structural change. Include an evidence boundary when it determines the recommendation.
2. **Interactive argument map.** Use [the HTML scaffold](assets/annotated-outline.html) for a standalone file. Match the visual language of the paper or project when a reference is available. Use short node labels and a clear reading direction. Keep the initial view to the paper title, verdict, and map. Each node opens with a click or keyboard and shows only one or two actionable edits. A shared detail area can keep the map steady as readers move between sections. Keep branding, kickers, help captions, secondary small text, legends, sidebars, and archives out of the default report. Provide a full audit or review table when requested.
3. **Markdown fallback.** If HTML output is unavailable or the user requests Markdown, start with the same verdict and a compact map. Give one or two edits under each node.

Check that the verdict and map are clear before opening a node, and every visible element helps the author navigate or make an edit. Verify that material claims are traceable, gaps have next actions, and each node opens the right edits. Keep each recommendation in one place.
