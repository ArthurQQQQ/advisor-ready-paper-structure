# Five-question research framing

Use these questions to develop a research argument from an idea, notes or an existing draft. Adapt the language to the reader and field. Begin with the current question and evidence. Let changes in either revise the framing. Use the [shared writing foundation](writing-foundations.md) to turn that argument into section and sentence-level prose.

## The five questions

| Question | What to establish | What to check while debating |
| --- | --- | --- |
| **1. What problem are we studying?** | Introduce the broader task, define unfamiliar terms, then isolate the precise unresolved question, setting and boundary. Give a plain-language description before technical notation. | Can a reader new to the field understand the task? Which population, assumptions or access conditions change the question? |
| **2. Why should the reader care?** | Name who faces the problem, what decision or capability is affected, and the consequence of leaving it unresolved. Connect technical value to a concrete use where evidence permits. | Is the claimed cost, reliability issue, scientific importance or wider impact supported? Use the strongest defensible motivation and leave speculative impact explicit. |
| **3. What makes it difficult?** | Identify obstacles inherent in the problem and explain how they frustrate a direct approach. Tie each obstacle to a requirement, rival explanation or question the study must address. | Does the proposed approach address this obstacle? Does the evidence establish that it does? For an analysis, what makes the effect hard to isolate or explain? Keep unresolved obstacles visible. |
| **4. What have others done about this precise problem?** | Find the closest actual attempts. For each, give one or two sentences about its approach, what it establishes, its relevant conditions and the remaining question. Use primary sources. | Does it address the same problem under comparable assumptions? Has the proposed gap already been solved? Describe strengths and bounded limits with sources. Revise the problem or contribution when the comparison changes it. |
| **5. What is our approach and why should it address the difficulty?** | Explain the principle, information used, operations and expected output in terms that generalize across a particular model or dataset. Connect each essential choice to the relevant obstacle and the evidence needed to test it. | For a method, what changes and what would establish its benefit? For an analysis, what comparison, intervention or measurement can answer the question and discriminate rival explanations? |

Keep the core explanation in question 5 independent of model names, benchmark names and dataset-specific constants. Preserve concrete implementation, data and evaluation identities in the experimental setting and reproducibility details. An analysis of a named system can define its subject while explaining the study logic in general terms.

Question 4 supplies the close comparison needed to motivate the introduction. Expand the wider literature organization when writing Related Work. A relevant prior method can remain a strong baseline even when it addresses much of the proposed problem.

## Iterate before drafting

- Establish a short first-pass answer to all five questions from what the author has supplied. Mark missing answers as open and proposed claims as tentative.
- In each subsequent turn, focus on the uncertainty that most changes the research. Debate a concrete assumption, alternative explanation or comparison, then ask one consequential question if a decision is needed. Update the affected answers. Return to earlier answers when a new finding changes their premises.
- Search original papers and official implementations during the discussion when the answer depends on prior work. Link a source to the assertion it supports, record the comparison conditions, and say what the finding changes. Save exploratory sources as evidence on the prior-work framing block while the topic is still under discussion. An incomplete or unsuccessful search leaves the novelty claim open.
- Carry the five answers forward across turns. Use existing Research Wall blocks with stable IDs such as `framing-problem`, `framing-value`, `framing-challenges`, `framing-prior-work` and `framing-approach`. Reuse equivalent existing blocks where their role matches. Link changed blocks to the current round and evidence.
- Show the compact five-question summary at the first synthesis, after a material change, and before selecting the paper structure. Routine turns can show the changed answer and the next gap. After the author confirms a testable topic, fix the formal baseline/control plan against that version.
- Generate the Quick Paper when requested or when the author is ready for the outline. Preserve remaining gaps in it. During experiments or revisions, use new evidence to revisit these questions and the contribution type.

A useful compact snapshot is a table with the question, current answer, supporting source or evidence IDs, and the next unresolved point. Give the reader the short conclusion first. Additional source details can sit in the corresponding expandable Research Wall block.

## Choose the paper's organizing contribution

Before producing the full outline or drafting, name the intended primary type as **Method paper** or **Analysis paper**, explain the choice from the central claim and available evidence, and identify any claim the evidence still cannot support. Keep the choice provisional when the contribution is unsettled. Record it in a `paper-type` Research Wall block with the relevant evidence and revisit it when the main claim changes.

| Primary type | Central contribution | Evidence that must carry the paper | Organizing sequence |
| --- | --- | --- | --- |
| **Method paper** | A proposed procedure, objective, representation or system change solves a specified problem under stated conditions. | Comparisons test the benefit against the closest alternatives, with component checks, generalization and cost where needed for the claims. Leave missing tests as gaps. | Problem and value → challenges and closest attempts → general solution principle → method → main comparisons and design tests → limits. |
| **Analysis paper** | A supported finding explains, characterizes or tests an effect, behavior, failure mode, trade-off or assumption. | A valid measurement protocol, controls or interventions, uncertainty, alternative explanations and scope checks support each finding. Distinguish an observed association from a causal explanation. | Question and value → competing explanations or predictions → study design and measures → findings in logical order → robustness and limits → implications. |

Classify by the contribution the paper asks readers to accept. Creating a diagnostic tool can support an analysis. Including ablations can support a method. For mixed work, choose the primary claim that organizes the narrative and describe the other contribution's supporting role. If the work primarily contributes a dataset, benchmark, theory or another form, state that explicitly and adapt the structure.

Keep the intended claim and current evidence separate. Weak or failed results can expose a gap in a method claim or motivate an analysis, but a change of research objective belongs in the author's decision record.

## Compact handoff to writing

Start the writing handoff with the primary paper type, its reason and the evidence boundary. Follow with the current five answers, the proposed numbered section order, the first analyses or comparisons needed, and a section-by-section table of existing support, missing logic or evidence, and the next writing or research action. Use the appropriate method or analysis sequence from the [section playbook](section-playbook.md). Carry unanswered questions into specific outline gaps and planned figures.
