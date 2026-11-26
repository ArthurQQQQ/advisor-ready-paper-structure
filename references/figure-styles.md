# Choose a paper-figure reference

Use this optional branch when the author wants concept illustrations, method diagrams, graphical abstracts, or visual alternatives for paper figures. Begin with the figure's role in the argument, the supplied evidence and actual figures from comparable papers. A structure review or prose edit can simply plan the needed displays.

## Verified ICLR references

These examples were checked against the conference papers on 2026-11-26. They are candidates for the author to inspect and choose from. Identify the visual organization to borrow, then build a figure for the current research.

| ID | Paper and exact figure | Organization to study | Source |
| --- | --- | --- | --- |
| R1 | **Self-RAG, ICLR 2024, Figure 1, PDF page 2** | A left/right comparison of ordinary RAG and Self-RAG. A worked text example connects retrieval, candidate generations, support labels and selection. Useful for explaining what a decision changes in the evidence and answer. | [Official paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/25f7be9694d7b32d5cc670927b8091e1-Paper-Conference.pdf#page=2) · [Author figure](https://selfrag.github.io/static/images/teaser_self_rag_v8.png) |
| R2 | **DuoAttention, ICLR 2025, Figure 2, PDF page 3** | Aligned identification/deployment panels. Matrices, operators and conditional routes depict the computation; stable colors identify corresponding objects across panels. Useful for a compact mechanism or implementation overview. | [Official paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/5c1ddd2e59df46fd2aa85c833b1b36ed-Paper-Conference.pdf#page=3) · [Author preprint figure](https://arxiv.org/html/2410.10819v1/method.png) |
| R3 | **rStar: Mutual Reasoning Makes Smaller LLMs Stronger Problem-Solver, ICLR 2025, Figure 2, PDF page 2** | A concrete question branches into candidate solutions, passes through generation and discrimination, then selects an answer. Numbered stages and restrained emphasis explain the interaction. Useful for generation/verification and feedback processes. | [Official paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/35514d533cdc278a7780daf0dbe7d0b7-Paper-Conference.pdf#page=2) · [Author repository](https://github.com/zhentingqi/rStar) |

For other needs, inspect [RAPTOR Figure 1](https://arxiv.org/pdf/2401.18059#page=2), which expands a tree into a layer and node detail, or [Differential Transformer Figure 2](https://proceedings.iclr.cc/paper_files/paper/2025/file/00b67df24009747e8bbed4c2c6f9c825-Paper-Conference.pdf#page=3), which pairs a computation diagram with pseudocode. Select references for the requested figure's explanatory role. A paper's acceptance does not certify a new figure's correctness or predict acceptance.

Use concrete paper/figure references as the starting point. A named palette or a background change alone does not establish the diagram's explanatory design.

## Show alternatives, then carry the choice forward

1. **Set the content.** Give the figure an ID and a short brief: its reader question, claim or design it illustrates, source/gap IDs, exact labels, modules, directed connections, branch conditions and destination. Identify proposed components and unknown results before styling.
2. **Show real references.** If the author has specified a reference or the paper has a confirmed figure profile, reuse it. When exploring, show a few actual figures from the requested venue or comparable accepted papers, with paper links, figure numbers and one-line observations about layout, comparison, example use or level of detail. Verify conference/year from the proceedings or decision record; a submission header alone does not establish acceptance. Inspect the pixels before describing visual traits. Prefer a legible original figure or an unaltered PDF figure-region rendering over an entire page. Attribute the original. If a source is unavailable, state what has not been inspected.
3. **Record the selection.** Let the author choose a specific figure, supply another reference, or describe a mixture. Save the confirmed direction in the paper's working artifact directory, for example `figure-style.md`, with source paper/URL, figure/version, what to borrow, palette, type roles, line/arrow treatment, density, destination and affected figure IDs. Attribute the selection to the author only after they make it. A recommended reference stays a recommendation. Reuse the profile for later figures and update it when the author changes their choice.
4. **Draw the real figure.** After the reference is selected, translate its relevant organizational ideas to the current figure brief. If the author requests generated alternatives, produce a few versions with the same scientific content, information density, aspect ratio and comparable label sizes. Use the available image-generation tool for illustrations, or vector/typesetting tools for exact technical content. Preserve the current study's identities and status; reference-paper claims, data and examples do not become this study's evidence. For an image edit, include the actual target through the tool's supported reference mechanism and keep the original. If generation is unavailable, deliver the briefs and prompts and say what has not been rendered.
5. **Check what the image says.** Inspect labels, paragraph/source IDs, module membership, arrow endpoints and direction, loop destinations, branch logic, qualifiers and proposed/completed status. In particular, check that every success path passes through each required condition. Correct a misleading connector or changed label before treating the image as a usable diagram. Review legibility at the intended display size.

Keep the choice lightweight: one representative diagram can establish the style for the paper. Generate alternatives again when requested or when a different destination materially changes the design.

Use the figure area to explain the research with examples, comparisons, object structure, computation or a useful local expansion. Size text and elements for the intended paper width. Put the figure's full title and explanation in the caption, using short panel headings inside where they help readers navigate.

## Preserve scientific meaning across styles

- Generate concept and method illustrations from verified or explicitly proposed content. A proposed mechanism, risk gate or target stays labeled as such. A population-level evaluation target is not an achieved result or an automatically equivalent per-example threshold.
- Plot measured curves, bars, uncertainty intervals, heatmaps and numerical tables from their actual source data with deterministic plotting or typesetting tools. Reuse the chosen palette and typography while preserving scales, observations, missing values and uncertainty. Never generate plausible measurements to fill an empty results panel.
- An empty result remains empty in a Quick Paper, with the next action adjacent to it. A concept drawing can explain the planned comparison without predicting its outcome.
- Use color together with labels, shape or line treatment. Preserve readability at the final manuscript, slide or web size. Inspect contrast and the actual exported figure.
- For exact formulas, small technical labels or editable delivery, use vector/typeset elements as needed and verify them against the brief. An image-generation PNG is a raster draft; describe an editable SVG/PDF as delivered only after creating and inspecting it.

For data-plot implementation and export, use the available scientific-visualization capability or equivalent plotting tools. Verify the actual venue's requirements when submission preparation is part of the request.

## Generation brief

Keep content and style separate so that changing the style does not change the research:

```text
Figure ID and destination: [current figure; manuscript / slides / web]
Reader question and scientific status: [what it explains; supported / proposed]
Content: [exact modules, labels, connections and branch conditions]
Evidence and gaps: [source IDs; missing facts or result cells]
Visual reference: [verified paper, figure, URL and organizational traits to borrow]
Layout: [aspect ratio, panel order, label hierarchy and density]
Checks: [required paths, qualifiers and labels to preserve]
```

For example, a planned early-stopping diagram can show read prefix → cited answer → support check → planned risk gate → stop or continue. A stop branch must follow both checks. The continue branch returns to the next unread part; unread content never enters the current answer. A displayed 5% false-stop target describes the evaluation objective, with calibration and achieved results left open until measured.
