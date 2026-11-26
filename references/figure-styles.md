# Choose a paper-diagram style

Use this optional branch when the author wants concept illustrations, method diagrams, graphical abstracts, or visual style alternatives for paper figures. Begin with the figure's role in the argument and the supplied evidence. A structure review or prose edit can simply plan the needed displays.

## Three starting directions

| ID | Direction | Visual recipe | Useful starting point |
| --- | --- | --- | --- |
| A | **Publication Minimal · 期刊极简** | White background, near-black sans-serif labels, thin clean connectors, aligned flat modules, restrained slate-blue and teal emphasis, pale neutral fills. | Manuscript method diagrams and study-design schematics. |
| B | **Academic Tech · 学院科技** | Deep midnight navy, off-white labels, cyan/teal routes and muted lavender modules, precise architectural spacing and restrained depth. Clear labels without decorative code or glow. | Conference presentations, system overviews and research demos. Adapt the background for a print destination if needed. |
| C | **Warm Editorial · 温润学院** | Ivory background, plum serif heading, crisp technical labels, muted teal arrows, lavender accents, subtle layered-paper treatment. Use texture behind the diagram without obscuring labels. | Problem-and-insight figures, graphical abstracts and shareable explanations. |

These are editable visual directions. They do not imply a journal's endorsement or submission compliance. The author can request another direction or combine traits, such as A's geometry with C's colors. Keep useful diagram components; add decorative objects only when they explain the subject.

## Show alternatives, then carry the choice forward

1. **Set the content.** Give the figure an ID and a short brief: its reader question, claim or design it illustrates, source/gap IDs, exact labels, modules, directed connections, branch conditions and destination. Identify proposed components and unknown results before styling.
2. **Reuse an existing choice.** If the author has specified a style or the paper already has a confirmed figure profile, use it. When they want alternatives, offer A/B/C. For a visual comparison, generate up to three previews using the same content, information density, aspect ratio and comparable label sizes. Label the candidates A/B/C and show the actual images, with a one-line description of each. Use the available image-generation tool for generated illustrations. If generation is unavailable, provide the briefs and prompts and state what has not been rendered.
3. **Record the selection.** Let the author pick a letter, supply a reference, or describe a mixture. Save the confirmed direction in the paper's working artifact directory, for example `figure-style.md`, with palette, type roles, background, line/arrow treatment, density, destination and affected figure IDs. Attribute the selection to the author only after they make it. A recommended default stays a recommendation. Reuse the profile for later figures in that paper and update it when the author changes their choice.
4. **Draw the real figure.** Use the selected direction with the current figure brief. Preserve approved content when restyling. For an image edit, include the actual target image through the generation tool's supported reference mechanism. Keep the original available.
5. **Check what the image says.** Inspect labels, paragraph/source IDs, module membership, arrow endpoints and direction, loop destinations, branch logic, qualifiers and proposed/completed status. In particular, check that every success path passes through each required condition. Correct a misleading connector or changed label before treating the image as a usable diagram. Review legibility at the intended display size.

Keep the choice lightweight: one representative diagram can establish the style for the paper. Generate alternatives again when requested or when a different destination materially changes the design.

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
Visual direction: [A / B / C, or the confirmed mixed profile]
Layout: [aspect ratio, panel order, label hierarchy and density]
Checks: [required paths, qualifiers and labels to preserve]
```

For example, a planned early-stopping diagram can show read prefix → cited answer → support check → planned risk gate → stop or continue. A stop branch must follow both checks. The continue branch returns to the next unread part; unread content never enters the current answer. A displayed 5% false-stop target describes the evaluation objective, with calibration and achieved results left open until measured.
