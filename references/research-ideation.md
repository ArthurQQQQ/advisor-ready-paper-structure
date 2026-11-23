# Research idea to Quick Paper

Follow this workflow when the author needs to shape a research question before writing or wants to continue a Quick Paper. Discuss the work in the current Codex conversation and keep a Research Wall that shows how each round fills the paper. Use the author's language and wording where possible.

## Keep the workspace current

On the first substantive exchange, create `research-state.json` and `research-workspace.html` in the author-selected output directory or the current project's chat artifact directory. Seed them with the author's actual idea, the first question or takeaway, and the first relevant paper blocks. On subsequent turns, update the same files. If an older state lacks the Research Wall arrays, add them and seed from the existing brief and known messages. Preserve the existing brief, baselines, and outline.

Maintain one JSON object with this shape. Use empty strings for unknown brief fields and empty arrays where there are no entries yet.

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
  "outline": "",
  "rounds": [],
  "blocks": [],
  "evidence": []
}
```

- `idea` records the author's starting point. The topic, metric, controls, and failure criterion make up the current brief. `openQuestion` records the question asked in this turn. Clear it when the topic is confirmed, then use it for the next consequential gap as the paper develops.
- Set status to `discussing` until the author confirms the topic, `confirmed` while the baseline search and outline are pending, and `ready` once the resulting Quick Paper is available. A ready Quick Paper can still have open evidence gaps.
- Each baseline has string fields `name`, `role`, `source`, `match`, and `notes`. Put the original HTTP or HTTPS URL in `source`. Use `match` for a concise assessment in the author's language and `notes` for the protocol conditions, source locator, unresolved differences, and next check. An empty source records a planned comparison or an unverified slot.
- An optional string `id` can identify the workspace's browser draft. Keep it stable for the same project and topic.
- Once the author has an outline, keep `outline` in sync with the current Quick Paper Markdown. Read any author changes to the Markdown before updating its HTML snapshot. If the topic changes materially, clear the baseline and outline fields for the new brief. Preserve the prior Quick Paper on disk for reference where needed.

## Add a round to the Research Wall

Before replying to every substantive author message, read the existing state and append a round. Capture the part of the message that moves the research forward: a choice, correction, objection, evidence, or new constraint. Add the takeaway and the next decision or action where useful. Record open proposals as proposals; a round can advance the discussion without settling anything. Leave out greetings and unrelated chat.

- Each round is an object with `id`, `label`, `author`, `decision`, and `blockIds`. Use a stable ID, paraphrase the author's point in `label`, and put their display name in `author`. In `decision`, state what you concluded, what changed, or what remains undecided. Put the IDs of blocks changed by this round in `blockIds`.
- Each block has `id`, `label`, `status`, `detail`, `roundIds`, and `evidenceIds`. Reuse the ID for the same question, metric, control, method, result, or other paper component. Update its status and reason, append the round ID to `roundIds`, and link current evidence or gaps by ID in `evidenceIds`. If the author revises a decision, update the block and record why in the new round so past decisions stay traceable.
- Use `open` for a question or slot still to fill, `suggestion` for a proposed change or next action, `conflict` when linked claims, assumptions, or evidence cannot all hold, and `supported` when the stated scope is supported by reasoning or evidence. In `detail`, identify what is missing, why the action helps, which two things conflict and what would resolve them, or exactly what is supported. Distinguish a design choice that follows logically from a claim established by data; explain what still requires a test even if the design is settled.
- Each evidence entry has `id`, `label`, `status`, and `detail`, plus optional `source` and `roundId`. Use `provided` for actual material the author supplied, `verified` for evidence you checked against its source, and `needed` for an absent or hypothetical result, or a source you still need to locate. State the claim the evidence bears on, its scope or locator, and what remains unknown. Include the original source URL when available and the originating round ID when applicable. A plan, candidate citation, or result nobody has supplied or checked stays a gap. Update the same evidence entry when the missing material arrives.

Save the updated state by replacing the completed JSON file in one operation, then run [the workspace renderer](../scripts/render-research-workspace.py) as `python3 <skill-dir>/scripts/render-research-workspace.py research-state.json research-workspace.html` from the artifact directory. Do this on each substantive round, including confirmation, new baseline findings, and Quick Paper updates.

When the author wants the research wall to update while open, run `python3 <skill-dir>/scripts/serve-research-workspace.py research-workspace.html research-state.json` from the artifact directory and give the author its loopback URL. Reuse a running preview for the same artifact. Keep updating the same state files so the live board can read them. Without the service, link the refreshed HTML and tell the author they can reload it. Link the editable Markdown when available. The author can download Markdown edits from the workspace; read the updated Markdown when they want Codex to carry those edits forward.

## Debate the idea and maintain the brief

Use the [five-question framing](research-framing.md) throughout the discussion. Establish current answers for the problem, value, challenges, closest prior attempts and general approach. Save each answer and its evidence in existing Research Wall blocks, then revisit the affected answers when new information changes the argument. At each turn, develop the most consequential gap. The five-question summary is a compact synthesis at major transitions.

- Start from what the author said. In each turn, state one assumption, rival explanation, failure case, or experimental trade-off that would change the design. Explain the practical consequence in a sentence and ask one focused question. Offer two concrete alternatives when that helps the author decide, with room for their own answer.
- Keep a concise brief with the **research question**, **main metric**, **fair comparison**, and **what would falsify the hypothesis**. If useful, name the population or setting, intended intervention, prediction, and a major confound. Mark tentative entries as proposed and missing entries as open. Attribute decisions to the author and revise the brief when their answer changes a choice.
- Ask the next question at the biggest unresolved choice. For example, if the author wants to stop reading a document partway through, whether to measure recall of gold evidence or final answer accuracy changes which comparison can explain a performance difference. Once a measure is chosen, examine the most consequential remaining failure mode or comparison condition.

## Confirm the topic

- Search close prior work while debating whenever it bears on one of the five questions, and use it to revise the brief. When the author has a testable direction, show the current five-question synthesis and experimental brief and ask for topic confirmation. Once confirmed, fix the scope for formal baseline/control selection and evaluation. A message that clearly confirms the displayed topic and requests search satisfies confirmation. Continue in the same turn where possible and carry unsettled details as open items.
- If the author revises the central question or comparison conditions after search, update the brief and ask them to confirm the changed topic. Recheck earlier baselines against the new brief before carrying them forward.

## Find baselines and check what they compare

During discussion, use targeted searches for the precise problem to challenge the proposed novelty, assumptions and approach. Once the topic is confirmed, use its question, intervention, evaluation setting and candidate methods to assemble the formal comparison plan. Search enabled scholarly or internet sources. Use public terminology for queries that come from unpublished work. Open original papers and official implementations or benchmark documentation to verify each baseline and its relevant conditions. Prefer the closest method for the claim, an informative control, and an upper or lower reference when each has a distinct role. A reasonable control proposed by the team can be listed as a planned comparison, with its provenance identified.

For each selected candidate, record a stable ID, its original source link and locator, its role, which conditions match, what still needs alignment or reproduction, and the next check. Compare the dataset and split, input or evidence access, primary metric, model and implementation, and training or inference budget when those conditions affect the claim.

| ID and baseline | Primary source and locator | Comparison role | Conditions and evidence | Next check |
| --- | --- | --- | --- | --- |
| B01 | Link to paper section, table, or implementation | Which claim it can test | Matched conditions, mismatches, and unknowns | What to align or verify |

Use the table in the Quick Paper. Scope descriptions to what the source supports and leave reported scores out of the new study's results. If sources are inaccessible or comparison conditions cannot be verified, record the specific missing source or comparison and retain a labeled slot for it. An incomplete search can yield a usable outline with those gaps visible.

## Keep development checks traceable

When the author asks to test a workflow, preserve its code and parameters before checking new documents. Record the sampling rule, exclusions, source versions, and the actual answers returned at each checkpoint. Check attribution to the current study, the question's target, and necessary qualifiers against the cited passages. Keep API failures visible alongside the completed decisions.

The [long-document evidence case](../examples/long-document-early-stop/README.md) records a development result and a frozen new-document check with different outcomes.

## Create the editable Quick Paper

Write an editable `quick-paper.md` alongside the workspace artifacts unless the author chooses a different location. Reuse a Quick Paper for the same confirmed topic if one exists. Follow any requested manuscript format or filename. Carry over what the author has confirmed and only the references you verified.

Before the outline, state the primary paper type, why its main claim and evidence support that choice, and any open evidence gap. Use the [method or analysis criteria](research-framing.md#choose-the-papers-organizing-contribution) and record the choice in the Research Wall. Then show the current five-question synthesis and use the corresponding [section sequence](section-playbook.md). A mixed contribution can identify a primary type with a supporting role for the other. Keep an unsettled classification provisional.

For an empirical paper, adapt these slots to the selected contribution:

- **Working title and brief.** Insert the confirmed question and comparison plan. Identify proposed choices and open items.
- **Abstract and introduction.** Give the question and motivation. Leave focused slots for the main contribution, outcomes, and takeaway when those still need evidence.
- **Related work and baselines.** Insert the sourced comparison table and leave slots for unverified candidates and alignment work.
- **Method or study design.** For a method paper, explain the general solution and agreed design choices before the implementation. For an analysis paper, specify the research questions or hypotheses, measurement protocol, controls or interventions, and competing explanations. Leave unknown operational details as labeled gaps.
- **Experimental setup.** Insert agreed metrics and fairness conditions. Leave slots for the data, splits, implementation settings needed to reproduce the results, and planned analysis as needed.
- **Results or findings.** Organize a method paper around comparisons supporting its proposed change. Organize an analysis paper around findings that answer its research questions. Prepare blank cells for the relevant comparisons, effect sizes, uncertainty, and failure slices. A caption or adjacent note identifies the value to fill and the evidence needed.
- **Discussion and conclusion.** Leave slots for interpretation, limitations, counterexamples, and a scope-bounded conclusion once the evidence is available.

Use placeholders that lead to a useful next action, such as `[Fill in the matched-budget evidence recall for B01 on the held-out split]`. Keep unknown result cells empty. The draft can open with a brief list of the next one or two items the author can supply.

## Continue as the author fills gaps

When the author returns with facts, references, results, or text, read the current Quick Paper before editing. Fill the matching slots using their evidence and preserve other writing. Update the baseline table or brief if the facts change, retain provenance, and ask one focused question about the next consequential gap. If new material changes the central topic, return to confirmation. When the author asks to review the manuscript's structure, use the normal review workflow with the current paper.
