# Choose a paper-figure reference

Use this optional branch when the author wants concept illustrations, method diagrams, graphical abstracts, or visual alternatives for paper figures. Begin with the figure's role in the argument, the supplied evidence and actual figures from comparable papers. A structure review or prose edit can simply plan the needed displays.

## Recent ICML paper-figure references

These examples were checked against the papers and author pages on 2026-11-26. Match the author's requested date range, venue/status and visual taste. When they want AI-generated aesthetics, verify that the source identifies the specific output as generated or enhanced; appearance and publication year do not establish provenance. The examples below are candidates for selection, with no preference inferred from their inclusion.

| Paper and exact figure | Organization to study | Source |
| --- | --- | --- |
| **DreamDojo, ICML 2026, Figure 1, PDF page 3** | White/gray surfaces with vivid lime-green emphasis. Video/image mosaics, robot imagery and training flows form four asymmetric regions with a clear visual hierarchy. Study how actual artifacts explain the stages. | [Official proceedings](https://proceedings.mlr.press/v306/gao26q.html) · [Author original figure](https://dreamdojo-world.github.io/overview.png) |
| **OmniShow, ICML 2026, Figure 2, PDF page 4** | A dense architecture on the left, mechanism expansions in the middle and training on the right. Pale blue, peach, green and lavender groups connect matching objects, matrices and detailed computation while retaining consistent geometry and typography. | [Official proceedings](https://proceedings.mlr.press/v306/zhou26ag.html) · [Paper figure](https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhou26ag/zhou26ag.pdf#page=4) · [Author project](https://correr-zhou.github.io/OmniShow/) |

Select references for both the requested figure's explanatory role and the author's visual preferences. Distinguish original diagrams, declared generated outputs, reference targets and failure cases when showing comparison galleries. Record production provenance only when the source provides it.

If the requested conference edition has not opened submissions or announced decisions, verify the current official timeline and label submissions or preprints accurately. Offer relevant available work with its actual status. Keep recency and AI-generation provenance as separate facts.

Use concrete paper/figure references as the starting point. A named palette or a background change alone does not establish the diagram's explanatory design.

## Show alternatives, then carry the choice forward

1. **Set the content.** Give the figure an ID and a short brief: its reader question, claim or design it illustrates, source/gap IDs, exact labels, modules, directed connections, branch conditions and destination. Identify proposed components and unknown results before styling.
2. **Show real references.** If the author has specified a reference or the paper has a confirmed figure profile, reuse it. When exploring, show a few actual figures matching the requested period, venue/status and aesthetic, with source links, figure numbers and observations about colors, typography, layout, examples and detail. Verify conference/year from the proceedings or decision record; a submission header alone does not establish acceptance. Inspect the pixels before describing visual traits. Prefer a legible original figure or an unaltered PDF figure-region rendering over an entire page. Attribute the original. If all candidates are rejected, use that feedback to find different examples before recommending them again. If a source is unavailable, state what has not been inspected.
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
