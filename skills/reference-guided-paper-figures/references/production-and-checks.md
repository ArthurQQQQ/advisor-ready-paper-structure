# Figure brief, provenance, and integration

## Minimal working brief

Save a compact record in the paper's existing figure/evidence area. Reuse the study's own schema when it already captures these fields.

```yaml
figure_id: construction-overview
reader_question: What does this transformation preserve and change?
scientific_status: proposed protocol
evidence: []          # verified source IDs and exact file/table/passage locators
gaps: []              # unknown facts or missing results stay explicit
exact_content: {}     # labels, objects, quantities, arrows, branch conditions
reference_images: []  # file or URL; version; target/style role; author choice
visual_profile: {}   # palette roles, type hierarchy, objects, connectors
destination: {}      # paper width, aspect ratio, file format, caption location
production: {}       # tool, prompt file, original output, final export
verification: {}     # semantic checks, visual checks, data checks, PDF pages
```

Keep the brief small enough to compare directly with the figure. Hash source data when precise conservation matters, and record any intended scientific change separately from styling.

## Semantic checks

Verify content before judging appearance:

- Can every factual count or result be traced to the cited source? Do populations and analysis units match?
- Are author-written examples, inherited benchmark material, observations and inferred states distinguished?
- Do identifiers and highlighted quotations map to the intended source and scope?
- Do all success paths pass through their required conditions? Do loops return to the correct operation?
- Does a timeline preserve recorded time, reference time and any unobserved transition time as different concepts?
- Are unsupported, disputed or out-of-grammar cases kept unknown? Is technical failure distinguished from a semantic unknown?
- Do proposed targets remain targets? Does repetition or exposure avoid being presented as independent information?

Use only checks relevant to the figure. A separate reviewer can compare the source brief with the image without receiving the author's desired conclusion; record unresolved issues rather than voting them away.

## Data panels

Read the actual source table before plotting. Record the analysis set, count unit, denominator, weighting, missingness and uncertainty definition. If a category is unknown, display or bound it rather than silently removing it. Show nominal targets and realized quantities with visibly different marks. Use raw counts beside percentages where they explain the denominator.

Generate bars and intervals deterministically. Recompute the plotted values from the frozen input and verify category sums. For a figure refresh, preserve table/data hashes unless a data correction was explicitly requested. Do not infer confidence intervals from bounds or draw invented replicates to fill a panel.

## Export and manuscript check

Keep the generator's original PNG unchanged. A PDF wrapper may preserve those pixels for LaTeX, but remains raster-containing. Keep SVG/PDF plot text and geometry editable when feasible, and inspect the actual export for clipping, font substitution and shifted hatches.

Check the figure at the intended paper width: labels, superscripts, connectors, contrast, legend and caption. Review grayscale or redundant encoding where color carries meaning. Inspect at least the complete changed PDF pages and the rest of the document for pagination, missing figures, broken references and layout regressions. Check that body prose and numerical tables were conserved, allowing only the requested edits and mechanical metadata changes.

Report delivered artifacts, which are raster/vector, what was verified, and any unresolved issue that affects interpretation. Do not claim a compiled PDF, integrated paper or editable figure exists until the corresponding artifact has been created and checked.
