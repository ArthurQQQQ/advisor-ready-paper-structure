# Writing the sections of an empirical paper

Apply the [shared writing foundation](writing-foundations.md) throughout drafting and revision. It supplies the core-insight thread, introduction sequence, intuition before mathematics, experimental narration, visual guidance and sentence-level conventions.

Choose the primary paper type from the [central claim and its evidence](research-framing.md#choose-the-papers-organizing-contribution), then use these sequences to choose what each paragraph or subsection does. Merge adjacent steps when they answer the same reader question.

| Type | Proposed section sequence | How to organize the evidence |
| --- | --- | --- |
| Method paper | Introduction → Close prior work → General idea and method → Experimental setup → Comparative results and component checks → Limits and conclusion | Each comparison tests the proposed change or a design choice. |
| Analysis paper | Introduction and research questions → Prior explanations or predictions → Study design and measurement → Findings → Robustness and competing explanations → Implications and limits | Each finding answers a question, with the controls and counterevidence needed to interpret it. |

Use the five framing answers as the argument behind the introduction. Explain terminology and task first, then stakes, challenges, closest attempts and the general approach. For question 5, a study design can be the approach. Put the model and dataset identities needed for reproducibility in their appropriate setup sections.

| Section | Writing sequence | What to look for in a draft |
|---|---|---|
| Title and abstract | Name the problem, the key approach, the strongest comparison or observation, and its scope. Write the evidence sentence after the body is settled. | The abstract and conclusion claim the same result under the same conditions. A missing result stays blank in the outline. |
| Introduction | Establish the task and stakes. Explain the working intuition and what close prior approaches can already do. State the specific unresolved problem and key idea, then give a compact preview of the actual experiments and findings. End with a contribution list whose claims already appear in the preceding introduction. Introduce baselines here only where they help establish the comparison. | Each gap leads to a design choice or research question. Strong claims about the literature need a verified source. |
| Related Work | Group nearby work by how it addresses the problem and explain the distinctions relevant to the paper's contribution. | Scope claims of novelty to the comparison the supplied sources support. Keep unsupported claims in the memo as gaps. |
| Method | State the key idea, then walk through inputs, operations, outputs, and the actual training and inference conditions. Explain the design choices that the experiments evaluate. | Each substantive component has a reason to be there. Describe the protocol and implementation from the supplied record. Move reproducibility detail to appendices only where readers can still locate it. |
| Experiments and Results | For each comparison, state the question, controls and reading guide, direct observation, interpretation, and implication for the design. Choose main results, ablation, transfer, failures, or cost only as the claims require. | Paired claims use comparable populations and conditions. An overall gain does not establish the effect of a component. Preserve adverse and inconclusive results that matter. |
| Discussion and limitations | State what the evidence explains, viable alternative explanations, and the conditions under which it applies. | A plausible mechanism remains an interpretation unless separately tested. Show how each material limitation changes the claim. |
| Conclusion | Return to the initial question. Summarize the completed work and supported finding, then connect any future work to a concrete limitation. | Every conclusion is traceable to evidence already presented. |
| Appendix or supplement | Provide details or additional evidence and link each item back to the main argument. | Empty internal planning slots belong in the working outline. Necessary conditions remain discoverable from the main text. |

For a weak comparison, specify the decision rule in plain language. For example, compare both methods on the same locked evaluation set, confirm metric and eligibility match, and only broaden the claim if the broader evidence supports it. The absence of a matching run leaves the broader claim open.
