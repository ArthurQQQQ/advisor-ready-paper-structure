---
name: advisor-ready-paper-structure
description: "Review and restructure a paper or outline, especially empirical ML/AI. Lead with a concise verdict and the first edits, then show a clickable whole-paper argument map with evidence, baseline checks, and specific revisions inside each section."
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

Give each node a short visible statement of the question it answers or the job it does. Show how it hands an assumption, design choice, result, or limitation to another node. Use a connection only where the paper's logic warrants it. Keep parallel experiments and supporting analyses distinct, especially when they test different populations, outcomes, or claims. Use cross-links for appendices and evidence that serves more than one section.

Inside each node, describe its proposed argument and the edit that makes it work. Anchor recommendations to the current heading, paragraph, figure, or table. Include exact evidence and gap IDs and the comparison boundaries that matter. For a move or split, name both the current location and the destination. For a new outline, name where material belongs. Give a completion check for a proposed edit and a practical fallback for an unresolved dependency.

The introduction leads from a concrete problem to the key idea and a bounded evidence preview. The method explains the key idea and follows the actual flow. Each experiment connects its purpose, comparison and reading guide, observation, interpretation, and implication for a design or claim. The conclusion returns to the opening question, states supported findings and limits, and draws future work from those limits. Other paper types may organize the argument around a proof, dataset, synthesis, or case.

## 3. Leave visible gaps and plan the displays

Write the working outline in the manuscript language. For bilingual guidance, give each section's job and writing sequence in both requested languages. Give each claim and gap a single shared ID across the two languages.

At the exact location of a substantive gap, leave the missing prose blank and show a short editor note with its gap ID. Write the note in the author's preferred second language. If unspecified, use Chinese notes for an English manuscript and English notes for a Chinese or other non-English manuscript. Notes say what to add or verify and why. Use smaller gray sans-serif notes and darker serif draft text in HTML, with an explicit text label for gaps so they are distinguishable without color. In Markdown, use visibly labeled italic blockquotes and retain the same IDs.

Plan only figures and tables needed for an argument. Reserve each at its intended section with a provisional title, the claim it would support, source or gap IDs, and enough specification to build it. For a figure give panels, axes/units or diagram components and the intended comparison. For a table give rows, columns, metric, analysis set, and uncertainty where applicable. Leave missing data cells and plot regions empty. Mark them with an adjacent note, never with dummy numbers, fabricated panels, or a claim that assumes the result.

## 4. Deliver a compact review

1. **Verdict and first edits.** Lead with one or two sentences that state the structural diagnosis, the strongest supported conclusion, and any uncertainty that materially changes it. Give one to three priority edits in execution order and link each to its node.
2. **Interactive argument map.** Use [the HTML scaffold](assets/annotated-outline.html) for a standalone file when file output is available. Use the conventions of a research-paper figure, with short labels, a consistent reading direction, evidence IDs, and explicit handoffs. Use native `<details>` and focusable `<summary>` so each node starts closed and opens with a click or keyboard. The map supplies the proposed outline. Put section rationale, source locators, baseline checks, editor notes, and display plans inside the node that uses them. Put shared checks or a source index in a separate collapsed panel when multiple nodes need them.
3. **Markdown fallback.** If HTML output is unavailable or the user requests Markdown, lead with the same verdict and priorities. Use a compact map with explicit handoffs, followed by details grouped by node. Honor requests for a different format or for a full review table.

Check the initial view on its own: the verdict, priority edits, and paper structure should be clear before opening any node. Verify that material claims have source locators, gaps have next actions, links land on their nodes, and planned displays connect to a claim or gap. Keep each detailed recommendation in one place.
