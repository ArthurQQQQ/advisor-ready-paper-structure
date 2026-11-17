# Research idea to Quick Paper

Follow this workflow when the author needs to shape a research question before writing or wants to continue a Quick Paper. Discuss the work in the current Codex conversation and keep a workspace artifact that the author can refresh and reopen. Use the author's language and wording where possible.

## Keep the workspace current

On the first substantive exchange, create `research-state.json` and `research-workspace.html` in the author-selected output directory or the current project's chat artifact directory. On subsequent turns, read and update the existing files. The HTML is a snapshot of the working brief, sources, and outline.

Maintain one JSON object with this shape. Use empty strings and an empty baseline list for unknown values.

```json
{
  "idea": "",
  "topic": "",
  "metric": "",
  "controls": "",
  "failure": "",
  "openQuestion": "",
  "status": "discussing",
  "baselines": [],
  "outline": ""
}
```

- `idea` records the author's starting point. The topic, metric, controls, and failure criterion make up the current brief. `openQuestion` records the question asked in this turn. Clear it when the topic is confirmed, then use it for the next consequential gap as the paper develops.
- Set status to `discussing` until the author confirms the topic, `confirmed` while the baseline search and outline are pending, and `ready` once the resulting Quick Paper is available. A ready Quick Paper can still have open evidence gaps.
- Each baseline has string fields `name`, `role`, `source`, `match`, and `notes`. Put the original HTTP or HTTPS URL in `source`. Use `match` for a concise assessment in the author's language and `notes` for the protocol conditions, source locator, unresolved differences, and next check. An empty source records a planned comparison or an unverified slot.
- An optional string `id` can identify the workspace's browser draft. Keep it stable for the same project and topic.
- Once the author has an outline, keep `outline` in sync with the current Quick Paper Markdown. Read any author changes to the Markdown before updating its HTML snapshot. If the topic changes materially, clear the baseline and outline fields for the new brief. Preserve the prior Quick Paper on disk for reference where needed.

After each substantive change to the brief, confirmation, baseline results, or outline, run [the workspace renderer](../scripts/render-research-workspace.py) as `python3 <skill-dir>/scripts/render-research-workspace.py research-state.json research-workspace.html` from the artifact directory. Link the refreshed HTML and, when available, the editable Markdown in the conversation. The author can download Markdown edits from the workspace. Read the updated Markdown when they want Codex to carry those edits forward.

## Debate the idea and maintain the brief

- Start from what the author said. In each turn, state one assumption, rival explanation, failure case, or experimental trade-off that would change the design. Explain the practical consequence in a sentence and ask one focused question. Offer two concrete alternatives when that helps the author decide, with room for their own answer.
- Keep a concise brief with the **research question**, **main metric**, **fair comparison**, and **what would falsify the hypothesis**. If useful, name the population or setting, intended intervention, prediction, and a major confound. Mark tentative entries as proposed and missing entries as open. Attribute decisions to the author and revise the brief when their answer changes a choice.
- Ask the next question at the biggest unresolved choice. For example, if the author wants to stop reading a document partway through, whether to measure recall of gold evidence or final answer accuracy changes which comparison can explain a performance difference. Once a measure is chosen, examine the most consequential remaining failure mode or comparison condition.

## Confirm the topic

- When the author has a testable direction, show the current brief and ask for confirmation in that turn. Start baseline search only after the author explicitly confirms that version of the topic. A message that clearly confirms a topic and requests search, including an author-submitted **confirm and search** handoff containing the displayed brief, satisfies this step. Carry any unsettled details forward as open items. Continue with the confirmed topic in the same turn when possible.
- If the author revises the central question or comparison conditions after search, update the brief and ask them to confirm the changed topic. Recheck earlier baselines against the new brief before carrying them forward.

## Find baselines and check what they compare

Search enabled scholarly or internet sources with terms for the confirmed question, intervention, evaluation setting, and candidate methods. Use public terminology for queries that come from unpublished work. Open original papers and official implementations or benchmark documentation to verify each baseline and its relevant conditions. Prefer the closest method for the claim, an informative control, and an upper or lower reference when each has a distinct role. A reasonable control proposed by the team can be listed as a planned comparison, with its provenance identified.

For each selected candidate, record a stable ID, its original source link and locator, its role, which conditions match, what still needs alignment or reproduction, and the next check. Compare the dataset and split, input or evidence access, primary metric, model and implementation, and training or inference budget when those conditions affect the claim.

| ID and baseline | Primary source and locator | Comparison role | Conditions and evidence | Next check |
| --- | --- | --- | --- | --- |
| B01 | Link to paper section, table, or implementation | Which claim it can test | Matched conditions, mismatches, and unknowns | What to align or verify |

Use the table in the Quick Paper. Scope descriptions to what the source supports and leave reported scores out of the new study's results. If sources are inaccessible or comparison conditions cannot be verified, record the specific missing source or comparison and retain a labeled slot for it. An incomplete search can yield a usable outline with those gaps visible.

## Create the editable Quick Paper

Write an editable `quick-paper.md` alongside the workspace artifacts unless the author chooses a different location. Reuse a Quick Paper for the same confirmed topic if one exists. Follow any requested manuscript format or filename. Carry over what the author has confirmed and only the references you verified. Adapt section headings to the work. For an empirical paper, use the following structure:

- **Working title and brief.** Insert the confirmed question and comparison plan. Identify proposed choices and open items.
- **Abstract and introduction.** Give the question and motivation. Leave focused slots for the main contribution, outcomes, and takeaway when those still need evidence.
- **Related work and baselines.** Insert the sourced comparison table and leave slots for unverified candidates and alignment work.
- **Method.** Insert agreed design decisions. Leave labeled slots for operational details, such as a stopping rule, protection against false stops, or a decision threshold.
- **Experimental setup.** Insert agreed metrics and fairness conditions. Leave slots for the data, splits, implementation settings needed to reproduce the results, and planned analysis as needed.
- **Results.** Prepare blank cells for the candidate comparison, effect sizes, uncertainty, and failure slices that matter. A caption or adjacent note identifies the value to fill and the evidence needed.
- **Discussion and conclusion.** Leave slots for interpretation, limitations, counterexamples, and a scope-bounded conclusion once the evidence is available.

Use placeholders that lead to a useful next action, such as `[Fill in the matched-budget evidence recall for B01 on the held-out split]`. Keep unknown result cells empty. The draft can open with a brief list of the next one or two items the author can supply.

## Continue as the author fills gaps

When the author returns with facts, references, results, or text, read the current Quick Paper before editing. Fill the matching slots using their evidence and preserve other writing. Update the baseline table or brief if the facts change, retain provenance, and ask one focused question about the next consequential gap. If new material changes the central topic, return to confirmation. When the author asks to review the manuscript's structure, use the normal review workflow with the current paper.
